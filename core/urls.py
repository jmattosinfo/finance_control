from django.contrib import admin
from django.urls import path
from core import views  # importa tudo do core/views.py
from django.contrib.auth import views as auth_views #para autenticação
from core import views as core_views


urlpatterns = [
    path('admin/', admin.site.urls),

    # principais
    path('', views.mes_atual, name='mes_atual'),
    path('sobre/', views.sobre, name='sobre'),
    
    
    
    # autenticação
    path("login/", core_views.login_view, name="login"),
    path('logout/', views.logout_view, name='logout'),
    path('login/', auth_views.LoginView.as_view(template_name='finance/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path("cadastro/", views.cadastro_view, name="cadastro"),
    
    
    
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
