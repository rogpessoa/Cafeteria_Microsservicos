import requests
from time import sleep

URL_PAGAMENTO = "http://localhost:5003/pagamentos"
URL_PEDIDOS = "http://localhost:5002/pedidos"

pagamentos = [
    {"id_pedido": 1},
    {"id_pedido": 2},
    {"id_pedido": 3}
]

for i, pagamento in enumerate(pagamentos, start=1):
    resposta = requests.post(URL_PAGAMENTO, json=pagamento)
    if resposta.status_code == 201:
        print(f"💰 Pagamento {i} realizado: {resposta.json()}")

        id_pedido = pagamento["id_pedido"]
        atualizacao = requests.patch(f"{URL_PEDIDOS}/{id_pedido}")
        if atualizacao.status_code == 200:
            print(f"✅ Pedido {id_pedido} atualizado para 'pago'")
        else:
            print(f"⚠️ Falha ao atualizar status do pedido {id_pedido}: {atualizacao.text}")

    else:
        print(f"❌ Erro no pagamento {i}: {resposta.text}")
    sleep(0.5)