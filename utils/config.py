import json

# load config.json
def load_config(config_file):
    with open(config_file, 'r') as file:
        config = json.load(file)
    wakeword = config['wakeword']
    syllables = config['syllables']
    return wakeword, syllables
