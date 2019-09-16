from django.shortcuts import render
from django.views.generic import ListView
from django.http import HttpResponse
from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404, render
import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib import pylab
from pylab import *
import io
from .models import *

class Basic(TemplateView):

    def home(request):
        return render(request,"principal.html")

    def teste(request):
        return render(request,'teste.html')

class Arquivos(TemplateView):
    arquivos = Arquivo.objects.all()

    def listar_arquivos(request):
        arquivos = Arquivo.objects.all()
        return render(request,"base.html",{'arq':arquivos})

    def plot_dados(request):
        arquivo = Arquivo.objects.get(pk=1)
        print(arquivo)
        print(type(arquivo))
        return render(request,"arquivos_list.html",{'arq':arquivo.documento})

    def plotar_dados_brutos(request,pk):
        arquivo = Arquivo.objects.get(pk = pk)
        nome = arquivo.codigo
        arquivo = arquivo.documento.readlines()
        plot_list = []
        item = []
        for linha in arquivo:
            linha = str(linha)
            linha = linha.replace("'","")
            linha = linha.replace("b","")
            linha = linha.replace("\n","")
            linha = linha.replace("\r","")
            valores = linha.split(',')
            for valor in valores:
                item.append(valor)
            aux = item.copy()
            plot_list.append(aux)
            item.clear()
        return render(request,"base.html",{'plot_list':plot_list,'codigo':nome})

class Grafico(TemplateView):
    def montar_grafico(request,pk):
        arquivo = Arquivo.objects.get(pk=pk)
        fourier_transform_size = 2048
        canais = arquivo.canais
        analise_canais = 50
        documento = arquivo.documento
        dados_grafico = {'fourier_size':fourier_transform_size,'canais':canais,'analise_canais':analise_canais,'arquivo':documento,'id':pk}
        return render(request,"base.html",dados_grafico)
        

class FDD():
    def power_spectral_density(degrees, fourier_transform_size, stream_file, delta):
        print(" power_spectral_density operante...")
        cross_spectral_density = np.zeros((degrees, degrees, int((fourier_transform_size / 2) + 1)),
                                          dtype=complex)  # Store the data 01 by means of a three-dimensional matrix 5 * 5 * 1025
        frequency = np.zeros((degrees, degrees, int((fourier_transform_size / 2) + 1)),
                             dtype=complex)  # build the matrix...
        n = stream_file.shape  # dimensions of stream file lines x columns
        stream_file = stream_file[1:]
        if n[0] > n[1]:
            acceleration = stream_file  # acceleration receives the data from the read file
        else:
            acceleration = np.transpose(
                stream_file)  # acceleration receives the data from the reading file in a transposed way
        for i in range(0, degrees):  #
            for j in range(0, degrees):  #
                print('laço', i, j, 'degrees', degrees)
                print(acceleration[:, i].shape)
                cross_spectral_density[:][i, j], frequency[:][i, j] = mlab.csd(
                    # applying welch in matrix padding: cross spectral density and frequency
                    acceleration[:, i],
                    acceleration[:, j],
                    NFFT=fourier_transform_size,
                    Fs=delta,
                    detrend=mlab.detrend_none,
                    window=np.hanning(fourier_transform_size),
                    noverlap=(int(fourier_transform_size / 2)),
                    pad_to=None,
                    sides='default',
                    scale_by_freq=True
                )
        return cross_spectral_density, frequency

    def spectral_value_decomposition(degrees, fourier_transform_size, cross_spectral_density):
        print(" spectral_value_decomposition operante")
        # Determines the frequencies in relation to the singular values of the matrix SPECTRAL DENSITY OF POWER
        eigen_values = np.zeros((int((fourier_transform_size / 2) + 1), degrees), dtype=complex)  # build a new matrix
        size = int((fourier_transform_size / 2) + 1)  # loop parameter
        for i in range(0, size):
            U, s, V = np.linalg.svd(cross_spectral_density[:, :, i], full_matrices=True, compute_uv=True)  # applies SVD
            eigen_values[i] = s  #
            eigen_vectors = U[:, 0]  #
        return eigen_values, eigen_vectors

    def system_frequency(degrees, fourier_transform_size, stream_file, delta):
        print("system_frequency operante")
        cross_spectral_density, frequency = FDD.power_spectral_density(degrees, fourier_transform_size, stream_file,delta)  # call power spectral density power function flame
        eigen_values, eigen_vectors = FDD.spectral_value_decomposition(degrees, fourier_transform_size, cross_spectral_density)  # call spectral value decomposition function
        return frequency, eigen_values

    def frequency_position(frequency_peaks, degrees, fourier_transform_size, stream_file, delta):
        print("frequency_position operante")
        cross_spectral_density, frequency = power_spectral_density(degrees, fourier_transform_size, stream_file,
                                                                   delta)  # call power spectral density power function flame
        frequency_positions = np.zeros((1, len(peaks)))  # creates a matrix based on peaks
        len_peak = len(peaks)  # was NP
        size = int((fourier_transform_size / 2) + 1)  # loop parameter
        for i in range(0, len_peak):
            cont = 0
        for k in range(0, size):
            if (frequency[1, 1, k] >= frequency_peaks[i]):
                frequency_positions[0, i] = cont
            else:
                cont = cont + 1
        return frequency_positions

    def vibration_mode_shapes(degrees, fourier_transform_size, stream_file, delta, position):
        print("vibration_mode_shapes operante")
        cross_spectral_density, frequency = power_spectral_density(degrees, fourier_transform_size, stream_file, delta)
        con = 0
        print(len(str(position[:][:])))
        phi = np.zeros((len(str(position[:][:])), degrees, 1))
        for i in range(0, len(position[0])):
            con = con + 1
            U, S, V = np.linalg.svd(cross_spectral_density[:, :, int(position[0][i])], full_matrices=False,
                                    compute_uv=True)
            phi[i][:, 0] = U[:, 0]
        return phi
