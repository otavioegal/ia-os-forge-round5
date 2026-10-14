# CMP-FD-12 v0.5 — Consistência

**Estado:** relato do autor. Não é evidência de PASS. Não executa oráculo.

| Afirmação que seria regressão | Onde esta pasta fica |
|---|---|
| Headroom lido antes do lock do Build | proibido, CMP-FD-01:11 e CMP-FD-01:159 |
| Apply liquida sem a fatia | proibido, CMP-FD-01:97 |
| `H` exclui E e a conta cabe 70 em 50 | negado, CMP-FD-01:35 e CMP-FD-01:37 |
| Pending é apagado quando o settlement posterior passa | negado, CMP-FD-01:145 |
| `task.status` no índice de sessão | negado, CMP-FD-13:105-111 |
| Ack preso ao `stream_id` do CONTROL | substituído, CMP-FD-02:27-31 |
| Principal divergente abre sessão | `PREAMBLE_AUTH`, CMP-FD-02:73, zero efeito |
| `i=1199` mic 32767 | corrigido para 28000, CMP-FD-07:128-130 |
| `consent_stop_deadline_ns` dentro de `observation` | negado, CMP-FD-02:14 |
| Half-duplex como equivalente do MVP | negado, CMP-FD-02 e CMP-FD-05 |
| Segundo ledger ou refund | negado, CMP-FD-01:16 |
| Flag ligada | CMP-FD-13, nasce e permanece desligada |
| História com pessoa inventada | CMP-FD-07:7-21, OPEN BLOCKING |

FX-01 continua com `OUTPUT` `reproduced_at_ns` null e `PLAYBACK_SPAN` preenchido. Interseção histórica `[300000000, 670000000]` não foi recalculada como teste. Os carimbos não foram alterados; só entrou `ack_stream_id` null, e por isso os digests não são os da v0.4.

## Suíte estática

Não é teste de produto, não é oracle run, não é BUILD-00. Comando:

`python3 tools/check_fd_fx01_static_suite.py`

Python 3.10.22. Exit 0. Última linha: `STATIC_FIXTURE_SUITE PASS_FIXTURE_ONLY`.

Digests positivos:

| Evento | SHA-256 |
|---|---|
| G0 OUTPUT | `31c0195cd87ada9328469cb87f442c2115aa47b197d94461d46dffac8dc1dc6b` |
| G0 SPAN | `b82af907b0cdc2cbbd57da332e7e65a40f3e8c00365bbc41001d9afae843a741` |
| I0 INPUT | `f070c324c1ec5021c72308c33dab60520d4e1fe3a14bad4e6d0f93e2f62197b6` |
| G1 OUTPUT | `b6bc930149090e80e7b2509f431463f57f67a157708a72ac8dc62af28ec4a75b` |
| G1 SPAN | `d40dd4acccdf71457fd3e423891502144cfbd9fe18e21afc325b7a1371cbdb00` |
| I1 INPUT | `00e6b6e7c94b7186fb7233d7d53793a2819c46136ded79063fa13b389e38d55b` |
| G2 OUTPUT | `1fc19817887d82cd679307c8d7f692906af790a1d07caac19825f4cb7fb828b3` |
| G2 SPAN | `23aa14acbbfe6e61982b49c10714f36093a23472e5c004c4cde2ce99db6723cb` |

Negativos da mesma suíte, todos exit diferente de zero: `FAIL_DUPLICATE_EVENT_ID`, `FAIL_ORPHAN_VECTOR`, `FAIL_DUPLICATE_JSON_KEY`, `FAIL_BAD_SHA256`, `FAIL_BAD_LENGTH`.

Aritmética da fixture, não o AEC: `i1199_mic 28000`, `i1159_mic 32767`, linha `STATIC_AEC_ARITHMETIC PASS_FIXTURE_ONLY`.

Forma da FX-02: `STATIC_ACK_FIXTURE_CHECK PASS_FIXTURE_ONLY`.

`PASS_FIXTURE_ONLY` significa só que os arquivos estáticos bateram entre si. Não promove O28, O58 nem qualquer outro oráculo a executado. O Codex da v0.4 não adotou a alegação anterior como evidência independente; esta também não pede isso.
