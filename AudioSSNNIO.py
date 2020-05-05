import matplotlib.pyplot as plt
import numpy as np

from IPython.display import Audio, display, clear_output

import librosa
import librosa.display

class AudioSSDS(data.Dataset):
    # sources is a list of sources
    def __init__(self, sr, duration, sources=None):
        if isinstance(sources, tuple):
            sources = list(sources)
        if isinstance(sources, list):
            for i, source in enumerate(sources):
                if isinstance(source, str):
                    source = np.load(source)
                sources[i] = source
            sources = np.stack(sources, axis=1)
            
        self.num_sources = len(sources)
        self.sr = sr
        self.duration = duration
        
        self.X = sources.sum(axis=1)
        self.Y = sources
        
    def __len__(self):
        return len(self.X)
    def __getitem__(self, index):
        return self.X[index], self.Y[index]

class AudioNNIOBase():
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