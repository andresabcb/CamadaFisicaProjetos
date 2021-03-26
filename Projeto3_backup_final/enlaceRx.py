#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#####################################################
# Camada Física da Computação
#Carareto
#17/02/2018
#  Camada de Enlace
####################################################

# Importa pacote de tempo
import time

# Threads
# só estaremos usando essa biblioteca quando for
# threading.Algumafuncao()
import threading

# Class
class RX(object):
    
    # inicialização
    def __init__(self, fisica):
        self.fisica      = fisica
        self.buffer      = bytes(bytearray())
        self.threadStop  = False
        self.threadMutex = True
        self.READLEN     = 1024

    def thread(self): 
        while not self.threadStop:
            if(self.threadMutex == True):
                rxTemp, nRx = self.fisica.read(self.READLEN)
                if (nRx > 0):
                    self.buffer += rxTemp  
                time.sleep(0.01)

    def threadStart(self):
        self.thread = threading.Thread(target=self.thread, args=())
        self.thread.start()

    def threadKill(self):
        self.threadStop = True

    def threadPause(self):
        self.threadMutex = False

    def threadResume(self):
        self.threadMutex = True

    def getIsEmpty(self):
        if(self.getBufferLen() == 0):
            return(True)
        else:
            return(False)

    def getBufferLen(self):
        return(len(self.buffer))

    def getAllBuffer(self, len):
        self.threadPause()
        b = self.buffer[:]
        self.clearBuffer()
        self.threadResume()
        return(b)

    def getBuffer(self, nData):
        self.threadPause()
        b           = self.buffer[0:nData]
        self.buffer = self.buffer[nData:]
        self.threadResume()
        return(b)

    def getNData(self, size):
        print('entrou no getNData')
        while(self.getBufferLen() < size):
            print(f'Tamanho do RxBuffer {self.getBufferLen()}')
            time.sleep(0.2)                 
        return(self.getBuffer(size))

    def getNDataHandshake(self, size):
        print('entrou no getNDataHandshake')
        # para o handshake:
        wait = 5 # seconds
        t_handshake_start1 = time.time()
        t_handshake_stop = (t_handshake_start1 + 5) #fixo
        print(t_handshake_stop)
        print(t_handshake_start1)
    
        # procura receber algo com o mesmo número de bytes
        while(self.getBufferLen() < size) and time.time() <= t_handshake_stop:
            time.sleep(0.2)
            print(f'O delta t no getNData é de {time.time() - t_handshake_stop}')
            print(f'Tamanho do RxBuffer {self.getBufferLen()}')

        if self.getBufferLen() >= size:
            return(self.getBuffer(size))
        else:
            return (0).to_bytes(1,byteorder='big')

    def clearBuffer(self):
        self.buffer = b""
