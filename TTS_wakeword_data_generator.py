from multiprocessing.connection import wait
from ovos_plugin_manager.tts import load_tts_plugin


from utils.config import load_config
from utils.load_engine_config import load_engine_config

from os import makedirs
import os.path
import time

engine_config = load_engine_config('config/TTS_engine_config.json')
larynx_host = engine_config[0]
TTS_list = engine_config[1]

wakeword_config = load_config('config/TTS_wakeword_config.json')
WAKEWORD = wakeword_config['wakeword']
SYLLABLES = wakeword_config['syllables']
WAKEWORD_DIR = WAKEWORD.replace(' ', '_')
WAKEWORD_PATH = f'./out/{WAKEWORD_DIR}/TTS/wake-word/'
NOT_WAKEWORD_PATH = f'./out/{WAKEWORD_DIR}/TTS/not-wake-word/parts/'


def permutate_syllables(SYLLABLES, WAKEWORD):
    permutated_syllables = []
    number_of_syllables = len(SYLLABLES)

    for syllable in SYLLABLES:
        syllable_index = SYLLABLES.index(syllable)
        next_syllable_index = syllable_index + 2
        if next_syllable_index <= number_of_syllables:
            #NOTE: if syllable and next syllable in wakeword are seperated by a space in wakeword, then the permutated syllables are seperated by a space
            permutated_syllable = ''.join(SYLLABLES[syllable_index:next_syllable_index])
            if permutated_syllable not in WAKEWORD:
                permutated_syllable = ' '.join(SYLLABLES[syllable_index:next_syllable_index])
            permutated_syllables.append(permutated_syllable)
    return permutated_syllables

permutated_syllables = permutate_syllables(SYLLABLES, WAKEWORD)
all_syllables = SYLLABLES + permutated_syllables
TTS_utterances = [WAKEWORD] + all_syllables


makedirs(WAKEWORD_PATH, exist_ok=True)
makedirs(NOT_WAKEWORD_PATH, exist_ok=True)

print(f'The TTS engines will be scraped for the following utterances: {TTS_utterances}')

#NOTE: A lot of TTS engines are commented out because I can't get them to work for now.
#TODO: Get all TTS engines to work
#TODO: Turn this big block of code into a few functions

#TODO: Document the following in the reu These TTS voices/engines aren't enabled:
"""
Mimic sounds too artificial
("ovos-tts-plugin-mimic", None, "wav"),

Alice and Laura don't sound like en voices
("ovos-tts-plugin-responsivevoice", 'Alice', "mp3"),
("ovos-tts-plugin-responsivevoice", 'Laura', "mp3"),

Karen gives the same voice as the AustralianFemale
("ovos-tts-plugin-responsivevoice", 'Karen', "mp3"),

Martin gives some unknown female voice
("ovos-tts-plugin-responsivevoice", 'Martin', "mp3"),

EnglishUnitedKingdom gives the same as the UKEnglishFemale
("ovos-tts-plugin-responsivevoice", 'EnglishUnitedKingdom', "mp3"),

All of these aren't install by default for larynx but can be downloaded
("neon-tts-plugin-larynx-server", "southern_english_female", "wav"),
("neon-tts-plugin-larynx-server", "southern_english_male", "wav"),
("neon-tts-plugin-larynx-server", "scottish_english_male", "wav"),
("neon-tts-plugin-larynx-server", "judy_bieber", "wav"),
("neon-tts-plugin-larynx-server", "cmu_ljm", "wav"),
("neon-tts-plugin-larynx-server", "cmu_rxr", "wav"),
("neon-tts-plugin-larynx-server", "cmu_rms", "wav"),
("neon-tts-plugin-larynx-server", "cmu_slp", "wav"),
("neon-tts-plugin-larynx-server", "cmu_slt", "wav"),
("neon-tts-plugin-larynx-server", "kathleen", "wav")
"""


for plug, voice, ext in TTS_list:
    #NOTE: Loads TTS engine, returns the slug with plugin name, voice name, and extension
    engine = load_tts_plugin(plug)
    if not engine:
        continue


    config_others = {
            "voice": voice
        }

    #NOTE: I don't see a log of this TTS using my server although I get the files. WTF? 
    config_larynx = {
        "host": larynx_host,
        "voice": voice,
        "vocoder": "hifi_gan/universal_large",
    }

    if plug is "neon-tts-plugin-larynx-server":
        tts = engine(lang="en-us", config=config_larynx)
    else:
        tts = engine(lang="en-us", config=config_others)

    if tts.voice:
        voice = voice or tts.voice.replace("/", "")
        print(f'Scraping TTS {voice} model')
    if voice:
        slug = f"{plug}_{voice}.{ext}"
    else:
        slug = f"{plug}.{ext}"

    #NOTE: Creates path to save TTS files, runs TTS on each utterance, and saves to path
    for utterance in TTS_utterances:
        if utterance is WAKEWORD:
            file_name = WAKEWORD + '_' + slug
            directory = WAKEWORD_PATH
            path = directory + file_name  
        else:
            #NOTE: labeling the files with count is important for the splitting process
            file_name = str(all_syllables.index(utterance))  + '_' + utterance + '_' + slug
            directory = NOT_WAKEWORD_PATH
            path = directory + file_name
        if not os.path.isfile(path):
            try:
                tts.get_tts(utterance, path)
                tts.playback.stop()
            except:
                #NOTE: Sometimes the TTS engine times out, so it will try again... This usually works unless there is something wrong with the TTS engine/server
                print(f'{utterance} failed to be TTSed with {plug} on {voice} \n Waiting for a minute then trying again')
                time.sleep(60)
                try:
                    tts.get_tts(utterance, path)
                    tts.playback.stop()
                except:
                    print(f'{utterance} STILL failed to be TTSed with {plug} on {voice} \n Check your settings and run the script again')
                    pass
        elif os.path.isfile(path):
            print(f"{path} already exists")