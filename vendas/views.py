from django.shortcuts import render
from .utils import fazer_predicao_fraude
from .models import Transacao

def simular_venda(request):
    resultado = None
    dados = {} 
    
    if request.method == 'POST':
        dados = {
            'amount': request.POST.get('amount'),
            'location': request.POST.get('location'),
            'merchant': request.POST.get('merchant'),
            'card_type': request.POST.get('card_type'),
        }
        
        foi_fraude, proba = fazer_predicao_fraude(dados)
        
        Transacao.objects.create(amount=dados['amount'],
            location=dados['location'],
            merchant=dados['merchant'],
            card_type=dados['card_type'],
            is_fraud=foi_fraude,
            probability=proba) 
        
        resultado = {
            'texto': "⚠️ TRANSAÇÃO NEGADA" if foi_fraude else "✅ TRANSAÇÃO APROVADA",
            'cor': "danger" if foi_fraude else "success",
            'confianca': f"{proba * 100:.2f}%"
        }


    # Devolvemos resultado E dados_preenchidos
    return render(request, 'vendas/simulador.html', {'resultado': resultado, 'dados': dados})