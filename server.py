from flask import Flask, render_template, request,jsonify,make_response
from werkzeug.utils import secure_filename
import os
import json
import librosa
import soundfile as sf
app = Flask(__name__)

UPLOAD_FOLDER = '/Users/chitralekhagupta/Documents/InfoSystems/SpeechTherapy/speech-to-text-cloud-offline/flasktry/upload'
# fullfilepath = os.path.join(UPLOAD_FOLDER, 'test.wav' ) #default test audio file
# @app.route('/')
# def index():
#   return render_template('index.html')

@app.route('/', methods = ['GET', 'POST'])
def index():
    print(request.method)
    if request.method == 'POST':
        print('post')
        f = request.files['file']
        filename = secure_filename(f.filename)
        fullfilepath = os.path.join(UPLOAD_FOLDER, filename )
        f.save(fullfilepath)
        fullfilepath = ConvertToWav(fullfilepath)

        transcript,confidence,startends = transcribe_file(fullfilepath)
        message = {'transcript':' '.join(transcript),'segments':transcript,'confidence':confidence, 'timestamps':startends}
        # lowconf_times = ""
        lowconf_times = []
        transcription = ''
        for ind in range(len(confidence)):
            if confidence[ind]<0.9:
                transcription = transcription+'<span style="background-color:#E78587">'+transcript[ind]+'</span>'
                # dictionary = "{ start: "+str(startends[ind][0])+", end: "+str(startends[ind][1])+", loop: false, color: 'hsla(359, 67%, 71%, 0.5)'}" #'hsla(400, 100%, 30%, 0.5)'
                dictionary = { 'start': startends[ind][0], 'end': startends[ind][1], 'loop': False, 'color': 'hsla(359, 67%, 71%, 0.5)'} #'hsla(400, 100%, 30%, 0.5)'
                lowconf_times.append(dictionary)
                # lowconf_times = lowconf_times+dictionary+','
            else:
                transcription = transcription+transcript[ind]
            transcription = transcription+' '
        # print(json.dumps(lowconf_times))
        return render_template("index.html",final = transcription,lowconf_regions=json.dumps(lowconf_times)) #lowconf_times[:-1]) #message['transcript']) #make_response(jsonify(message),201)
        # return 'success'
        
    elif request.method == 'GET':
        return render_template('index.html')
    else:
        return 'Unsuccessful'
    

# @app.route('/link/')
# def my_link():
#   print ('I got clicked!')
#   return 'This is from python script.'

def transcribe_file(speech_file):
    wordlevel = 1
    """Transcribe the given audio file asynchronously."""
    from google.cloud import speech

    client = speech.SpeechClient()

    with open(speech_file, "rb") as audio_file:
        content = audio_file.read()

    """
     Note that transcription is limited to a 60 seconds audio file.
     Use a GCS file for audio longer than 1 minute.
    """
    audio = speech.RecognitionAudio(content=content) #uri=speech_file) #

    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="en-US",
        enable_word_time_offsets=True,
        enable_word_confidence=True
    )
    operation = client.long_running_recognize(config=config, audio=audio)

    print("Waiting for operation to complete...")
    response = operation.result(timeout=90)

    # Each result is for a consecutive portion of the audio. Iterate through
    # them to get the transcripts for the entire audio file.
    transcript = []
    confidence = []
    startends = []
    for result in response.results:
        # The first alternative is the most likely one for this portion.
        alternative = result.alternatives[0]
        # print(u"Transcript: {}".format(alternative.transcript))
        # print("Confidence: {}".format(alternative.confidence))

        if not wordlevel:
            transcript.append(alternative.transcript)
            confidence.append(alternative.confidence)
            count = 0
            startend = []

        for word_info in alternative.words:
            word = word_info.word
            start_time = word_info.start_time
            end_time = word_info.end_time
            conf = word_info.confidence
            if wordlevel:
                transcript.append(word)
                confidence.append(conf)
                startends.append([start_time.total_seconds(),end_time.total_seconds()])

            # print(
            #     f"Word: {word}, start_time: {start_time.total_seconds()}, end_time: {end_time.total_seconds()}"
            # )
            if not wordlevel:
                if count==0:
                    startend.append(start_time.total_seconds())
                count=count+1
        if not wordlevel:
            startend.append(end_time.total_seconds())
            startends.append(startend)
    print(transcript,confidence,startends)
    return transcript,confidence,startends #result.alternatives[0].transcript

def ConvertToWav(filename):
    newfilename = filename.split('.')[0]+'.wav'
    data,sr = librosa.load(filename,sr=16000,mono=True)
    sf.write(newfilename, data, sr)
    return newfilename
    
if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port=8080)