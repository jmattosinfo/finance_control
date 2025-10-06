# apps.py serve para configurar a aplicação Django, definindo seu nome e outras configurações específicas.
# Você pode personalizar o comportamento da aplicação aqui, se necessário. 
# Por exemplo, definir sinais ou configurações específicas de inicialização.

from django.apps import AppConfig


class FinanceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'finance'
