%matplotlib inline
import gc

import matplotlib.pyplot as plt
import numpy as np

from tqdm.notebook import tqdm

import librosa
import librosa.display

import torch
import torch.nn as nn
import torchaudio

from torchsummary import summary

import util
import audio_ss_dataset
import base_nnio
import mag_nnio
import models.base_models

torch.manual_seed(0)
np.random.seed(0)



from models.base_models import *


model = torch.load('models/ftnn_naive_med_epochs300.pth', map_location=torch.device('cpu'))


audionnio = base_nnio.BaseNNIO(8000, 2.0)

def discard_tone(y, sr):
    """Discards the tone in a audio sample.
    y should be a numpy array of size (sr*2.0)
    where sr is the sample rate."""
    y = torch.from_numpy(y).to(torch.float)
    y = torchaudio.transforms.Resample(sr, 8000) (y)
    y = audionnio.audio_to_nn_input(y[None, ...])
    with torch.no_grad():
        y = model(y)
    y = audionnio.nn_output_to_audio(y)[0, ...]
    return y.numpy()
