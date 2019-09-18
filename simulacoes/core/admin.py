from django.contrib import admin
from .models import  Acelerometro,Arquivo, ArquivoEstatisticas
from .forms import ArquivoForm

# Register your models here.

class EstatisticasTabular(admin.TabularInline):
    model = ArquivoEstatisticas
    extra = 0
    max_num = 0
    search_fields = ['id']
    readonly_fields = ['canal','media','desvio','variancia','curtoses']
    can_delete = False


class AcelerometroAdmin(admin.ModelAdmin):
    search_fields = ['codigo','descricao','localizacao']
    list_display = ['id','codigo','descricao','localizacao','eixoX','eixoY','eixoZ']
    list_editable = ['eixoX','eixoY','eixoZ']
    ordering = ['codigo']

class ArquivoAdmin(admin.ModelAdmin):
    search_fields = ['codigo','dataLeitura', 'estatisticas']
    list_display = ['id','codigo','canais','dataLeitura','dataUpload','estatisticas']
    list_display_links = ['id','codigo','canais','dataLeitura','dataUpload','estatisticas']
    ordering = ['dataUpload','codigo']
    autocomplete_fields = ['acelerometro']
    form = ArquivoForm
    inlines = [EstatisticasTabular]


admin.site.register(Acelerometro, AcelerometroAdmin)
admin.site.register(Arquivo, ArquivoAdmin)
