from os import makedirs

from utils.TTS_generator_class import TTSGenerator

TTS_generator_instance = TTSGenerator()

TTS_utterances, WAKEWORD_PATH, NOT_WAKEWORD_PATH = TTS_generator_instance.load_wakeword_config(
    wakeword_model_name="model_name")

makedirs(WAKEWORD_PATH, exist_ok=True)
makedirs(NOT_WAKEWORD_PATH, exist_ok=True)

TTS_generator_instance.scrape_tts_engines(
    utterances=TTS_utterances, wakeword_scraping=True)

source_directories = [
    WAKEWORD_PATH,
    NOT_WAKEWORD_PATH,
]

wakeword_destination = WAKEWORD_PATH.replace('./out/', '')
not_wakeword_destination = NOT_WAKEWORD_PATH.replace('./out/', '')

destination_directories = [
    f'./out/converted/{wakeword_destination}',
    f'./out/converted/{not_wakeword_destination}',
]

for source_directory, destination_directory in zip(source_directories, destination_directories):
    TTS_generator_instance.convert_audio_files(
        source_directory, destination_directory)
