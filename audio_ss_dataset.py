import numpy as np

from torch.utils import data

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