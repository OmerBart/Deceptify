import os

import wave
from threading import Event, Thread
import pyaudio
from faster_whisper import WhisperModel
from LLM.llm import Llm
import speech_recognition as sr

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"


def GoogleSpeechRecognition():
    r = sr.Recognizer()
    llm = Llm()
    wait_for_llm = Event()

    with sr.Microphone() as source:
        audio = r.listen(source)
    while True:
        try:
            transcription = r.recognize_google(audio)
            print(transcription)
            t = Thread(target=llm.get_answer, args=(transcription, wait_for_llm,))
            t.start()
            wait_for_llm.wait()
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Recognition service; {0}".format(e))


def record_chunk(p, stream, file_path, chunk_length=3):
    frames = []
    for _ in range(0, int(16000 / 1024 * chunk_length)):
        data = stream.read(1024)
        frames.append(data)

    wf = wave.open(file_path, 'wb')
    wf.setnchannels(1)
    wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
    wf.setframerate(16000)
    wf.writeframes(b''.join(frames))
    wf.close()


def transcribe_chunk(model, file_path):
    segments, info = model.transcribe(file_path, beam_size=7)
    transcription = ' '.join(segment.text for segment in segments)
    return transcription


def main2(getAnswerEvent=None):
    # Choose your model settings
    model_size = "medium.en"
    llm = Llm()
    model = WhisperModel(model_size, device="cuda", compute_type="float16")
    wait_for_llm = Event()
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=1024)

    accumulated_transcription = ""  # Initialize an empty string to accumulate transcriptions

    try:
        while True:
            chunk_file = "temp_chunk.wav"
            record_chunk(p, stream, chunk_file)
            transcription = transcribe_chunk(model, chunk_file)
            print(transcription)
            os.remove(chunk_file)

            # Append the new transcription to the accumulated transcription
            # TODO: send the transcription to the llm
            t = Thread(target=llm.get_answer, args=(transcription, wait_for_llm,))
            t.start()
            wait_for_llm.wait()
    except KeyboardInterrupt as e:
        stream.stop_stream()
        stream.close()
        p.terminate()


if __name__ == '__main__':
    main2()
