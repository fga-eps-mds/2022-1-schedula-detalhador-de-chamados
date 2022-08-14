# Detalhador de chamados
---

## Integrantes

| Matricula  | Membro                          | Disciplina |
|------------|---------------------------------|------------|
| 18/0106970 | Matheus Gabriel Alves Rodrigues | EPS        |
| 18/0113151 | Eduardo Nunes Picolo            | EPS        |
| 18/0129287 | Pedro Henrique Vieira de Lima   | EPS        |
| 14/0065547 | Roberto Martins da Nóbrega      | EPS        |
| 18/0130722 | Samuel Nogueira Bacelar         | EPS        |
| 21/1043647 | Giovanni Alvissus               | MDS        |
| 20/0027158 | Rodrigo Edmar Wright Dos Santos | MDS        |
| 20/0042327 | Nicolas Chagas Souza            | MDS        |
| 19/0127767 | Davi Silva Matias               | MDS        |
| 20/0072854 | Bruno Seiji Kishibe             | MDS        |
| 20/2017521 | Algusto Rodrigues Caldas        | MDS        |
| 18/0113496 | Guilherme de Oliveira Mendes    | MDS        |

## Execução

```
    $ git clone
    $ cd schedula-detalhador-de-chamados
    $ docker-compose up --build -d
```
acessar o site: `http://localhost:5000/`

## Testes

```bash
docker exec -it detalhador-de-chamados pytest --cov -vv
```
## Lint

Instalando dependencias

```
pip install isort flake8 autopep8
```

Verifica o pep8 nos arquivos do projeto
``` 
flake8 **/*.py
``` 
Verifica os imports da aplicação
``` 
isort **/*.py --diff
``` 
Resolve problemas com a ordenação dos imports
``` 
isort --atomic .
```
Utiliza o autopep8 para tentar resolver a maioria dos problemas do flake8
``` 
autopep8 --in-place --aggressive --aggressive **/*.py
```
