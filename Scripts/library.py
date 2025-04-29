import os
import shutil
import ctypes
import tkinter as tk
from tkinter import StringVar, Label, Button, filedialog, messagebox
import whisper
from elevenlabs.client import ElevenLabs



model = whisper.load_model('base')



def transcript(audio_caminho, pasta_destino):
    nome_txt = os.path.splitext(os.path.basename(audio_caminho))[0] + ".txt"
    destino_txt = os.path.join(pasta_destino, nome_txt)

    result = model.transcribe(audio_caminho, fp16=False)
    texto = result.get('text', '')

    with open(destino_txt, 'w', encoding='utf-8') as f:
        f.write(texto)
    return destino_txt



def clone_voice(audio_path, api_key):
    try:
        client = ElevenLabs(api_key=api_key)
        
        voice = client.clone(
            name="cloned_voice",
            description="Cloned from uploaded audio",
            files=[audio_path],
        )
        print("Voz clonada com sucesso:", voice)
        return True
    except Exception as e:
        print("Erro ao clonar voz:", e)
        return False