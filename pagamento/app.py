import requests
from flask import Flask, request, jsonify, Response
import json
import os

app = Flask("pagamentos")

ARQUIVO_PAGAMENTOS = os.path.join(os.path.dirname(__file__), "pagamento.json")
URL_PEDIDOS = "http://pedidos:5002/pedidos"
URL_PRODUTOS = "http://produtos:5001/produtos"

INFO = {"Pagina": "Pagamentos",
        "Autor": "Rogério"
        }

@app.get("/")
def get():
    return Response(json.dumps(INFO), status=200, mimetype="application/json")


def carregar_pagamentos():
    with open(ARQUIVO_PAGAMENTOS) as arquivo:
        return json.load(arquivo)

def salvar_pagamentos(pagamentos):
    with open(ARQUIVO_PAGAMENTOS, "w") as arquivo:
        json.dump(pagamentos, arquivo, indent=2)

@app.get("/pagamentos")
def listar_pagamentos():
    return jsonify(carregar_pagamentos())

@app.post("/pagamentos")
def realizar_pagamento():
    dados = request.json
    id_pedido = dados.get("id_pedido")
    if not id_pedido:
        return {"erro": "Campo id_pedido é obrigatório"}, 400

    pedidos = requests.get(URL_PEDIDOS).json()
    pedido = next((p for p in pedidos if p["id"] == id_pedido), None)
    if not pedido:
        return {"erro": "Pedido não encontrado"}, 404

    produto = requests.get(f"{URL_PRODUTOS}/{pedido['id_produto']}").json()

    novo_pagamento = {
        "id": len(carregar_pagamentos()) + 1,
        "id_pedido": id_pedido,
        "valor": produto["preco"],
        "status": "pago"
    }

    pagamentos = carregar_pagamentos()
    pagamentos.append(novo_pagamento)
    salvar_pagamentos(pagamentos)

    return jsonify(novo_pagamento), 201

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5003)
