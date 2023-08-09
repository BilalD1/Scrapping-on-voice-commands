from cluster import Cluster
from db import DBhelper
from flask import Flask, request, jsonify
import io, os, subprocess
from google.oauth2 import service_account
from google.cloud import speech
from flask_cors import CORS

def mp3_to_wav(audio_name):
    print(audio_name)
    folder_path = '/home/ubuntu/Audio'
    mp3_file = folder_path + "/"  + audio_name
    wav_file = folder_path + "/" + str(audio_name[:-4]) + ".wav"
    input_file_path = mp3_file
    output_file_path = wav_file
    analyzeduration_microseconds = 10000000  # 10 seconds
    probesize_bytes = 5000000  # 5 megabytes
    ffmpeg_command = f'ffmpeg -analyzeduration {analyzeduration_microseconds} -probesize {probesize_bytes} -i "{input_file_path}" "{output_file_path}"'
    try:
        subprocess.run(ffmpeg_command, check=True, shell=True, stderr=subprocess.PIPE)
        print('FFmpeg command executed successfully.')
    except subprocess.CalledProcessError as e:
        print(f'FFmpeg execution error: {e.stderr.decode()}')
    os.remove(mp3_file)
    del input_file_path,mp3_file,output_file_path,analyzeduration_microseconds
    return wav_file

app = Flask(__name__)
CORS(app)

@app.route("/fetch_links", methods = ['POST'])
def fetch_links():
    db_helper = DBhelper()
    clus = Cluster()
    link_request = request.get_json()
    search_query = link_request["query"]
    label = clus.predict_cluster(search_query)
    links = db_helper.search_db(label).replace("[","").replace("]","").replace('"',"").split(",")
    if (search_query not in clus.sentences) and ("diabetes" in search_query):
        clus.append_sentence(search_query)
    del clus, db_helper
    return links

@app.route('/transcription',methods = ['POST'])
def transcribe():
    client_file = 'API Keys/meta-buckeye-390005-463d1940e83d.json'
    credentials = service_account.Credentials.from_service_account_file(client_file)
    client = speech.SpeechClient(credentials=credentials)
    data = request.get_json()
    
    audio_file = "Audio/" + data['value']
    if data['value'][-3:] == "wav":
        with io.open(audio_file, 'rb') as f:
            content = f.read()
            audio = speech.RecognitionAudio(content=content)
        config = speech.RecognitionConfig(
            encoding = speech.RecognitionConfig.AudioEncoding.LINEAR16,
            language_code = 'en-US'
        )
        response = client.recognize(config=config, audio = audio)
        try:
            transcription = response.results[0].alternatives[0].transcript
        except:
            transcription = "Audio is empty"
        os.remove(audio_file)
        return transcription

    elif data["value"][-3:]=="mp3":
        try:
            audio_file = mp3_to_wav(data['value'])
        except Exception as e:
            return "code: 1 An unexpected error occurred:"+str(e)
        try:
            with io.open(audio_file, 'rb') as f:
                content = f.read()
                audio = speech.RecognitionAudio(content=content)
        except Exception as e:
            return "Code: 2 An unexpected error occurred:"+str(e)
        try:
            config = speech.RecognitionConfig(
                encoding = speech.RecognitionConfig.AudioEncoding.LINEAR16,
                language_code = 'en-US'
            )
            response = client.recognize(config=config, audio = audio)
            transcription = response.results[0].alternatives[0].transcript
        except Exception as e:
            return "code: 3 An unexpected error occurred:"+str(e)
        os.remove(audio_file)
        return transcription
if __name__ == '__main__':
    app.run(debug = True)