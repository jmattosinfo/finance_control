from django.contrib import admin
from django.urls import path
from core import views  # importa tudo do core/views.py

urlpatterns = [
    path('admin/', admin.site.urls),

    # principais
    path('', views.mes_atual, name='mes_atual'),
    #path('home/', views.mes_atual, name='home_redirect'),
    path('sobre/', views.sobre, name='sobre'),

    
    # transações
    path('nova/', views.nova_transacao, name='nova_transacao'),
    path('transacoes/', views.listar_transacoes, name='listar_transacoes'),
    path('excluir/<int:transacao_id>/', views.excluir_transacao, name='excluir_transacao'),
    path('editar/<int:transacao_id>/', views.editar_transacao, name='editar_transacao'),
    


    # meses
    path('mes/<int:ano>/<int:mes>/', views.mes_atual, name='mes_navegar'),
    #path('mes/', views.mes_atual_padrao, name='mes_atual_padrao'),
    path('grafico/<int:ano>/<int:mes>/', views.grafico_mes, name='grafico_mes'),
    
    
    path('teste-context/', views.teste_context_processor, name='teste_context'),

]
