from flask import Flask, Response, jsonify, request, send_file
import http.client
import requests
import json
from flask_cors import CORS
import os
# from google.cloud import speech_v1p1beta1
# from google.cloud.speech_v1p1beta1 import enums
from URL_Audio_adapter import *
from util import *
import random
import models.base_models
from models.base_models import *
from discard_tone import *
# import speech_recognition
import urllib.request
from U_Net_model import unet
from Prediction import prediction
from scipy.io.wavfile import write


app = Flask(__name__)
CORS(app)

@app.route("/") 
def index(): 
    return "Hello, world!"

'''

at the time this code only takes a file loaded onto GS Bucket
-may be a feature or a bug
-want to fix it most likely
-run this to get this to work:
http://127.0.0.1:5000/speech_to_text?uri={"uri":"gs://cloud-samples-data/speech/brooklyn_bridge.mp3"}
'''
# 10B2_bsB99wG4u1ejGCPPizj3MYaIiz-P

@app.route('/speech_recognition')
def speech_recognize():
    '''So far, this code is able to store a file into file name.
    audio_file has the name of the file, e.g. ./audio.wav, which is saved locally by urlretrieve
    '''
    args = request.args
    uri = json.loads(args['uri'])['uri']
    # return uri
    model = args['model']
    mix = args['mix']
    audio_file = url_to_audio_file(uri)
    '''
    currently we only support tone
    '''
    if model == 'Tone':
        y = audio_file_to_array(audio_file, 8000)
        #first add a random tone
        frequency = random.randint(500, 1200)
        if 'mix' in args:
            y_tone = generate_tone(8000, len(y)/8000, np.array([frequency]), np.array([0.06]))[0]
            y = np.add(y, y_tone)
        #handle tone: this will return the URL
        #takes 2 sec clips and 8000 sr
        ys = audio_array_to_duration_segments(y, 8000, 2.0 )
        #now get the results for each of the ys and, get the individual sound arrays, concatenate them, and convert to a .wav
        #file locally
        total_model_output = []
        for y in ys:
            model_output = discard_tone(np.array(y), 8000)
            total_model_output.extend(model_output.tolist())
        denoised_data = np.array(total_model_output)
        print(denoised_data.shape)
        file_name = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        file_name = file_name+'.wav'
        path_to_file='./audioFiles/'+file_name
        # librosa.output.write_wav(path_to_file, denoised_data[0], 8000)
        write(path_to_file, 8000, denoised_data)
        # return path_to_file
        return send_file(
            path_to_file, 
            mimetype="audio/wav", 
            as_attachment=True, 
            attachment_filename=file_name
        )
    elif model == "Dog":
        audio_file = url_to_audio_file(uri)
        weights_path = './dog_model'
        model = unet()
        # audio_input_prediction = [audio_file]
        sample_rate = 8000
        min_duration = 1
        frame_length = 8064
        hop_length_frame = 8064
        n_fft = 255
        hop_length_fft = 63
        #we need to split the arbitrary length audio file into 

        sr, data_hold = scipy.io.wavfile.read(audio_file)  
        broken = [data_hold[x:x+sr] for x in range(0, len(data_hold), sr)]
        one_sec_files = []
        for i in broken:
            t = ''.join(random.choices(string.ascii_uppercase + string.digits, k=12))
            file_name = './audioFiles/'+t+'.wav'
            i = np.array(i,dtype=np.float32)
            write(t, sr, i)
            one_sec_files.append(t)


        final_sound_list = []
        for one_sec_file in one_sec_files:
            denoised_data = prediction(weights_path, model, [one_sec_file], sample_rate, 
                                    min_duration, frame_length, hop_length_frame, n_fft, hop_length_fft)
            final_sound_list.extend(denoised_data.tolist())

        file_name = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))[1]
        file_name = file_name+'.wav'
        path_to_file='./audioFiles/'+file_name
        librosa.output.write_wav(path_to_file, 8000, numpy.array(final_sound_list))
        return send_file(
            path_to_file, 
            mimetype="audio/wav", 
            as_attachment=True, 
            attachment_filename=file_name
        )

@app.route('/speech_to_text')
def sample_recognize():
    """
    Performs synchronous speech recognition on an audio file
    Args:
      storage_uri URI for audio file in Cloud Storage, e.g. gs://[BUCKET]/[FILE]
    """
    args = request.args
    storage_uri = json.loads(args['uri'])['uri']
    print(storage_uri)
    client = speech_v1p1beta1.SpeechClient()
    # storage_uri = 'gs://cloud-samples-data/speech/brooklyn_bridge.mp3'
    # The language of the supplied audio
    language_code = "en-US"
    # Sample rate in Hertz of the audio data sent
    sample_rate_hertz = 44100
    # Encoding of audio data sent. This sample sets this explicitly.
    # This field is optional for FLAC and WAV audio formats.
    encoding = enums.RecognitionConfig.AudioEncoding.MP3
    config = {
        "language_code": language_code,
        "sample_rate_hertz": sample_rate_hertz,
        "encoding": encoding,
    }
    audio = {"uri": storage_uri}
    response = client.recognize(config, audio)
    for result in response.results:
        # First alternative is the most probable result
        alternative = result.alternatives[0]
        break
    return {
        'transcript': alternative.transcript
    }

if __name__ == "__main__":
    app.run()