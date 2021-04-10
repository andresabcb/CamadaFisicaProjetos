from enlace import *
import time
import numpy as np
import math
from functionsnovo import *

zero_em_bytes = (0).to_bytes(1,byteorder='big')

def send_package(file_bytes,com1,teste,transm_num):
    print('---------SEND PACKAGE---------')
    print('entrei na send_package')
    ## INICIALIZAÇÃO
    print("começando o envio dos pacotes da imagem")
    file_size = len(file_bytes)
    bytes_per_package = 114
    total_packages = math.ceil(file_size/bytes_per_package) # cte
    print(f'O número de pacotes será {total_packages}')

    # inicialização
    package_number = 1
    m = 0 # multiplicador para pegar os pedaços da img
    # try_connection = True
    
    ## CRIANDO O PACOTE
    while package_number <= total_packages:
        # tem que vir primeiro para criar o payload
        if package_number == total_packages:
            print('É o último pacote')
            payload = file_bytes[0+bytes_per_package*m:]
        else:
            print('Não é o último pacote')
            payload = file_bytes[0+bytes_per_package*m:bytes_per_package*(m+1)]

        print(f'o payload é {payload}')

        # ERRO ITEM 4:
        if teste == 4:
            package_len = len(payload) + 14 - 2
        else:
            package_len = len(payload) + 14 # len head + eop
        
        # ERRO TESTE 3 - resposta no server:
        if teste == 3:
            package_number += 2

        print(f'o tamanho do pacote é de: {package_len}')
        last_package_sent = (package_number-1)
        print(last_package_sent)
        payload_len = len(payload)
        print(f'!!!!!!o tamanho do payload é de: {payload_len}')
        msg_type_sent = 3
        head_img, len_head_img = create_head(msg_type_sent,total_packages,package_number,payload_len,package_number,last_package_sent)
        print(f'o head do pacote é {head_img}')
        #payload_len = int.from_bytes(head_img[5],'big')
        payload_len = head_img[5]
        print(f'O tamanho esperado de payload é: {payload_len}')
        package, len_package = create_package(head_img,payload)
        print(f'pacote a ser enviado: {package} com tamanho {len_package}')

        # RESPOSTA ERRO ITEM 4
        if package_len == len_package:
            print('Item 4 TUDO OK: os lens sao iguais')
        else:
            print('Item 4 ATENÇÃO: os lens sao diferentes')
            break

        head = package[:10]
        eop = package[-4:]
        payload = package[10:-4]

        ## ENVIO DO PACOTE
        # sending head and eop
        head_eop = head + eop

        sends_list = [head_eop,package]
        n = 1
        for item in sends_list:
            print('----------ENVIANDO---------')
            com1.sendData(item)
            create_log('c','e',transm_num,msg_type_sent,len_package, package_number, total_packages)
            if item == package:
                print(f"Package número {package_number} enviado com tamanho {len(item)}")
                print('---PAYLOAD---')
                print(item[10:-4])
            elif item == head_eop:
                print(f"Head e eop número {package_number} enviado com tamanho {len(item)}")
            print("Aguardando resposta")

            ## RECEBIMENTO DA RESPOSTA
            try_connection = True
            i = 1 # 4 vezes para dar 20 segundos no timer
            while try_connection:
                print('--------RECEBENDO-----------')
                getdata_len = 15
                resposta, len_resposta = com1.getDataHandshake(getdata_len) # loop
                print(f'A resposta foi recebida: \n{resposta}')

                # SEM RESPOSTA
                if resposta == zero_em_bytes and i<=4:
                    try_again = input("Servidor inativo. Tentar novamente? S/N ")

                    if try_again == "S" or try_again == "s":
                        com1.sendData(item)
                        create_log('c','e',transm_num,msg_type_sent,len_package, package_number, total_packages)
                        print(f"head e eop número {package_number} reenviados com tamanho {len(head_eop)}")
                        try_connection = True
                        i+=1
                    elif try_again == 'N' or try_again == 'n':
                        print('a conexão não foi estabelecida')
                        try_connection = False
                        return zero_em_bytes
                    else:
                        print('a mensagem digitada não é uma opção\nfinalizando operação')
                        try_connection = False
                        return zero_em_bytes

                # COM RESPOSTA
                else:
                    # msg_type = int.from_bytes(resposta[0],'big') # h0
                    msg_type = resposta[0]
                    create_log('c','r',transm_num,msg_type,getdata_len, package_number, total_packages)
                    
                    if msg_type == 6:
                        # consertar o erro - como? kk
                        com1.sendData(item)
                        create_log('c','e',transm_num,msg_type_sent,len_package, package_number, total_packages)
                        print(f"head e eop número {package_number} reenviados com tamanho {len(head_eop)}")
                        try_connection = True
                    elif msg_type == 4:
                        try_connection = False
                        print(f'!!!O valor de N é {n}')
                        if n==2:
                            package_number+=1
                            m+=1
                        n+=1
                    else:
                        print('O tipo de resposta não está correto (não foi 4 nem 6)')
                        return zero_em_bytes

