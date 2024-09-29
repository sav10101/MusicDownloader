import os
import subprocess
import sys
import yt_dlp
import tkinter as tk
from tkinter import filedialog

def instalar_paquete(paquete):
    subprocess.check_call([sys.executable, "-m", "pip", "install", paquete])

def verificar_ffmpeg_instalado():
    subprocess.run(["ffmpeg", "-version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    instalar_paquete("ffmpeg-python")

def descargar_audio_youtube(url_video, directorio_destino):
    opciones_descarga = {
        'format': 'bestaudio/best',
        'extractaudio': True,
        'audioformat': 'webm',
        'outtmpl': os.path.join(directorio_destino, '%(title)s.%(ext)s'),
    }
    with yt_dlp.YoutubeDL(opciones_descarga) as ydl:
        ydl.download([url_video])

def convertir_archivos_webm_a_mp3(directorio_destino):
    for archivo in os.listdir(directorio_destino):
        if archivo.endswith(".webm"):
            archivo_mp3 = os.path.join(directorio_destino, archivo[:-5] + ".mp3")
            archivo_webm = os.path.join(directorio_destino, archivo)
            subprocess.run(["ffmpeg", "-i", archivo_webm, archivo_mp3], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            os.remove(archivo_webm)

def procesar_archivo_con_enlaces(ruta_archivo):
    directorio_destino = 'resultados'
    os.makedirs(directorio_destino, exist_ok=True)
    with open(ruta_archivo, 'r') as archivo:
        enlaces = archivo.readlines()
    for enlace in enlaces:
        enlace = enlace.strip()
        if enlace:
            descargar_audio_youtube(enlace, directorio_destino)
    convertir_archivos_webm_a_mp3(directorio_destino)

def seleccionar_archivo_enlaces():
    ruta_archivo = filedialog.askopenfilename(title="Selecciona el archivo de enlaces", filetypes=[("Text files", "*.txt")])
    if ruta_archivo:
        procesar_archivo_con_enlaces(ruta_archivo)

def ejecutar_aplicacion():
    verificar_ffmpeg_instalado()
    root = tk.Tk()
    root.title("Music Downloader")
    root.geometry("500x300")
    boton_seleccionar = tk.Button(root, text="Descargar musica", command=seleccionar_archivo_enlaces)
    boton_seleccionar.pack(pady=20)
    root.mainloop()

if __name__ == "__main__":
    ejecutar_aplicacion()
