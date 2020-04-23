# audio_dataset.py
import librosa
import os
import random

import numpy as np

from common_audio import set_sample_length

rand = random.Random(42)

audio_endings = ('.mp3', '.wav', '.flac')

class AudioDataSet:
    def __init__(self, ds_dir, sr, duration):
        self.sr = sr
        self.duration = duration

        self.current_file_idx = 0
        
        self.files = []
        for r, d, f in os.walk(ds_dir):
            for file in f:
                if file.endswith(audio_endings):
                    self.files.append(os.path.join(r, file))
        rand.shuffle(self.files)
        
    def length(self):
        return len(self.files)
    
    def load(self, file_idxs, sr=None, duration=None, pbar=None):
        if sr is None:
            sr = self.sr
        if duration is None:
            duration = self.duration
        ys = []
        if pbar is not None:
            pbar.reset(total=len(file_idxs))
        for file_idx in file_idxs:
            y, _ = librosa.load(self.files[file_idx], sr=sr, mono=True, offset=0.0, duration=duration)
            y = set_sample_length(y, sample_length=int(sr*duration))
            ys.append(y)
            if pbar is not None:
                pbar.update(1)
        return np.array(ys)

    def load_next(self, batch_num, sr=None, duration=None, pbar=None):
        if self.current_file_idx + batch_num > self.length():
            self.current_file_idx = 0
            
        file_idxs = range(self.current_file_idx, self.current_file_idx + batch_num)
        self.current_file_idx += batch_num
        return self.load(file_idxs, sr=sr, duration=duration, pbar=pbar)
    def reset_next(self):
        self.current_file_idx = 0