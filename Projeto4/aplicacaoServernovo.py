# Projeto 4 - Andresa B. C. Bicudo

from enlace import *
import time
import numpy as np
from functionsnovo import *
from functionsnovo2 import *

# python -m serial.tools.list_ports
# sudo chmod a+rw /dev/ttyACM1 
# ou o nome da outra porta

serialName = "/dev/ttyACM1"

def main():
    try:
        com2 = enlace(serialName)
        print("a porta server abriu")
        com2.enable()
        print("inicialização server ok")

        imageW = "./img/recebidacopia.png"

        zero_em_bytes = (0).to_bytes(1,byteorder='big')
        transm_num = 5

        ## HANDSHAKE - TIPO 2 - funcionando
        print("aguardando handshake")
        getdata_len = 15
        handshake, len_handshake = com2.getData(getdata_len) # nao tem timer
        print("recebeu o handshake {0} de tamanho {1}" .format(handshake,len_handshake))

        time.sleep(1)
        print(handshake[0]) # ja é int - consertar
        # h0 = int_from_bytes(handshake[0])
        # h2 = int_from_bytes(handshake[2])
        h0 = handshake[0]
        h2 = handshake[2]
        number_package = handshake[4]
        package_total = handshake[3]

        if handshake != zero_em_bytes:
            create_log('s','r',transm_num,h0,getdata_len, number_package, package_total)

        if h0 == 1 and h2 == 12:
            print('Handshake recebido e é para mim')

        ## TIPO 2 - ENVIANDO RESPOSTA - OCIOSO
        head_resp, len_head_resp = create_head(2,1,1,0,1,0)
        package_resp, len_package_resp = create_package(head_resp,zero_em_bytes)
        com2.sendData(package_resp)

        ## RECEIVING IMAGE - TIPO 4 e TIPO 6
        image_payloads = receive_package(com2,transm_num)
        len_img_payloads = len(image_payloads)
        print(image_payloads)
        print(f"O tamanho da imagem final é:\n{len_img_payloads}")

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