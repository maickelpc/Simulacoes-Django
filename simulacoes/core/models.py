from django.db import models
from datetime import datetime
from datetime import timedelta
from django.db.models import StdDev, Avg, Variance
from scipy.stats import kurtosis
import numpy as np
from django.db import transaction
import threading
import time


# Create your models here.

class Acelerometro(models.Model):
    id = models.AutoField(primary_key=True)
    codigo = models.CharField(max_length=100, unique=True, verbose_name='Code')
    descricao = models.CharField(max_length=100, verbose_name='Description')
    localizacao = models.CharField(max_length=100,verbose_name='Location')

    eixoX = models.BooleanField(verbose_name='Axis X')
    eixoY = models.BooleanField(verbose_name='Axis Y')
    eixoZ = models.BooleanField(verbose_name='Axis Z')


    def __str__(self):
        return self.codigo + ' - ' + self.descricao

    class Meta:
        verbose_name = 'Accelerometer'
        verbose_name_plural = 'Accelerometers'

class Arquivo(models.Model):
    TIPOS_ARQUIVO = (
        ('UEME', 'UEME'),
        ('OTHER', 'OTHER'),
    )

    def file_directory_path(instance, filename):
        # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
        return 'arquivos/{0}/{1}'.format(instance.acelerometro.id, datetime.now().strftime("%Y_%m_%d_%H_%M_%S")+'.'+filename.__str__()[-3:])

    id = models.AutoField(primary_key=True)
    codigo = models.CharField(max_length=100,unique=True,verbose_name='Code')
    documento = models.FileField(upload_to=file_directory_path, verbose_name='File')
    acelerometro = models.ForeignKey(Acelerometro, on_delete=models.PROTECT, related_name='acelerometro_arquivo', verbose_name='Accelerometer')
    canais = models.IntegerField(verbose_name='Channels')
    dataLeitura = models.DateTimeField(verbose_name='Date / time of initial reading')
    frequencia = models.IntegerField(verbose_name='Frequency in Hz')
    tipo = models.CharField( max_length=10, choices=TIPOS_ARQUIVO,  default='OTHER',)
    estatisticas = models.BooleanField(default=False, verbose_name='Statistics')
    estatistica_observacoes = models.TextField(blank=True, null=True, verbose_name='Comments on the statistics')


    dataUpload = models.DateTimeField(auto_now_add = True, verbose_name='Upload Date')

    def __str__(self):
        return self.codigo

    def save(self, calcula=True , *args, **kwargs):
        novo = (self.id == None);
        super().save(*args, **kwargs)  # Call the "real" save() method.
        id = str(self.id)
        if calcula and not self.estatisticas and self.tipo == 'UEME':
            thread = threading.Thread(target=calculaMetodosEstatisticosUEME, args=(id))
            thread.start()

    def trata_conteudo_documento(self):
        documento = self.documento
        domain = 3
        if self.tipo == 'UEME':
            file_content_by_domain = []
            time = []
            file = documento.readlines()
            for i in range(0,domain):
                file_content_by_domain.append('')
                file_content_by_domain[i] = []   
            for line in file:
                elements = line.split()
                time.append(elements[0])
                file_content_by_domain[0].append(elements[1])
                file_content_by_domain[0].append(elements[2])
                file_content_by_domain[0].append(elements[3])
                file_content_by_domain[1].append(elements[4])
                file_content_by_domain[1].append(elements[5])
                file_content_by_domain[1].append(elements[6])
                file_content_by_domain[2].append(elements[7])
                file_content_by_domain[2].append(elements[8])
                file_content_by_domain[2].append(elements[9])
            return list(file_content_by_domain)
        else:
            arquivo = documento.readlines()
            plot_list = []
            item = []
            for linha in arquivo:
                linha = str(linha)
                linha = linha.replace("'","")
                linha = linha.replace("b","")
                linha = linha.replace("\\n","")
                linha = linha.replace("\\r","")
                valores = linha.split(',')
                for valor in valores:
                    item.append(valor)
                aux = item.copy()
                plot_list.append(aux)
                item.clear()
            return plot_list

    def plot_dados_brutos(self):
        print(self.documento[10])

    class Meta:
        verbose_name = "File"
        verbose_name_plural = 'Files'

