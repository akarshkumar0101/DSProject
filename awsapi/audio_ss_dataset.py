import torch

class AudioSSDS(torch.utils.data.Dataset):
    # sources is a list of sources
    def __init__(self, sr, duration, sources=None):
        if isinstance(sources, tuple):
            sources = list(sources)
        if isinstance(sources, list):
#             for i, source in enumerate(sources):
# #                 if isinstance(source, str):
# #                     source = np.load(source)
#                 sources[i] = source
            sources = torch.stack(sources, dim=1)
    
        
        self.num_sources = sources.shape[1]
        self.sr = sr
        self.duration = duration
        
        self.X = sources.sum(dim=1)
        self.Y = sources
        
    def __len__(self):
        return len(self.X)
    def __getitem__(self, index):
        return self.X[index], self.Y[index]