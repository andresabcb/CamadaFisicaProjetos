from enlace import *
import time
import numpy as np
import math

# serialName1 = "/dev/ttyACM2"
# com1 = enlace(serialName1)

# serialName2 = "/dev/ttyACM1" 
# com2 = enlace(serialName2)

'''HEAD
Tipo de pacote (dados, comando etc.)
Versão (IPv4, IPv6)
Número do pacote (incremental durante a transmissão)
Tamanho do dado que o pacote pode transmitir
O destinatário
A origem'''

def create_head(package_number, package_total, package_len, dest, origin, package_type = 1, version = 0):
    print("entrei na função head")
    # package type: 0 - handshake / 1- dados
    # origin e dest = 0 = client / = 1 = server
    
    package_number = (package_number).to_bytes(2,byteorder ='big')
    package_total = (package_total).to_bytes(2,byteorder ='big')
    package_len = (package_len).to_bytes(2,byteorder ='big')
    
    package_type = (package_type).to_bytes(1,byteorder = 'big')
    version = (version).to_bytes(1,byteorder ='big')
    dest = (dest).to_bytes(1,byteorder ='big')
    origin = (origin).to_bytes(1,byteorder ='big')

    '''version - 0 = 'IPv4' / 1 = 'IPv6'
    package_type - 0 = 'handshake'-  = 'dados'
    dest - 0 = 'client'/ 1 = 'server'
    origin - 0 = 'client'/1 = 'server'''
    
    head = package_number + package_total + package_len + dest + origin + package_type + version
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

def create_end_of_package(id_bytes=123456789):
    print("entrei na função eop")
    eop = (id_bytes).to_bytes(4, byteorder='big')
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
    head, len_head = create_head(1, 1, 1, 0, 1, 0)
    handshake, len_handshake = create_package(head,payload_handshake)
    print(f'O pacote handshake tem o tamanho: {len_handshake}')

    check_parameters(handshake)

    ## HANDSHAKE
    try_connection = True
    com1.sendData(handshake)
    print(f"handshake enviado:\nHandshake: {handshake}\nLen Handshake: {len_handshake}")

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
            else:
                print('resposta não reconhecida\nfinalizando operação')
                try_connection = False
        else:
            if resposta == handshake:
                print('enviado e recebido são iguais')
            return resposta, len_resposta

def send_package(file_bytes,com1):
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

        package_len = len(payload) + 14 # len head + eop
        print(f'o tamanho do pacote é de: {package_len}')
        head_img, len_head_img = create_head(package_number,total_packages,package_len,0,1)
        print(f'o head do pacote é {head_img}')
        payload_len = int.from_bytes(head_img[4:6],'big')
        print(f'O tamanho esperado de package é: {payload_len}')
        package, len_package = create_package(head_img,payload)
        print(f'pacote a ser enviado: {package} com tamanho {len_package}')

        check_parameters(package)

        if package_len == len_package:
            print('os lens sao iguais')
        else:
            print('os lens sao diferentes')

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

        txresp, ntxresp = com1.getData(15)
        print(f'A resposta foi recebida: {txresp}')

        package_number+=1
        m+=1