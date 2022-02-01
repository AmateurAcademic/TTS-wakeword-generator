from config import load_config

def load_engine_config(TTS_engine_config_file):
    TTS_engine_config = load_config(TTS_engine_config_file)
    larynx_host = TTS_engine_config['larynx_host']
    TTS_engines = TTS_engine_config['TTS_engines']
    def convert_engines_to_tuples(TTS_engines):
        TTS_engine_tuples = []
        for TTS_engine in TTS_engines:
            TTS_engine_plugin = TTS_engine['plugin']
            TTS_engine_voice = TTS_engine['voice']
            TTS_engine_output_type = TTS_engine['output_type']
            TTS_engine_tuples.append((TTS_engine_plugin, TTS_engine_voice, TTS_engine_output_type))
        return larynx_host, TTS_engine_tuples
    return convert_engines_to_tuples(TTS_engines)