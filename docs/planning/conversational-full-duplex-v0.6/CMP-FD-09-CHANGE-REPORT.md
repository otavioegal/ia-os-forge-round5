# CMP-FD-09 v0.6 — Change report

**Estado:** PROPOSTA. Não é PASS. Não edita v0.1, v0.2, v0.3, v0.4, v0.5, FDP-16A v1.7, CMP v0.3, ata, ADR nem parecer.

A v0.5 deixava `ack_of_sequence = 0` sem linha de resultado quando o peer high-water também era 0. Esta pasta marca zero como `422 ACK_SEQUENCE_ZERO`, com efeito zero, antes da comparação com o high-water. O mesmo código vale depois que o high-water já subiu. Não é duplicata e não é regressão.

A escrita do peer high-water passa a ser uma linha travada e um `UPDATE` cujo predicado exige `n > peer_ack_high_water`. Ack regressivo não escreve. As duas ordens de commit de `n=1` e `n=2` terminam em 2.

O índice único da v0.5 não impede vários `session_id` null. A baseline não declara essa coluna `NOT NULL`. A opção B conta essas linhas no predicado ativo. Uma já aborta a migration inteira, sem inventar id e sem apagar task. O check nasce `NOT VALID` e só é validado se a contagem é zero. O índice vem depois. `task.status` continua fora do predicado.

Nada disso foi migration, oracle ou BUILD-00. LOW-01 não mudou.
