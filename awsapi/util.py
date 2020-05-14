import gc
import torch
import math
import numpy as np

import torch

def generate_tone(sr, duration, freq, amplitude=None):
    """generate a tone or tones with a sample_rate sr (float), duration in seconds, and the frequencies and amplitudes (np arrays)"""
    # cases: number number, array number, array array
    if amplitude is None:
        amplitude = np.ones_like(freq)
    freq, amplitude = freq[:, None], amplitude[:, None]
    length = int(sr*duration)
    full = np.tile(np.arange(length), (freq.shape[1], 1))
    y = amplitude * np.cos(2*np.pi/sr * freq * full)
    return y

def get_batch_indices(all_indices, batch_size, shuffle=True, drop_last=False):

    if drop_last:
        num_batches = len(all_indices)//batch_size
    else:
        num_batches = math.ceil(len(all_indices)/batch_size)
    batch_indices = [all_indices[i*batch_size:(i+1)*batch_size] for i in range(num_batches)]
    if shuffle:
        np.random.shuffle(batch_indices)
    return batch_indices


# utility
def to_torch(*arrays, device, dtype):
    if len(arrays) == 1:
        array = arrays[0]
        if isinstance(array, np.ndarray):
            array = torch.from_numpy(array)
        return array.to(device, dtype)
    ret = ()
    for array in arrays:
        ret += to_torch(array, device=device, dtype=dtype),
    return ret

def to_np(*arrays):
    if len(arrays) == 1:
        return arrays[0].detach().cpu().numpy()
    ret = ()
    for array in arrays:
        ret += to_np(array),
    return ret


def clear_mem(print_mem=False):
    gc.collect()
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
        if print_mem:
            print('total: ', torch.cuda.get_device_properties(0).total_memory/1e9)
            print('cached: ', torch.cuda.memory_cached()/1e9)
            print('allocated: ', torch.cuda.memory_allocated()/1e9)
        
        
