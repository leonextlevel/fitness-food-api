# FITNESSE FOOD API

Projeto com objetivo de extrair dados do site [Open Food Facts](https://world.openfoodfacts.org/) através de
web scraping e gerar uma API REST de consulta.
O scraping deve ser executado através de um sistema Cron executado uma vez ao dia.

## Principais linguagens, frameworks e tecnologias utilizadas

* Linguagem Python
* Django
* Django Rest Framework
* Pip-tools (gerenciamento de dependências)
* Pytest
* Model Bakery (Fixtures do Django)
* Flake8 e Blue (linters)
* Isort (Organização )
* Swagger (Documentação OpenAPI)
* BeautifulSoup (Scraping)
* Docker e docker-compose
* PostgreSQL

## Instalação e Execução

**Requisitos:** Docker e docker-compose instalados.

1. Copie o conteúdo de contrib/env-sample para um arquivo .env na raiz do projeto.

```bash
cp contrib/env-sample .env
```

2. Construa a imagem

```bash
docker-compose build
```

3. Suba o banco de dados

```bash
docker-compose up -d db
```

4. Aplique as migrações do Django no banco de dados

```bash
docker-compose run --rm api python manage.py migrate
```

5. Execute a API

```bash
docker-compose run --rm --service-ports api
```

6. Execute o cron

```bash
docker-compose up cron
```


### Utilitários

1. Compilar dependências *(Lembre de executar o build da imagem novamente após)*

```bash
docker-compose run --rm api bash -c "pip-compile --generate-hashes /usr/src/requirements/production.in && pip-compile --generate-hashes /usr/src/requirements/development.in"
```

2. Executar testes

```bash
docker-compose run --rm api pytest --cov .
```

3. Executar o flake8 (linter)

```bash
docker-compose run --rm api flake8 .
```

## Orientações

1. Acesse a documentação do Swagger para ter aos endpoints disponíveis na API: http://localhost:8080/swagger/ *(edite a porta se necessário)*

2. Edite o arquivo crontabs caso queira mudar o tempo de execução do cron ([Formato do comando](https://jjw.com.br/arquivos/cron.html))



>  This is a challenge by [Coodesh](https://coodesh.com/)
