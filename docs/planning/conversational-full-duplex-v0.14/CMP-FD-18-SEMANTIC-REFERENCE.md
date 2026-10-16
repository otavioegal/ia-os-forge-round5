# CMP-FD-18 v0.14 — Referência semântica, não ratificada

**Estado:** CANDIDATE. Não é golden humano. Não é PASS. NEW-GOV-01 permanece OPEN.

## O que este arquivo é

`fixtures/CMP-FD-FX-05-semantic-reference.json` fixa literais do schema v0.14: path, constraint, valor esperado, SHA-256 do schema, SHA-256 da fixture, SHA-256 do sintético e o digest canônico dos 308 bindings. A proveniência é `tools/draft_semantic_reference.py`, escrito nesta sessão. Esse script não importa o checker. O checker confere com `literal_bindings` em `check_fd_fx03_ack.py:1338`, que é iterativo. O rascunho é recursivo. Concordância dos 308 não é ato do Founder.

Campos obrigatórios do arquivo:

| Campo | Valor exigido pelo checker |
|---|---|
| `ratification` | `PENDING_HUMAN_APPROVAL` |
| `independence` | `NOT_RATIFIED` |
| `proves_product` | false |
| `full_product_coverage` | false |
| `new_gov_01` | `OPEN` |
| `generator` | não pode ser `tools/check_fd_fx03_ack.py` |

Outro valor em ratificação, independência ou `new_gov_01` devolve `FAIL_INVENTED_APPROVAL` em `check_fd_fx03_ack.py:1414`. Não há golden ratificado para copiar. Inventar aprovação violaria o prompt.

A referência cobre só os contratos deste pacote. Não cobre o produto. Não cobre O92. Não cobre PostgreSQL.

## O que uma edição de um lado só dispara

`cardinality_probes` em `check_fd_fx03_ack.py:1471` altera uma cópia em memória. O arquivo publicado não muda. Cada caso tem de nomear o path divergente. Os casos em que 508 e 2443 ficam iguais:

| Caso | Edição | 508 / 2443 | Hosts atuais | Path |
|---|---|---|---|---|
| const | const e o valor da fixture passam a `cmp.fd.fx03.ack.OTHER`, juntos | iguais | o par alterado continua coerente entre si | `document.schema.const` |
| minItems | 6 passa a 5. A fixture tem 7 chaves | iguais | aceitos | `document.initial_keys.minItems` |
| minLength | `note` passa de 1 para 2. O texto tem 241 caracteres | iguais | aceitos | `document.note.minLength` |
| ref | `step.counter_delta.ref` passa de `counter` para `document` | iguais | `FAIL_SCHEMA` | `step.counter_delta.ref` |
| required/optional | no corpo positivo, `error_code` sai de required e `opaque` entra | iguais | aceitos | `positive.expected_original_outcome_body.required` |

O caso `ref` para `document` mostra que a conta não se mexe mesmo quando o alvo não é compatível. O validador antigo ainda devolve `FAIL_SCHEMA`. A referência não depende dessa falha: ela aponta o path.

O caso compatível não usa um segundo objeto já existente, porque este schema não tem dois objetos com a mesma forma. A sonda cria `counter_alias` em memória, cópia de `counter`, e aponta `step.counter_delta.ref` para ele. Os hosts continuam aceitos. Contra o schema que já contém o alias, a troca move 0 regras e 0 ocorrências. A conta absoluta vai a 521 porque o alias acrescenta 13 regras de objeto (6 campos obrigatórios inteiros, cada um com TYPE e ABSENCE, mais EXTRA). Os dois lados da troca têm as mesmas 521 e as mesmas 2443. O path `step.counter_delta.ref` diverge da referência publicada, que ainda diz `counter`. O alias não entra no schema commitado. 508 continua sendo a conta do schema publicado.

## O que não é detectado

Se o mesmo autor alterar o valor no schema, o valor na fixture quando for o caso, o esperado na referência e os digests da referência, o comparador não tem fonte externa ratificada. A sonda faz isso com o const e imprime `SAME_AUTHOR_BOTH_SIDES not_detected path=document.schema.const`. Isso é falha de independência, declarada, não um sucesso. NEW-GOV-01 fica OPEN até um golden ratificado por pessoa autorizada.

O enumerador de IDs foi escrito na mesma sessão. Se o mesmo erro conceitual estiver no checker e no enumerador, os conjuntos fecham e o erro permanece. A referência de literais pega mudança de valor que não muda cardinalidade. Não pega um erro que tenha sido copiado para dentro dela.

## DSL fechada

A fixture `fixtures/CMP-FD-FX-06-unknown-keyword.json` é negativa e não é autoridade. O checker exige `FAIL_UNKNOWN_KEYWORD` no keyword `allOf`. Também injeta `nullable` e `allOf` em cópias do schema de autoridade. Bool e int não se coercem. Os dois sinais de nulidade são os tipos `nullable_int` e `nullable_uuid`, não um keyword.
