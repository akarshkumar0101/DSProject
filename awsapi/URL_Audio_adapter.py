from __future__ import print_function
import urllib.request
from google_drive_downloader import GoogleDriveDownloader as gdd
import random
import string
import librosa.core
# from httplib2 import Http
# from apiclient import errors
# from apiclient.http import MediaFileUpload
# from apiclient.discovery import build
# from httplib2 import Http
# import oauth2client.file
# import mimetypes
# from pygdrive3 import service



#this will break apart the audio into segments


def url_to_audio_file(uri):
    #generate a random 8 char sequence name
    file_name = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
    file_name = './audioFiles/'+file_name+'.wav'

    gdd.download_file_from_google_drive(file_id=uri,
                                    dest_path=file_name,
                                    unzip=False)
    return file_name

#might be too long of an audio file
#need to break it into parts, feed one by one
def audio_file_to_array(audio_file, sr):
    y, _ =librosa.core.load(audio_file, sr)
    return y

def audio_array_to_duration_segments(y, sr, duration):
    '''This will cut the sound array into smaller duration segments to feed into the model
    '''
    y_list = y.tolist()
    ys = []
    for i in range(0, len(y_list), int(sr*duration)):
        y_slice = y_list[i:i+int(sr*duration)]
        if i+int(sr*duration) > len(y_list):
            y_slice.extend([0 for _ in range(i+int(sr*duration)-len(y_list))])
        ys.append(y_slice)
    return ys

def audio_to_url(path_to_file, file_name):
    # SCOPES = 'https://www.googleapis.com/auth/drive'
    # store = oauth2client.file.Storage('./DSProject-6e84665a8537.json')
    # creds = store.get()
    # drive_service = build('drive', 'v3', http=creds.authorize(Http()))
    # file_name= audio_file.split('/')[-1]
    # file_metadata = {'name': file_name}
    # media = MediaFileUpload(audio_file,
    #                         mimetype='audio/wav')
    # file = drive_service.files().create(body=file_metadata,
    #                                     media_body=media,
    #                                     fields='id').execute()
    # print(file.get('id'))
    return send_file(
         path_to_file, 
         mimetype="audio/wav", 
         as_attachment=True, 
         attachment_filename=file_name)

