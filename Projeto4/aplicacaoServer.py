# Projeto 4 - Andresa B. C. Bicudo

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
        ## ABRINDO A PORTA
        # objeto enlace - recebe a porta - camada física
        com2 = enlace(serialName)
        print("a porta server abriu")
    
        com2.enable()
        print("inicialização server ok")

        imageW = "./img/recebidacopia.png"

        # útil ao longo do código
        zero_em_bytes = (0).to_bytes(1,byteorder='big')

        # o número aqui tem que ser igual ao do to_bytes do aplicacaoClient.py
        ## HANDSHAKE
        print("aguardando handshake")
        rxhextest, nRx = com2.getData(15)
        print("recebeu o handshake {0} de tamanho {1}" .format(rxhextest,nRx))

        ## TIPO 2 - ESPERANDO
        head_resp, len_head_resp = create_head(2,1,1,0,1,0)
        package_resp, len_package_resp = create_package(head_resp,zero_em_bytes)
        com2.sendData(package_resp)

        ## RECEIVING IMAGE - TIPO 4 e TIPO 6

        # criando pacote de resposta do tipo 4
        head_resp_ok, len_head_resp_ok = create_head(4,0,1,1,1,1)
        payload_resp_ok = (104).to_bytes(1,'big')
        package_resp_ok, len_package_resp_ok = create_package(head_resp_ok,payload_resp_ok)

        # criando pacote de resposta do tipo 6
        head_resp_nao_ok, len_head_resp__nao_ok = create_head(6,0,1,1,1,1)
        payload_resp_nao_ok = (106).to_bytes(1,'big')
        package_resp_nao_ok, len_package_resp_nao_ok = create_package(head_resp_nao_ok,payload_resp_nao_ok)

        # inicializando a soma de bytes - payloads
        # image_payloads = zero_em_bytes
        image_payloads = bytearray()

        print('recebendo o envio client')
        # inicializando para entrar no while
        number_package = 0
        package_total = 1

        num_package = number_package - 1 # teste item 3
        while number_package < package_total:
            # recebendo o head antes, e depois 
            # conferindo o tamanho do package
            # para usar no getData
            head_eop, nhead_eop = com2.getDataHandshake(14)
            print(f'head e eop recebidos: {head_eop}')
            package_len = int.from_bytes(head_eop[4:6],'big')
            print(f'esperando {package_len} bytes')
            package, npackage = com2.getDataHandshake(package_len)
            print(f'pacote recebido: {package}')
            print(f'tamanho do pacote recebido: {npackage}')

            # teste item 3
            if number_package == num_package + 1:
                print('Item 3 TUDO OK: a ordem está correta')
                # com2.sendData(package_resp_ok)
            else:
                print('Item 3 ATENÇÃO: a ordem dos pacotes está incorreta')
                # com2.sendData(package_resp_nao_ok)
                break

            check_parameters(package)

            head = package[:10]
            eop = package[-4:]
            payload = package[10:-4]
            print(f'tamanho do payload = {len(payload)}')

            num_package = number_package
            number_package = int.from_bytes(package[0:2],'big')
            package_total =  int.from_bytes(package[2:4],'big')
            print(f'Pacote {number_package} / {package_total}')

            image_payloads.extend(payload)

            print(f'enviando resposta número {number_package}')
            #com2.sendData(package_resp)
            ## rever isso aqui

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