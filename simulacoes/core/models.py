from django.db import models

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
        return self.descricao;

    class Meta:
        verbose_name = 'Acelerômetro'
        verbose_name_plural = 'Acelerômetros'


# Criar a classe responsável pelo arquivo.