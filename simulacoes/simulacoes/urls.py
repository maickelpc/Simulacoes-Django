"""simulacoes URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from core.views import *
from django.conf.urls.static import static
from . import settings
from django.contrib.staticfiles.urls import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
 
urlpatterns = [
    path('select_to_compare/', Arquivos.list_archievs_to_compare, name="archievs_to_compare"),
    path('compare_datas/<int:pk>/',Grafico.select_archiev_to_compare_data, name="select_archiev_to_compare_data"),
    path('admin/', admin.site.urls),
    path('', Arquivos.listar_arquivos, name="arquivos"),
    path('plotBruto/<int:pk>/',Arquivos.plotar_dados_brutos, name="plotBruto"),
    path('graphics_records/', Grafico.graphics_records, name = "graphics_records"),
    path('montarGrafico/<int:pk>/', Grafico.montar_grafico,name="montarGrafico"),
    path('plotarGrafico/',Grafico.plotar_grafico,name="plotarGrafico"),
    path('relatory/<str:time>/<str:channels>/<str:channels_analysis>/<str:code>/<str:fourier_size>/<str:status>/',Grafico.graph_relatory,name="relatory"),
    path('relatory_csv/<str:time>/<str:channels>/<str:channels_analysis>/<str:code>/<str:fourier_size>/<str:status>/',Grafico.graph_relatory_csv,name="relatory_csv"),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
