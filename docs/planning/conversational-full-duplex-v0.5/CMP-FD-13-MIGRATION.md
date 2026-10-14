# CMP-FD-13 v0.5 — Migration tenant e índice de sessão

**Especificação. Nenhuma migration foi executada.** Não é PASS. Não liga flag.

`forge.conversation.delta.v4` nasce desligada. `forge.conversation.delta.v3` permanece desligada e esta página não a integra. Escritores do delta ficam inativos enquanto a validação não terminou. Esta página não os liga.

A coluna de sessão é `session_status`. A coluna `task.status` da baseline permanece o enum de produto. Este texto não escreve `SESSION_OPEN` no predicado e não mistura as duas.

## 1. Ordem, numa transação, não executada

Locks de tabela, nesta ordem, para não inverter o lock de runtime que começa no Build: `forge.build`, `forge.task`, `forge.operation`, `forge.reservation`. Modo `ACCESS EXCLUSIVE`. Se um lock não for obtido, a transação aborta. Nada fica pela metade.

### 1.1 Reservation, colunas anuláveis

```sql
ALTER TABLE forge.reservation
  ADD COLUMN IF NOT EXISTS organization_id uuid NULL,
  ADD COLUMN IF NOT EXISTS project_id uuid NULL;
```

Linha nova de conversação, depois da flag um dia ligada, copia o par da Operation na mesma transação de insert. Isso não é executado aqui.

### 1.2 Backfill e órfãos

```sql
SELECT count(*) AS orphan_reservation
FROM forge.reservation r
WHERE NOT EXISTS (
  SELECT 1 FROM forge.operation o WHERE o.id = r.operation_id
);

SELECT count(*) AS tenant_mismatch
FROM forge.reservation r
JOIN forge.operation o ON o.id = r.operation_id
WHERE r.organization_id IS NOT NULL
  AND (r.organization_id <> o.organization_id OR r.project_id <> o.project_id);
```

Qualquer contagem maior que zero: `ROLLBACK`. Não se inventa org. Não se sobrescreve o par divergente. A flag permanece desligada.

Se as duas contagens são zero:

```sql
UPDATE forge.reservation r
SET organization_id = o.organization_id,
    project_id = o.project_id
FROM forge.operation o
WHERE r.operation_id = o.id
  AND r.organization_id IS NULL;
```

O join é por `operation.id` uuid, não por `operation_ref`.

### 1.3 Unique em Operation e FK

`(organization_id, project_id, id)` não é a chave primária. A primária é `id`. A FK composta precisa do unique explícito.

```sql
ALTER TABLE forge.operation
  ADD CONSTRAINT operation_org_project_id_uniq
  UNIQUE (organization_id, project_id, id);

ALTER TABLE forge.reservation
  ADD CONSTRAINT reservation_operation_tenant_fk
  FOREIGN KEY (organization_id, project_id, operation_id)
  REFERENCES forge.operation (organization_id, project_id, id)
  NOT VALID;

ALTER TABLE forge.reservation
  VALIDATE CONSTRAINT reservation_operation_tenant_fk;

ALTER TABLE forge.reservation
  ALTER COLUMN organization_id SET NOT NULL,
  ALTER COLUMN project_id SET NOT NULL;
```

`SET NOT NULL` só depois de `VALIDATE` ter sucesso e de esta contagem ser zero:

```sql
SELECT count(*) AS reservation_null_tenant
FROM forge.reservation
WHERE organization_id IS NULL OR project_id IS NULL;
```

Contagem maior que zero: `ROLLBACK`. Flag desligada.

### 1.4 Índice de sessão, predicado explícito

Antes do índice, duplicata histórica:

```sql
SELECT organization_id, project_id, session_id, count(*) AS n
FROM forge.task
WHERE execution_domain = 'CONVERSATION'
  AND session_status IN ('OPEN', 'CLOSING', 'ORPHAN_HELD')
GROUP BY organization_id, project_id, session_id
HAVING count(*) > 1;
```

Se voltar linha: `ROLLBACK`, código de spec `DUPLICATE_OPEN_SESSION`. Não se apaga task. Não se cria o índice. Flag desligada.

Se zero linhas:

```sql
CREATE UNIQUE INDEX task_conversation_open_session_uidx
  ON forge.task (organization_id, project_id, session_id)
  WHERE execution_domain = 'CONVERSATION'
    AND session_status IN ('OPEN', 'CLOSING', 'ORPHAN_HELD');
```

Não existe índice único só em `session_id`. `task.status` não entra no `WHERE`. Task de produto, com `execution_domain` diferente ou `session_status` null, fica fora do índice.

Conflito dentro do mesmo org e projeto, depois do índice: `409 ANCHOR_EXISTS`, e só depois de achar a linha neste tenant. O mesmo UUID de sessão em outra org não conflita e não é citado. Sondagem cross-tenant sem linha local: `404` opaco, zero escrita.

### 1.5 Movimento e pending

```sql
ALTER TABLE forge.operation_money_movement
  ADD COLUMN IF NOT EXISTS settles_proof_id uuid NULL;
```

`SETTLEMENT` conversacional preenche `settles_proof_id`. Linha histórica fica null. Não se reescreve movimento já cometido.

A razão `SESSION_SLICE` é valor aditivo de `pending_provider_cost.reason`. Consumidor que não a entende falha fechado. Não coage para `OVER_ESTIMATE` e não liquida.

### 1.6 Flag

Enquanto qualquer passo acima não tiver commitado, ou enquanto `reservation_null_tenant` não for zero, ou enquanto a constraint não estiver validada, `forge.conversation.delta.v4` permanece desligada. Esta página não a liga mesmo depois do desenho.

## 2. Lookup, ingest, replay

Predicado de Operation, Reservation e `command_commit`: org e projeto do canal mais o id. Ingest só grava prova na operation daquele tenant. Replay não lê commit de outro tenant e não o trava.

Id estrangeiro preexistente usa o mesmo `404` opaco. Zero efeito na linha de lá.

## 3. Volta

| Passo | Pode desfazer se | Bloqueio |
|---|---|---|
| flag | segue desligada | flag ligada com operation não terminal |
| índice de sessão | zero task conversacional no predicado | senão `ROLLBACK_BLOCKED` |
| `settles_proof_id` | zero movimento conversacional com a coluna preenchida | não se apaga movimento |
| FK | nenhum writer do delta e zero reservation conversacional nova | FK não sai se aponta para operation com movimento |
| NOT NULL | não se apaga reservation para “limpar” | `ROLLBACK_BLOCKED` se a coluna já carrega par usado por movimento |
| unique de Operation | nenhum FK depende dele | senão `ROLLBACK_BLOCKED` |

`SESSION_CLOSED`, movement, prova, pending, outbox, audit e `command_commit` cometido não são apagados. Rollback para no primeiro bloqueio.
