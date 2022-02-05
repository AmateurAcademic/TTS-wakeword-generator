from ovos_plugin_manager.tts import load_tts_plugin
from os import makedirs
from load_engine_config import load_engine_config
import os.path
import time

engine_config = load_engine_config('config/TTS_engine_config.json')
larynx_host = engine_config[0]
TTS_list = engine_config[1]

def load_popular_word_corpus(file_path):
    with open(file_path, 'r') as f:
        popular_words = f.read().splitlines()
    return popular_words

RANDOM_COLLECTED_UTTERANCES_PATH = './out/random/'
POPULAR_WORDS = load_popular_word_corpus('./config/google-10000-english.txt')


longer_popular_words = []
for utterance in POPULAR_WORDS:
    if len(utterance) > 3:
        longer_popular_words.append(utterance)
        

makedirs(RANDOM_COLLECTED_UTTERANCES_PATH, exist_ok=True)

for plug, voice, ext in TTS_list:
    engine = load_tts_plugin(plug)
    if not engine:
        continue
    
    config_others = {
        "voice": voice
        }

    config_larynx = {
        "host": larynx_host,
        "voice": voice,
        "vocoder": "hifi_gan/universal_large",
    }

    if "larynx" in plug:
        tts = engine(lang="en-us", config=config_larynx)
    else:
        tts = engine(lang="en-us", config=config_others)
#TODO: refactor code here to use the same code as TTS_wakeword_data_generator.py
    if tts.voice:
        voice = voice or tts.voice.replace("/", "")
    if voice:
        slug = f"{plug}_{voice}.{ext}"
    else:
        slug = f"{plug}.{ext}"

    for utterance in longer_popular_words:
        path = RANDOM_COLLECTED_UTTERANCES_PATH + utterance + '_' + slug
        if not os.path.isfile(path):
            try:
                tts.get_tts(utterance, path)
                tts.playback.stop()
            except:
                #NOTE: Sometimes the TTS engine times out, so it will try again... This usually works unless there is something wrong with the TTS engine/server
                print(
                    f'{utterance} failed to be TTSed with {plug} on {voice} \n Waiting for a minute then trying again')
                time.sleep(60)
                try:
                    tts.get_tts(utterance, path)
                    tts.playback.stop()
                except:
                    print(
                        f'{utterance} STILL failed to be TTSed with {plug} on {voice} \n Check your settings and run the script again')
                    pass
        elif os.path.isfile(path):
            print(f"{path} already exists")
