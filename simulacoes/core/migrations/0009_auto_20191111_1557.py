# Generated by Django 2.2.1 on 2019-11-11 18:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_graphresults_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='graphresults',
            name='time',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True, verbose_name='ToTAL PROCESS TIME'),
        ),
    ]
