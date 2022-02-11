from utils.TTS_generator_class import TTSGenerator


TTS_generator_instance = TTSGenerator()

source_directory = './out/random_TTS_mp3s/'
destination_directory = './out/converted/random_TTS_mp3s/'

TTS_generator_instance.convert_audio_files(
    source_directory, destination_directory)