class GraphResults(models.Model):
    archiev = models.ForeignKey(Arquivo, on_delete = models.PROTECT)
    fourier_size = models.IntegerField()
    channels = models.IntegerField()
    channels_analysis = models.IntegerField()
    graph = models.ImageField(upload_to = "graph_images/", blank = False)

    def __str__(self):
        return "graph results"

class ArquivoEstatisticas(models.Model):
    id = models.AutoField(primary_key=True)
    arquivo = models.ForeignKey(Arquivo, on_delete=models.CASCADE, related_name='arquivo_estatistica', verbose_name="File")
    canal = models.SmallIntegerField(default=1, verbose_name='Channel')

    media = models.FloatField(blank=True, null=True, verbose_name="Average")
    desvio = models.FloatField(blank=True, null=True, verbose_name="Standard deviation")
    variancia = models.FloatField(blank=True, null=True, verbose_name="variance")
    curtoses = models.FloatField(blank=True, null=True, verbose_name="Kurtosis")

def calculaMetodosEstatisticosUEME(*args, **kwargs):
    print("#################################################################################")
    print("####################### INICIANDO CALCULOS DO ARQUIVO ###########################")
    print("#################################################################################")
    
    s = ""
    for c in args:
        s += c
    
    id = int(s)
    print(id)
 
    inicio = datetime.now()
    arquivo = Arquivo.objects.filter(pk=id).get()
    arquivo.estatistica_observacoes += '\nStarting method of statistical calculations in:' + inicio.strftime("%d/%m/%Y, %H:%M:%S")
    arquivo.estatisticas = True;
    arquivo.save(False)
    try:
        with transaction.atomic():
            fileUpload = arquivo.documento
            ArquivoEstatisticas.objects.filter(arquivo=arquivo).delete()
            arrayParaEstatisticas = []
            for i in range(arquivo.canais):
                canal = []
                arrayParaEstatisticas.append(canal)

            for linha in fileUpload:
                aux = str(linha)
                aux = aux.rstrip().lstrip()
                aux = aux.replace("b'", "")
                aux = aux.replace("\\r\\n'", "")
                dados = aux.split("\\t")
                dados.pop()
                canal = 1;

                for n in dados:
                    valor = float(n)
                    arrayParaEstatisticas[canal-1].append(valor)
                    canal += 1

                    if (canal > arquivo.canais):
                        canal = 1


            ## Estatísticas

            # media = LeituraUEME.objects.filter(arquivo=arquivo).aggregate(valor=Avg('aceleracao'))
            # desvioPadrao = LeituraUEME.objects.filter(arquivo=arquivo).aggregate(valor=StdDev('aceleracao'))
            # variancia = LeituraUEME.objects.filter(arquivo=arquivo).aggregate(valor=Variance('aceleracao'))

            for i in range(arquivo.canais):
                estatisticas = ArquivoEstatisticas()
                estatisticas.arquivo = arquivo
                estatisticas.canal = i+1

                estatisticas.media = np.average(arrayParaEstatisticas[i])
                estatisticas.desvio = np.std(arrayParaEstatisticas[i])
                estatisticas.variancia = np.var(arrayParaEstatisticas[i])
                estatisticas.curtoses = kurtosis(arrayParaEstatisticas[i])
                estatisticas.save()


            final = datetime.now()
            arquivo.estatisticas = True
            arquivo.estatistica_observacoes += '\nSuccess: method of statistical calculations completed in:' + final.strftime("%d/%m/%Y, %H:%M:%S")

            arquivo.save()
            print("Finalizou")


    except:
        final = datetime.now()
        print("Erro: Não foi possivel concluir a leitura dos dados")
        arquivo.estatistica_observacoes += '\nError in statistical calculations. Finished in:' + final.strftime("%d/%m/%Y, %H:%M:%S")
        arquivo.estatisticas = False
        arquivo.save(False)
