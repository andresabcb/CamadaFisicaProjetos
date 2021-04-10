from enlace import *
import time
import numpy as np
import math

def create_head(msg_type, package_total, package_number, payload_len, restart_package, last_package, sensor_id = 101, server_id = 102, CRC = 0):
    print("entrei na função head")
    # msg_type: 1 - handshake / 2- server esperando
    # 3- levando um bloco dos dados / 4- resposta correta ao 3
    # 5- time out / 6- msg tipo 3 inválida

    # h0 – tipo de mensagem
    # h1 – id do sensor
    # h2 – id do servidor
    # h3 – número total de pacotes do arquivo
    # h4 – número do pacote sendo enviado
    # h5 – se tipo for handshake:id do arquivo
    # h5 – se tipo for dados: tamanho do payload
    # h6 – pacote solicitado para recomeço quando há erro no envio
    # h7 – último pacote recebido com sucesso
    # h8 – h9 – CRC

    '''list_params = [msg_type,sensor_id,server_id,package_total,package_number,payload_len,restart_package,last_package]
    for param in list_params:
        param = (param).to_bytes(1,byteorder = 'big')'''

    msg_type = (msg_type).to_bytes(1,byteorder = 'big')
    sensor_id = (sensor_id).to_bytes(1,byteorder = 'big')
    server_id = (server_id).to_bytes(1,byteorder = 'big')
    package_total = (package_total).to_bytes(1,byteorder ='big')
    package_number = (package_number).to_bytes(1,byteorder ='big')
    ## quando for um handshake o h5 será o id do arquivo
    payload_len = (payload_len).to_bytes(1,byteorder ='big')
    restart_package = (restart_package).to_bytes(1,byteorder ='big')
    last_package = (last_package).to_bytes(1,byteorder ='big')
    CRC = (CRC).to_bytes(2,byteorder ='big')

    # zerei temporariamente alguns dos parâmetros
    # para testar o que já tenho
    h0 = msg_type
    h1 = sensor_id # sensor = client // inventado
    h2 = server_id # inventado
    h3 = package_total
    h4 = package_number
    h5 = payload_len # se h0 for 1, isso será o id do arquivo # inventado
    h6 = restart_package
    h7 = last_package
    h8h9 = CRC # 2bytes # proximo projeto

    head = h0 + h1 + h2 + h3 + h4 + h5 + h6 + h7 + h8h9

    # print("cheguei até aqui head")
    len_head = len(head)
    # print(head)
    # print(len_head)
    
    if len_head == 10:
        # ver se compensa retornar uma lista ou um tuple mesmo
        return (head, len_head) #bytes e int 
    else:
        print('len head != 10')

'''EOP:
Sequência de bytes conhecida para ser possível a identificação
Possível verificação
'''
# PAYLOAD – variável entre 0 e 114 bytes. Reservado à transmissão dos arquivos.
# EOP – 4 bytes: 0xFF 0xAA 0xFF 0xAA

def create_end_of_package():
    print("entrei na função eop")
    # eop = (id_bytes).to_bytes(4, byteorder='big')
    eop = b'\xFF\xAA\xFF\xAA'
    len_eop = len(eop)
    return (eop, len_eop)

def create_package(head, payload):
    print("entrei na função package")
    eop, len_eop = create_end_of_package()
    package = head + payload + eop
    len_package = len(package)
    return (package, len_package)

def check_parameters(package):
    head = package[:10]
    eop = package[-4:]
    payload = package[10:-4]

    if len(head) == 10:
        print('head ok')
    else:
        print('head not ok')

    if len(eop) == 4:
        print('eop ok')
    else:
        print('eop not ok')

    if len(payload) <= 114:
        print('payload ok')
    else:
        print('payload not ok')

    if len(package) <= 128 and len(package) > 14:
        print('package ok')
    else:
        print('package not ok')

