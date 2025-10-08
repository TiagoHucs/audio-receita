import tkinter as tk
from tkinter import messagebox
from gtts import gTTS
import qrcode
import hashlib
import time
import os
from PIL import Image, ImageTk
import webbrowser
import platform
import subprocess

qr_filename_global = None  # variavel para guardar o ultimo qrcode gerado

def gerar():
    global qr_filename_global

    texto = entry_texto.get("1.0", tk.END).strip()
    url_base = entry_url.get().strip()
    #senha = entry_senha.get().strip()

    if not texto or not url_base:
        messagebox.showerror("Erro", "Todos os campos são obrigatórios!")
        return

    # Cria hash único baseado em texto + senha + timestamp
    hash_input = f"{texto}{time.time()}"
    hash_nome = hashlib.sha256(hash_input.encode()).hexdigest()[:16]  # reduzido a 16 caracteres

    # Gera áudio
    audio = gTTS(texto, lang="pt")
    audio_filename = f"{hash_nome}.mp3"
    audio.save(audio_filename)

    # Gera QR Code
    url_final = f"{url_base.rstrip('/')}/{audio_filename}"
    qr = qrcode.make(url_final)
    qr_filename = f"{hash_nome}.jpg"
    qr.save(qr_filename)

    qr_filename_global = qr_filename

    # Mostrar QR Code na interface
    img = Image.open(qr_filename)
    img = img.resize((200, 200))  # reduz tamanho para caber na tela
    img_tk = ImageTk.PhotoImage(img)

    qr_label.config(image=img_tk)
    qr_label.image = img_tk  # manter referência para não ser coletado
    btn_imprimir.config(state="normal")

    messagebox.showinfo("Sucesso", f"Áudio salvo: {audio_filename}\nQR Code salvo: {qr_filename}")

def imprimir():
    """Abre o QR Code no visualizador padrão do sistema para permitir impressão"""
    if qr_filename_global:
        sistema = platform.system()
        try:
            if sistema == "Windows":
                os.startfile(qr_filename_global, "print")  # abre direto na impressora
            elif sistema == "Darwin":  # macOS
                subprocess.run(["open", qr_filename_global])
            else:  # Linux
                subprocess.run(["xdg-open", qr_filename_global])
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível imprimir: {e}")
    else:
        messagebox.showwarning("Aviso", "Nenhum QR Code gerado ainda!")

# Interface Tkinter
root = tk.Tk()
root.title("Gerador de Áudio + QRCode")
root.geometry("420x550")

tk.Label(root, text="Digite o texto:").pack(anchor="w", padx=10, pady=5)
entry_texto = tk.Text(root, height=5, width=45)
entry_texto.pack(padx=10, pady=5)

tk.Label(root, text="URL base:").pack(anchor="w", padx=10, pady=5)
entry_url = tk.Entry(root, width=45)
entry_url.pack(padx=10, pady=5)

#tk.Label(root, text="Senha:").pack(anchor="w", padx=10, pady=5)
#entry_senha = tk.Entry(root, show="*", width=45)
#entry_senha.pack(padx=10, pady=5)

btn = tk.Button(root, text="Gerar", command=gerar)
btn.pack(pady=15)

qr_label = tk.Label(root)  # aqui vai aparecer o QR Code
qr_label.pack(pady=10)

btn_imprimir = tk.Button(root, text="Imprimir QR Code", command=imprimir, state="disabled")
btn_imprimir.pack(pady=10)

root.mainloop()
