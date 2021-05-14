from utils2 import plota_graficos
from suaBibSignal import *
import peakutils    #alternativas  #from detect_peaks import *   #import pickle
import numpy as np
import sounddevice as sd
import soundfile as sf
import matplotlib.pyplot as plt
import time
from utils import *
from utils2 import *
from funcoes_LPF import filtro, LPF

# 1. Faça a leitura de um arquivo de áudio .wav de poucos segundos (entre 2 e 5) previamente gravado com uma
# taxa de amostragem de 44100Hz.
# 2. Normalize esse sinal: multiplicar o sinal por uma constante (a maior possível), 
# de modo que todos os pontos do sinal permaneçam dentro do intervalo[-1,1].
# 3. Reproduza o sinal e verifique que continua audível.
# 4. Filtre as altas frequências desse sinal (frequências acima de 4000 Hz).
# 5. Reproduza o sinal e verifique que continua audível (porém agora, sem as frequências altas, o som está mais
# “opaco”).
# 6. Module esse sinal de áudio em AM com portadora de 20000 Hz. 
# (Essa portadora deve ser uma senoide começando em zero)
# 7. Execute e verifique que não é perfeitamente audível.

# 8. Construa o gráfico nos domínios do tempo e da frequência (Fourier) 
# para os seguintes sinais:
# a. Sinal de áudio original.
# b. Sinal de áudio normalizado.
# c. Sinal de áudio filtrado.
# d. Sinal de áudio modulado.
# e. Verifique a banda que o sinal modulado ocupa. 
# Verifique que esteja dentro de 16KHz e 24kHz.
# Nomeie os gráficos de maneira a ser possível saber 
# o que se trada, por exemplo “Fourier do sinal
# modulado”.
# 9. Escolha um de seus colegas e o envie (por exemplo, por email) o arquivo 
# contendo o áudio modulado.


def main():
    signal = signalMeu()
    fs = 44100
    tempo = 3

    audio = 'wav/andresa.wav' # se quiser o arquivo pronto
    #lista_audio = record(fs,tempo) ## se quiser gravar na hora

    lista_audio1, samplerate = sf.read(audio)
    print('cheguei aqui')
    print(f'lista audio: {lista_audio1}')
    print(f'samplerate: {samplerate}')
    lista_audio = np.ravel(lista_audio1)
    print(type(lista_audio))
    time_audio = int(len(lista_audio)/samplerate)

    play_audio(lista_audio1, samplerate,'original antes do ravel')

    ## ORIGINAL
    t = np.linspace(0,tempo,len(lista_audio)) ## ver se deixa tempo ou muda p time_audio
    plot_and_play(signal,t,lista_audio,samplerate,'original depois do ravel')

    ## NORMALIZANDO
    maximo = max(abs(lista_audio))
    k = 1/maximo # chutei o valor entre [-1,1]
    sinal_normal = lista_audio*k
    print(f'O sinal normal é:{sinal_normal}')

    plot_and_play(signal,t,sinal_normal,samplerate,'Normal audio')

    ## FILTRAR
    cutoff = 4000
    sinal_filtrado = filtro(sinal_normal,samplerate,cutoff)

    plot_and_play(signal,t,sinal_filtrado,samplerate,'Filtrado')

    portadora = 20000 # diminuir p 14000 se nao der
    ampl = 1
    x1, sin1 = signal.generateSin(portadora,ampl,time_audio,samplerate)
    sinal_modulado = sinal_filtrado * sin1

    plot_and_play(signal,t,sinal_modulado,samplerate,'Modulado')

    # sf.write('andresa_modulada.wav', sinal_modulado, samplerate)

if __name__ == "__main__":
    main()