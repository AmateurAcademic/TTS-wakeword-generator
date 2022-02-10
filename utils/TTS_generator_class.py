from ovos_plugin_manager.tts import load_tts_plugin


from utils.basic_file_operations_class import BasicFileOperations
from utils.basic_audio_operations_class import BasicAudioOperations


import os.path
from os import makedirs
import time
import json


class TTSGenerator:
    def __init__(self):
        def load_config(config_file):
            with open(config_file, 'r') as file:
                config = json.load(file)
            return config
        def load_engine_config(TTS_engine_config_file):
            TTS_engine_config = load_config(TTS_engine_config_file)
            larynx_host = TTS_engine_config['larynx_host']
            TTS_engines = TTS_engine_config['TTS_engines']

            def convert_engines_to_tuples(TTS_engines):
                TTS_engine_tuples = []
                for TTS_engine in TTS_engines:
                    TTS_engine_plugin = TTS_engine['plugin']
                    TTS_engine_voice = TTS_engine['voice']
                    TTS_engine_output_type = TTS_engine['output_type']
                    TTS_engine_tuples.append(
                        (TTS_engine_plugin, TTS_engine_output_type, TTS_engine_voice))
                return larynx_host, TTS_engine_tuples

            return convert_engines_to_tuples(TTS_engines)

        engine_config = load_engine_config(
            os.getcwd() + '/config/TTS_engine_config.json')
        self.larynx_host = engine_config[0]
        self.TTS_list = engine_config[1]

        self.WAKEWORD_PATH = None
        self.NOT_WAKEWORD_PATH = None
        self.TTS_utterances = None

    def load_wakeword_config(self, wakeword_model_name):
        def load_config(config_file):
            with open(config_file, 'r') as file:
                config = json.load(file)
            return config
        
        wakeword_config = load_config(
            os.getcwd() + '/config/TTS_wakeword_config.json')
        WAKEWORD = wakeword_config['wakeword']
        SYLLABLES = wakeword_config['syllables']
        self.WAKEWORD_PATH = f'./out/{wakeword_model_name}/wake-word/TTS/'
        self.NOT_WAKEWORD_PATH = f'./out/{wakeword_model_name}/not-wake-word/TTS/parts/'
        
        def permutate_syllables(SYLLABLES, WAKEWORD):
            permutated_syllables = []
            number_of_syllables = len(SYLLABLES)

            for syllable in SYLLABLES:
                syllable_index = SYLLABLES.index(syllable)
                next_syllable_index = syllable_index + 2
                if next_syllable_index <= number_of_syllables:
                    #NOTE: if syllable and next syllable in wakeword are seperated by a space in wakeword, then the permutated syllables are seperated by a space
                    permutated_syllable = ''.join(
                        SYLLABLES[syllable_index:next_syllable_index])
                    if permutated_syllable not in WAKEWORD:
                        permutated_syllable = ' '.join(
                            SYLLABLES[syllable_index:next_syllable_index])
                    permutated_syllables.append(permutated_syllable)
            return permutated_syllables

        permutated_syllables = permutate_syllables(SYLLABLES, WAKEWORD)
        all_syllables = SYLLABLES + permutated_syllables
        self.TTS_utterances = [WAKEWORD] + all_syllables

        return self.TTS_utterances, self.WAKEWORD_PATH, self.NOT_WAKEWORD_PATH


    @staticmethod
    def load_word_corpus(
        file_path, min_word_length_limit=None):
        with open(file_path, 'r') as f:
                word_corpus = f.read().splitlines()

        def filter_word_corpus(
            word_corpus, min_word_length_limit):
            filtered_word_corpus = []
            for utterance in word_corpus:
                if len(utterance) >= min_word_length_limit:
                    filtered_word_corpus.append(utterance)
            return filtered_word_corpus

        if min_word_length_limit is not None:
            word_corpus = filter_word_corpus(word_corpus, min_word_length_limit)
        
        return word_corpus

    def load_TTS_engine(self, plugin, output_type, voice=None):
        TTS_engine = load_tts_plugin(
        plugin)

        config_others = {
            "voice": voice,
        }
        

        if self.larynx_host is None:
                config_larynx = {
                    "voice": voice,
                    "vocoder": "hifi_gan/universal_large",
                }
        else:
            config_larynx = {
                "host": self.larynx_host,
                "voice": voice,
                "vocoder": "hifi_gan/universal_large",
            }

        if "larynx" in plugin:
            tts = TTS_engine(lang="en-us", config=config_larynx)
        else:
            tts = TTS_engine(lang="en-us", config=config_others)

        if tts.voice:
            voice = voice or tts.voice.replace("/", "")
        if voice:
            slug = f"{plugin}_{voice}.{output_type}"
        else:
            slug = f"{plugin}.{output_type}"

        return tts, slug

    def make_wakeword_collection_path(
        self, utterance, slug):
        wakeword = self.TTS_utterances[0]
        all_syllables = self.TTS_utterances[1:]
        if utterance is wakeword:
            file_name = wakeword.replace(' ', '_') + '-' + slug
            file_path = self.WAKEWORD_PATH + file_name
        else:
            file_name = str(all_syllables.index(utterance)) + '_' + utterance.replace(' ', '_') + '-' + slug
            file_path = self.NOT_WAKEWORD_PATH + file_name
        return file_path


    def make_corpus_collection_path(self, utterance, slug):
        file_name =  utterance.replace(' ', '_') + '-' + slug
        RANDOM_COLLECTED_UTTERANCES_PATH = './out/random-tmp/'
        makedirs(RANDOM_COLLECTED_UTTERANCES_PATH, exist_ok=True)
        
        return RANDOM_COLLECTED_UTTERANCES_PATH + file_name

    
    def get_TTS_audio(
        self, utterance, file_path, tts, slug):
        '''Uses the loaded TTS engine to get the audio of the utterance. Sometimes the TTS engine times out, so it will try again... This usually works unless there is something wrong with the TTS engine/server'''
        if not os.path.isfile(file_path):
            try:
                tts.get_tts(utterance, file_path)
                tts.playback.stop()
            except:
                print(
                    f'utterance {utterance} failed to be TTSed with {slug} \n Waiting for half a minute then trying again')
                time.sleep(30)
                try:
                    tts.get_tts(utterance, file_path)
                    tts.playback.stop()
                except:
                    print(
                        f'{utterance} STILL failed to be TTSed with {slug} \n Check your settings and run the script again')
                    pass
        elif os.path.isfile(file_path):
            print(f"{file_path} already exists")


    def scrape_tts_engines(
        self, utterances, wakeword_scraping):
        '''Scrapes the TTS engines from the TTS_engine_config.json file for all utterances'''
        for plugin, output_type, voice in self.TTS_list:
            tts, slug = self.load_TTS_engine(plugin, output_type, voice)
            if not tts:
                continue
            for utterance in utterances:
                if wakeword_scraping:
                    file_path = self.make_wakeword_collection_path(utterance, slug)
                else:
                    file_path = self.make_corpus_collection_path(utterance, slug)
                self.get_TTS_audio(utterance, file_path, tts, slug)
                print(f'Scraped TTS {slug} for utterance {utterance}')


    #TODO: add a function to convert all mp3s to wavs and all wavs into correct sample rate

    def convert_audio_files(
        self, source_directory, destination_directory):
        '''Converts all audio files in the source directory to the destination directory'''
        BasicAudioOperations.convert_mp3s_in_directory_to_wavs(
            source_directory, destination_directory)
        BasicAudioOperations.change_sample_rate_of_wavs_in_directory(
            source_directory, destination_directory)
