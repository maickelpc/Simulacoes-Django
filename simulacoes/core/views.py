from django.views.generic import ListView
from django.http import HttpResponse,FileResponse
from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404, render
from django.core.paginator import Paginator
import datetime
import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib import pylab
from pylab import *
import io
from .models import *
from .forms import *
import time
from reportlab.pdfgen import canvas
import csv
#from matplotlib.backends.backend_agg import FigureCanvasAgg
import urllib, base64

class Arquivos(TemplateView):
    arquivos = Arquivo.objects.all()

    def listar_arquivos(request):
        arquivos = Arquivo.objects.all()
        return render(request,"archievList.html",{'arq':arquivos})

    def plotar_dados_brutos(request,pk):
        arquivo = Arquivo.objects.get(pk = pk)
        nome = arquivo.codigo
        try:
            if arquivo.tipo == 'UEME':
                full_plot_list = arquivo.trata_conteudo_documento()
                paginator = Paginator(full_plot_list,100)
                page = request.GET.get('page')
                plot_list = paginator.get_page(page)
                return render(request,"base.html",{'plot_list':plot_list,'codigo':nome,'tipo':'UEME'})
            else:
                full_plot_list = arquivo.trata_conteudo_documento()
                paginator = Paginator(full_plot_list,100)
                page = request.GET.get('page')
                plot_list = paginator.get_page(page)
                return render(request,"base.html",{'plot_list':plot_list,'codigo':nome,'tipo':'COMPOSTO'})
        except: 
            return render(request,"plot.html",{'message':"Erro ao ler dados do arquivo, verifique se o formato é válido",'codigo':nome,'id':pk})

