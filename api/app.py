from flask import Flask, Response, jsonify, request
import http.client
import requests
import json
from flask_cors import CORS
import os
from google.cloud import speech_v1p1beta1
from google.cloud.speech_v1p1beta1 import enums
import speech_recognition
import urllib.request


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

@app.route('/speech_recognition')
def speech_recognize():

    '''So far, this code is able to store a file into file name.
    audio_file has the name of the file, e.g. ./audio.wav, which is saved locally by urlretrieve
    '''

    args = request.args
    uri = json.loads(args['uri'])['uri']
    file_name = uri.split('/')[-1]
    audio_file, _ = urllib.request.urlretrieve(uri, file_name)








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

