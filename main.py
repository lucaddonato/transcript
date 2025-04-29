'''
transcript - versão 1.0
pip install -U openai-whisper elevenlabs
'''


from Scripts.library import *



def janela():
    root = tk.Tk()
    root.title("transcript")
    root.geometry("550x250")
    ctypes.windll.shcore.SetProcessDpiAwareness(2) # Alta resolução


    desktop = os.path.join(os.path.expanduser("~"), "Desktop")
    os.makedirs(desktop, exist_ok=True)


    vars = {
        'audio': tk.StringVar(),
        'pasta': tk.StringVar(value=desktop),
        'ffmpeg': tk.StringVar(),
        'api': tk.StringVar(),
        'modo': tk.StringVar(value='transcrever')
    }



    def selecionar(campo, dir_seletor=False, tipos=None, label=None):
        if dir_seletor:
            caminho = filedialog.askdirectory(title="Selecione a pasta")
        else:
            caminho = filedialog.askopenfilename(title=campo.title(), filetypes=tipos)
        if caminho:
            vars[campo].set(caminho)
            texto = caminho if dir_seletor else os.path.basename(caminho)
            label.config(text=texto)
            if campo == 'ffmpeg':
                path = os.path.dirname(caminho)
                os.environ['PATH'] = path + os.pathsep + os.environ.get('PATH', '')


    tk.Label(root, text='transcript', font=('Calibri', 20, 'bold')).pack(pady=5)


    frame_modo = tk.Frame(root)
    frame_modo.pack(fill='x')
    tk.Label(frame_modo).pack(side='left')

    for texto, valor in [('Transcrever', 'transcrever'), ('Clonar', 'clonar')]:
        tk.Radiobutton(frame_modo, text=texto, variable=vars['modo'], value=valor).pack(side='left', padx=5)


    seletores = [
        {'campo': 'audio', 'texto': 'Upload audio', 'tipos': [("Audio files", "*.mp3 *.wav *.flac *.m4a *.ogg")], 'dir': False},
        {'campo': 'pasta', 'texto': 'Local', 'tipos': None, 'dir': True},
        {'campo': 'ffmpeg', 'texto': 'ffmpeg', 'tipos': [("FFmpeg exe", "ffmpeg.exe")], 'dir': False}
    ]


    labels = {}

    for sel in seletores:
        frame = tk.Frame(root)
        frame.pack(fill='x', padx=10, pady=5)
        lbl = tk.Label(frame, text=vars[sel['campo']].get() if sel['campo']=='pasta' else 'Nenhum {} selecionado.'.format(sel['campo']))
        btn = tk.Button(frame, text=sel['texto'], command=lambda s=sel, l=lbl: selecionar(s['campo'], s['dir'], s['tipos'], l))
        btn.pack(side='left', padx=(0,5))
        lbl.pack(side='left')
        labels[sel['campo']] = lbl


    api_frame = tk.Frame(root)
    tk.Label(api_frame, text='API Key:').pack(side='left')
    tk.Entry(api_frame, textvariable=vars['api'], width=40).pack(side='left', padx=(0,5))
    btn_verificar = tk.Button(api_frame, text='Verificar', command=lambda: verificar())
    btn_verificar.pack(side='left')
    status_clone = tk.Label(api_frame, text='')
    status_clone.pack(side='left', padx=(10,0))

    txt_frame = tk.Frame(root)
    btn_txt = tk.Button(txt_frame, text='Texto de clonagem', command=lambda: selecionar('audio', False, [("Text files", "*.txt")], status_clone))
    btn_txt.pack(side='left')


    btn_confirmar = tk.Button(root, text='Transcrever', command=lambda: transcrever())
    btn_confirmar.pack(pady=20)



    def transcrever():
        if not vars['audio'].get():
            messagebox.showwarning('Aviso', 'Nenhum arquivo selecionado')
            return
        if shutil.which('ffmpeg') is None:
            messagebox.showerror('Erro', "ffmpeg não encontrado. Se instalado, use o botão 'Selecionar ffmpeg'.")
            return
        try:
            destino = transcript(vars['audio'].get(), vars['pasta'].get())
            messagebox.showinfo('Concluído', f'{destino}')
        except Exception as e:
            messagebox.showerror('Erro', f'{e}')



    def verificar():
        if not vars['audio'].get():
            messagebox.showwarning('Aviso', 'Nenhum áudio selecionado.')
            return
        sucesso = clone_voice(vars['audio'].get(), vars['api'].get())
        status_clone.config(text='Áudio clonado com sucesso' if sucesso else 'Erro ao clonar voz', fg='green' if sucesso else 'red')



    def atualiza_modo(*_):
        modo = vars['modo'].get()
        if modo == 'transcrever':
            btn_confirmar.pack(pady=20)
            api_frame.pack_forget(); txt_frame.pack_forget()
        else:
            btn_confirmar.pack_forget()
            api_frame.pack(fill='x', padx=10, pady=5)
            txt_frame.pack(fill='x', padx=10, pady=5)
    vars['modo'].trace_add('write', atualiza_modo)
    atualiza_modo()
    root.mainloop()
if __name__ == '__main__':
    janela()