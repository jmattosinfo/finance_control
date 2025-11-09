from datetime import date

def mes_atual_context(request):
    """
    Context processor que fornece ano e mês atuais
    para todos os templates.
    """
    hoje = date.today()
    return {
        "ano_atual": hoje.year,
        "mes_atual": hoje.month
    }
