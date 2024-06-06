from data.prompt import Prompt
import pyaudio
import wave
import requests
from dotenv import load_dotenv
import os
import pyautogui
import time
import app

load_dotenv()

SERVER_URL = os.getenv('SERVER_URL')


def create_user(username, password):
    try:
        url = f"{SERVER_URL}/data"
        data = {"username": username, "password": password}
        response = requests.post(url, json=data)
        if response.status_code == 409:
            return False
        response.raise_for_status()
        try:
            result = response.json()
        except requests.exceptions.JSONDecodeError:
            print(f"Server response: {response.text}")
            return False
        return True
    except requests.exceptions.RequestException as e:
        return False


def createvoice_profile(username, profile_name, file_path):
    url = f"{SERVER_URL}/voice_profile"
    with open(file_path, 'rb') as f:
        files = {'file': f}
    data = {'username': username, 'profile_name': profile_name}
    response = requests.post(url, files={'file': file_path}, data=data)
    response.raise_for_status()
    return response.json()


def generate_voice(prompt, description):
    try:
        # Send request to generate voice and get job ID
        url = f"{SERVER_URL}/generate_voice"
        data = {"prompt": prompt, "description": description}
        response = requests.post(url, json=data)
        response.raise_for_status()
        job_id = response.json().get("job_id")

        # Polling the job status
        while True:
            status_url = f"{SERVER_URL}/result/{job_id}"
            status_response = requests.get(status_url)
            if status_response.status_code == 200:
                with open("AudioFiles/" + prompt + ".wav", "wb") as f:
                    f.write(status_response.content)
                return True
            elif status_response.status_code == 202:
                time.sleep(1)  # Wait a second before polling again
            else:
                print("Error", "Failed to retrieve the generated voice.")
                return False
    except requests.exceptions.RequestException as e:
        print(None, "Error", f"Failed to generate voice: {str(e)}")
        return False


def get_device_index(device_name):
    p = pyaudio.PyAudio()
    device_index = None
    for i in range(p.get_device_count()):
        dev = p.get_device_info_by_index(i)
        if device_name in dev['name']:
            device_index = i
            break
    p.terminate()
    return device_index


def play_audio_through_vbcable(audio_file_path, device_name="CABLE Input"):
    # Open the audio file
    wf = wave.open(audio_file_path, 'rb')
    playback_name = "CABLE Input"
    # Instantiate PyAudio
    p = pyaudio.PyAudio()
    device_index = get_device_index(device_name)
    # Open a stream with the same format as the audio file
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True,
                    output_device_index=device_index)

    default_stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                            channels=wf.getnchannels(),
                            rate=wf.getframerate(),
                            output=True)
    # Read data in chunks
    chunk = 1024
    data = wf.readframes(chunk)

    # Play the audio file
    while data:
        stream.write(data)
        default_stream.write(data)
        data = wf.readframes(chunk)

    # Stop stream
    stream.stop_stream()
    default_stream.stop_stream()
    stream.close()
    default_stream.close()

    # Close PyAudio
    p.terminate()

    # Close the audio file
    wf.close()


# Whatsapp open and close function

def open_whatsapp():
    pyautogui.press('winleft')
    time.sleep(1)
    pyautogui.write('WhatsApp')
    time.sleep(2)
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
    call_button_pos = pyautogui.locateCenterOnScreen('API/'
                                                     'Photos/CallButton.png')  # Use an image of the call button
    if call_button_pos:
        pyautogui.click(call_button_pos)
    else:
        print("Call button not found. Please ensure the image is correct and visible on the screen.")


def end_call():
    end_call_button_pos = pyautogui.locateCenterOnScreen('API/Photos/EndCallButton.png')
    if end_call_button_pos:
        pyautogui.click(end_call_button_pos)
    else:
        print("End call button not found. Please ensure the image is correct and visible on the screen.")


def ExecuteCall(contact_name, event):
    open_whatsapp()
    search_contact(contact_name)
    start_call()
    event.wait()
    end_call()


