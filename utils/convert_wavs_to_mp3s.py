from basic_file_operations_class import BasicFileOperations
from pydub import AudioSegment

def convert_wav_to_mp3(file, source_directory, destination_directory):
    if file.endswith('.wav'):
        try:
            sound = AudioSegment.from_file(source_directory+file)
            sound = sound.set_frame_rate(16000)
            sound = sound.set_channels(1)
            wav_file_name = file.replace('.wav', '.mp3')
            BasicFileOperations.make_directory(destination_directory)
            sound.export(destination_directory+wav_file_name, format="mp3")
        except:
            print(f"Error with {file}")


def convert_wavs_in_directory_to_mp3s(source_directory, destination_directory):
    '''converts all wav files in source_directory to mp3 files in destination_directory and copies any mp3 files in source_directory to destination_directory'''
    files = BasicFileOperations.get_files(source_directory)
    BasicFileOperations.make_directory(destination_directory)
    if all(file.endswith('.mp3') for file in files):
        print('All files are already in mp3 format')
    else:
        print(f'Converting {len(files)} wav files to mp3')
        for file in files:
            convert_wav_to_mp3(
                file, source_directory, destination_directory)
            if file.endswith('.mp3'):
                BasicFileOperations.copy_file(file, source_directory, destination_directory)
        print('Conversion complete')

convert_wavs_in_directory_to_mp3s('./out/converted/random/', './out/converted/random_mp3s/')
