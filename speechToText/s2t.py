import random
import time
import speech_recognition as sr

stop = False
msg = ''


# this is called from the background thread
def convert(recognizer, audio):
    try:
        print("Google Speech Recognition thinks you said " + recognizer.recognize_google(audio))
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))


# The objects
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
