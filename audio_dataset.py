# audio_dataset.py
import librosa
import os
import random

import numpy as np

audio_endings = ('.mp3', '.wav', '.flac')

class AudioDataSet:
    """AudioDataset helps organize and load a audio dataset split into different directories. 
    Because audio takes up so much space, this will only load the clips that need to be used"""
    def __init__(self, ds_dir, sr, duration, shuffle=True, random_state=42):
        """Initalize with the directory of audio files ds_dir (will scan all subdirectories recursively), 
        the sample_rate sr you wish to have on the whole dataset, and duration of the clips in seconds."""
        self.sr = sr
        self.duration = duration

        self.current_file_idx = 0
        
        self.files = []
        for r, d, f in os.walk(ds_dir):
            for file in f:
                if file.endswith(audio_endings):
                    self.files.append(os.path.join(r, file))
                    
        if shuffle:
            rand = random.Random(random_state)
            rand.shuffle(self.files)
    
    def num_samples(self):
        """The number of files/sampels in audio set."""
        return len(self.files)
    
    def load(self, file_idxs, sr=None, duration=None, pbar=None):
        """Load the specified file indices as an np array of shape (len(file_idxs), sr*duration)"""
        if sr is None:
            sr = self.sr
        if duration is None:
            duration = self.duration
        ys = []
        if pbar is not None:
            pbar.reset(total=len(file_idxs))
        for file_idx in file_idxs:
            y, _ = librosa.load(self.files[file_idx], sr=sr, mono=True, offset=0.0, duration=duration)
            y = librosa.util.fix_length(y, int(sr*duration), mode='wrap')
            ys.append(y)
            if pbar is not None:
                pbar.update(1)
        return np.array(ys)

    def load_next(self, batch_size, sr=None, duration=None, pbar=None):
        """Load the next batch_size files as an np array of shape (batch_size, sr*duration)"""
        if self.current_file_idx + batch_size > self.num_samples():
            self.current_file_idx = 0
            
        file_idxs = range(self.current_file_idx, self.current_file_idx + batch_size)
        self.current_file_idx += batch_size
        return self.load(file_idxs, sr=sr, duration=duration, pbar=pbar)
    def reset_next(self):
        """Reset the file index for the load_next function."""
        self.current_file_idx = 0

class FastAudioDataSet:
    def __init__(self, fads_file):
        self.data = np.load(fads_file)
        self.current_idx = 0
    
    def get_data(self):
        return self.data
    
    def num_samples(self):
        return len(self.data)
    
    def get_idxs(self, idxs):
        return self.data[idxs]
    
    def get_next(self, batch_size):
        if self.current_idx + batch_size > self.num_samples():
            self.current_idx = 0
        idxs = range(self.current_idx, self.current_idx+batch_size)
        self.current_idx += batch_size
        return self.get_idxs(idxs)
    
    def reset_next(self):
        self.current_idx = 0
    

def generate_tone(sr, duration, freq, amplitude=None):
    """generate a tone or tones with a sample_rate sr (float), duration in seconds, and the frequencies and amplitudes (np arrays)"""
    # cases: number number, array number, array array
    if amplitude is None:
        amplitude = np.ones_like(freq)
    freq, amplitude = freq[:, None], amplitude[:, None]
    length = int(sr*duration)
    full = np.tile(np.arange(length), (freq.shape[1], 1))
    y = amplitude * np.sin(2*np.pi/sr * freq * full)
    return y