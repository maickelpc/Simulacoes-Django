from django import forms
from django.forms import ModelForm

from .models import Arquivo

class ArquivoForm(ModelForm):

    #estatisticas = forms.BooleanField(widget=forms.TextInput(attrs={'readonly':'readonly'}), label="Possui Estatísticas?", required=False)
    estatistica_observacoes = forms.CharField(widget=forms.Textarea(attrs={'readonly': 'readonly'}), label="Observações Estatatísticas",  required=False)

    class Meta:
        model = Arquivo
        fields = ('__all__')

class GraficoForm(forms.Form):
    analise_canais = forms.IntegerField(label="Channels analysis",initial=50)
    fourier_size = forms.IntegerField(label="Fourier transform size",initial=2048)