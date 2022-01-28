from ovos_plugin_manager.tts import load_tts_plugin
from os import makedirs
from utils.config import load_config

wakeword, syllables = load_config('config/TTS_config.json')
WAKEWORD_DIR = wakeword.replace(' ', '_')
WAKEWORD_PATH = f'./out/{WAKEWORD_DIR}/TTS/wake-word/'
NOT_WAKEWORD_PATH = f'./out/{WAKEWORD_DIR}/TTS/not-wake-word/parts/'


def permutate_syllables(syllables, wakeword):
    permutated_syllables = []
    number_of_syllables = len(syllables)

    for syllable in syllables:
        syllable_index = syllables.index(syllable)
        next_syllable_index = syllable_index + 2
        if next_syllable_index <= number_of_syllables:
            #NOTE: if syllable and next syllable in wakeword are seperated by a space in wakeword, then the permutated syllables are seperated by a space
            permutated_syllable = ''.join(syllables[syllable_index:next_syllable_index])
            if permutated_syllable not in wakeword:
                permutated_syllable = ' '.join(syllables[syllable_index:next_syllable_index])
            permutated_syllables.append(permutated_syllable)
    return permutated_syllables

permutated_syllables = permutate_syllables(syllables, wakeword)
all_syllables = syllables + permutated_syllables
TTS_utterances = [wakeword] + all_syllables


makedirs(WAKEWORD_PATH, exist_ok=True)
makedirs(NOT_WAKEWORD_PATH, exist_ok=True)

print(TTS_utterances)

#NOTE: A lot of TTS engines are commented out because I can't get them to work for now.
#TODO: Get all TTS engines to work
#TODO: Turn this big block of code into a few functions

TTS_list = [
    #("ovos-tts-plugin-mimic", None, "wav"),
    ("ovos-tts-plugin-mimic2", None, "wav"),
    ("ovos-tts-plugin-google-tx", None, "wav"),
    ("ovos-tts-plugin-pico", None, "wav"),
    #NOTE: Alice and Laura sound like the speak another langauge!
    #("ovos-tts-plugin-responsivevoice", 'Alice', "mp3"),
    ("ovos-tts-plugin-responsivevoice", 'AustralianFemale', "mp3"),
    ("ovos-tts-plugin-responsivevoice", 'AustralianMale', "mp3"),
    ("ovos-tts-plugin-responsivevoice", 'Karen', "mp3"),
    ("ovos-tts-plugin-responsivevoice", 'Martin', "mp3"),
    #("ovos-tts-plugin-responsivevoice", 'Laura', "mp3"),
    ("ovos-tts-plugin-responsivevoice", 'UKEnglishFemale', "mp3"),
    ("ovos-tts-plugin-responsivevoice", 'UKEnglishMale', "mp3"),
    ("ovos-tts-plugin-responsivevoice", 'USEnglishFemale', "mp3"),
    ("ovos-tts-plugin-responsivevoice", 'USEnglishMale', "mp3"),
    ("ovos-tts-plugin-responsivevoice", 'EnglishUnitedKingdom', "mp3"),
    ("ovos-tts-plugin-responsivevoice", 'EnglishIndia', "mp3"),
    # ("neon-tts-plugin-larynx-server", "mary_ann", "wav"),
    # ("neon-tts-plugin-larynx-server", "southern_english_female", "wav"),
    # ("neon-tts-plugin-larynx-server", "southern_english_male", "wav"),
    # ("neon-tts-plugin-larynx-server", "scottish_english_male", "wav"),
    # ("neon-tts-plugin-larynx-server", "northern_english_male", "wav"),
    # ("neon-tts-plugin-larynx-server", "judy_bieber", "wav"),
    # ("neon-tts-plugin-larynx-server", "harvard", "wav"),
    # ("neon-tts-plugin-larynx-server", "blizzard_fls", "wav"),
    # ("neon-tts-plugin-larynx-server", "blizzard_lessac", "wav"),
    # ("neon-tts-plugin-larynx-server", "ljspeech", "wav"),
    # ("neon-tts-plugin-larynx-server", "cmu_aew", "wav"),
    # ("neon-tts-plugin-larynx-server", "cmu_ahw", "wav"),
    # ("neon-tts-plugin-larynx-server", "cmu_aup", "wav"),
    # ("neon-tts-plugin-larynx-server", "cmu_bdl", "wav"),
    # ("neon-tts-plugin-larynx-server", "cmu_clb", "wav"),
    # ("neon-tts-plugin-larynx-server", "cmu_eey", "wav"),
    # ("neon-tts-plugin-larynx-server", "cmu_fem", "wav"),
    # ("neon-tts-plugin-larynx-server", "cmu_jmk", "wav"),
    # ("neon-tts-plugin-larynx-server", "cmu_ksp", "wav"),
    # ("neon-tts-plugin-larynx-server", "cmu_ljm", "wav"),
    # ("neon-tts-plugin-larynx-server", "cmu_lnh", "wav"),
    # ("neon-tts-plugin-larynx-server", "cmu_rms", "wav"),
    # ("neon-tts-plugin-larynx-server", "cmu_rxr", "wav"),
    # ("neon-tts-plugin-larynx-server", "cmu_slp", "wav"),
    # ("neon-tts-plugin-larynx-server", "cmu_slt", "wav"),
    # ("neon-tts-plugin-larynx-server", "ek", "wav"),
    # ("neon-tts-plugin-larynx-server", "kathleen", "wav")
]

for plug, voice, ext in TTS_list:
    #NOTE: Loads TTS engine, returns the slug with plugin name, voice name, and extension
    engine = load_tts_plugin(plug)
    if not engine:
        continue

    tts = engine(lang="en-us", config={"voice": voice})
    if tts.voice:
        voice = voice or tts.voice.replace("/", "")
    if voice:
        slug = f"{plug}_{voice}.{ext}"
    else:
        slug = f"{plug}.{ext}"

    #NOTE: Creates path to save TTS files, runs TTS on each utterance, and saves to path
    for utterance in TTS_utterances:
        if utterance is wakeword:
            file_name = wakeword + '_' + slug
            directory = WAKEWORD_PATH
            path = directory + file_name  
        else:
            #NOTE: labeling the files with count is important for the splitting process
            file_name = str(all_syllables.index(utterance))  + '_' + utterance + '_' + slug
            directory = NOT_WAKEWORD_PATH
            path = directory + file_name
        tts.get_tts(utterance, path)
        tts.playback.stop()
        