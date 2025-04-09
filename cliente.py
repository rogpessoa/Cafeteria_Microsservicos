import requests
import time

URL_PEDIDO = "http://localhost:5002/pedidos"

pedidos = [
    {"id_produto": 1},
    {"id_produto": 2},
    {"id_produto": 3}
]

for i, pedido in enumerate(pedidos, start=1):
    resposta = requests.post(URL_PEDIDO, json=pedido)
    if resposta.status_code == 201:
        print(f"✅ Pedido {i} criado: {resposta.json()}")
    else:
        print(f"❌ Erro ao criar pedido {i}: {resposta.text}")
    time.sleep(0.5)
