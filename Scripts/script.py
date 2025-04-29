from Scripts.library import *


model = whisper.load_model('base')



def transcript(audio_caminho, pasta_destino):
    nome_txt = os.path.splitext(os.path.basename(audio_caminho))[0] + ".txt"
    destino_txt = os.path.join(pasta_destino, nome_txt)

    result = model.transcribe(audio_caminho, fp16=False)
    texto = result.get('text', '')

    with open(destino_txt, 'w', encoding='utf-8') as f:
        f.write(texto)
    return destino_txt