def send_handshake(payload_handshake,com1):
    head, len_head = create_head(1,0,1,1,1,1)
    handshake, len_handshake = create_package(head,payload_handshake)
    print(f'O pacote handshake tem o tamanho: {len_handshake}')

    check_parameters(handshake)

    ## HANDSHAKE
    try_connection = True
    com1.sendData(handshake)
    print(f"handshake enviado:\nHandshake: {handshake}\nLen Handshake: {len_handshake}")

    # sleep de 5 segundos?

    while try_connection:
        # confere o tempo dentro do getdatahandshake
        resposta, len_resposta = com1.getDataHandshake(15)
        print(resposta)
        zero_em_bytes = (0).to_bytes(1,byteorder='big')

        if resposta == zero_em_bytes: #getNData no enlaceRx
            try_again = input("Servidor inativo. Tentar novamente? S/N ")

            if try_again == "S" or try_again == "s":
                com1.sendData(handshake)
                try_connection = True
            elif try_again == 'N' or try_again == 'n':
                print('a conexão não foi estabelecida')
                try_connection = False
                return resposta, len_resposta
            else:
                print('resposta não reconhecida\nfinalizando operação')
                try_connection = False
                return resposta, len_resposta
        else:
            # resolver esse probleminha
            if resposta[1:] == handshake[1:]:
                print('enviado e recebido são iguais')
            else:
                print('enviado e recebido não são iguais')
            return resposta, len_resposta

def send_package(file_bytes,com1,teste):
    print("começando o envio dos pacotes da imagem")
    file_size = len(file_bytes)
    # o package len vai ser o tanto de slices que vamos ter que dar na imagem
    # com isso o tanto de pacotes a serem enviados separadmente
    bytes_per_package = 114
    total_packages = math.ceil(file_size/bytes_per_package) # cte
    print(f'O número de pacotes será {total_packages}')
    package_number = 1  # inicialização
    m = 0 # multiplicador para pegar os pedaços da img

    while package_number <= total_packages:
        if package_number == total_packages:
            print('É o último pacote')
            payload = file_bytes[0+bytes_per_package*m:]
        else:
            print('Não é o último pacote')
            payload = file_bytes[0+bytes_per_package*m:bytes_per_package*(m+1)]

        # ERRO ITEM 4:
        if teste == 4:
            package_len = len(payload) + 14 - 2
        else:
            package_len = len(payload) + 14 # len head + eop
        
        # ERRO TESTE 3:
        if teste == 3:
            package_number += 2

        print(f'o tamanho do pacote é de: {package_len}')
        head_img, len_head_img = create_head(3,total_packages,package_number,len(payload),package_number,package_number-1)
        ## antigo: create_head(package_number,total_packages,package_len,0,1)
        print(f'o head do pacote é {head_img}')
        payload_len = int.from_bytes(head_img[4:6],'big')
        print(f'O tamanho esperado de package é: {payload_len}')
        package, len_package = create_package(head_img,payload)
        print(f'pacote a ser enviado: {package} com tamanho {len_package}')

        check_parameters(package)

        # teste item 4
        if package_len == len_package:
            print('Item 4 TUDO OK: os lens sao iguais')
        else:
            print('Item 4 ATENÇÃO: os lens sao diferentes')
            break

        head = package[:10]
        eop = package[-4:]
        payload = package[10:-4]

        # sending package
        head_eop = head + eop
        com1.sendData(head_eop)
        print(f"head e eop número {package_number} enviados com tamanho {len(head_eop)}")
        time.sleep(0.05)
        com1.sendData(package)
        print(f'O tamanho do pacote enviado é {len(package)}')
        print(f"package número {package_number} enviado\naguardando resposta")

        txresp, ntxresp = com1.getDataHandshake(15)
        print(f'A resposta foi recebida: {txresp}')

        zero_em_bytes = (0).to_bytes(1,byteorder='big')
        if txresp == zero_em_bytes:
            break

        package_number+=1
        m+=1

# • Instante do envio ou recebimento
# • Envio ou recebimento
# • Tipo de mensagem (de acordo com o protocolo)
# • Tamanho de bytes total
# • Pacote enviado (caso tipo 3)
# • Total de pacotes (caso tipo 3 )
# • CRC do payload para mensagem tipo 3 (caso tenha implementado)
# 29/09/2020 13:34:23.089 / envio / 3 / 128 / 1 / 23/ F23F

# nao foi testada ainda:
def create_log(owner, way, msg, transmission_number, msg_type, time, date):
    # owner = quem chamou (client ou server) - int
    # way - envio ou recebimento
    # msg = o que vai escrever - string
    # logs_list = a lista de arquivos log - list
    ## conferir se pode ser a lista dos arquivos ou só dos nomes de arquivo

    if owner == 0:
        owner = 'Client'
    elif owner == 1:
        owner = 'Server'

    if way == 0:
        way = 'envio'
    elif way == 1:
        way = 'recebimento'

    file = f'./logs/{owner}{transmission_number}.txt'
    line = f"{date} {time}/{way}/{msg}/{msg_type}"

    log = open(file,'wb')
    log.write(line)

    log.close() # fecha o arquivo