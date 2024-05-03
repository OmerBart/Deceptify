import random
import time
import speech_recognition as sr


# this is called from the background thread
def convert(recognizer, audio):
    if filename:  # Checks if the filename var filled already.
        with open(filename, 'w') as audio_file:
            try:
                msg = recognizer.recognize_google(audio)
                print("Google Speech Recognition thinks you said " + msg)
                audio_file.write(msg)  # Writing the message to the transcript.
            except sr.UnknownValueError:
                print("Google Speech Recognition could not understand audio")
            except sr.RequestError as e:
                print("Could not request results from Google Speech Recognition service; {0}".format(e))


# The objects
filename = input("Enter file name: ") + '.txt'  # Opening some file to write the transcript

r = sr.Recognizer()
m = sr.Microphone()
print("Say something!")

with m as source:
    r.adjust_for_ambient_noise(source)  # calibrate once, before we start listening

stop_listening_func = r.listen_in_background(m,
                                             convert)  # Running a background thread for converting the speech into text.

for _ in range(50):  # Wasting time in the main thread for 5 seconds.
    time.sleep(0.2)  # The main thread is doing other things.

counter = 0
rnd = random.randint(1, 10000)
while counter != rnd:  # Doing some stuff while the other thread converting speech to text.
    counter = random.randint(1, 10000)

stop_listening_func(wait_for_stop=False)
print(f"Conversation transcript saved on: {filename}")
