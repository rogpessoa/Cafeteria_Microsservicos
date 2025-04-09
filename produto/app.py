import os
from flask import Flask, jsonify, Response
import json

app = Flask("produtos")

ARQUIVO_PRODUTOS = os.path.join(os.path.dirname(__file__), "produto.json")

INFO = {"Loja": "Café Purista",
        "Autor": "Rogerio",
        "Pagina": "Produtos - Cafe"
        }

def carregar_produtos():
    if os.path.exists(ARQUIVO_PRODUTOS):
        with open(ARQUIVO_PRODUTOS, "r", encoding="utf-8") as arquivo:
            try:
                return json.load(arquivo)
            except json.JSONDecodeError:
                return []
    return []
@app.get("/")
def get():
    return Response(json.dumps(INFO), status=200, mimetype="application/json")
@app.get("/produtos")
def listar_produtos():
    produtos = carregar_produtos()
    return jsonify(produtos), 200

@app.get("/produtos/<int:id_produto>")
def obter_produto(id_produto):
    with open(ARQUIVO_PRODUTOS) as arquivo:
        produtos = json.load(arquivo)
    produto = next((p for p in produtos if p['id'] == id_produto), None)
    if produto:
        return jsonify(produto)
    return {'erro': 'Produto não encontrado'}, 404

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001)
