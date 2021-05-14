from suaBibSignal import *
import peakutils    #alternativas  #from detect_peaks import *   #import pickle
import numpy as np
import sounddevice as sd
import soundfile as sf
import matplotlib.pyplot as plt
import time
from utils import *
from funcoes_LPF import filtro, LPF

def plota_graficos(x,y,title=''):
    plt.figure(title)
    plt.plot(x,y)
    plt.grid()
    plt.title(title)
    plt.show()

def play_audio(sinal,samplerate,title=''):
    print('----------------')
    print(f'!!!!!! Iniciando reprodução do áudio {title}')
    sd.play(sinal, samplerate)
    # aguarda fim do audio
    sd.wait()
    print(f'!!!!!! Finalizando reprodução do áudio {title}')

def plot_and_play(signal,t,sinal,samplerate,title=''):
    plota_graficos(t,sinal,title)
    signal.plotFFT(sinal,samplerate,title)
    play_audio(sinal, samplerate,title)

def record(fs,tempo,channels=1):
    print("!!! A captação começará em 3 segundos")
    print("3")
    time.sleep(1)
    print("2")
    time.sleep(1)
    print("1")
    time.sleep(1)
    print("!!! A gravação foi inicializada")
    numAmostras = fs*tempo
    audio = sd.rec(int(numAmostras), fs, channels=channels)
    sd.wait()
    print(f'Shape do audio{audio.shape}') # virou um array
    print(f'++++++++Áudio:\n {audio}') # lista de lista
    lista_audio = np.ravel(audio)
    return lista_audio