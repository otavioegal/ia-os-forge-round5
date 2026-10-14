# CMP-FD-12 v0.4 — Relatório de consistência do autor

**Isto não é evidência de fechamento.** O parecer v0.3 já recusou o relatório do próprio autor como prova. O Codex independente relê o SHA. Status do pacote: CANDIDATE FOR CODEX REVIEW. Não é PASS.

## O que foi conferido no texto, sem teste de produto

| Checagem | Resultado do autor |
|---|---|
| Leitura monetária antes do lock do Build | não encontrada; o primeiro lock está em CMP-FD-01:43 |
| `OpenConversationalAnchor` aceitando `budget_limit_minor` | rejeitado, CMP-FD-01:12, `422 UNKNOWN_FIELD` |
| Settlement só pelo estimate | substituído pela conta da fatia, CMP-FD-01:33 |
| Subtrair E duas vezes | explicitamente proibido, CMP-FD-01:36 |
| CAS antes do lookup de `command_id` | invertido, CMP-FD-01:48 antes da linha 49 |
| Unique só em `session_id` | negado, CMP-FD-01:147 e CMP-FD-13:11 |
| `consent_stop_deadline_ns` dentro de `observation` | negado, CMP-FD-02:92 e CMP-FD-04:19 |
| `observation_tolerance_ns` dentro de `observation` | negado, CMP-FD-02:92 e CMP-FD-06:12 |
| `mic[i] = 16000` apagando eco | substituído por soma e clamp, CMP-FD-07:151 |
| `HELLO_ACK` único exigindo campos de sucesso no erro | separado em SUCCESS e ERROR, CMP-FD-02:50 |
| `PLAYBACK_SPAN` ou os seis carimbos removidos | presentes, CMP-FD-02:86-88 |
| Ledger paralelo ou moeda nova | negados, CMP-FD-01:16 |
| Downgrade para half-duplex | negado, CMP-FD-02:77 |
| CMP-O-28 substituído por CMP-FD-O28 | negado, CMP-FD-05:10 e CMP-FD-07:5 |
| História marcada Ready | não; CMP-FD-07:7-23 permanece OPEN BLOCKING DoR |
| Flag v3 ligada, ou v2 integrada | não; CMP-FD-13:14 |

Essas linhas são a leitura do autor. Não são auditoria.

## Checagem estática de fixture

Não é teste de produto, não executa O01..O52, não é migration e não é BUILD-00.

| Item | Valor |
|---|---|
| Comando | `python3 tools/check_fd_fx01_digests.py` a partir da pasta do pacote, caminho absoluto no ambiente do autor `/workspace/artifacts/fd-v04/tools/check_fd_fx01_digests.py` |
| Interpretador | Python 3.10.22 |
| Código de saída | 0 |
| Última linha | `STATIC_FIXTURE_DIGEST_CHECK PASS_FIXTURE_ONLY` |

`PASS_FIXTURE_ONLY` significa só que os oito `event_digest` armazenados batem com o SHA-256 do JSON canônico descrito em CMP-FD-02:116-123 e com a coluna `sha256` do arquivo de vetores. Não significa que o pacote passou.

| Índice | Rótulo | sha256 |
|---|---|---|
| 0 | G0 OUTPUT | `850ed372de0f47d47d40b777274dc6eddcb6ab2989a36801d159b1d1871cd04c` |
| 1 | G0 SPAN | `bd56e4057353a017c34dcd24a95e627460edd78f73c8ab4ebb792706e340c140` |
| 2 | I0 INPUT | `8348bfbffe533905987410923dafe416db167efc3f1cda59c59fecf8193293ca` |
| 3 | G1 OUTPUT | `93700e9614a1d89006646c6a9a32f3ed44281c01480f85ca9a54e59068ea2a02` |
| 4 | G1 SPAN | `2f146eb304051b712297d0dbb93d411194cc8c53fee9a2546bd158e6152b4de3` |
| 5 | I1 INPUT | `25eaa9fb47868cf3992c029dcd6d045fdf817323281090e90d9f3a4ff352c244` |
| 6 | G2 OUTPUT | `b91ce3a655afd359eed1f5cc4fc5f711673ff8d9a3062f0784cbcccf80c50cbc` |
| 7 | G2 SPAN | `872bd9d774cac70f0e4045b0626f42203bb4ce78aad797ce2404c17d2de83a7a` |

O primeiro digest, G0 OUTPUT, é o mesmo algoritmo já usado na v0.3 para aquele corpo. A v0.4 não troca o algoritmo; tira o corpo do Markdown.

## O que esta página não afirma

Não afirma que NEW-HIGH-04, NEW-HIGH-03, NEW-MEDIUM-01, HIGH-03, NEW-MEDIUM-03, NEW-MEDIUM-04, NEW-MEDIUM-05 ou NEW-MEDIUM-06 estejam fechados. Não afirma que LOW-01 esteja resolvido. Não afirma que os 91 oráculos v1.7, os 36 CMP-O ou os CMP-FD-O tenham corrido. Não pede integração na baseline.
