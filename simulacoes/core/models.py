from django.db import models
from datetime import datetime

# Create your models here.
class Acelerometro(models.Model):
    id = models.AutoField(primary_key=True)
    codigo = models.CharField(max_length=100, unique=True, verbose_name='Código')
    descricao = models.CharField(max_length=100, verbose_name='Descrição')
    localizacao = models.CharField(max_length=100,verbose_name='Localização')

    eixoX = models.BooleanField(verbose_name='Eixo X')
    eixoY = models.BooleanField(verbose_name='Eixo Y')
    eixoZ = models.BooleanField(verbose_name='Eixo Z')


    def __str__(self):
        return self.codigo + ' - ' + self.descricao;

    class Meta:
        verbose_name = 'Acelerômetro'
        verbose_name_plural = 'Acelerômetros'

class Arquivo(models.Model):
    def file_directory_path(instance, filename):
        # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
        return 'arquivos/{0}/{1}'.format(instance.acelerometro.id, datetime.now().strftime("%Y_%m_%d_%H_%M_%S")+'.'+filename.__str__()[-3:])


    id = models.AutoField(primary_key=True)
    codigo = models.CharField(max_length=100,unique=True,verbose_name='Código')
    documento = models.FileField(upload_to=file_directory_path, verbose_name='Arquivo')
    acelerometro = models.ForeignKey(Acelerometro, on_delete=models.PROTECT, related_name='acelerometro_arquivo', verbose_name='Acelerômetro')
    canais = models.IntegerField(verbose_name='Canais')
    dataLeitura = models.DateTimeField(verbose_name='Data/hora da leitura inicial')
    frequencia = models.IntegerField(verbose_name='Frequência em Hz')
    dataUpload = models.DateTimeField(auto_now = True, verbose_name='Data de Upload')



    def __str(self):
        return self.codigo




    class Meta:
        verbose_name = "Arquivo"
        verbose_name_plural = 'Arquivos'



# Criar a classe responsável pelo arquivo.