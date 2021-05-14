from suaBibSignal import *
import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt
import sys
from utils import *
from utils2 import *
from funcoes_LPF import *

# 10. Peça a um de seus colegas para lhe enviar o arquivo modulado por ele.
# 11. Verifique que o sinal recebido tem a banda dentro de 16kHz e 24kHz (faça o Fourier).

#### HELP!
# 12. Demodule o áudio enviado pelo seu colega.

# 13. Filtre as frequências superiores a 4kHz.
# 14. Execute o áudio do sinal demodulado e verifique que novamente é audível.
# 15. Mostre o gráfico no domínio do tempo e da frequência (Fourier) do sinal demodulado. 
# Verifique que as frequências voltaram a ser baixas (região audível).

def main():
    signal = signalMeu()
    tempo = 3
    portadora = 20000

    ## ABRINDO O ARQUIVO
    audio = 'wav/modularizado_leo.wav'
    audio_modulado, samplerate = sf.read(audio)
    print('li o áudio!!!')
    print(f'lista audio: {audio_modulado}')
    print(f'samplerate: {samplerate}')
    # lista_audio = audio_modulado
    lista_audio = np.ravel(audio_modulado) # deixando pronto para usar
    print(type(lista_audio))
    time_audio = int(len(lista_audio)/samplerate) # CONSERTAR

    signal.plotFFT(lista_audio,samplerate,'Áudio modulado')
    ## verificar se está entre 16 e 24 Hz

    ## DEMODULANDO
    sinal_demodulado = lista_audio * portadora

    ## FILTRANDO
    cutoff = 4000 #Hz
    sinal_filtrado = filtro(sinal_demodulado, samplerate, cutoff)
    t = np.linspace(0,tempo,len(lista_audio))
    ## ver se é para executar mesmo o do demodulado
    plot_and_play(signal,sinal_demodulado,t,samplerate,'Sinal Demodulado')

if __name__ == "__main__":
    main()
