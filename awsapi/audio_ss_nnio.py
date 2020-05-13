#import matplotlib.pyplot as plt
import numpy as np

#from IPython.display import Audio, display

class AudioSSNNIO():
    """Class to control Neural Network Input/Output for project in Audio Source Separation"""
    def __init__(self, sr, duration):
        """Initialize with sr, duration, and the number of sources."""
        self.sr = sr
        self.duration = duration
        
    def audio_to_nn_input(self, X_batch):
        """Transform the given mixed signal for the neural network to input.
        X_batch will have shape (batch_size, len(y)) where len(y) = sr*duration."""
        raise NotImplementedError
    def audio_to_nn_output(self, Y_batch):
        """Transform the given source separated signals for the neural network to output.
        Y_batch will have shape (batch_size, num_sources=2, len(y)) where len(y) = sr*duration."""
        raise NotImplementedError
        
    def nn_input_to_audio(self, X_batch):
        """Transform the input of the neural network back into usable audio.
        X_batch will have shape (batch_size, nn_num_input_channels(), h, w) where h, w are 
        determined by the size of the input spectrum in audio_to_nn_input(...)."""
        raise NotImplementedError

    def nn_output_to_audio(self, Y_batch):
        """Transform the output of the neural network back into usable audio.
        Y_batch will have shape (batch_size, nn_num_output_channels(), h, w) where h, w are 
        determined by the size of the input spectrum in audio_to_nn_output(...)."""
        raise NotImplementedError
        
    def show_play_nn_input(self, X_batch, ts=['raw', 'audio'], sample_idx=0):
        """Convenience wrapper to fast show and play network input."""
        y = self.nn_input_to_audio(X_batch)[sample_idx]
        return self.show_play_audio(y, ts)
    def show_play_nn_output(self, Y_batch, ts=['raw', 'audio'], sample_idx=0):
        """Convenience wrapper to fast show and play network output."""
        y = self.nn_output_to_audio(Y_batch)[sample_idx]
        return self.show_play_audio(y, ts)
    
    # for jupyter notebook only
    def show_play_audio(self, y, ts=['raw', 'audio']):
        """Show the signal y in a jupyter notebook. 
        ts determines different ways you want to show the signal. 
        ts can have:
        -'raw'
        -'audio'
        other options can be added on by different implementations."""
        
        if 'raw' in ts:
            plt.plot(np.linspace(0, self.duration, len(y)), y)
            plt.show()
        if 'audio' in ts:
            display(Audio(y, rate=self.sr))

