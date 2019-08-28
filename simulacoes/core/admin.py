from django.contrib import admin
from .models import  Acelerometro

# Register your models here.
class AcelerometroAdmin(admin.ModelAdmin):
    search_fields = ['codigo','descricao','localizacao']
    list_display = ['id','codigo','descricao','localizacao','eixoX','eixoY','eixoZ']
    list_editable = ['eixoX','eixoY','eixoZ']
    ordering = ['codigo']

admin.site.register(Acelerometro, AcelerometroAdmin)