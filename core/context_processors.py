# core/context_processors.py
from datetime import date

def mes_atual_context(request):
    hoje = date.today()
    return {
        "ano_atual": hoje.year,
        "mes_atual": hoje.month
    }
