from pydub import AudioSegment
from speechbrain.inference.ASR import EncoderASR
import whisper

def asr_fon(model,path_audio_fon):
    if path_audio_fon.split('.')[-1]=="webm":
        audio = AudioSegment.from_file(path_audio_fon, format='webm')
        wav_path = path_audio_fon.replace('.webm', '.wav')
    else:
        wav_path=path_audio_fon
    audio.export(wav_path, format='wav')
    text=model.transcribe_file(wav_path)
    return (text,"fon")

def asr_multi(model,path_audio,lang="yo"):
    result = model.transcribe(path_audio)
    return (result['text'],lang)


# asr fon
#asr_model = EncoderASR.from_hparams(source="speechbrain/asr-wav2vec2-dvoice-fongbe", savedir="pretrained_models/asr-wav2vec2-dvoice-fongbe")
#print(asr_fon(asr_model,"output.wav"))



