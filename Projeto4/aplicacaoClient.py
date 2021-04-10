# Projeto 4 - Andresa B. C. Bicudo

# UART, baudrate 115200, sem bit de paridade
# o que faço com isso?

from enlace import *
import time
import numpy as np
from functions import *

# para saber a sua porta, execute no terminal:
# python -m serial.tools.list_ports
# se estiver usando windows, o gerenciador de dispositivos informa a porta

serialName = "/dev/ttyACM2"           # Ubuntu (variacao de)
#serialName = "/dev/cu.usbmodem1411" # Mac    (variacao de)
#serialName = "COM6"                  # Windows(variacao de)

t_start = time.time()

def main():
    try:
        ## ABRINDO A PORTA
        # objeto enlace - recebe a porta - camada física
        com1 = enlace(serialName)
        print("a porta client abriu")
    
        com1.enable()
        #Se chegamos até aqui, a comunicação foi aberta com sucesso. Faça um print para informar.
        print("inicialização client ok")

        ## com interação:
        #input_image = input("Digite o caminho da imagem (a partir da pasta Projeto 1: ./")
        #imageR = str("./"+input_image)

        ## sem interação:
        imageR = "./img/image.png"

        #controle
        print("Carregando imagem para transmissão:")
        print("- {}".format(imageR))
        print("----------------------")

        zero_em_bytes = (0).to_bytes(1,byteorder='big')

        # TESTE DE FUNÇÕES
        head_test, len_head_test = create_head(1,0,0,1,1,0,1,0,0)
        print(head_test, len_head_test)

        eop_test, len_eop_test = create_end_of_package()
        print(eop_test, len_eop_test)

        ## TXBUFFER
        # txBuffer é uma lista de bytes
        txBuffer = open(imageR,'rb').read()
        # print(txBuffer)
        typee = type(txBuffer)
        print(f'o tipo de tx buffer é {typee}')
        # tamanho da lista com os bytes da imagem
        txLen = len(txBuffer)
        print(f'O tamanho da lista de bytes é: \n {txLen}')

        # o número aqui tem que ser igual ao do getData do aplicacaoServer.py
        # transformando o tamanho da lista em hexadecimal - do maior para o menor
        txHexLen = (txLen).to_bytes(2, byteorder='big')
        print(f'O tamanho da lista de bytes em hexadecimal é: \n {txHexLen}')

        print("txbuffer ok, a comunicação vai começar")

        ## HANDSHAKE - TIPO 1
        payload_handshake = zero_em_bytes
        resposta, len_resposta = send_handshake(payload_handshake,com1)
        print(f'Resposta HANDSHAKE {resposta}')

        ## SENDING IMAGE - TIPO 3
        if resposta != zero_em_bytes:
            time.sleep(0.5)
            send_package(txBuffer,com1,1)

            ## ERRO ITEM 4
            # descomentar quando for fazer o teste
            #send_package(txBuffer,com1,4)

            ## ERRO ITEM 3
            # descomentar quando for fazer o teste
            #send_package(txBuffer,com1,3)

        # Encerra comunicação
        print("-------------------------")
        print("Comunicação encerrada Client")
        print("-------------------------")
        com1.disable()

        txHexLenInt = int.from_bytes(txHexLen, byteorder='big')

        t_stop = time.time()
        t_total = t_stop - t_start
        vel = t_total/txHexLenInt
        print(f'O tempo total para rodar a aplicação foi de:\n{t_total}')
        print(f'A velocidade em bytes/segundo foi de:\n{vel}')
        
    except Exception as erro:
        print("ops no Client! :-\\")
        print(erro)
        com1.disable()
        
    #so roda o main quando for executado do terminal ... 
    # se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()