# Generated by Django 2.2.5 on 2019-09-17 16:36

import core.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Acelerometro',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('codigo', models.CharField(max_length=100, unique=True, verbose_name='Código')),
                ('descricao', models.CharField(max_length=100, verbose_name='Descrição')),
                ('localizacao', models.CharField(max_length=100, verbose_name='Localização')),
                ('eixoX', models.BooleanField(verbose_name='Eixo X')),
                ('eixoY', models.BooleanField(verbose_name='Eixo Y')),
                ('eixoZ', models.BooleanField(verbose_name='Eixo Z')),
            ],
            options={
                'verbose_name': 'Acelerômetro',
                'verbose_name_plural': 'Acelerômetros',
            },
        ),
        migrations.CreateModel(
            name='Arquivo',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('codigo', models.CharField(max_length=100, unique=True, verbose_name='Código')),
                ('documento', models.FileField(upload_to=core.models.Arquivo.file_directory_path, verbose_name='Arquivo')),
                ('canais', models.IntegerField(verbose_name='Canais')),
                ('dataLeitura', models.DateTimeField(verbose_name='Data/hora da leitura inicial')),
                ('frequencia', models.IntegerField(verbose_name='Frequência em Hz')),
                ('tipo', models.CharField(choices=[('UEME', 'UEME'), ('OUTRO', 'OUTRO')], default='OUTRO', max_length=10)),
                ('estatisticas', models.BooleanField(default=False)),
                ('estatistica_observacoes', models.TextField(blank=True, null=True)),
                ('dataUpload', models.DateTimeField(auto_now=True, verbose_name='Data de Upload')),
                ('acelerometro', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='acelerometro_arquivo', to='core.Acelerometro', verbose_name='Acelerômetro')),
            ],
            options={
                'verbose_name': 'Arquivo',
                'verbose_name_plural': 'Arquivos',
            },
        ),
        migrations.CreateModel(
            name='ArquivoEstatisticas',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('canal', models.SmallIntegerField(default=1)),
                ('media', models.FloatField(blank=True, null=True)),
                ('desvio', models.FloatField(blank=True, null=True)),
                ('variancia', models.FloatField(blank=True, null=True)),
                ('curtoses', models.FloatField(blank=True, null=True)),
                ('arquivo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='arquivo_estatistica', to='core.Arquivo')),
            ],
        ),
    ]
