# Distributed Transactions Lab

Laboratório Python/FastAPI para estudar consistência entre PostgreSQL e MongoDB.

## Subir

```bash
docker compose up --build
```

Swagger: http://localhost:8000/docs  
Health: http://localhost:8000/health

## Cenário 1: PostgreSQL -> MongoDB

POST `/api/customers/postgres-then-mongo`

```json
{
  "id": "11111111-1111-4111-8111-111111111111",
  "name": "Ana",
  "email": "ana@example.com"
}
```

Falha simulada no MongoDB:
`POST /api/customers/postgres-then-mongo?fail_at=mongo`

## Cenário 2: MongoDB -> PostgreSQL

POST `/api/customers/mongo-then-postgres`

Falha simulada no PostgreSQL:
`POST /api/customers/mongo-then-postgres?fail_at=postgres`

## Inspeção

- `GET /api/customers/{customer_id}/debug`
- `GET /api/customers/transactions/{transaction_id}`

## Limitações e próximos passos

1. A implementação é Saga com transações locais e compensação, não 2PC distribuído.
2. SQLite é um journal local para uma única instância; não serve como coordenador compartilhado em múltiplas réplicas.
3. O recovery worker ainda não está implementado. Será necessário reconciliar o journal com os bancos após crash, inclusive no intervalo entre a gravação e a atualização do journal.
4. Compensações são condicionadas ao `operation_id` para não apagar registros de outra operação.
5. Esta versão usa chamadas síncronas para facilitar a leitura do fluxo.
6. Não usar em produção sem recuperação, testes de integração, autenticação, observabilidade e revisão de segurança.

## Comparação conceitual

PostgreSQL suporta `PREPARE TRANSACTION`, `COMMIT PREPARED` e `ROLLBACK PREPARED`.
MongoDB possui transações ACID próprias, mas não oferece participação XA genérica equivalente para um coordenador externo.
Assim, não há 2PC nativo entre os dois usando esses mecanismos. O laboratório demonstrará essa limitação e comparará com Saga.
