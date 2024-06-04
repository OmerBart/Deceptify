from twisted.internet.protocol import DatagramProtocol
import pyaudio
import random
from twisted.internet import reactor
import wave
import sys
import time
import os


def generate_random_port():
    return random.randint(1024, 49151)


PORT = generate_random_port()
OTHER_CLIENT_PORT = 28421  # Send the other client's port or generate it.
OTHER_CLIENT_IP = '127.0.0.1'


class Client(DatagramProtocol):
    def startProtocol(self, other_client=(OTHER_CLIENT_IP, OTHER_CLIENT_PORT)):
        py_audio = pyaudio.PyAudio()  # Create a virtual audio driver
        self.buffer = 2048  # The number of bytes to read or write (as audio)
        self.other_client = other_client  # tuple --> (ip,port)
        # self.audio_path = sys.argv[1] # Some wav file to sent to myself.
        self.audio_path = os.path.expanduser(r"C:\Users\Hadar\Downloads\Mirror's Edge Theme Song HQ.wav")

        # Check available input devices and their capabilities
        input_device_info = py_audio.get_device_info_by_index(py_audio.get_default_input_device_info()["index"])
        print(f"Input Device Info: {input_device_info}")

        # Use mono (1 channel) if stereo (2 channels) is not supported
        channels = 1 if input_device_info["maxInputChannels"] < 2 else 2

        # Defining the i/o streams to get and receive data.
        self.output_stream = py_audio.open(format=pyaudio.paInt16, output=True, rate=48000, channels=2,
                                           frames_per_buffer=self.buffer)
        self.input_stream = py_audio.open(format=pyaudio.paInt16, input=True, rate=44800, channels=channels,
                                          frames_per_buffer=self.buffer)

        reactor.callInThread(self.send_audio)

    def send_audio(self):
        py_audio = pyaudio.PyAudio()

        with wave.open(self.audio_path, 'rb') as wav_file:
            print("WAV FILE OPENED, sleeping for 2 seconds before sending...")
            time.sleep(2)

            # Get the frame rate of the audio file
            frame_rate = wav_file.getframerate()
            frames_per_buffer = 2048

            # Calculate the duration of each chunk in seconds
            chunk_duration = frames_per_buffer / frame_rate

            # Speed adjustment factor (1.0 = normal speed, < 1.0 = faster, > 1.0 = slower)
            speed_factor = 0.7  # Adjust this value to speed up the audio

            while True:
                data = wav_file.readframes(frames_per_buffer)  # Read the data in chunks of 1024 bytes.
                if not data:
                    break

                # Send the audio data
                self.transport.write(data, self.other_client)

                # Sleep to maintain the correct playback speed, adjusted by the speed factor
                time.sleep(chunk_duration * speed_factor)

            print("Done sending the target audio file.")

    def record(self, audio_record=None):
        if not audio_record:  # Checks if there is some voice record that we want to send back to the client.
            print("Please record yourself")
            while True:  # If not so, we enable the client to record himself
                data = self.input_stream.read(self.buffer)
                # print(data)
                self.transport.write(data, self.other_client)  # Sending the data to another client

    def datagramReceived(self, datagram, addr):  # This function is called when we receive some data
        self.output_stream.write(datagram)


if __name__ == '__main__':
    print(f"Working on port {PORT}")
    reactor.listenUDP(PORT, Client())
    reactor.run()
