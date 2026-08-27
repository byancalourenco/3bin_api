# main.py

#importando os arquivos
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import Base, engine, get_db
from models import ProdutoDB
from schemas import ProdutoCreate, ProdutoResponse

# imports para a atividade 2 
from models import FilmesDB
from schemas import FilmesCreate, FilmesResponse

from fastapi import HTTPException
from fastapi.middleware.cors import CORSMiddleware





Base.metadata.create_all(bind=engine) # cria as tabelas, se ainda não existirem
app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    # em produção, restringir para o domínio real do front-end
    allow_methods=['*'],
    allow_headers=['*'],
)

# get -  retorna uma lista
@app.get('/produtos', response_model=list[ProdutoResponse])
def listar_produtos(db: Session = Depends(get_db)):
    #  select * from produtos
    return db.query(ProdutoDB).all()

# post
@app.post('/produtos', response_model=ProdutoResponse, status_code=201)
def criar_produto(produto: ProdutoCreate, db: Session = Depends(get_db)):
    novo_produto = ProdutoDB(**produto.dict())
    db.add(novo_produto)
    db.commit()
    db.refresh(novo_produto)
    return novo_produto

# GET /produtos/{id} -> retorna um único produto pelo id
@app.get('/produtos/{produto_id}', response_model=ProdutoResponse)
def obter_produto(produto_id: int, db: Session = Depends(get_db)):
    produto = db.query(ProdutoDB).filter(ProdutoDB.id == produto_id).first()
    if produto is None:
        raise HTTPException(status_code=404, detail='Produto não encontrado')
    return produto

# DELETE /produtos/{id} -> remove um produto do banco de dados
@app.delete('/produtos/{produto_id}', status_code=204)
def remover_produto(produto_id: int, db: Session = Depends(get_db)):
    produto = db.query(ProdutoDB).filter(ProdutoDB.id == produto_id).first()
    if produto is None:
        raise HTTPException(status_code=404, detail='Produto não encontrado')
    db.delete(produto)
    db.commit()
    return {"mensagem": "Produto excluido com sucesso!"}


# PUT /produtos/{id} -> atualiza um produto existente no banco
@app.put('/produtos/{produto_id}', response_model=ProdutoResponse)
def atualizar_produto(produto_id: int, dados: ProdutoCreate, db: Session = Depends(get_db)):
    produto = db.query(ProdutoDB).filter(ProdutoDB.id == produto_id).first()
    if produto is None:
        raise HTTPException(status_code=404, detail='Produto não encontrado')
    produto.nome = dados.nome
    produto.preco = dados.preco
    produto.quantidade = dados.quantidade
    db.commit()
    db.refresh(produto)
    return produto    


# atividade 2


# get
@app.get('/filmes', response_model=list[FilmesResponse])
def listar_filmes(db: Session = Depends(get_db)):
    return db.query(FilmesDB).all()


# get
@app.get('/filmes/{produto_id}', response_model=FilmesResponse)
def obter_filme(filmes_id: int, db: Session = Depends(get_db)):
    filmes = db.query(FilmesDB).filter(FilmesDB.id == filmes_id).first()
    if filmes is None:
        raise HTTPException(status_code=404, detail='Filme não encontrado')
    return filmes

# post
@app.post('/filmes', response_model=FilmesResponse, status_code=201)
def criar_filme(filmes: FilmesCreate, db: Session = Depends(get_db)):
    novo_filme = FilmesDB(**filmes.dict()) 
    db.add(novo_filme) 
    db.commit()
    db.refresh(novo_filme)
    return novo_filme

# delete
@app.delete('/filmes/{filmes_id}', status_code=204)
def remover_filme(filmes_id: int, db: Session = Depends(get_db)):
    filmes = db.query(FilmesDB).filter(FilmesDB.id == filmes_id).first()
    if filmes is None:
        raise HTTPException(status_code=404, detail='Filme não encontrado')
    db.delete(filmes)
    db.commit()
    return HTTPException(status_code=204, detail='Filme deletado com sucesso')

# put
@app.put('/filmes/{filmes_id}', response_model=FilmesResponse)
def atualizar_filme(filmes_id: int, dados: FilmesCreate, db: Session = Depends(get_db)):
    filmes = db.query(FilmesDB).filter(FilmesDB.id == filmes_id).first()
    if filmes is None:
        raise HTTPException(status_code=404, detail='Filme não encontrado')
    filmes.titulo = dados.titulo
    filmes.diretor = dados.diretor
    filmes.genero = dados.genero
    filmes.duracao = dados.duracao
    db.commit()
    db.refresh(filmes)
    return filmes  