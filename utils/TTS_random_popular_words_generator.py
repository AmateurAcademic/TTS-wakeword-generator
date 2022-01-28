from ovos_plugin_manager.tts import load_tts_plugin
from os import makedirs

def load_popular_word_corpus(file_path):
    with open(file_path, 'r') as f:
        popular_words = f.read().splitlines()
    return popular_words

RANDOM_COLLECTED_UTTERANCES_PATH = './out/random_longer_words/'
POPULAR_WORDS = load_popular_word_corpus('./config/google-10000-english.txt')


longer_popular_words = []
for utterance in POPULAR_WORDS:
    if len(utterance) > 3:
        longer_popular_words.append(utterance)
        

makedirs(RANDOM_COLLECTED_UTTERANCES_PATH, exist_ok=True)

for plug, voice, ext in [
    #("ovos-tts-plugin-mimic", None, "wav"),
    #mimic and google commented out because they are done (well google blocked the API requests any further)
    #("ovos-tts-plugin-mimic2", None, "wav"),
    #("ovos-tts-plugin-google-tx", None, "wav"),
   # ("ovos-tts-plugin-pico", None, "wav"),
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
    ("ovos-tts-plugin-responsivevoice", 'EnglishIndia', "mp3")
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
    ]:
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

    for utterance in longer_popular_words:
        tts.get_tts(utterance, RANDOM_COLLECTED_UTTERANCES_PATH + utterance + '_' + slug)
        tts.playback.stop()