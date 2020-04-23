# common_audio.py

import matplotlib.pyplot as plt
import numpy as np

import librosa, librosa.display

from IPython.display import Audio, display, clear_output

def play_audio(y, sr, autoplay=False):
    display(Audio(y, rate=sr, autoplay=autoplay))

# TODO: add the f_max=8000 term in melspectrogram (but this breaks the spectrogram_to_audio)
def audio_to_spectrogram(y, sr, normalize=True):
    spectrogram = librosa.feature.melspectrogram(y=y, sr=sr)
    spectrogram = librosa.power_to_db(spectrogram, ref=np.max)
    if normalize:
        spectrogram = np.interp(spectrogram, (-80., 0.), (-1., +1.))
    return spectrogram
def audios_to_spectrograms(ys, sr, normalize=True):
    spectrograms = []
    for y in ys:
        spectrograms.append(audio_to_spectrogram(y, sr, normalize))
    return np.array(spectrograms)
def spectrogram_to_audio(spectrogram, sr, normalize=True):
    if normalize:
        spectrogram = np.interp(spectrogram, (-1., +1.), (-80., 0.))
    spectrogram = librosa.db_to_power(spectrogram)
    yp = librosa.feature.inverse.mel_to_audio(spectrogram, sr=sr)
    return yp

# def my_audio_to_spectrogram(y, sr):
#     return librosa.stft(y)

# def my_spectrogram_to_audio(spectrogram, sr):
#     return librosa.istft(spectrogram)


def add_spectrograms(*spectrograms, normalize=True):
    result = np.zeros_like(spectrograms[0])
    for spectrogram in spectrograms:
        if normalize:
            spectrogram = np.interp(spectrogram, (-1., +1.), (-80., 0.))
        result += librosa.db_to_power(spectrogram)
    result = librosa.power_to_db(result)
    if normalize:
        result = np.interp(result, (-80., 0.), (-1., +1.))
    return result
# first - second - third, etc.
def subtract_spectrograms(*spectrograms, normalize=True):
    result = spectrograms[0]
    if normalize:
        result = np.interp(result, (-1., +1.), (-80., 0.))
    result = librosa.db_to_power(result)

    for i in range(1, len(spectrograms)):
        spectrogram = spectrograms[i]
        if normalize:
            spectrogram = np.interp(spectrogram, (-1., +1.), (-80., 0.))
        result -= librosa.db_to_power(spectrogram)
    result = librosa.power_to_db(result)
    if normalize:
        result = np.interp(result, (-80., 0.), (-1., +1.))
    return result


# for jupyter notebook only
def show_audio(y, sr):
    librosa.display.waveplot(y=y, sr=sr)

def show_spectrogram(spectrogram, sr):
    plt.figure(figsize=(10, 4))
    librosa.display.specshow(spectrogram, x_axis='time', y_axis='mel', sr=sr, fmax=8000, cmap='gray')
    plt.colorbar(format='%2.2f')
    plt.title('Mel-frequency spectrogram')
    plt.tight_layout()
    

# sets sample_length of y by either cropping or by duplicating to length
def set_sample_length(y, sample_length):
    if len(y) > sample_length:
        y = y[:sample_length]
    if len(y) < sample_length:
        factor = sample_length//len(y)
        oy = y.copy()
        for i in range(factor-1):
            y = np.concatenate((y, oy), axis=0)
        leftover = sample_length - len(y)
        y = np.concatenate((y, oy[:leftover]), axis=0)
    return y
