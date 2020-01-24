from pathlib import Path
from deepspeech import Model
import numpy as np
import pyshark
# import speech_recognition as sr
import wave,os,sys



# rtp_list = []
# cap = pyshark.FileCapture('/Users/bwarner/PycharmProjects/socketstuff/sith.pcap', display_filter='rtp')
# raw_audio = open('my_audio.raw','wb')
# for i in cap:
#     try:
#         rtp = i[3]
#         if rtp.payload:
#              print(rtp.payload)
#              rtp_list.append(rtp.payload.split(":"))
#     except:
#         pass

# for rtp_packet in rtp_list:
#     packet = " ".join(rtp_packet)
#     print(packet)
#     audio = bytearray.fromhex(packet)
#     raw_audio.write(audio)

def speechRec(audio_data):
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

    with open('temp.wav','wb') as f:
        f.write(audio_data)

    ds = Model(model_name,beam_width)
    ds.enableDecoderWithLM(langauage_model, trie, lm_alpha, lm_beta)
    print(ds.sampleRate())

    # r = sr.Recognizer()
    # with sr.Microphone(sample_rate=sample_rate) as source:
    #     print("Say Something")
    #     audio = r.listen(source)
    #     fs = audio.sample_rate
    #     audio = np.frombuffer(audio.frame_data, np.int16)

    with wave.open('temp.wav', 'rb') as fin:
        fs = fin.getframerate()
        print("Framerate: ", fs)
        audio = np.frombuffer(fin.readframes(fin.getnframes()), np.int16)
        audio_length = fin.getnframes() * (1/sample_rate)

    print("Infering {} file".format('temp.wav'))

    return ds.stt(audio)