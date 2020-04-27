# common_audio.py

import matplotlib.pyplot as plt
import numpy as np

import librosa, librosa.display

from IPython.display import Audio, display, clear_output

def complex_to_channels(spectrograms):
    """Turn the complex spectrograms into channels.
    (..., F, T) with dtype=complex -> (..., 2, F, T) with dtype=float
    """
    return np.stack((np.real(spectrograms), np.imag(spectrograms)), axis=-3)
def channels_to_complex(spectrograms):
    """Turn the channels into complex spectrograms.
    (..., 2, F, T) with dtype=float -> (..., F, T) with dtype=complex
    """
    return spectrograms[..., 0, :, :] + 1.0j * spectrograms[..., 1, :, :]
    
def audio_to_spectrogram(ys, sr):
    """Turn a series of audio signals into complex spectrograms."""
    spectrograms = []
    for y in ys:
        spectrogram = librosa.stft(y=y, n_fft=256, hop_length=64)
#         spectrogram = np.stack((np.real(spectrogram), np.imag(spectrogram)))
        spectrograms.append(spectrogram)
    spectrograms = np.array(spectrograms)    
    return spectrograms

def spectrogram_to_audio(spectrograms, sr):
    """Turn a series of complex spectrograms into audio signals"""
    ys = []
    for spectrogram in spectrograms:
        yp = librosa.istft(spectrogram, hop_length=64)
        ys.append(yp)
    return np.array(ys)

def add_spectrograms(*spectrograms):
    """Add the spectrograms."""
    return np.sum(spectrograms, axis=0)
# first - second - third, etc.
def subtract_spectrograms(*spectrograms):
    """Subtract the first spectrogram given with the rest."""
    return spectrograms[0] - add_spectrograms(spectrograms[1:])

# for jupyter notebook only

def play_audio(y, sr, autoplay=False):
    """Play the signal y in a jupyter notebook."""
    display(Audio(y, rate=sr, autoplay=autoplay))

def show_audio(y, sr):
    """Show the signal y in a jupyter notebook"""
    librosa.display.waveplot(y=y, sr=sr,)

def show_spectrogram(spectrogram, sr, figsize=(10,4)):
    """Show the spectrogram in a jupyter notebook"""
    plt.figure(figsize=figsize)
    librosa.display.specshow(spectrogram, sr=sr, hop_length=64, x_axis='time', y_axis='hz')
    plt.colorbar(format='%2.2f')
    plt.title('Frequency Spectrogram')
    plt.tight_layout()
    
def show_complete_spectrogram(spectrogram, sr):
    show_spectrogram(np.abs(spectrogram), sr, figsize=(5,2))
    plt.show()
    show_spectrogram(np.angle(spectrogram), sr, figsize=(5,2))
    plt.show()
    show_spectrogram(np.real(spectrogram), sr, figsize=(5,2))
    plt.show()
    show_spectrogram(np.imag(spectrogram), sr, figsize=(5,2))
    plt.show()
    