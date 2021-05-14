from suaBibSignal import *
import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt
import sys

def signal_handler(signal, frame):
    print('You pressed Ctrl+C!')
    sys.exit(0)

#converte intensidade em db
def todB(s):
    sdB = 10*np.log10(s)
    return(sdB)

def tecla_to_index(string):
    if string == "0":
        return 0
    elif string == "1":
        return 1
    elif string == "2":
        return 2
    elif string == "3":
        return 3
    elif string == "4":
        return 4
    elif string == "5":
        return 5
    elif string == "6":
        return 6
    elif string == "7":
        return 7
    elif string == "8":
        return 8
    elif string == "9":
        return 9
    elif string == "X":
        return 10
    elif string == "#":
        return 11
    else:
        print("A tecla selecionada não significa nada")

def acha_frequencias(tecla_str):
    # TABELA DTMF
    # o item de índice 0 vai ser referente à tecla 0
    # e assim sucessivamente
    # quando chegar no 10 = # e 11 = X
    #        1209 Hz 1336 Hz 1477 Hz 1633 Hz
    # 697 Hz	1	2	3	A
    # 770 Hz	4	5	6	B
    # 852 Hz	7	8	9	C
    # 941 Hz	*	0	#	D
    tecla0 = [941,1336]

    tecla1 = [697,1209]
    tecla2 = [697,1336]
    tecla3 = [697,1477]

    tecla4 = [770,1209]
    tecla5 = [770,1336]
    tecla6 = [770,1477]

    tecla7 = [852,1209]
    tecla8 = [852,1336]
    tecla9 = [852,1477]

    tecla10 = [941,1209]
    tecla11 = [941,1477]

    lista_dtmf = [tecla0,tecla1,tecla2,tecla3,tecla4,tecla5,tecla6,tecla7,tecla8,tecla9,tecla10,tecla11]

    tecla = tecla_to_index(tecla_str)
    freq1 = lista_dtmf[tecla][0]
    freq2 = lista_dtmf[tecla][1]

    return freq1, freq2

def encontra_tecla_pelos_picos(picos):
    # TABELA DTMF
    # o item de índice 0 vai ser referente à tecla 0
    # e assim sucessivamente
    # quando chegar no 10 = # e 11 = X
    #        1209 Hz 1336 Hz 1477 Hz 1633 Hz
    # 697 Hz	1	2	3	A
    # 770 Hz	4	5	6	B
    # 852 Hz	7	8	9	C
    # 941 Hz	*	0	#	D
    tecla0 = [941,1336]

    tecla1 = [697,1209]
    tecla2 = [697,1336]
    tecla3 = [697,1477]

    tecla4 = [770,1209]
    tecla5 = [770,1336]
    tecla6 = [770,1477]

    tecla7 = [852,1209]
    tecla8 = [852,1336]
    tecla9 = [852,1477]

    tecla10 = [941,1209]
    tecla11 = [941,1477]

    # just in case...
    # linhas_dtmf = [697,770,852,941]
    # colunas_dtmf = [1209,1336,1477]
    valores_dtmf = [697,770,852,941,1209,1336,1477]
    lista_dtmf = [tecla0,tecla1,tecla2,tecla3,tecla4,tecla5,tecla6,tecla7,tecla8,tecla9,tecla10,tecla11]
    
    valores_tecla = []
    for pico in picos:
        for freq_dtmf in valores_dtmf:
            if pico<freq_dtmf+2 and pico>freq_dtmf-2:
                valores_tecla.append(freq_dtmf)
    print(valores_tecla)
    
    if len(valores_tecla) == 2:
        print('achei uma tecla compatível com a tabela DTMF')
        encontrada = False
        for i in range(len(lista_dtmf)):
            tecla = lista_dtmf[i]
            if (valores_tecla == tecla) or (valores_tecla[0] == tecla[1] and valores_tecla[1] == tecla[0]):
                if i == 10:
                    print("a tecla encontrada foi a número *")
                if i == 11:
                    print("a tecla encontrada foi a número #")
                print(f"a tecla encontrada foi a número {i}")
                encontrada = True
        if not encontrada:
            print("Os dois valores encontrados não são compatíveis com nenhuma tecla da tabela DTMF")
    else:
        print('não achei uma tecla compatível com a tabela DTMF')