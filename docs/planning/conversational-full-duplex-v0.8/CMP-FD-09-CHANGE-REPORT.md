# CMP-FD-09 v0.8 — Change report

**Estado:** PROPOSTA. Não é PASS. Não edita v0.1, v0.2, v0.3, v0.4, v0.5, v0.6, v0.7, FDP-16A v1.7, CMP v0.3, ata, ADR nem parecer.

FD07-05: a fixture passa a ter `FX03-NEGATIVE-SEQUENCE` com `n=-1`. O checker exige o id e lê `zero_effect`, `zero_new_effect`, `zero_money`, `opens_mic` e `opaque` em toda linha negativa. Mutação de campo declarado falha com código específico.

FD07-06: a chave passa a ser o trio dentro do tenant. O mapa estático recusa mudança de outra chave. Há tenant errado, receiver ausente e stream não alocado. O par null continua `NO_ACK` e o ou-exclusivo continua `ACK_SCOPE_MISMATCH` antes de unallocated.

FD07-07: a SQL da v0.6 é repetida, com `ON CONFLICT DO NOTHING` como grafia do insert já exigido. O teste de duas transações e a corrida de trios distintos ficam NOT RUN. O replay sequencial não é essa corrida.

FD07-08: replay usa `forge.command_commit` e `event_id` de `forge.event.v1`. Não há ledger novo. Mesma identidade, identidade distinta, digest reusado e crash antes do commit estão especificados. O rollback da fixture é modelo, não banco.

FD07-09: v0.5/v0.6 candidatos, sem parecer independente incorporado. O manifest cobre 91 arquivos históricos iguais no SHA base e no parent.

HIGH-03 não fecha. LOW-01 não muda. A flag não liga.
