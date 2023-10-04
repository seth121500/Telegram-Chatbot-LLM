import requests
import urllib
import winsound

def speak(sentence):
    speaker_id = 20
    params_encoded = urllib.parse.urlencode({'text':sentence,'speaker':speaker_id})
    r = requests.post(f'http://127.0.0.1:50021/audio_query?{params_encoded}')
    voicevox_query = r.json()
    voicevox_query['speedScale'] = 1
    voicevox_query['volumeScale'] = 2.4
    voicevox_query['intonationScale'] = 1.1
    voicevox_query['prePhonemeLength'] = 1.0
    voicevox_query['postPhonemeLength'] = 1.0
    params_encoded = urllib.parse.urlencode({'speaker':speaker_id})
    r = requests.post(f'http://127.0.0.1:50021/synthesis?{params_encoded}',json=voicevox_query)
    with open('./output.wav','wb') as outfile:
        outfile.write(r.content)

##speak("これは私がやっているテストです")