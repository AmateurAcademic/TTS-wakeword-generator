# Google most popular search words TTS data set
34,082 audio files of the most popular words in US English.

## TTS Voices
The following plugins were used to get the TTS audio captured in the data set:
* [OVOS Mimic2](https://github.com/OpenVoiceOS/ovos-tts-plugin-mimic2)
* [OVOS ResponsiveVoice](https://github.com/OpenVoiceOS/ovos-tts-plugin-responsivevoice)
  * AustralianMale
  * AustralianFemale
  * Karen
* [gTTS](https://github.com/OpenVoiceOS/ovos-tts-plugin-google-tx)

## Data set
The data set was collected using the [google-10000-english.txt](https://github.com/first20hours/google-10000-english/blob/master/google-10000-english.txt) data set.
This data set was filtered by word length, so only words with 4 letters or more were used.
