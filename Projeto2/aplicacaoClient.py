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

t_start = time.time()

# para saber a sua porta, execute no terminal :
# python -m serial.tools.list_ports
# se estiver usando windows, o gerenciador de dispositivos informa a porta

serialName = "/dev/ttyACM2"           # Ubuntu (variacao de)
#serialName = "/dev/cu.usbmodem1411" # Mac    (variacao de)
#serialName = "COM6"                  # Windows(variacao de)

def main():
    try:
        #declaramos um objeto do tipo enlace com o nome "com". 
        #Essa é a camada inferior à aplicação. Observe que um parametro
        #para declarar esse objeto é o nome da porta.

        # objeto - recebe a porta - camada física
        com1 = enlace(serialName)
        print("a porta client abriu")
    
        # Ativa comunicacao. Inicia os threads e a comunicação serial 
        com1.enable()
        #Se chegamos até aqui, a comunicação foi aberta com sucesso. Faça um print para informar.
        print("inicialização client ok")
        
        # gerando os dados a serem transmitidos,
        # que são uma lista de bytes - com o nome de txBuffer. 
        # Ela sempre irá armazenar os dados a serem enviados.

        # interação:
        input_image = input("Digite o caminho da imagem (a partir da pasta Projeto 1: ./")
        imageR = str("./"+input_image)

        # sem interação:
        #imageR = "./img/image.png"

        #controle
        print("Carregando imagem para transmissão:")
        print("- {}".format(imageR))
        print("----------------------")

        # lista de dados
        # read and b ?
        txBuffer = open(imageR,'rb').read()
        ##print(f'A lista de bytes é: \n {txBuffer}')
        
        ##print("Salvando dados no arquivo:")
        ##print("- {}".format(imageW))

        # tamanho da lista com os bytes da imagem
        txLen = len(txBuffer)
        print(f'O tamanho da lista de bytes é: \n {txLen}')

        # o número aqui tem que ser igual ao do getData do aplicacaoServer.py
        # combinamos o número 2 dessa vez
        # transformando o tamanho da lista em hexadecimal - do maior para o menor
        txHexLen = (txLen).to_bytes(2, byteorder='big')
        print(f'O tamanho da lista de bytes em hexadecimal é: \n {txHexLen}')
       
        # Transmitindo os dados com a função sendData 
        # que é um método da camada enlace
        print("txbuffer ok, a transmissão vai começar")

        # enviando o número hexadecimal do tamanho da lista de bytes da imagem
        # Cuidado! Apenas trasmitimos arrays de bytes! Nao listas!
        time.sleep(1.5)
        com1.sendData(txHexLen)
        print("txHexLen enviado")

        time.sleep(0.1)
        com1.sendData(txBuffer)
        print("txBuffer enviado")

        #comparar o inteiro (recebido)(converter) com o hex (que foi enviado)
        txGet, ntx = com1.getData(2)
        print("recebeu {}" .format(txGet))
        
        if txGet == txHexLen:
            print("enviado e recebido são iguais")
    
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