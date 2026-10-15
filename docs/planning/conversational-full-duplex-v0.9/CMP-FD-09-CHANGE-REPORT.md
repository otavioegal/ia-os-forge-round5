# CMP-FD-09 v0.9 — Change report

**Estado:** PROPOSTA. Não é PASS. Não edita v0.1 a v0.8, baseline, CMP, ata, ADR nem parecer.

FD07-08 e NEW-MEDIUM-07: `forge.command_commit` passa a guardar `command_digest`, `original_outcome_code`, `original_outcome_body` e `outcome_digest`. O replay devolve transporte 200 e o outcome guardado. A fixture `FX03-REPLAY-ORIGINAL-422` separa transporte 200 de original 422. Digest diferente não troca a linha e não duplica `event_id`. O lookup fica depois do tenant e antes do receiver mutável.

FD07-09 e NEW-MEDIUM-08: o manifest tem `base_sha` e `parent_sha`. Cada path tem os dois blobs Git e os dois SHA-256. O v0.1 em `docs/planning/conversational-full-duplex/` entra no conjunto. Não há boolean no lugar da comparação. Sem `--repo` o checker declara NOT_RUN.

FD07-07: o protocolo futuro pede barreira, as duas ordens, trios distintos, `pg_locks` ou timeout, e rollback. Continua NOT RUN. A corrida sequencial não é essa prova.

FD07-05: `n=-1` e os efeitos de dinheiro, microfone, high-water e opacidade permanecem. O harness agora muta `peer_ack_high_water_before` e `expected_stage`. Pós-lock grava `command_commit`; o pré-lock, inclusive a sequence negativa, não grava.

FD07-06: a chave tenant e os 404 opacos permanecem. O par null continua antes do lookup.

O schema da fixture recusa chave extra, UUID inválido e initial key fora de `participants` ou `allocated_by_session`. `proves_product` é false.
