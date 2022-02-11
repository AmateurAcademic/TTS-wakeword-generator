from utils.TTS_generator_class import TTSGenerator

import os
from os import makedirs

TTS_generator_instance = TTSGenerator()

#print(TTS_generator_instance.TTS_list)

#TTS_utterances, WAKEWORD_PATH, NOT_WAKEWORD_PATH = TTS_generator_instance.load_wakeword_config(
#    wakeword_model_name="test_model_name")


#makedirs(WAKEWORD_PATH, exist_ok=True)
#makedirs(NOT_WAKEWORD_PATH, exist_ok=True)

'''print(TTS_generator_instance.TTS_list[0])

plugin, output_type, voice = TTS_generator_instance.TTS_list[0]

tts, slug = TTS_generator_instance.load_TTS_engine(
    plugin, output_type, voice)'''

#TODO: add check for utterance path: if wakeword scraping else corpus scraping

#utterance = TTS_utterances[5]
#print(TTS_generator_instance.make_wakeword_collection_path(
#    utterance=utterance, slug=slug, wakeword_path=WAKEWORD_PATH, not_wakeword_path=NOT_WAKEWORD_PATH, TTS_utterances=TTS_utterances))


"""file_path = os.getcwd() + '/config/google-10000-english.txt'

word_corpus = TTS_generator_instance.load_word_corpus(
    file_path, min_word_length_limit=4)

utterance = word_corpus[5]

file_path = TTS_generator_instance.make_corpus_collection_path(
    utterance, slug)


    

TTS_generator_instance.get_TTS_audio(utterance, file_path, tts, slug)
"""

# 1. scrape tts engines for wakeword collections
'''TTS_utterances, WAKEWORD_PATH, NOT_WAKEWORD_PATH = TTS_generator_instance.load_wakeword_config(
    wakeword_model_name="test_model_name")


makedirs(WAKEWORD_PATH, exist_ok=True)
makedirs(NOT_WAKEWORD_PATH, exist_ok=True)

TTS_generator_instance.scrape_tts_engines(utterances=TTS_utterances, wakeword_scraping=True)
'''
# 2. scrape tts engines for corpus collections
corpus_file_path = os.getcwd() + '/config/test.txt'

word_corpus = TTS_generator_instance.load_word_corpus(
    file_path=corpus_file_path, min_word_length_limit=4)

TTS_generator_instance.scrape_tts_engines(utterances=word_corpus, wakeword_scraping=False)

RANDOM_COLLECTED_UTTERANCES_PATH = './out/random-tmp/'

CONVERTED_PATH = './out/converted/random-tmp/'


TTS_generator_instance.convert_audio_files(source_directory=RANDOM_COLLECTED_UTTERANCES_PATH, destination_directory=CONVERTED_PATH)