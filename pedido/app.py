import requests
from flask import Flask, request, jsonify, Response
import json
import os
app = Flask("pedidos")
ARQUIVO_PEDIDOS = os.path.join(os.path.dirname(__file__), "pedido.json")
URL_PRODUTOS = "http://produtos:5001/produtos"


INFO = {"Pagina": "Pedidos",
        "Autor": "Rogério"
        }


def carregar_pedidos():
    with open(ARQUIVO_PEDIDOS) as arquivo:
        return json.load(arquivo)

def salvar_pedidos(pedidos):
    with open(ARQUIVO_PEDIDOS, "w") as arquivo:
        json.dump(pedidos, arquivo, indent=2)

@app.get("/")
def get():
    return Response(json.dumps(INFO), status=200, mimetype="application/json")

@app.get("/pedidos")
def listar_pedidos():
    return jsonify(carregar_pedidos())

@app.post("/pedidos")
def criar_pedido():
    dados = request.json
    id_produto = dados.get("id_produto")
    if not id_produto:
        return {"erro": "Campo id_produto é obrigatório"}, 400

    resposta = requests.get(f"{URL_PRODUTOS}/{id_produto}")
    if resposta.status_code != 200:
        return {"erro": "Produto não encontrado"}, 404

    pedidos = carregar_pedidos()
    novo_pedido = {
        "id": len(pedidos) + 1,
        "id_produto": id_produto,
        "status": "pendente"
    }
    pedidos.append(novo_pedido)
    salvar_pedidos(pedidos)

    return jsonify(novo_pedido), 201

@app.patch("/pedidos/<int:id_pedido>")
def atualizar_status(id_pedido):
    pedidos = carregar_pedidos()
    for pedido in pedidos:
        if pedido["id"] == id_pedido:
            pedido["status"] = "pago"
            salvar_pedidos(pedidos)
            return jsonify(pedido), 200
    return {"erro": "Pedido não encontrado"}, 404


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002)
