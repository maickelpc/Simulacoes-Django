from django import forms
from django.forms import ModelForm

from .models import Arquivo

class ArquivoForm(ModelForm):

    #estatisticas = forms.BooleanField(widget=forms.TextInput(attrs={'readonly':'readonly'}), label="Possui Estatísticas?", required=False)
    estatistica_observacoes = forms.CharField(widget=forms.Textarea(attrs={'readonly': 'readonly'}), label="Observações Estatatísticas",  required=False)

    class Meta:
        model = Arquivo
        fields = ('__all__')