# Generated by Django 2.2.5 on 2019-11-01 14:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_auto_20191005_1503'),
    ]

    operations = [
        migrations.AlterField(
            model_name='graphresults',
            name='channels',
            field=models.CharField(max_length=30),
        ),
    ]
