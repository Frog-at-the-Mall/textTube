#!/usr/bin/env python

import youtube_dl
import sys
import subprocess
from ibm_watson import SpeechToTextV1
from ibm_watson.websocket import RecognizeCallback, AudioSource
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

SAVE_PATH = r"C:\Users\mattb\PythonDev\tubeText"
link = sys.argv[1]
print("ok")

ydl_opts = {
    'outtmpl': 'C:\\Users\\mattb\\PythonDev\\textTube\\audio.wav',
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
}
with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    ydl.download([link]) 
print('Download Completed!')
print('Now sending to our boy Watson')

#get these from ibm watson services page
apikey = 'li6eCcgWXOnPeRe7cIciTLTnawPwxbN3Neh9OJiQzAiE'
url = 'https://api.us-south.speech-to-text.watson.cloud.ibm.com/instances/a1e90730-6be0-4eaa-8b7e-0640c2805118'

# Setup service
authenticator = IAMAuthenticator(apikey)
stt = SpeechToTextV1(authenticator=authenticator)
stt.set_service_url(url)

with open('audio.mp3', 'rb') as f:
    res = stt.recognize(audio=f, content_type='audio/mp3', model='en-US_NarrowbandModel', continuous=True).get_result()

len(res['results'])
text = [result['alternatives'][0]['transcript'].rstrip() + '.\n' for result in res['results']]
transcript = ''.join(text)
with open('output.txt', 'w') as out:
    out.writelines(transcript)

print('Complete')
