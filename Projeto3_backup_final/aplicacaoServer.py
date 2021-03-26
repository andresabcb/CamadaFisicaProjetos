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
from functions import *

# para saber a sua porta, execute no terminal :
# python -m serial.tools.list_ports
# se estiver usando windows, o gerenciador de dispositivos informa a porta

serialName = "/dev/ttyACM1"           # Ubuntu (variacao de)
#serialName = "/dev/cu.usbmodem1411" # Mac    (variacao de)
#serialName = "COM6"                  # Windows(variacao de)

def main():
    try:

        # objeto enlace - recebe a porta - camada física
        com2 = enlace(serialName)
        print("a porta server abriu")
    
        com2.enable()
        print("inicialização server ok")

        imageW = "./img/recebidacopia.png"

        # o número aqui tem que ser igual ao do to_bytes do aplicacaoClient.py
        ## HANDSHAKE
        print("aguardando handshake")
        rxhextest, nRx = com2.getData(15)
        print("recebeu o handshake {0} de tamanho {1}" .format(rxhextest,nRx))

        com2.sendData(rxhextest)

        ## RECEIVING IMAGE

        # criando pacote de resposta
        head_resp, len_head_resp = create_head(0,0,0,0,1)
        payload_resp = (123).to_bytes(1,'big')
        package_resp, len_package_resp = create_package(head_resp,payload_resp)
        # len = 15

        #inicializando a soma de bytes - payloads
        # zero_em_bytes = (0).to_bytes(1,byteorder='big')
        # image_payloads = zero_em_bytes
        image_payloads = bytearray()

        # dependo dos dados do primeiro get para começar o while
        # por isso tenho que fazer a primeira vez fora
        print('recebendo o envio client')
        # head fixo = 10

        # inicializando para entrar no while
        number_package = 0
        package_total = 1
        while number_package < package_total:
            # recebendo o head antes, e depois 
            # conferindo o tamanho do package
            # para usar no getData
            head_eop, nhead_eop = com2.getData(14)
            print(f'head e eop recebidos: {head_eop}')
            package_len = int.from_bytes(head_eop[4:6],'big')
            print(f'esperando {package_len} bytes')
            package, npackage = com2.getData(package_len)

            print(f'pacote recebido: {package}')
            print(f'tamanho do pacote recebido: {npackage}')

            check_parameters(package)

            head = package[:10]
            eop = package[-4:]
            payload = package[10:-4]
            print(f'tamanho do payload = {len(payload)}')

            number_package = int.from_bytes(package[0:2],'big')
            package_total =  int.from_bytes(package[2:4],'big')
            print(f'Pacote {number_package} / {package_total}')

            image_payloads.extend(payload)

            print(f'enviando resposta número {number_package}')
            com2.sendData(package_resp)

        # convertendo em imagem
        # print(f"A imagem semifinal é:\n{image_payloads}")
        len_img_payloads = len(image_payloads)
        print(f"O tamanho da imagem final é:\n{len_img_payloads}")
        # len_img = len(image)
        # print(f"O tamanho da imagem final é:\n{len_img}")

        f = open(imageW,'wb')
        f.write(image_payloads)

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


'''PROJETO 2----------------------
        rxInt = int.from_bytes(rxHexLen, byteorder='big')

        rxBuffer, nRxbuffer = com2.getData(rxInt)
        rxLen = len(rxBuffer)
        rxHexLen = (rxLen).to_bytes(2, byteorder='big')

        com2.sendData(rxHexLen)
        print("enviou {}" .format(rxHexLen))'''