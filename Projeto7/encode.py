from suaBibSignal import *
import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt
import sys
from utils import *

# Lado emissor
#  Perguntar ao usuário qual número, entre 0 e 9 ele quer digitar.
#  Emitir por alguns segundos as duas frequências relativas ao número escolhido.
#  Plotar o gráfico com as duas frequências somadas.
#  Opcional: Você poderá também salvar o sinal gerado em um arquivo.

def main():
    # OBJETIVO - Gerar 2 senóides
    # Cada uma com frequência correspondente à tecla pressionada

    # INÍCIO
    com1 = signalMeu()
    print("Inicializando encoder")
    tecla_str = input('Digite uma tecla do teclado numérico DTMF (DE 0 A 9)')
    print("Aguardando usuário")

    freq1, freq2 = acha_frequencias(tecla_str)

    print("Gerando Tons base")
    fs = 44100 # taxa de amostragem
    ampl = 1
    time = 2 # segundos

    # gerando as senoides:
    x1, sin1 = com1.generateSin(freq1,ampl,time,fs)
    x2, sin2 = com1.generateSin(freq2,ampl,time,fs)

    # sinal a ser emitido
    sin = sin1+sin2

    # função da biblioteca sounddevice = reproduzir o som
    # tone = NumPy array
    # fs = sampling frequency
    print("Executando as senoides (emitindo o som)")
    sd.play(sin, fs)
    # aguarda fim do audio
    sd.wait()
    # print("Gerando Tom referente ao símbolo : {}".format(num))
    
    # construa o gráfico do sinal emitido e o gráfico da transformada de Fourier
    # Cuidado!
    # Como as frequencias sao relativamente altas, 
    # voce deve plotar apenas alguns pontos (alguns periodos) 
    # para conseguirmos ver o sinal

    # PLOTANDO OS GRÁFICOS
    com1.plotFFT(sin, fs)
    plt.show()
    t = np.linspace(0,time,len(sin))
    plt.plot(t, sin)
    plt.show()
    print("Gráficos plotados")

if __name__ == "__main__":
    main()
