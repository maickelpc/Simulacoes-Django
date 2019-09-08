# Generated by Django 2.2.4 on 2019-09-07 14:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_arquivo_estatistica_observacoes'),
    ]

    operations = [
        migrations.CreateModel(
            name='LeituraUEME',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('dataInicio', models.DateTimeField()),
                ('acrescimoSegundos', models.FloatField()),
                ('dataReal', models.DateTimeField()),
                ('orientacao', models.CharField(max_length=1)),
                ('aceleracao', models.FloatField()),
                ('leitura', models.BigIntegerField()),
                ('acelerometro', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='leitura_acelerometro', to='core.Acelerometro')),
                ('arquivo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='arquivo_leitura', to='core.Arquivo')),
            ],
        ),
    ]