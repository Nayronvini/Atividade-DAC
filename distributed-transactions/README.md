## Aviso Importante

Por se tratar de um pojeto academico simples o .env não foi ocultado

Como executar o projeto

## Tutorial de Uso

### 1. Iniciar o Docker

Abra o Docker Desktop e aguarde até que o Docker Engine esteja em execução.

### 2. Iniciar o projeto

Abra o terminal na pasta raiz do projeto (onde está o arquivo docker-compose.yml) e execute:

`docker compose up --build`

Aguarde a inicialização dos serviços:
- API Python
- PostgreSQL
- MongoDB

Observação: o terminal continuará exibindo mensagens dos containers. Isso é normal, não precisa aguardar as mensagens pararem.

### 3. Acessar a API

Abra o navegador no endereço:
http://localhost:8000/docs

A página apresenta os endpoints disponíveis e permite executar os testes diretamente pelo navegador.

### 4. Execução dos casos de teste

#### Caso 1 — Inserção PostgreSQL → MongoDB

Endpoint: POST /api/customers/postgres-then-mongo

Expanda o endpoint.
Clique em Try it out.

Informe os dados:
{
  "name": "Cliente Teste 1",
  "email": "teste1@email.com"
}

Clique em Execute.

Resultado esperado:
- Inserção realizada no PostgreSQL.
- Inserção realizada no MongoDB.
- Transação finalizada com sucesso.

#### Caso 2 — Inserção MongoDB → PostgreSQL

Endpoint: POST /api/customers/mongo-then-postgres

Repita o procedimento anterior, utilizando:
{
  "name": "Cliente Teste 2",
  "email": "teste2@email.com"
}

Resultado esperado:
- Inserção realizada no MongoDB.
- Inserção realizada no PostgreSQL.
- Transação finalizada com sucesso.

#### Caso 3 — Falha na inserção do MongoDB

Endpoint: POST /api/customers/postgres-then-mongo
Expanda o endpoint e clique em Try it out.

Informe um novo cliente:
{
  "name": "Cliente Teste 3",
  "email": "teste3@email.com"
}

No parâmetro fail_at, informe mongo.
Clique em Execute.

Resultado esperado:
- O cliente é inserido inicialmente no PostgreSQL.
- A inserção no MongoDB falha propositalmente.
- A Saga executa a compensação no PostgreSQL.

O registro criado no PostgreSQL é removido.
A API deverá retornar um erro HTTP, pois a falha foi provocada intencionalmente.

#### Caso 4 — Falha na inserção do PostgreSQL

Endpoint: POST /api/customers/mongo-then-postgres
Expanda o endpoint e clique em Try it out.

Informe um novo cliente:
{
  "name": "Cliente Teste 4",
  "email": "teste4@email.com"
}

No parâmetro fail_at, informe postgres.
Clique em Execute.

Resultado esperado:
- O cliente é inserido inicialmente no MongoDB.
- A inserção no PostgreSQL falha propositalmente.
- A Saga executa a compensação no MongoDB.

O registro criado no MongoDB é removido.
A API deverá retornar um erro HTTP, pois a falha foi provocada intencionalmente.

### 5. Consultar os resultados

Para verificar os resultados dos testes, utilize:
GET /api/customers/transactions/{transaction_id}: consulta o estado da transação.
GET /api/customers/{customer_id}/debug: consulta os dados do cliente nos dois bancos.

Os identificadores são retornados nas respostas da API.

### 6. Encerrar o projeto

No terminal, pressione Ctrl + C e execute:
docker compose down
Pronto! Os containers serão encerrados e os dados persistidos nos volumes serão mantidos.