import audio_ss_nnio

#import matplotlib.pyplot as plt

import torch
import torchaudio

class BaseNNIO(audio_ss_nnio.AudioSSNNIO):
    def __init__(self, sr, duration, n_fft=300, normalized=False):
        super().__init__(sr, duration)
        self.n_fft = n_fft
        self.normalized = normalized
        
    def audio_to_nn_input(self, X_batch):
        # X_batch is (batch_size, len(y))
        
        X_batch = X_batch.stft(n_fft=self.n_fft, normalized=self.normalized) #stft
        X_batch =  X_batch.permute(0, -1, -3, -2) # shape
        return X_batch
    
    def audio_to_nn_output(self, Y_batch):
        # Y_batch is (batch_size, num_sources=2, len(y))
        Y_batch = Y_batch[:, 0, :].stft(n_fft=self.n_fft, normalized=self.normalized) #stft
        Y_batch = Y_batch.permute(0, -1, -3, -2) # shape
        return Y_batch
    
    def nn_input_to_audio(self, X_batch):
        X_batch = X_batch.permute(0, -2, -1, -3) # shape
        
        X_batch = torchaudio.functional.istft(X_batch, n_fft=self.n_fft, #istft
                                              normalized=self.normalized, length=int(self.sr*self.duration))
        
        return X_batch
    def nn_output_to_audio(self, Y_batch):
        Y_batch = Y_batch.permute(0, -2, -1, -3) # shape
        
        Y_batch = torchaudio.functional.istft(Y_batch, n_fft=self.n_fft, #istft
                                              normalized=self.normalized, length=int(self.sr*self.duration))
        return Y_batch
    def show_play_nn_output(self, Y_batch, X_batch, transform_X_batch=True, ts=['raw', 'audio'], sample_idx=0):
        """Convenience wrapper to fast show and play network output."""
        y = self.nn_output_to_audio(Y_batch, X_batch, transform_X_batch)[sample_idx][0]
        return self.show_play_audio(y, ts)
        
        
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
