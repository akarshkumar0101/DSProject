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

def complex_to_log_magnitude_phase_channels(spectrograms):
    """
    Turn the complex spectrograms into log(magnitude) and phase channels.
    (..., F, T) with dtype=complex -> (..., 2, F, T) with dtype=float
    """
    return np.stack((np.log(np.abs(spectrograms)), np.angle(spectrograms)),axis=-3)
    
    
def log_mag_phase_to_complex(spectrograms):
    """Turn the log and phase channels channels into complex spectrograms.
    (..., 2, F, T) with dtype=float -> (..., F, T) with dtype=complex
    uses euler's formula to convert back: complex = magnitude*e^(j*phase_angle)
    """
    return np.exp(spectrograms[..., 0, :, :]) * np.exp(1.0j * spectrograms[..., 1, :, :])


    
def audio_to_spectrogram(ys, sr, mel=False, n_fft=256, hop_length=64):
    """
    Turn a series of audio signals into complex spectrograms.
    If mel is true, the mel spectrogram will be generated, else the normal one 
    """
    spectrograms = []
    for y in ys:
        spectrogram_params = {'y':y, 'n_fft':n_fft, 'hop_length':hop_length}
        if mel:
            spectrogram_params['sr']=sr
        spectrogram = librosa.feature.melspectrogram(**spectrogram_params) if mel \
            else librosa.stft(**spectrogram_params)
#         spectrogram = np.stack((np.real(spectrogram), np.imag(spectrogram)))
        spectrograms.append(spectrogram)
    spectrograms = np.array(spectrograms)    
    return spectrograms   

def spectrogram_to_audio(spectrograms, sr, mel=False, n_fft=256, hop_length=64):
    """
    Turn a series of complex spectrograms into audio signals
    If mel is true, it convert the spectrogram to stft, then apply the istft
    """
    ys = []
    for spectrogram in spectrograms:
        yp = librosa.istft(librosa.feature.inverse.mel_to_stft(spectrogram, n_fft=n_fft, sr=sr), hop_length=hop_length) if mel \
            else librosa.istft(spectrogram, hop_length=hop_length)
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

def show_spectrogram(spectrogram, sr, figsize=(10,4), y_axis='hz'):
    """Show the spectrogram in a jupyter notebook"""
    plt.figure(figsize=figsize)
    librosa.display.specshow(spectrogram, sr=sr, hop_length=64, x_axis='time', y_axis=y_axis)
    plt.colorbar(format='%2.2f')
    plt.title('Frequency Spectogram ( {} )'.format(y_axis))
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
    
print('test')
