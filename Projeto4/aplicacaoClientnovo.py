# Projeto 4 - Andresa B. C. Bicudo

from enlace import *
import time
import numpy as np
from functionsnovo import *
from functionsnovo2 import *

# python -m serial.tools.list_ports
# sudo chmod a+rw /dev/ttyACM1 
# ou o nome da outra porta

serialName = "/dev/ttyACM2"

t_start = time.time()

def main():
    try:
        com1 = enlace(serialName)
        print("a porta client abriu")
        com1.enable()
        print("inicialização client ok")

        ## com interação:
        #input_image = input("Digite o caminho da imagem (a partir da pasta Projeto 1: ./")
        #imageR = str("./"+input_image)

        ## sem interação:
        imageR = "./img/image.png"
        print("Carregando imagem para transmissão:")
        print("- {}".format(imageR))
        print("----------------------")

        zero_em_bytes = (0).to_bytes(1,byteorder='big')
        # TESTES PARA A ENTREGA DO PROJ 4
        transm_num = 6

        ## TESTE DE FUNÇÕES
        '''head_test, len_head_test = create_head(1,0,0,1,1,0,1,0,0)
        print(head_test, len_head_test)
        eop_test, len_eop_test = create_end_of_package()
        print(eop_test, len_eop_test)'''

        # head, len_head = create_head2(1, 1, 1, 0, 1, 0)
        # print('--------------------------')
        # print('--------------------------')
        # print(head)

        # head, len_head = create_head(1, 1, 1, 0, 1, 0)
        # print('--------------------------')
        # print('--------------------------')
        # print(head)

        '''package_len = 0
        total_packages = 0
        package_number = 0 # h8h9
        create_log('c','e',1,1,package_len, package_number, total_packages)'''
        
        ## TXBUFFER
        txBuffer = open(imageR,'rb').read()
        txLen = len(txBuffer)
        print(f'O tamanho da lista de bytes é: \n {txLen}')
        txHexLen = (txLen).to_bytes(2, byteorder='big')
        print(f'O tamanho da lista de bytes em hexadecimal é: \n {txHexLen}')
        print("txbuffer ok, a comunicação vai começar")

        ## HANDSHAKE - TIPO 1 - funcionando
        payload_handshake = zero_em_bytes
        resposta, len_resposta = send_handshake(payload_handshake,com1,transm_num)
        print(f'Resposta HANDSHAKE {resposta}')

        ## SENDING IMAGE - TIPO 3
        if resposta != zero_em_bytes:
            time.sleep(0.5)
            send_package(txBuffer,com1,1,transm_num)

            ## ERRO ITEM 4
            # descomentar quando for fazer o teste
            #send_package(txBuffer,com1,4,transm_num)

            ## ERRO ITEM 3
            # descomentar quando for fazer o teste
            #send_package(txBuffer,com1,3,transm_num)

        # Encerra comunicação
        print("-------------------------")
        print("Comunicação encerrada Client")
        print("-------------------------")
        com1.disable()

        txHexLenInt = int.from_bytes(txHexLen, byteorder='big')

        t_stop = time.time()
        t_total = t_stop - t_start
        vel = t_total/txHexLenInt
        print(f'O tempo total para rodar a aplicação client foi de:\n{t_total}')
        print(f'A velocidade em bytes/segundo foi de:\n{vel}')
        print(txBuffer)
        print(f'O tamanho da imagem devia ser: \n {txLen}')
        
    except Exception as erro:
        print("ops no Client! :-\\")
        print(erro)
        com1.disable()
        
    #so roda o main quando for executado do terminal ... 
    # se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()