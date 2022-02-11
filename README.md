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

For Larynx, you may want to [setup your own server](https://github.com/rhasspy/larynx) and configure the `larynx_host` in `config/TTS_engine_config.json` to the server's IP address and port number (ie https://127.0.0.1:5002). You can also leave it as `null` and it will use the default server (Neon).

## Usage
* Add your wakeword and the syllables of your wakeword to `config/TTS_wakeword_config.json`
* Edit the `config/TTS_engine_config.json` for the TTS engines and voices you would like to use
* Run `python TTS_wakeword_generator.py` (you can edit the name of the sub directory it creates in `out/` in this file with `wakeword_model_name`
* (OPTIONAL) Run `python TTS_words_generator.py` if you want to scrape a bunch of random popular words (for EN-US this is already in the `data/` directory so you don't have to) WARNING: This can take a very long time to complete and should only be performed if you require another language, I wouldn't recommend doing it for more than 3 or 4 voices as it takes so long!
* If you want to use the default random TTS data instead of generating your own: Unzip `random_TTS_mp3s.zip` to the `out/` directory and run `python convert_prescraped_data.py` (NOTE: I will automate this step with this [git issue](https://github.com/AmateurAcademic/TTS-wakeword-generator/issues/5))
* All of the converted files are in `out/converted/`

# How does it work?
It's prety simple:
1. `wakeword`: every TTS voice says the wakeword (ie 'hey Jarvis')
2. `not-wakeword`: every TTS voice says the individual syllables of the wakeword (ie 'hey', 'jar', 'vis')
3. `not-wakeword`: every TTS voice says all of the syllable pairs of the wakeword (ie 'hey jar', 'Jarvis')

### Hey, what's with the `random_TTS_mp3s.zip`?
The `config/google-10000-english.txt` file has been used to generate additional `not-wakeword` samples using `TTS_words_generator.py`, cutting off any words with less than 4 characters.

It takes a long time to generate all of the samples, so you can use the pre-generated files in `data/random_TTS_mp3s.zip`.

These files are great for `not-wakeword` samples. So if you are incrementally training a wakeword model for the `not-wakeword` class, you can use these files as a starting point to test for false wake ups and add the audio that fails into your data set. :)

WARNING: `config/google-10000-english.txt` is a list of the most popular words in English according to Google searches. This can include 'dirty and offensive words'. But do you really want your wakeword to wakeup when it hears something like a swear word?

#### Shout out to [JarbasAl](https://github.com/JarbasAl) and the whole [OpenVoiceOS](https://github.com/OpenVoiceOS/) crew!
