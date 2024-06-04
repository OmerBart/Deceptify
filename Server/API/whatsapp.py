
import pyautogui
import time
import pyaudio
import wave
import os


# Path to your audio file
audio_path = os.path.expanduser(r"C:\Users\Hadar\PycharmProjects\Deceptify\Server\API\Recordings\i_love_bananas.wav")


def play_audio(file_path):
    chunk = 2048
    wf = wave.open(file_path, 'rb')
    data = wf.readframes(chunk)
    p = pyaudio.PyAudio()

    # Open stream using the virtual audio device (default microphone)
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),

                    rate=wf.getframerate(),
                    output=True)

    while data:
        stream.write(data)
        data = wf.readframes(chunk)

    stream.stop_stream()
    stream.close()
    p.terminate()
    wf.close()


def open_whatsapp():
    pyautogui.press('winleft')
    time.sleep(1)
    pyautogui.write('WhatsApp')
    time.sleep(1)
    pyautogui.press('enter')


def search_contact(contact_name):
    # Click on the search bar (Ctrl + F)
    pyautogui.hotkey('ctrl', 'f')
    time.sleep(1)
    # Type the contact name
    pyautogui.write(contact_name, interval=0.1)
    time.sleep(1)
    # Press enter to select the contact
    pyautogui.press('enter')
    time.sleep(1)
    contact_x = 300  # Adjust this value
    contact_y = 200  # Adjust this value

    # Click on the contact in the search results to open the chat
    pyautogui.click(contact_x, contact_y)
    time.sleep(2)  # Wait for the chat to open

def start_call():
    # Click on the call button (assuming the call button is in a consistent position relative to the window)
    call_button_pos = pyautogui.locateCenterOnScreen('Photos/CallButton.png')  # Use an image of the call button
    if call_button_pos:
        pyautogui.click(call_button_pos)
    else:
        print("Call button not found. Please ensure the image is correct and visible on the screen.")
    time.sleep(5)  # Wait for the call to connect


if __name__ == '__main__':
    contact_name = 'Aviv'  # Replace with the actual contact name

    open_whatsapp()
    search_contact(contact_name)
    start_call()

    # Stream the audio recording
    play_audio(audio_path)
