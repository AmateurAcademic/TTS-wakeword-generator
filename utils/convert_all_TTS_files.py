import json
from basic_audio_operations_class import BasicAudioOperations
from utils.config import load_config

config = load_config(config_file='./config/TTS_wakeword_config.json')


WAKEWORD = config['wakeword']
SYLLABLES = config['syllables']
WAKEWORD_DIR = WAKEWORD.replace(' ', '_')
#TODO: add random text
WAKEWORD_PATH = f'./out/{WAKEWORD_DIR}/TTS/wake-word/'
NOT_WAKEWORD_PATH = f'./out/{WAKEWORD_DIR}/TTS/not-wake-word/parts/'
RANDOM_NOT_WAKEWORD_PATH = './out/random_TTS_mp3s/'

source_directories = [
    WAKEWORD_PATH,
    NOT_WAKEWORD_PATH,
    RANDOM_NOT_WAKEWORD_PATH
    ]
destination_directories = [
    f'./out/converted/{WAKEWORD_DIR}/TTS/wake-word/',
    f'./out/converted/{WAKEWORD_DIR}/TTS/not-wake-word/parts/',
    './out/converted/random_TTS_mp3s/'
]

for source_directory, destination_directory in zip(source_directories, destination_directories):
    BasicAudioOperations.convert_mp3s_in_directory_to_wavs(source_directory, destination_directory)
    BasicAudioOperations.change_sample_rate_of_wavs_in_directory(source_directory, destination_directory)

