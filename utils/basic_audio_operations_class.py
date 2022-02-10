from pydub import AudioSegment
from scipy.io import wavfile
from utils.basic_file_operations_class import BasicFileOperations


class BasicAudioOperations:

    @staticmethod
    def read_wave_file(file):
        if file.endswith('.wav'):
            try:
                sample_frequency, wave_data = wavfile.read(file)
                return sample_frequency, wave_data
            except:
                print(f"Error with {file}")

    @staticmethod
    def write_wave_file(file, sample_frequency, data):
        wavfile.write(file, sample_frequency, data)

    @staticmethod
    def convert_mp3_to_wav(
        file, source_directory, destination_directory):
        if file.endswith('.mp3'):
            try:
                sound = AudioSegment.from_file(source_directory+file)
                sound = sound.set_frame_rate(16000)
                sound = sound.set_channels(1)
                wav_file_name = file.replace('.mp3', '.wav')
                BasicFileOperations.make_directory(
                    destination_directory)
                sound.export(
                    destination_directory+wav_file_name, format="wav")
            except:
                print(f"Error with {file}")

    @staticmethod
    def convert_mp3s_in_directory_to_wavs(
        source_directory, destination_directory):
        files = BasicFileOperations.get_files(source_directory)
        BasicFileOperations.make_directory(destination_directory)
        if all(file.endswith('.wav') for file in files):
            print('All files are already in wav format')
        else:
            print(f'Converting {len(files)} mp3 files to wav')
            for file in files:
                BasicAudioOperations.convert_mp3_to_wav(
                    file, source_directory, destination_directory)
            print('Conversion complete')

    @staticmethod
    def change_sample_rate_of_wav_file(
        file, source_directory, destination_directory):
        '''This will take a wav file and change the sample rate to 16000 (required for precise)'''
        #TODO: I think I might have messed something up here (maybe I fixed it?), retest this!
        if file.endswith('.wav'):
            try:
                sound = AudioSegment.from_file(source_directory+file)
                if sound.frame_rate != 16000:
                    sound = sound.set_frame_rate(16000)
                    sound = sound.set_channels(1)
                    sound.export(destination_directory+file, format="wav")
                    return True
                elif sound.frame_rate == 16000:
                    return False
            except:
                print(f"Error with {file}")
                pass


    @staticmethod
    def change_sample_rate_of_wavs_in_directory(
        source_directory, destination_directory):
        print('This will also copy all files already in 16000 sample rate into the destination directory')
        files = BasicFileOperations.get_files(source_directory)
        BasicFileOperations.make_directory(destination_directory)
        for file in files: 
            if file.endswith('.wav'):
                converted = BasicAudioOperations.change_sample_rate_of_wav_file(
                    file, source_directory, destination_directory)
                if converted is False:
                    BasicFileOperations.copy_file(
                        file, source_directory, destination_directory)
