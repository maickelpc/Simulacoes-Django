from django.contrib import admin
from .models import  Acelerometro,Arquivo

# Register your models here.


class AcelerometroAdmin(admin.ModelAdmin):
    search_fields = ['codigo','descricao','localizacao']
    list_display = ['id','codigo','descricao','localizacao','eixoX','eixoY','eixoZ']
    list_editable = ['eixoX','eixoY','eixoZ']
    ordering = ['codigo']

class ArquivoAdmin(admin.ModelAdmin):
    search_fields = ['codigo','dataLeitura']
    list_display = ['codigo','canais','dataLeitura','dataUpload']
    ordering = ['dataUpload','codigo']
    autocomplete_fields = ['acelerometro']

admin.site.register(Acelerometro, AcelerometroAdmin)
admin.site.register(Arquivo, ArquivoAdmin)