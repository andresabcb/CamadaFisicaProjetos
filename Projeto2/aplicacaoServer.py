#####################################################
# Camada Física da Computação
#Carareto
#11/08/2020
#Aplicação
####################################################

#esta é a camada superior, de aplicação do seu software de comunicação serial UART.
#para acompanhar a execução e identificar erros, construa prints ao longo do código! 

from enlace import *
import time
import numpy as np

# para saber a sua porta, execute no terminal :
# python -m serial.tools.list_ports
# se estiver usando windows, o gerenciador de dispositivos informa a porta

serialName = "/dev/ttyACM1"           # Ubuntu (variacao de)
#serialName = "/dev/cu.usbmodem1411" # Mac    (variacao de)
#serialName = "COM6"                  # Windows(variacao de)

def main():
    try:
        #declaramos um objeto do tipo enlace com o nome "com". Essa é a camada inferior à aplicação. Observe que um parametro
        #para declarar esse objeto é o nome da porta.

        # objeto - recebe a porta - camada física
        com2 = enlace(serialName)
        print("a porta server abriu")
    
        # Ativa comunicacao
        com2.enable()

        #Se chegamos até aqui, a comunicação foi aberta com sucesso
        print("inicialização server ok")

        imageW = "./img/recebidacopia.png"

        #Agora vamos iniciar a recepção dos dados. 
        #Se algo chegou ao RX, deve estar automaticamente guardado
        #Observe o que faz a rotina dentro do thread RX

        #Será que todos os bytes enviados estão realmente guardadas? Será que conseguimos verificar?
        #Veja o que faz a funcao do enlaceRX  getBufferLen

        # o número aqui tem que ser igual ao do to_bytes do aplicacaoClient.py
        rxHexLen, nRx = com2.getData(2)
        print("recebeu {}" .format(rxHexLen))

        rxInt = int.from_bytes(rxHexLen, byteorder='big')

        rxBuffer, nRxbuffer = com2.getData(rxInt)
        rxLen = len(rxBuffer)
        rxHexLen = (rxLen).to_bytes(2, byteorder='big')

        com2.sendData(rxHexLen)
        print("enviou {}" .format(rxHexLen))

        f = open(imageW,'wb')
        f.write(rxBuffer)

        #fecha o arquivo
        f.close()
    
        # Encerra comunicação
        print("-------------------------")
        print("Comunicação encerrada Server")
        print("-------------------------")
        com2.disable()
        
    except Exception as erro:
        print("ops no Server! :-\\")
        print(erro)
        com2.disable()
        

    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()
