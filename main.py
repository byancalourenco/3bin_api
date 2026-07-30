# importanção do FastAPI
from fastapi import FastAPI

# criação da aplicação
app = FastAPI()

# criação de rota
@app.get("/")
def Raiz():
    return {"mensagem": "Minha primeira API em FastAPI!"}

# outra rota
@app.get("/clientes")
def Clientes():
    return {"mensagem": "Lista de clientes"}


# @ - decorator
# objeto, método, URL, função