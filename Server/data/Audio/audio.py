import os
import librosa
import numpy as np
import soundfile as sf
from pydub import AudioSegment


def bytes_to_array(b):
    # Determine the number of elements in the buffer based on the data type
    num_elements = len(b) // np.dtype(np.float64).itemsize

    if len(b) % np.dtype(np.float64).itemsize != 0:
        b = b[:num_elements * np.dtype(np.float64).itemsize]
    return np.frombuffer(b, dtype=np.float64)


def array_to_bytes(a):  # Converting a numpy array into a byte-like array.
    return a.tobytes(order='C')


def read_wav(path, sr, duration=None, mono=True):
    wav, _ = librosa.load(path, mono=mono, sr=sr, duration=duration)
    return wav


def write_wav(wav, sr, path, format='wav', subtype='PCM_16'):
    sf.write(path, wav, sr, format=format, subtype=subtype)


def trim_wav(wav):
    wav, _ = librosa.effects.trim(wav)
    return wav


def crop_random_wav(wav, length):
    """
    Randomly crop a part of a wav file.
    :param wav: a waveform
    :param length: length to be randomly cropped.
    :return: a randomly cropped part of wav.
    """
    assert (wav.ndim <= 2)
    assert (type(length) == int)

    wav_len = wav.shape[-1]
    start = np.random.choice(range(np.maximum(1, wav_len - length)), 1)[0]
    end = start + length
    if wav.ndim == 1:
        wav = wav[start:end]
    else:
        wav = wav[:, start:end]
    return wav


def mp3_to_wav(src_path, tar_path):
    """
    Read mp3 file from source path, convert it to wav and write it to target path.
    Necessary libraries: ffmpeg, libav.

    :param src_path: source mp3 file path
    :param tar_path: target wav file path
    """
    AudioSegment.from_mp3(src_path).export(tar_path, format='wav')


def prepr_audio(mp3_source_path, target_path, sr=22050):
    """
    Convert MP3 to WAV, preprocess the audio, and return a numpy array.
    :param mp3_source_path: Source MP3 file path.
    :param target_path: Target WAV file path.
    :param sr: Sample rate for the audio.
    :return: Numpy array of the processed audio.
    """
    mp3_to_wav(mp3_source_path, target_path)
    wav, _ = librosa.load(target_path, sr=sr, mono=True)
    wav = trim_wav(wav)
    wav = librosa.util.normalize(wav)
    return wav
