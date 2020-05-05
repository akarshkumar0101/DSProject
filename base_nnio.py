import audio_ss_nnio

import matplotlib.pyplot as plt

import numpy as np

import librosa
import librosa.display


class BaseNNIO(audio_ss_nnio.AudioSSNNIO):
    def __init__(self, sr, duration, num_sources):
        super().__init__(sr, duration, num_sources)
    def nn_num_input_channels(self):
        return 2
    def nn_num_output_channels(self):
        return 2
    def audio_to_nn_input(self, X_batch):
        return self.complex_to_channels(self.audio_to_spectrogram(X_batch))
    def audio_to_nn_output(self, Y_batch):
        res = []
        for source_idx in range(self.num_sources-1):
            res.append(self.complex_to_channels(self.audio_to_spectrogram(Y_batch[:, source_idx, :])))
        return np.concatenate(res, axis=1)
    def nn_output_to_audio(self, Y_batch):
        return self.spectrogram_to_audio(self.channels_to_complex(Y_batch))
        
    # for jupyter notebook only
    def show_audio(self, y, t='raw'):
        if t == 'raw':
            librosa.display.waveplot(y=y, sr=self.sr)
        else:
            spectrogram = self.audio_to_spectrogram([y])[0]
            if t == 'mag':
                plt.figure(figsize=(10,4))
                librosa.display.specshow(np.abs(spectrogram), sr=self.sr, hop_length=64, x_axis='time', y_axis='hz')
                plt.colorbar(format='%2.2f')
                plt.title('Magnitude of STFT')
                plt.tight_layout()
            elif t == 'detail':
                fig, axs = plt.subplots(2,2, figsize=(10,4))
                axs[0, 0].set_title('Magnitude')
                axs[0, 1].set_title('Phase')
                axs[1, 0].set_title('Real Part')
                axs[1, 1].set_title('Imag Part')
                librosa.display.specshow(np.abs(spectrogram), sr=self.sr, hop_length=64, x_axis='time', y_axis='hz', ax=axs[0, 0])
                librosa.display.specshow(np.angle(spectrogram), sr=self.sr, hop_length=64, x_axis='time', y_axis='hz', ax=axs[0, 1])
                librosa.display.specshow(np.real(spectrogram), sr=self.sr, hop_length=64, x_axis='time', y_axis='hz', ax=axs[1, 0])
                librosa.display.specshow(np.imag(spectrogram), sr=self.sr, hop_length=64, x_axis='time', y_axis='hz', ax=axs[1, 1])
    
    
    def complex_to_channels(self, spectrograms):
        """Turn the complex spectrograms into channels.
        (..., F, T) with dtype=complex -> (..., 2, F, T) with dtype=float
        """
        return np.stack((np.real(spectrograms), np.imag(spectrograms)), axis=-3)

    def channels_to_complex(self, spectrograms):
        """Turn the channels into complex spectrograms.
        (..., 2, F, T) with dtype=float -> (..., F, T) with dtype=complex
        """
        return spectrograms[..., 0, :, :] + 1.0j * spectrograms[..., 1, :, :]


    def audio_to_spectrogram(self, ys):
        """Turn a series of audio signals into complex spectrograms."""
        spectrograms = []
        for y in ys:
            spectrogram = librosa.stft(y=y, n_fft=256, hop_length=64)
            spectrograms.append(spectrogram)
        spectrograms = np.array(spectrograms)    
        return spectrograms

    def spectrogram_to_audio(self, spectrograms):
        """Turn a series of complex spectrograms into audio signals"""
        ys = []
        for spectrogram in spectrograms:
            yp = librosa.istft(spectrogram, hop_length=64)
            ys.append(yp)
        return np.array(ys)


    