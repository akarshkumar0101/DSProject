from flask import Flask, Response, jsonify, request
import http.client
import requests
import json
from flask_cors import CORS
import os
from google.cloud import speech_v1p1beta1
from google.cloud.speech_v1p1beta1 import enums


app = Flask(__name__)
CORS(app)

@app.route("/") 
def index(): 
    return "Hello, world!"


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
    print(type(response.results))
    for result in response.results:
        # First alternative is the most probable result
        alternative = result.alternatives[0]
        print(u"Transcript: {}".format(alternative.transcript))
        print(type(alternative.transcript))
        break

    return {
        'transcript': alternative.transcript
    }

if __name__ == "__main__":
    app.run()

