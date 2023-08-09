import io, os
from google.oauth2 import service_account
from google.cloud import speech
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/transcription',methods = ['POST'])
def transcribe():
    client_file = 'API Keys/meta-buckeye-390005-463d1940e83d.json'
    credentials = service_account.Credentials.from_service_account_file(client_file)
    client = speech.SpeechClient(credentials=credentials)
    data = request.get_json()
    audio_file = "/home/ubuntu/Audio/" + data['value']
    with io.open(audio_file, 'rb') as f:
        content = f.read()
        audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
        encoding = speech.RecognitionConfig.AudioEncoding.LINEAR16,
        #sample_rate_hertz = 44100,
        language_code = 'en-US'
    )
    response = client.recognize(config=config, audio = audio)
    transcription = response.results[0].alternatives[0].transcript
    print(transcription)
    os.remove(audio_file)
    return transcription

if __name__ == '__main__':
    app.run(debug = True)