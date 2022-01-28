import os
from os import listdir
from os.path import isfile, join
import shutil
from pydub import AudioSegment
from scipy.io import wavfile


class BasicFileOperations:
    @staticmethod
    def get_files(source_directory):
        return [f for f in listdir(source_directory) if isfile(join(source_directory, f))]

    @staticmethod
    def get_number_of_files(source_directory):
        return len(BasicFileOperations.get_files(source_directory))
    
    @staticmethod
    def get_limited_number_of_files(source_directory, max_number_of_files):
        max_number_of_files -= 1
        files = [f for f in listdir(source_directory)[:max_number_of_files] if isfile(join(source_directory, f))]
        return files

    @staticmethod
    def copy_file(file, source_directory, destination_directory):
        try:
            shutil.copyfile(source_directory+file, destination_directory+file)
        except:
            print(f"Error with {file}")

    @staticmethod
    def rename_file(old_filename, new_filename, directory=''):
        try:
            os.rename(directory + old_filename, directory + new_filename)
        except:
            print(f"Error with {old_filename}")

    @staticmethod
    def backup_file(source_file, destination_file, source_directory=None):
        '''This will rename a file in a directory
        It will also copy the file to the destination directory'''
        try:
            if source_directory:
                shutil.copyfile(source_directory + source_file, source_directory + destination_file)
            else:
                shutil.copyfile(source_file, destination_file)
        except:
            print(f"Error with {source_file}")
    
    @staticmethod
    def make_directory(directory):
        if not os.path.exists(directory):
            os.makedirs(directory)

    @staticmethod
    def copy_directory(files, source_directory, destination_directory):
        BasicFileOperations.make_directory(destination_directory)
        for file in files:
            try:
                shutil.copyfile(source_directory + file, destination_directory + file)
            except:
                ...
    
    @staticmethod
    def delete_directory(directory):
        if os.path.exists(directory):
            print(f'Deleting {directory}')
            shutil.rmtree(directory)
        else:
            print(f'Directory {directory} does not exist')

    @staticmethod
    def delete_file(file):
        if os.path.exists(file):
            print(f'Removing {file}')
            os.remove(file)
        else:
            print(f'File {file} does not exist')

    @staticmethod
    def delete_files_in_directory(files, directory):
        for file in files:
            BasicFileOperations.delete_file(directory + file)

    @staticmethod
    def rename_directory(source_directory, destination_directory):
        if os.path.exists(destination_directory):
            print(f'Directory {destination_directory} already exists')
        else:
            if os.path.exists(source_directory):
                os.rename(source_directory, destination_directory)
                print(f'Directory {source_directory} renamed to {destination_directory}')
            else:
                print(f'Directory {source_directory} does not exist')

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
    def convert_mp3_to_wav(file, source_directory, destination_directory):
        if file.endswith('.mp3'):
            try:
                sound = AudioSegment.from_file(source_directory+file)
                sound = sound.set_frame_rate(16000)
                sound = sound.set_channels(1)
                wav_file_name = file.replace('.mp3', '.wav')
                BasicFileOperations.make_directory(destination_directory)
                sound.export(destination_directory+wav_file_name, format="wav")
            except:
                print(f"Error with {file}")

    @staticmethod
    def convert_mp3s_in_directory_to_wavs(source_directory, destination_directory):
        files = BasicFileOperations.get_files(source_directory)
        BasicFileOperations.make_directory(destination_directory)
        if all(file.endswith('.wav') for file in files):
            print('All files are already in wav format')
        else:
            print(f'Converting {len(files)} mp3 files to wav')
            for file in files:
                BasicFileOperations.convert_mp3_to_wav(file, source_directory, destination_directory)
            print('Conversion complete')

    @staticmethod
    def change_sample_rate_of_wav_file(file, source_directory, destination_directory):
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
                else:
                    return False
            except:
                print(f"Error with {file}")
                return False

    @staticmethod
    def change_sample_rate_of_wavs_in_directory(source_directory, destination_directory):
        print('This will also copy all files already in 16000 sample rate into the destination directory')
        files = BasicFileOperations.get_files(source_directory)
        BasicFileOperations.make_directory(destination_directory)
        for file in files: 
            if file.endswith('.wav'):
                converted = BasicFileOperations.change_sample_rate_of_wav_file(file, source_directory, destination_directory)
                if not converted:
                    BasicFileOperations.copy_file(file, source_directory, destination_directory)

    @staticmethod
    def split_files_into_multiple_directories(files, number_of_files_per_directory, source_directory, destination_directory):
        '''This will take a directorey with a huge amount of files and break them down into smaller directories
        It can have a max number of files (might have to refactor get_files for getting only a max number)'''
        directory_number = 1
        file_count = 1
        for file in files:
            if file_count < number_of_files_per_directory:
                BasicFileOperations.copy_file(file, source_directory, destination_directory + '_0' + str(directory_number))
                file_count += 1
            elif file_count == number_of_files_per_directory:
                BasicFileOperations.copy_file(file, source_directory, destination_directory + '_0' + str(directory_number))
                directory_number += 1
                file_count = 1