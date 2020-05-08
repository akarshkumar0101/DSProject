import audio_ss_nnio

import matplotlib.pyplot as plt

import numpy as np

class BaseNNIO(audio_ss_nnio.AudioSSNNIO):
    def __init__(self, sr, duration, n_fft=300, normalized=False, magphase_representation=False):
        super().__init__(sr, duration)
        self.n_fft = n_fft
        self.normalized = normalized
        
    def audio_to_nn_input(self, X_batch):
        # X_batch is (batch_size, len(y))
        return X_batch.stft(n_fft=self.n_fft, normalized=self.normalized).permute(0, -1, -3, -2)
    
    def audio_to_nn_output(self, Y_batch):
        # Y_batch is (batch_size, num_sources=2, len(y))
        return Y_batch[:, 0, :].stft(n_fft=self.n_fft, normalized=self.normalized).permute(0, -1, -3, -2)
    
    def nn_input_to_audio(self, X_batch):
        return torchaudio.functional.istft(X_batch.permute(0, -2, -1, -3), 
                                           n_fft=self.n_fft, normalized=self.normalized, length=int(self.sr*self.duration))
    def nn_output_to_audio(self, Y_batch):
        voice = torchaudio.functional.istft(Y_batch.permute(0, -2, -1, -3), 
                                           n_fft=self.n_fft, normalized=self.normalized, length=int(self.sr*self.duration))
        return voice
        
        
    # for jupyter notebook only
    def show_play_audio(self, y, ts=['raw', 'audio']):
        spectrogram = y.stft(n_fft=self.n_fft, normalized=self.normalized)
        spec_mag, spec_phase = torchaudio.functional.magphase(spectrogram)
        
        if 'mag' in ts:
            plt.figure(figsize=(10,4))
            plt.imshow(spec_mag.numpy())
            plt.colorbar(format='%2.2f')
            plt.title('Magnitude of STFT')
            plt.tight_layout()
            plt.show()
        if 'detail' in ts:
            fig, axs = plt.subplots(2,2, figsize=(10,4))
            axs[0, 0].set_title('Magnitude')
            axs[0, 1].set_title('Phase')
            axs[1, 0].set_title('Real Part')
            axs[1, 1].set_title('Imag Part')
            
            axs[0, 0].imshow(spec_mag.numpy())
            axs[0, 1].imshow(spec_phase.numpy())
            axs[1, 0].imshow(spectrogram[..., 0].numpy())
            axs[1, 1].imshow(spectrogram[..., 1].numpy())
            plt.show()
        super().show_play_audio(y, ts)
