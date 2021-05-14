
import numpy as np
import sounddevice as sd
import matplotlib.pyplot as plt
from scipy.fftpack import fft
from scipy import signal as window

class signalMeu:
    def __init__(self):
        self.init = 0

    # def __init__(self):
    #     self.init = 0

    # O tamanho da lista tempo estará associado à duração do som. 
    # A intensidade é controlada pela constante A (amplitude da senoide). 
    # Seja razoável.
    def generateSin(self, freq, amplitude, time, fs):
        # Senóide genérica: A*sin(2*pi*f*t)
        n = time*fs
        x = np.linspace(0.0, time, n)
        s = amplitude*np.sin(freq*x*2*np.pi)
        return (x, s)

    def calcFFT(self, signal, fs):
        # https://docs.scipy.org/doc/scipy/reference/tutorial/fftpack.html
        N  = len(signal)
        print(f"N vale {N}")
        W = window.windows.hamming(N)
        print(f"W vale {W}")
        T  = 1/fs
        print(f"T vale {T}")
        xf = np.linspace(0.0, 1.0/(2.0*T), N//2)
        print(f"xf vale {xf}")
        yf = fft(signal*W)
        print(f"yf vale {yf}")
        return(xf, np.abs(yf[0:N//2]))

    def plotFFT(self, signal, fs, title): # adicionei o title
        x,y = self.calcFFT(signal, fs)
        plt.figure()
        plt.plot(x, np.abs(y))
        plt.title(f'Fourier {title}')
        plt.show() # tirar se não for legal
