# CMP-FD-09 v0.14 — Change report

**Estado:** PROPOSTA. Não é PASS. Não edita v0.1 a v0.13, baseline, CMP, ata, ADR nem parecer.

O parecer da v0.13 aceitou, por inspeção estática, objeto inline, tipo de elemento de array de objeto e chave JSON duplicada. Não reproduziu 508 nem 2443. Não viu golden externo. Apontou que a DSL não recusa keyword desconhecido. O veredito daquele parecer é PASS WITH CONDITIONS DOCUMENT-ONLY e o estado continua CANDIDATE. Esta pasta não converte isso em PASS.

O que entra, sem mudar a regra de campo do ACK:

- `dsl_problems` em `check_fd_fx03_ack.py:1206` fecha a DSL desta pasta. As chaves admitidas são `id`, `authority`, `objects`, `required`, `allowed`, `fields`, `groups`, `same_length`, `type`, `const`, `minLength`, `minItems`, `ref`, `items`. Os tipos admitidos são `uuid`, `nullable_uuid`, `int`, `nullable_int`, `bool`, `string`, `sha256`, `object`, `array`, `uuid_map`. `$ref`, `allOf`, `oneOf`, `anyOf`, `enum`, `format`, `nullable` e o resto do JSON Schema padrão não são desta DSL. Keyword fora da lista devolve `FAIL_UNKNOWN_KEYWORD`. A fixture `fixtures/CMP-FD-FX-06-unknown-keyword.json` carrega `allOf` e tem de falhar. O processo sai diferente de 0 se essa recusa não acontecer.
- `literal_bindings` em `check_fd_fx03_ack.py:1338` é iterativo. `tools/draft_semantic_reference.py` é recursivo e não importa o checker. Os dois têm de concordar nos 308 literais. O arquivo `fixtures/CMP-FD-FX-05-semantic-reference.json` guarda path, tipo de constraint, valor, digest do schema, digest da fixture, digest do sintético e a proveniência. A proveniência é esta sessão de autoria. Não há ato humano. `ratification` é `PENDING_HUMAN_APPROVAL`. `independence` é `NOT_RATIFIED`. Se o arquivo disser que foi aprovado, o checker devolve `FAIL_INVENTED_APPROVAL`.
- As contraprovas em `check_fd_fx03_ack.py:1471` alteram const, `minItems`, `minLength`, `ref` e required/optional. 508 e 2443 permanecem iguais nas quatro primeiras e na troca required/optional. O alvo compatível de `ref` é um alias em memória com a mesma forma de `counter`: a troca em si move 0 regras e 0 ocorrências. O checker nomeia o path que divergiu. Se o mesmo autor mudar o schema e o valor esperado juntos, a linha impressa é `SAME_AUTHOR_BOTH_SIDES not_detected`. Isso não é PASS. É o residual que mantém NEW-GOV-01 OPEN.
- `fixtures/CMP-FD-FX-07-coverage-ids.json` lista os 508 IDs e os 2443 IDs, com digest de cada um. Quem gerou o arquivo foi `tools/enumerate_coverage_ids.py`, que não importa o checker. O checker compara o conjunto. Concordância nesta sessão não é ratificação humana.
- Chave JSON duplicada também é recusada na referência, na fixture negativa e no manifesto de IDs.

O que não mudou: ordem de ACK, replay 422/200, 409 imutável, 404 opaco, par null, `n` negativo, high-water monotônico, isolamento e zero movimento. O parecer v0.2 não foi editado. `chosen_verdict` continua null.

Não houve migration, PostgreSQL, provider, deploy, gasto nem BUILD-00. A flag permanece desligada. 508 e 2443 não foram forçados: são a mesma conta da v0.13 porque as regras de campo não mudaram. O número novo, 308, é a conta de literais normativos, não uma regra de mutação a mais. O 521 da contraprova compatível é 508 mais as 13 regras do objeto alias, iguais dos dois lados da troca. O alias não está no schema publicado.
