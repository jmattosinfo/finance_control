# aqui no admin.py você registra seus modelos para que possam ser gerenciados 
# através do painel de administração do Django.
from django.contrib import admin
from .models import Transacao

admin.site.register(Transacao)
class TransacaoAdmin(admin.ModelAdmin):
    list_display = ('descricao', 'valor', 'data', 'categoria', 'pago') # Campos a serem exibidos na lista de transações
    list_filter = ('data', 'categoria', 'pago') # Filtros laterais para facilitar a busca
    search_fields = ('descricao', 'categoria') # Campos que podem ser pesquisados
    list_editable = ('pago',) # Permite editar o campo 'pago' diretamente na lista

# Register your models here.

