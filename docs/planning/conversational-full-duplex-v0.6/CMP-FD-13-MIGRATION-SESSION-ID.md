# CMP-FD-13 v0.6 — session_id nas sessões ativas

**Especificação. Nenhuma migration foi executada.** Não é PASS. Não liga flag.

A opção escolhida é a B. FDP-16A v1.7, seção 3.2, não tem coluna `session_id` e portanto não a declara `NOT NULL`. A coluna é do delta conversacional. Esta página não finge a opção A.

A v0.5 criava o índice único parcial e parava. Em PostgreSQL esse índice trata `NULL` como distinto de outro `NULL`. Várias tasks ativas podem ter `session_id` nulo sem colidir. Esta página fecha isso antes do índice.

O predicado ativo continua exatamente:

```text
execution_domain = 'CONVERSATION'
AND session_status IN ('OPEN', 'CLOSING', 'ORPHAN_HELD')
```

`task.status` não entra. A v0.5 não é editada. Os passos de tenant daquela migration continuam a proposta vigente e correm na mesma transação que o portão abaixo. Se este portão falha, a transação inteira faz `ROLLBACK`. Nada de tenant, índice ou check fica commitado. `forge.conversation.delta.v4` permanece desligada. `forge.conversation.delta.v3` não é integrada.

## 1. Contagem, antes do índice

```sql
SELECT count(*) AS active_conversation_null_session
FROM forge.task
WHERE execution_domain = 'CONVERSATION'
  AND session_status IN ('OPEN', 'CLOSING', 'ORPHAN_HELD')
  AND session_id IS NULL;
```

Contagem maior que zero: `ROLLBACK` da migration inteira. Código de spec `NULL_ACTIVE_SESSION`. Não se inventa UUID. Não se apaga task. Não se cria o índice. Não se valida check. A flag segue desligada.

Uma linha já basta. Não se espera a contagem dois. O `GROUP BY` de duplicata da v0.5 não substitui esta contagem: um único null não é duplicata e ainda assim é inválido.

## 2. Check, só se a contagem é zero

```sql
ALTER TABLE forge.task
  ADD CONSTRAINT task_conversation_active_session_id_not_null
  CHECK (
    NOT (
      execution_domain = 'CONVERSATION'
      AND session_status IN ('OPEN', 'CLOSING', 'ORPHAN_HELD')
    )
    OR session_id IS NOT NULL
  ) NOT VALID;

ALTER TABLE forge.task
  VALIDATE CONSTRAINT task_conversation_active_session_id_not_null;
```

`VALIDATE` com falha: `ROLLBACK` da migration inteira. Mesmas proibições da seção 1.

O check não exige `session_id` em task de produto, nem em task conversacional fora de `OPEN`, `CLOSING` e `ORPHAN_HELD`.

## 3. Índice, só depois do check validado

A contagem de duplicata da v0.5 permanece, com o mesmo predicado. Se ela voltar linha: `ROLLBACK` inteiro, código `DUPLICATE_OPEN_SESSION`, sem apagar task.

Se essa contagem é zero:

```sql
CREATE UNIQUE INDEX task_conversation_open_session_uidx
  ON forge.task (organization_id, project_id, session_id)
  WHERE execution_domain = 'CONVERSATION'
    AND session_status IN ('OPEN', 'CLOSING', 'ORPHAN_HELD');
```

O índice sozinho não fecha null. O check fecha. Com o check validado, o predicado do índice não contém `session_id` null, então a folga de null do unique não tem linha para aproveitar.

Não existe índice único só em `session_id`.

## 4. Conflito e 404

Segunda abertura no mesmo org, projeto e `session_id`, com status ainda no predicado: `409 ANCHOR_EXISTS`, só depois de achar a linha neste tenant.

O mesmo UUID em outra org não conflita e não é citado. Sondagem sem linha local: `404` com corpo `{"error_code":"NOT_FOUND","retryable":false,"terminal":true}`. Sem lock na linha estrangeira.

Insert com `session_id` null dentro do predicado, depois do check: a constraint rejeita. A transação do insert aborta. Nenhuma task nova fica gravada.

## 5. Volta

O check e o índice só saem se não houver task conversacional no predicado. Senão `ROLLBACK_BLOCKED`. Não se apaga task, movimento, prova, pending, outbox, audit nem `command_commit` para abrir caminho. A flag não é ligada em nenhum dos dois sentidos.
