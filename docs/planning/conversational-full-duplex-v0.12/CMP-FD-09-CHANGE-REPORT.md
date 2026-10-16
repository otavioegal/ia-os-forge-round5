# CMP-FD-09 v0.12 — Change report

**Estado:** PROPOSTA. Não é PASS. Não edita v0.1 a v0.11, baseline, CMP, ata, ADR nem parecer.

FD11-NEW-01 e NEW-LOW-03: a v0.11 validava tipos, mas a mutação era amostral. Esta pasta não troca a regra do schema. Troca o gerador. `schema_jobs` declara uma mutação por campo do schema. `occurrence_jobs` declara ausência e tipo em cada caso do host e em cada índice de `setup`, `steps`, `commit_order` e `expected_steps`. A contagem esperada é recalculada à parte. Se divergir, o checker devolve `FAIL_COVERAGE_GAP` e não imprime PASS.

Os campos opcionais de `positive` não existem na linha comportamental. O host `SYN-POSITIVE-ALL-OPTIONAL` os contém. Sem esse host, a regra fica sem caminho e a cobertura falha. `SYN-NEGATIVE-ALL-OPTIONAL` reúne os opcionais de `negative` num único caso. `SYN-RECEIVER-REMOVED-SETUP-2` e `SYN-CROSS-TENANT-SETUP-2` têm `setup` de tamanho 2, porque a fixture comportamental só tinha tamanho 1.

O que não mudou: ordem de ACK, replay 422/200, 409 imutável, 404 opaco, par null, `n` negativo, high-water monotônico, isolamento e zero movimento. NEW-MEDIUM-09 continua sem veredito escolhido. O parecer v0.2 não foi editado. `BYTES MATCH` neste turno é relato do autor, leitura somente, não auditoria independente.

Não houve migration, PostgreSQL, provider, deploy, gasto nem BUILD-00. A flag permanece desligada.
