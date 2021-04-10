from enlace import *
import os.path
import time
import numpy as np
import math

# msg_type: 1 - handshake / 2- server esperando
# 3- levando um bloco dos dados / 4- resposta correta ao 3
# 5- time out / 6- msg tipo 3 inválida

zero_em_bytes = (0).to_bytes(1,byteorder='big')

'''def int_from_bytes(bytess):
    integer = int.from_bytes(bytess,'big')
    return integer'''

# do projeto passado - funcionando
def create_head2(package_number, package_total, package_len, dest, origin, package_type = 1, version = 0):
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

def create_head(msg_type, package_total, package_number, payload_len, restart_package, last_package, sensor_id = 11, server_id = 12, CRC = 0):
    # recebe em int e transforma em bytes
    print("entrei na função head")

    h0 = (msg_type).to_bytes(1,byteorder = 'big')
    print(f'O tipo da mensagem colocado no head é:\n{h0}')
    h3 = (package_total).to_bytes(1,byteorder ='big')
    h4 = (package_number).to_bytes(1,byteorder ='big')
    ## quando for um handshake o h5 será o id do arquivo # 55
    h5 = (payload_len).to_bytes(1,byteorder ='big')
    h6 = (restart_package).to_bytes(1,byteorder ='big')
    h7 = (last_package).to_bytes(1,byteorder ='big')
    h1 = (sensor_id).to_bytes(1,byteorder = 'big') # sensor_id
    #h1 = zero_em_bytes
    h2 = (server_id).to_bytes(1,byteorder = 'big') # server id
    h8h9 = (CRC).to_bytes(2,byteorder ='big')

    list_h = [h0, h1, h2, h3, h4, h5, h6, h7, h8h9]
    '''head = bytearray()

    for h in list_h:
        head.extend(h)

    print(f'o head é: {head}')'''

    head = h0 + h1 + h2 + h3 + h4 + h5 + h6 + h7 + h8h9
    # head = bytes(head)
    print('----------------------------')
    print(head)
    '''for h in list_h:
        print(h)
    for i in range(0,7):
        print(head[i])
    print(head[8:])'''

    len_head = len(head)
    
    if len_head == 10:
        return (head, len_head) #bytes e int 
    else:
        print('len head != 10')

def create_end_of_package():
    # já recebe em bytes
    print("entrei na função eop")
    eop = b'\xFF\xAA\xFF\xAA'
    len_eop = len(eop)
    return (eop, len_eop)

def check_parameters(head,payload,eop):
    # se receber o pacote todo e dividir
    # vai ter o tamanho do que eu dividi
    # a resposta vai ser um falso positivo sempre
    package = head + payload + eop

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

def create_package(head, payload):
    # head varia muito, então virou parâmetro
    print("entrei na função package")
    eop, len_eop = create_end_of_package()
    package = head + payload + eop
    len_package = len(package)
    check_parameters(head,payload,eop)
    return (package, len_package)

# 29/09/2020 13:34:23.089 / envio / 3 / 128 / 1 / 23/ F23F
# precisa ajustar a criação do arquivo e testar escrever no mesmo arquivo
def create_log(owner, way, transmission_number, msg_type, package_len, package_number, total_packages, CRC = zero_em_bytes, time = time.time(), date = '9/4/2021'):
    print('==criando arquivo log==')
    # owner = quem chamou (client ou server) - str
    # way - envio ou recebimento
    # msg = o que vai escrever - string
    # logs_list = a lista de arquivos log - list
    ## conferir se pode ser a lista dos arquivos ou só dos nomes de arquivo
    if owner == 'c' or owner == 'C':
        owner = 'Client'
    elif owner == 's' or owner == 'S':
        owner = 'Server'

    if way == 'e' or way == 'E':
        way = 'envio'
    elif way == 'r' or way == 'R':
        way = 'recebimento'

    filee = f"./logs/{owner}{transmission_number}.txt"
    print(filee)
    line = f"\n{date} {time} / {way} / {msg_type} / {package_len} / {package_number} {total_packages} / {CRC}"
    print(line)
    if os.path.isfile(filee):
        print ("File exists")
        log = open(filee,'at')
    else:
        print ("File does not exist")
        log = open(filee,'wt')
    log.write(line)

    log.close() # fecha o arquivo

def send_handshake(payload_handshake,com1,transm_num):
    ## TIPO 1
    msg_type = 1
    id_arquivo = 55
    package_total = 1
    package_number = 1
    last_package = package_number - 1
    head, len_head = create_head(msg_type,package_total,package_number,id_arquivo,package_number,last_package)
    handshake, len_handshake = create_package(head,payload_handshake)
    print(f'O pacote handshake tem o tamanho: {len_handshake}')

    try_connection = True
    com1.sendData(handshake)
    create_log('c','e',transm_num,msg_type,len_handshake, package_number, package_total)
    print(f"handshake enviado:\nHandshake: {handshake}\nLen Handshake: {len_handshake}")
    # sleep de 5 segundos?

    while try_connection:
        resposta, len_resposta = com1.getDataHandshake(15) # loop 
        print(resposta)

        if resposta == zero_em_bytes:
            try_again = input("Servidor inativo. Tentar novamente? S/N ")

            if try_again == "S" or try_again == "s":
                com1.sendData(handshake)
                create_log('c','e',transm_num,msg_type,len_handshake, package_number, package_total)
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
            if resposta[0] == 2:
                print('mensagem tipo 2 recebida')
            else:
                print('mensagem tipo 2 não identificada')
            '''# resolver esse probleminha
            if resposta[1:] == handshake[1:]:
                print('enviado e recebido são iguais')
            else:
                print('enviado e recebido não são iguais')'''
            return resposta, len_resposta