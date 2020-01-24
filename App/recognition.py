from pathlib import Path
from deepspeech import Model
import numpy as np
# import speech_recognition as sr
import wave,os,sys

def speechRec(audio_data):

    # r = sr.Recognizer()
    # with sr.Microphone(sample_rate=sample_rate) as source:
    #     print("Say Something")
    #     audio = r.listen(source)
    #     fs = audio.sample_rate
    #     audio = np.frombuffer(audio.frame_data, np.int16)

    sample_rate = 16000
    beam_width = 500
    lm_alpha = 0.75
    lm_beta = 1.85
    n_features = 29
    n_context = 9

    data_folder = Path('deepspeech-0.6.1-models')
    model_name = str(data_folder / "output_graph.pbmm")
    alphabet = str(data_folder / "alphabet.txt")
    langauage_model = str(data_folder / "lm.binary")
    trie = str(data_folder / "trie")
    audio_file = 'temp.wav'

    with open(audio_file,'wb') as f:
        f.write(audio_data)

    ds = Model(model_name,beam_width)
    ds.enableDecoderWithLM(langauage_model, trie, lm_alpha, lm_beta)
    # print(ds.sampleRate())

    with wave.open(audio_file, 'rb') as fin:
        fs = fin.getframerate()
        print("Framerate: ", fs)
        audio = np.frombuffer(fin.readframes(fin.getnframes()), np.int16)
        audio_length = fin.getnframes() * (1/sample_rate)

    if os.path.exists(audio_file):
        os.remove(audio_file)
    else:
        sys.exit("The file {} does not exist".format(audio_file))
    # print("Infering {} file".format(audio_file))

    return ds.stt(audio)