class Grafico(TemplateView):
    

    def graph_relatory_csv(request,time,channels,channels_analysis,code,fourier_size,status):
        # Create the HttpResponse object with the appropriate CSV header.
        x = datetime.now().strftime("%x %X")
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="%s.csv"'%x

        writer = csv.writer(response)
        writer.writerow(['Report: %s'%x])
        writer.writerow(['Fourier Transform size: %s'%fourier_size])
        writer.writerow(['Channels: %s'%channels])
        writer.writerow(['Channels Analysis: %s'%channels_analysis])
        writer.writerow(['Used Archiev: %s'%code])
        writer.writerow(['Total Process Time: %s'%time])
        writer.writerow(['Save Status: %s'%status])
        return response

    def graph_relatory(request,time,channels,channels_analysis,code,fourier_size,status):
        try:
            # Create a file-like buffer to receive PDF data.
            buffer = io.BytesIO()
            # Create the PDF object, using the buffer as its "file."
            p = canvas.Canvas(buffer)
            # Draw things on the PDF. Here's where the PDF generation happens.
            # See the ReportLab documentation for the full list of functionality.
            
            x = datetime.now().strftime("%x %X")
            p.drawString(200,800,"Report")
            p.drawString(300,800,"%s" %x)
            p.drawString(20,750,"Fourier Transform size: %s" %fourier_size)
            p.drawString(20,735,"Channels: %s" %channels)
            p.drawString(20,720,"Channels Analysis: %s" %channels_analysis)
            p.drawString(20,705,"Used Archiev: %s" %code)
            p.drawString(20,690,"Total Process Time: %s Seconds" %time)
            p.drawString(20,675,"Save Status: %s" %status)
            # Close the PDF object cleanly, and we're done.
            p.showPage()
            p.save()
            # FileResponse sets the Content-Disposition header so that browsers
            # present the option to save the file.
            buffer.seek(0)
            return FileResponse(buffer, as_attachment=True, filename='report.pdf')
        except:
            return HttpResponse("Error at write the pdf report document...")

    def montar_grafico(request,pk):
        arquivo = Arquivo.objects.get(pk = pk)
        form = GraficoForm()
        form.canais = arquivo.canais
        plot_list = arquivo.trata_conteudo_documento()
        size_channels = []
        for i in range(0,arquivo.canais):
            size_channels.append(i)
        context = {
            'id' : pk,
            'form' : form,
            'size_channels' : size_channels,
        }
        return render(request,"form.html",context)

    def plotar_grafico(request):
        if request.method == 'POST':
            
            start_time = time.time() # start time
            form = GraficoForm(request.POST)
            canais,analise_canais,fourier_size,id = int(request.POST['canais']), int(request.POST['analise_canais']),int(request.POST['fourier_size']),request.POST['id']
            channels = request.POST.getlist('channel') # importante detalhe!!!
            x ="media/graph_images/"+ datetime.now().strftime("%Y_%m_%d_%Hh_%Mm_%Ss") + ".png"
            dic = {'channels':canais,'channels_analysis':analise_canais,'fourier_size':fourier_size,'id':id,'name': x}
            arquivo = get_object_or_404(Arquivo, pk = id)
            if arquivo.tipo == "UEME":
                try:
                    arq = arquivo.trata_conteudo_documento()
                    arq = np.array(arq,dtype='float64')
                    print(arq)
                    print('\n',len(arq),'\n')
                except:
                    return render(request,"archievList.html",{'form':form,'message':'O documento selecionado não pode ser processado...','id':id})
            else:
                arq = arquivo.trata_conteudo_documento()
                arq_filtered = []
                size = len(channels)
                for index in channels:
                    index = int(index)
                    arq_filtered.append(arq[index])
                arq = np.array(arq_filtered,dtype='float64')
                canais = size
                #arq = genfromtxt(arquivo.documento, delimiter=",")# Padrão, este refere-se ao original; deve ser mantido em caso de falha
            frequency, eigen_values = Grafico.system_frequency(canais, fourier_size, arq, analise_canais)
            fig = plt.figure(figsize=(20, 10), dpi=100)
            ax = fig.add_subplot(111)
            ax.cla()
            ax.grid(True)
            for i in range(0, canais):
                ax.semilogy(frequency[i, i, :], eigen_values[:, i])  # 5 points tolerance
            ax.legend(loc='center', bbox_to_anchor=(0.8, 0.5))
            fig = plt.gcf()
            # armazenar imagem do plot em Bytes
            buf = io.BytesIO()
            fig.savefig(buf, format='png')
            buf.seek(0)
            string = base64.b64encode(buf.read())       
            uri = 'data:image/png;base64,' + urllib.parse.quote(string)
            html = '<img src = "%s"/>' % uri
            end_time = time.time() # end time
            total_decorrido = str(round((start_time - end_time),2))
            total_decorrido = total_decorrido.replace('-','')
            try:
                plt.savefig(x,format='png')
            except: 
                save_status = "unsaved chart datas, error at save graph image..."
                return render(request,"form.html",{'form':form,'time':total_decorrido,'id':id,'response':html,'uri':uri,'save_status':save_status})
            save_status = Grafico.save_graph_data(dic)
            return render(request,"response.html",{'form':form,'time':total_decorrido,'id':id,'response':html,'uri':uri,'save_status':save_status})
        else:
            form = GraficoForm
            return render(request,"form.html",{'form':form,'message':'Error in process'})

    def save_graph_data(dic):
        try:
            object = GraphResults(archiev=Arquivo.objects.get(pk = dic['id']), channels=dic['channels'], channels_analysis=dic['channels_analysis'], fourier_size=dic['fourier_size'],graph=dic['name'])
            object.save()
            return 'chart data successfully saved'
        except:
            return 'unsaved chart datas'
        
    def power_spectral_density(degrees, fourier_transform_size, stream_file, delta):
        print(" power_spectral_density operante...")
        cross_spectral_density = np.zeros((degrees, degrees, int((fourier_transform_size / 2) + 1)),dtype=complex)  # Store the data 01 by means of a three-dimensional matrix 5 * 5 * 1025
        frequency = np.zeros((degrees, degrees, int((fourier_transform_size / 2) + 1)),dtype=complex)  # build the matrix...
        try:
            n = stream_file.shape  # dimensions of stream file lines x columns
            if n[0] > n[1]:
                acceleration = stream_file  # acceleration receives the data from the read file
            else:
                acceleration = np.transpose(stream_file)  # acceleration receives the data from the reading file in a transposed way
        except:
            n = (len(stream_file),len(stream_file[0]))  # dimensions of stream file lines x columns
            if n[0] > n[1]:
                acceleration = stream_file  # acceleration receives the data from the read file
            else:
                acceleration = np.transpose(stream_file)  # acceleration receives the data from the reading file in a transposed way
        for i in range(0, degrees):  #
            for j in range(0, degrees):  #
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
        cross_spectral_density, frequency = Grafico.power_spectral_density(degrees, fourier_transform_size, stream_file,delta)  # call power spectral density power function flame
        eigen_values, eigen_vectors = Grafico.spectral_value_decomposition(degrees, fourier_transform_size, cross_spectral_density)  # call spectral value decomposition function
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
