import os

from utils.TTS_generator_class import TTSGenerator

TTS_generator_instance = TTSGenerator()

corpus_file_path = os.getcwd() + '/config/google-10000-english.txt'

word_corpus = TTS_generator_instance.load_word_corpus(
    file_path=corpus_file_path, min_word_length_limit=4)

TTS_generator_instance.scrape_tts_engines(
    utterances=word_corpus, wakeword_scraping=False)

RANDOM_COLLECTED_UTTERANCES_PATH = './out/random/'

CONVERTED_PATH = './out/converted/random/'


TTS_generator_instance.convert_audio_files(
    source_directory=RANDOM_COLLECTED_UTTERANCES_PATH, destination_directory=CONVERTED_PATH)
