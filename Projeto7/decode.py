from suaBibSignal import *
import peakutils    #alternativas  #from detect_peaks import *   #import pickle
import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt
import time
from utils import *

def main():
    # um objeto da classe da sua biblioteca de apoio (cedida)
    signal = signalMeu()

    sd.default.samplerate = 44100 #taxa de amostragem
    # sd.default.channels = numCanais # o numero de canais, tipicamente são 2. Placas com dois canais. Se ocorrer problemas pode tentar com 1. No caso de 2 canais, ao gravar um audio, terá duas listas
    # duration =  tempo #tempo em segundos que ira aquisitar o sinal acustico captado pelo mic

    # calcule o numero de amostras "numAmostras" que serao feitas 
    # (numero de aquisicoes) durante a gravação.
    recording_time = 2 # seconds
    tx_amostragem = 44100 # ou 48.000
    numAmostras = tx_amostragem*recording_time

    print("!!! A captação começará em 3 segundos")
    print("3")
    time.sleep(1)
    print("2")
    time.sleep(1)
    print("1")
    time.sleep(1)
    print("!!! A gravação foi inicializada")

    # para gravar:
    # gravação da placa
    audio = sd.rec(int(numAmostras), tx_amostragem, channels=1)
    print(audio.shape) # virou um array
    print(audio) # lista de lista
    # sinal = audio[0][:]
    # print(sinal)

    # sound = "/snd/tecla5.wav"
    # audio = open(sound,'rb').read()
    sd.wait()
    print("------FIM")

    # ANÁLISE DE ÁUDIO:
    print(f'O tipo de áudio captado foi {type(audio)}')

    # EXTRAÇÃO - das amostras dentro da gravação
    # extrair das informações
    ## dados = 
    # eliminar os trechos de silencio
    
    # VETOR TEMPO
    # use a funcao linspace e crie o vetor tempo
    # Um instante correspondente a cada amostra!
    t = np.linspace(0,recording_time,len(audio))
    print("passei o t")

    # DADOS x TEMPO
    plt.plot(t, audio) # dosar os pontos

    plt.show()
    
    ## Calcula e exibe o Fourier do sinal audio
    ## Saidas = a amplitude e as frequencia

    # TESTE
    # freqteste = 1000
    # tempo = 3 # segundos
    # fs = 44100
    # ampl = 1
    # xteste, sinteste = signal.generateSin(freqteste,ampl,tempo,fs)
    # xfteste, yfteste = signal.calcFFT(sinteste, fs)
    
    sinal = []
    for i in range(len(audio)):
        sinal.append(audio[i])
        # print(audio[i])
    
    lista_audio = audio.ravel()

    xf, yf = signal.calcFFT(lista_audio, tx_amostragem)
    plt.figure("F(y)")
    plt.plot(xf,yf)
    plt.grid()
    plt.title('Fourier audio')

    # aqui estarão os picos da transformada = as freqs mais presentes no sinal
    # alguns picos devem corresponder as freqs DTMF

    # DESCOBRINDO A TECLA PRESSIONADA:
    # Extrair os picos e compará-los à tabela DTMF
    # Se tudo deu certo - 2 picos serão PRÓXIMOS aos valores da tabela
    # Os demais serão picos de ruídos

    # EXTRAINDO OS PICOS

    # utilizar a funcao peakutils.indexes(,,)
    # argumentos = dois parâmetros importantes: "thres" e "min_dist".
    # "thres" = a sensibilidade da funcao 
    # /quao elevado tem que ser o valor do pico para de fato ser considerado um pico
    # "min_dist" é relativo à tolerância 
    # /quao próximos 2 picos identificados podem estar
    # /se a funcao identificar um pico na posicao 200, só identificara outro a partir do 200+min_dis. 
    # Isso evita que varios picos sejam identificados em torno do 200, 
    # uma vez que todos sejam provavelmente resultado de pequenas variações de uma unica frequencia a ser identificada.

    # Valores iniciais de teste:
    ## thres = 0.4
    ## min_dist = 50
    #yf é o resultado da transformada de fourier
    index = peakutils.indexes(yf, thres=0.2, min_dist=50)
    print("index de picos {}" .format(index))

    # printe os picos encontrados!

    picos = []
    print('Picos encontrados:')
    for i in index:
        print(xf[i])
        print('\n')
        picos.append(xf[i])
    print(picos)
    
    # encontre na tabela duas frequencias proximas às frequencias de pico encontradas 
    # e descubra qual foi a tecla

    encontra_tecla_pelos_picos(picos)

    # print o valor tecla!!!
    # Se acertou, parabens! Voce construiu um sistema DTMF

    # Você pode tentar também identificar a tecla de um telefone real! 
    # Basta gravar o som emitido pelo seu celular ao pressionar uma tecla. 

    ## Exiba gráficos do fourier do som gravados
    plt.show()

if __name__ == "__main__":
    main()