from unittest.mock import MagicMock
from fastapi.testclient import TestClient
from main import app, get_db
from models import ProdutoDB, FilmesDB

client = TestClient(app)

# testes produtos

# get - produtos
def test_listar_produtos_com_mock():
    db_mock = MagicMock()
    db_mock.query.return_value.all.return_value = [
        ProdutoDB(id=1, nome='Teclado', preco=89.90, quantidade=15)
    ]
    app.dependency_overrides[get_db] = lambda: db_mock

    resposta = client.get('/produtos')

    assert resposta.status_code == 200
    assert resposta.json()[0]['nome'] == 'Teclado'

    app.dependency_overrides.clear()

#  post - produtos
def test_criar_produto_com_mock():
    db_mock = MagicMock()

    def simular_refresh(produto):
        produto.id = 1  

    db_mock.refresh.side_effect = simular_refresh
    app.dependency_overrides[get_db] = lambda: db_mock

    novo_produto = {'nome': 'Monitor', 'preco': 799.90, 'quantidade': 5}
    resposta = client.post('/produtos', json=novo_produto)

    assert resposta.status_code == 201
    db_mock.add.assert_called_once()
    db_mock.commit.assert_called_once()

    app.dependency_overrides.clear()


# get com id - produtos
def test_obter_produto_com_mock():

    # config banco falso
    db_mock = MagicMock()

    # com o id, vai pegar o primeiro registro que encontar
    db_mock.query.return_value.filter.return_value.first.return_value = (
        ProdutoDB(id=1, nome='Teclado', preco=89.90, quantidade=15)
    )
    app.dependency_overrides[get_db] = lambda: db_mock

    # simulação de busca com id (id=1)
    resposta = client.get('/produtos/1')

    assert resposta.status_code == 200
    assert resposta.json()['id'] == 1
    app.dependency_overrides.clear()

# put - produtos
def test_atualizar_produto_com_mock():
    db_mock = MagicMock()
    produto_existente = ProdutoDB(id=1, nome='Teclado', preco=89.90, quantidade=15)
    db_mock.query.return_value.filter.return_value.first.return_value = produto_existente
    app.dependency_overrides[get_db] = lambda: db_mock

    dados_novos = {'nome': 'Teclado Mecânico', 'preco': 120.00, 'quantidade': 10}
    resposta = client.put('/produtos/1', json=dados_novos)

    assert resposta.status_code == 200
    assert resposta.json()['nome'] == 'Teclado Mecânico'
    db_mock.commit.assert_called_once()
    app.dependency_overrides.clear()

# delete - produtos
def test_remover_produto_com_mock():
    db_mock = MagicMock()
    produto_existente = ProdutoDB(id=1, nome='Teclado', preco=89.90, quantidade=15)
    db_mock.query.return_value.filter.return_value.first.return_value = produto_existente
    app.dependency_overrides[get_db] = lambda: db_mock

    resposta = client.delete('/produtos/1')

    assert resposta.status_code == 204
    db_mock.delete.assert_called_once_with(produto_existente)
    db_mock.commit.assert_called_once()
    app.dependency_overrides.clear()

# teste filmes

# get - filmes
def test_listar_filmes_com_mock():
    db_mock = MagicMock()
    db_mock.query.return_value.all.return_value = [
        FilmesDB(id=1, titulo='Inception', diretor='Nolan', genero='Ficção', duracao=148)
    ]
    app.dependency_overrides[get_db] = lambda: db_mock

    resposta = client.get('/filmes')

    assert resposta.status_code == 200
    assert resposta.json()[0]['titulo'] == 'Inception'
    app.dependency_overrides.clear()

# post - filmes
def test_criar_filme_com_mock():
    db_mock = MagicMock()

    def simular_refresh(filme):
        filme.id = 1

    db_mock.refresh.side_effect = simular_refresh
    app.dependency_overrides[get_db] = lambda: db_mock

    novo_filme = {'titulo': 'Matrix', 'diretor': 'Wachowski', 'genero': 'Ficção', 'duracao': 136}
    resposta = client.post('/filmes', json=novo_filme)

    assert resposta.status_code == 201
    db_mock.add.assert_called_once()
    db_mock.commit.assert_called_once()
    app.dependency_overrides.clear()

# get com id - filmes
def test_obter_filme_com_mock():
    db_mock = MagicMock()
    db_mock.query.return_value.filter.return_value.first.return_value = (
        FilmesDB(id=1, titulo='Inception', diretor='Nolan', genero='Ficção', duracao=148)
    )
    app.dependency_overrides[get_db] = lambda: db_mock

    resposta = client.get('/filmes/1')

    assert resposta.status_code == 200
    assert resposta.json()['id'] == 1
    app.dependency_overrides.clear()

# put - filmes
def test_atualizar_filme_com_mock():
    db_mock = MagicMock()
    filme_existente = FilmesDB(id=1, titulo='Inception', diretor='Nolan', genero='Ficção', duracao=148)
    db_mock.query.return_value.filter.return_value.first.return_value = filme_existente
    app.dependency_overrides[get_db] = lambda: db_mock

    dados_novos = {'titulo': 'Inception Gold', 'diretor': 'Nolan', 'genero': 'Ficção', 'duracao': 148}
    resposta = client.put('/filmes/1', json=dados_novos)

    assert resposta.status_code == 200
    assert resposta.json()['titulo'] == 'Inception Gold'
    db_mock.commit.assert_called_once()
    app.dependency_overrides.clear()

# delete - filmes
def test_remover_filme_com_mock():
    db_mock = MagicMock()
    filme_existente = FilmesDB(id=1, titulo='Inception', diretor='Nolan', genero='Ficção', duracao=148)
    db_mock.query.return_value.filter.return_value.first.return_value = filme_existente
    app.dependency_overrides[get_db] = lambda: db_mock

    resposta = client.delete('/filmes/1')

    # Retorna 204 se deletado com sucesso
    assert resposta.status_code == 204
    db_mock.delete.assert_called_once_with(filme_existente)
    db_mock.commit.assert_called_once()
    app.dependency_overrides.clear()

