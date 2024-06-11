from fastapi import FastAPI

app = FastAPI()

vendas = {
    1: {"item": "lata", "preco_unitario": 4, "quantidade": 5},
    2: {"item": "garrafa 2L", "preco_unitario": 15, "quantidade": 5},
    3: {"item": "garrafa 750ml", "preco_unitario": 10, "quantidade": 5},
    4: {"item": "lata mini", "preco_unitario": 2, "quantidade": 5},
}

produtos = {
    1: {"nome": "lata", "preco": 4},
    2: {"nome": "garrafa 2L", "preco": 15},
    3: {"nome": "garrafa 750ml", "preco": 10},
    4: {"nome": "lata mini", "preco": 2},
}

@app.get("/")
def home():
    return {"Vendas": len(vendas)}

@app.get("/vendas/{id_venda}")
def pegar_venda(id_venda: int):
    if id_venda in vendas:
        return vendas[id_venda]
    else:
        return {"Erro": "ID Venda inexistente"}

@app.get("/produtos")
def listar_produtos():
    return produtos

@app.get("/produtos/{id_produto}")
def pegar_produto(id_produto: int):
    if id_produto in produtos:
        return produtos[id_produto]
    else:
        return {"Erro": "ID Produto inexistente"}