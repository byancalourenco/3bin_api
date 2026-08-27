# models.py - o bd pode ter várias tabelas, representa cada tabela
from sqlalchemy import Column, Integer, String, Float
from database import Base

# informa o nome, tipo, chave, etc
class ProdutoDB(Base):
    __tablename__ = 'produtos'
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    preco = Column(Float, nullable=False)
    quantidade = Column(Integer, nullable=False)

#  atividade 2
class FilmesDB(Base):
    __tablename__ ='filmes'
    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String(100), nullable=False)
    diretor = Column(String(100), nullable=False)
    genero = Column(String(100), nullable=False)
    duracao  = Column(Integer, nullable=False)