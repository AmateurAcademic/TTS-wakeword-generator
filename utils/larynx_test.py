from ovos_plugin_manager.tts import load_tts_plugin
from os import makedirs
from load_engine_config import load_engine_config
import os.path
import time
import LarynxServerTTSPlugin

engine_config = load_engine_config('config/TTS_engine_config.json')
larynx_host = engine_config[0]
TTS_list = engine_config[1]

larynx_TTS_list = [engine for engine in TTS_list if "larynx" in engine[0]]

print(larynx_TTS_list)



TEST_UTTERANCE_PATH = './out/test/'
TEST_UTTERANCE = "This is a test"


for plug, voice, ext in TTS_list:
    engine = load_tts_plugin(plug)
    if not engine:
        continue

    config_larynx = {
        "host": larynx_host,
        "voice": voice,
        "vocoder": "hifi_gan/universal_large",
    }
    print(LarynxServerTTSPlugin.url)
    tts = engine(lang="en-us", config=config_larynx)
    print(f'config: {config_larynx}')
    print(f'engine url: {engine.url}')
"""#TODO: refactor code here to use the same code as TTS_wakeword_data_generator.py
    if tts.voice:
        voice = voice or tts.voice.replace("/", "")
    if voice:
        slug = f"{plug}_{voice}.{ext}"
    else:
        slug = f"{plug}.{ext}"

    
    path = TEST_UTTERANCE_PATH + TEST_UTTERANCE + '_' + slug
    if not os.path.isfile(path):
        try:
            tts.get_tts(TEST_UTTERANCE, path)
            tts.playback.stop()
        except:
            #NOTE: Sometimes the TTS engine times out, so it will try again... This usually works unless there is something wrong with the TTS engine/server
            print(
                f'{TEST_UTTERANCE} failed to be TTSed with {plug} on {voice} \n Waiting for a minute then trying again')
            time.sleep(60)
            try:
                tts.get_tts(TEST_UTTERANCE, path)
                tts.playback.stop()
            except:
                print(
                    f'{TEST_UTTERANCE} STILL failed to be TTSed with {plug} on {voice} \n Check your settings and run the script again')
                pass
    elif os.path.isfile(path):
        print(f"{path} already exists")
"""