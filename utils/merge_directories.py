from basic_file_operations_class import BasicFileOperations
SOURCE_DIRECTORY = './out/random_longer_words/'
DESTINATION_DIRECTORY = './out/random/'

files = BasicFileOperations.get_files(SOURCE_DIRECTORY)
BasicFileOperations.copy_directory(files=files, source_directory=SOURCE_DIRECTORY, destination_directory=DESTINATION_DIRECTORY)