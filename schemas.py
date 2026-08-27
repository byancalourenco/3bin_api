# schemas.py

# posso ter vários schemas

from pydantic import BaseModel

class ProdutoBase(BaseModel):
    nome: str
    preco: float
    quantidade: int

class ProdutoCreate(ProdutoBase):
    pass

class ProdutoResponse(ProdutoBase):
 id: int


 # obrigatorio
class Config:
    from_attributes = True

#  atividade 2 

class FilmesBase(BaseModel):
    titulo: str
    diretor: str
    genero: str
    duracao: int

class FilmesCreate(FilmesBase):
    pass

class FilmesResponse(FilmesBase):
    id: int

