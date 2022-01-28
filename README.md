# TTS Wakeword Generator
Use several TTS engines to produce a collection of wakeword (and not wakeword) samples.

## Why?
Collecting wakeword samples is a very common task in voice applications, but it is not always fun to do it manually. This tool helps you to generate a collection of samples for your wakeword. 

## NOTE
In a future release, this will be integrated into the [Precise Wakeword Model Maker](https://github.com/secretsauceai/precise-wakeword-model-maker).

## Installation
`pip install -r requirements.txt`

For picovoice you need to install:

`sudo apt-get install libttspico0`

`sudo apt-get install libttspico-utils`

## Usage
* Add your wakeword and the syllables of your wakeword to `config/TTS_config.json`
* Run `python tts_wakeword_generator.py`
* Unzip `data/random_TTS_mp3s.zip` and put the `random_TTS_mp3s` directory in `out/` directory
* Run `python utils/convert_all_TTS_files.py`
* The converted files are in `out/converted/`

# How does it work?
It's prety simple:
1. `wakeword`: every TTS voice says the wakeword (ie 'hey Jarvis')
2. `not-wakeword`: every TTS voice says the individual syllables of the wakeword (ie 'hey', 'jar', 'vis')
3. `not-wakeword`: Every TTS voice says all of the syllable pairs of the wakeword (ie 'hey jar', 'Jarvis')

### Hey, what's with the `random_TTS_mp3s.zip`?
The `config/google-10000-english.txt` file has been used to generate additional `not-wakeword` samples using `util/TTS_random_popular_words_generator.py`, cutting off any words with less than 4 characters.

It takes a long time to generate all of the samples, so you can use the pre-generated files in `data/random_TTS_mp3s.zip`.

These files are great for `not-wakeword` samples. So if you are incrementally training a wakeword model for the `not-wakeword` class, you can use these files as a starting point. 

WARNING 1: If you run `util/TTS_random_popular_words_generator.py` yourself, it could take a very long time to generate all of the samples.

WARNING 2: `config/google-10000-english.txt` is a list of the most popular words in English according to Google searches. This can include 'dirty and offensive words'. But do you really want your wakeword to wakeup when it hears something like a swear word?

#### Shout out to [JarbasAl](https://github.com/JarbasAl) and the whole [OpenVoiceOS](https://github.com/OpenVoiceOS/) crew!
