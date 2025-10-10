"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from finance import views # Importa as views do aplicativo finance. Isso permite que você use as funções definidas em finance/views.py para lidar com as requisições.
from . import views # Importa as views do próprio aplicativo. O . indica que o módulo está no mesmo diretório.

urlpatterns = [
    path('admin/', admin.site.urls), # Rota para o painel de administração
    path('', views.home, name='home'), # Rota para a página inicial
    path("", views.listar_transacoes, name="listar_transacoes"),
    path("nova/", views.nova_transacao, name="nova_transacao"),
    path("home/", views.home, name="home"),
    path("sobre/", views.sobre, name="sobre"), # Rota para a página sobre
    path("excluir/<int:transacao_id>/", views.excluir_transacao, name="excluir_transacao"), # Rota para excluir uma transação pelo ID
]
