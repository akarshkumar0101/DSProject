import matplotlib.pyplot as plt
import numpy as np

from IPython.display import Audio, display

import librosa
import librosa.display

class AudioSSNNIO():
    def __init__(self, sr, duration, num_sources):
        """Initialize with sr and duration. """
        self.sr = sr
        self.duration = duration
        self.num_sources = num_sources
        
    def nn_num_input_channels(self):
        """The number of input channels you wish the neural network to process."""
        raise NotImplementedError
    def nn_num_output_channels(self):
        """The number of output channels you wish the neural network to learn."""
        raise NotImplementedError
        
    def audio_to_nn_input(self, X_batch):
        """Transform the given mixed signal for the neural network to input."""
        raise NotImplementedError
    def audio_to_nn_output(self, Y_batch):
        """Transform the given source separated signals for the neural network to output."""
        raise notImplementedError

    def nn_output_to_audio(self, Y_batch):
        """Transform the output of the neural network back into usable audio."""
        raise NotImplementedError
    
    # for jupyter notebook only
    def play_audio(self, y):
        """Play the signal y in a jupyter notebook."""
        display(Audio(y, rate=self.sr))

    def show_audio(self, y, t='raw'):
        """Show the signal y in a jupyter notebook"""
        if t == 'raw':
            librosa.display.waveplot(y=y, sr=self.sr)
    
    def show_and_play_audio(self, y, t='raw'):
        self.show_audio(y, t=t)
        plt.show()
        self.play_audio(y)