# testar depois
def create_resp_package(msg_type):
    # criando pacote de resposta do tipo 4
    head_resp, len_head_resp_ok = create_head(msg_type,0,1,1,1,1)
    id_string = (f'10{msg_type}')
    id_int = str(id_string)
    payload_resp = (id_int).to_bytes(1,'big')
    package_resp, len_package_resp_ok = create_package(head_resp,payload_resp)
    return package_resp

def receive_package(com2,transm_num):
    print('entrei na receive_package')
    # criando pacote de resposta do tipo 4
    type_num_ok = 4
    head_resp_ok, len_head_resp_ok = create_head(type_num_ok,0,1,1,1,1)
    payload_resp_ok = (104).to_bytes(1,'big')
    package_resp_ok, len_package_resp_ok = create_package(head_resp_ok,payload_resp_ok)

    # criando pacote de resposta do tipo 6
    type_num_nao_ok = 6
    head_resp_nao_ok, len_head_resp__nao_ok = create_head(type_num_nao_ok,0,1,1,1,1)
    payload_resp_nao_ok = (106).to_bytes(1,'big')
    package_resp_nao_ok, len_package_resp_nao_ok = create_package(head_resp_nao_ok,payload_resp_nao_ok)

    # criando pacote de resposta do tipo 5
    type_num_timeout = 5
    head_resp_timeout, len_head_resp_timeout = create_head(type_num_timeout,0,1,1,1,1)
    payload_resp_timeout = (105).to_bytes(1,'big')
    package_resp_timeout, len_package_resp_timeout = create_package(head_resp_timeout,payload_resp_timeout)

    # inicializando a soma de bytes - que vai ser a imagem
    image_payloads = bytearray()

    # inicialização
    number_package = 0
    package_total = 1

    # TESTE ITEM 3
    num_package = number_package - 1
    while number_package < package_total:
        # for item in items_list:
        # items list teria que ser um dicionario (o que enviar e quanto receber)
        try_connection = True
        i = 1

        while try_connection:
            print('entrei no try_connection')
            print('---------RECEBENDO-----------')
            getdata_len = 14
            head_eop, nhead_eop = com2.getDataHandshake(14)
            print('sai do getdatahandshake')

            # SEM RESPOSTA
            if head_eop == zero_em_bytes and i<=4:
                try_again = input("Servidor inativo. Tentar novamente? S/N ")

                if try_again == "S" or try_again == "s":
                    try_connection = True
                    i+=1
                elif try_again == 'N' or try_again == 'n':
                    print('a conexão não foi estabelecida')
                    try_connection = False
                    image_payloads = zero_em_bytes
                    return image_payloads
                else:
                    print('a mensagem digitada não é uma opção\nfinalizando operação')
                    try_connection = False
                    image_payloads = zero_em_bytes
                    return image_payloads
                    
            elif i>4:
                com2.sendData(package_resp_timeout)
                image_payloads = zero_em_bytes
                create_log('s','e',transm_num,type_num_timeout,getdata_len, 1, 1)
                return image_payloads

            # COM RESPOSTA
            elif head_eop != zero_em_bytes:
                # msg_type = int.from_bytes(head_eop[0],'big') # h0
                msg_type = head_eop[0]
                # package total começa com 1 para entrar no while
                create_log('s','r',transm_num,msg_type,getdata_len, number_package, package_total)
                print(f"Head e eop número {number_package} recebido com tamanho {len(head_eop)}")
                print(f'o tipo da mensagem é {msg_type}')

                if msg_type == 3:
                    time.sleep(1)
                    print(f'head e eop recebidos: {head_eop}')
                    #package_len = int.from_bytes(head_eop[5],'big')
                    payload_len = head_eop[5]
                    print(f'esperando {payload_len} bytes')

                    ## conferir se o package está ok
                    # teste
                    ok = True
                    if ok:
                        print('head e eop estão ok')
                        print('----------ENVIANDO-----------')
                        com2.sendData(package_resp_ok)
                        create_log('s','e',transm_num,type_num_ok,getdata_len, 1, package_total)
                        try_connection = False
                    else:
                        print('head e eop não estão ok')
                        print('---------ENVIANDO------------')
                        com2.sendData(package_resp_nao_ok)
                        create_log('s','e',transm_num,type_num_nao_ok,getdata_len, 1, 1)
                        try_connection = False
                        image_payloads = zero_em_bytes
                        return image_payloads
                else:
                    print('o tipo da mensagem recebida é diferente de 3')

            else:
                print('a resposta e o i estao funcionando mal')

        try_connection = True
        i = 1
        while try_connection:
            payload_len = head_eop[5]
            package_len = payload_len + 14
            print(f'---------RECEBENDO {package_len} bytes-------------')
            package, npackage = com2.getDataHandshake(package_len)
            
            # SEM RESPOSTA
            if package == zero_em_bytes and i<=4:
                try_again = input("Servidor inativo. Tentar novamente? S/N ")

                if try_again == "S" or try_again == "s":
                    try_connection = True
                    i+=1
                elif try_again == 'N' or try_again == 'n':
                    print('a conexão não foi estabelecida')
                    try_connection = False
                    return image_payloads
                else:
                    print('a mensagem digitada não é uma opção\nfinalizando operação')
                    try_connection = False
                    return image_payloads

            elif i>4:
                com2.sendData(package_resp_timeout)
                image_payloads = zero_em_bytes
                create_log('s','e',transm_num,type_num_timeout,getdata_len, 1, 1)
                return image_payloads

            # COM RESPOSTA
            elif package != zero_em_bytes:
                print('tive resposta')
                print(f"Package número {number_package} recebido com tamanho {npackage}")
                #msg_type = int.from_bytes(package[0],'big') # h0
                head = package[:10]
                eop = package[-4:]
                payload = package[10:-4]
                print(f'tamanho do payload = {len(payload)}')
                print(f'!!!!payload recebido = {payload}')
                image_payloads.extend(payload)

                msg_type = package[0]
                print(f'o tipo da mensagem é {msg_type}')
                create_log('s','r',transm_num,msg_type,package_len, number_package, package_total)

                num_package = number_package
                
                print(f' O número de checagem do pacote é {num_package}')
                # number_package = int.from_bytes(package[0:2],'big')
                # package_total =  int.from_bytes(package[2:4],'big')
                number_package = package[4]
                package_total = package[3]
                print(f'---Pacote {number_package} / {package_total}---')
                
                if msg_type == 3:
                    time.sleep(1)
                    print(f'---Enviando resposta número {number_package}---')
                    ## conferir se o package está ok
                    # teste
                    ok = True
                    if ok:
                        print('msg está ok')
                        print('----------ENVIANDO-----------')
                        com2.sendData(package_resp_ok)
                        create_log('s','e',transm_num,type_num_ok,len_package_resp_ok, 1, 1)
                        try_connection = False
                        package_len
                    else:
                        print('msg não está ok')
                        print('----------ENVIANDO-------------')
                        com2.sendData(package_resp_nao_ok)
                        create_log('s','e',transm_num,type_num_nao_ok,len_package_resp_nao_ok, 1, 1)
                        try_connection = False
                        break
                else:
                    print('o tipo da mensagem recebida é diferente de 3')

            else:
                print('a resposta e o i estao funcionando mal')

        # teste item 3
        if number_package == num_package + 1:
            print('Item 3 TUDO OK: a ordem está correta')
            # com2.sendData(package_resp_ok)
        else:
            print('Item 3 ATENÇÃO: a ordem dos pacotes está incorreta')
            # com2.sendData(package_resp_nao_ok)
            # break

    return image_payloads