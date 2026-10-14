# CMP-FD-00 v0.4 — Índice e status

**Estado do pacote:** PROPOSTA. **CANDIDATE FOR CODEX REVIEW**. Não é PASS. O autor não fecha finding.
**SHA auditado da v0.3:** `2fe0b0b2b75f2fc1430f639839e2d29d563f6dcb`. Veredito daquele SHA: FAIL DOCUMENT-ONLY, parecer `docs/reviews/PARECER-CODEX-FULL-DUPLEX-v0.3-2026-10-14.md`.
**Prompt desta rodada:** `docs/reviews/PROMPT-GROK-FULL-DUPLEX-v0.4-CORRECTIVE.md`.
**Pasta:** `docs/planning/conversational-full-duplex-v0.4/`. Aditiva. Não edita v1.7, CMP v0.3, full-duplex v0.1, v0.2, v0.3, ata, ADR nem parecer.
**Schema proposto:** `forge.conversation.delta.v3`, nasce desligado. Não integra `forge.conversation.delta.v2`. Não autoriza migration, deploy nem BUILD-00.

## Arquivos

| Arquivo | Papel |
|---|---|
| CMP-FD-00-INDEX.md | este índice |
| CMP-FD-01-LEDGER-SETTLEMENT-TENANT-CAS.md | fatia no settlement, cadeia até Reservation, replay antes do CAS, unicidade composta |
| CMP-FD-02-MEDIA-CONTRACT.md | HELLO / HELLO_ACK_SUCCESS / HELLO_ACK_ERROR, ACK, digest, campos fora do envelope, crosswalk speech |
| CMP-FD-03-LIFECYCLE.md | preservação de MEDIUM-01 |
| CMP-FD-04-POLICY.md | preservação de MEDIUM-02 e MEDIUM-03; prazo de corte fora do envelope |
| CMP-FD-05-UX.md | preservação de MEDIUM-04 |
| CMP-FD-06-OBSERVABILITY.md | preservação de MEDIUM-05; tolerância fora do envelope |
| CMP-FD-07-ORACLES.md | O37 expandido, O41..O52, LOW-01 OPEN BLOCKING, AEC aditivo |
| CMP-FD-08-TRACEABILITY.md | achado para path:line |
| CMP-FD-09-CHANGE-REPORT.md | o que esta pasta acrescenta e o que não toca |
| CMP-FD-10-FINDING-DISPOSITION.md | causa, texto, path:line, negativo, status CANDIDATE |
| CMP-FD-11-OPEN-QUESTIONS.md | o que continua sem decisão humana |
| CMP-FD-12-CONSISTENCY-REPORT.md | checagens do autor, inclusive o digest estático |
| CMP-FD-13-MIGRATION-ROLLBACK.md | passos especificados e não executados |
| fixtures/CMP-FD-FX-01-events.json | oito eventos com `event_digest` |
| fixtures/CMP-FD-FX-01-digest-vectors.json | `canonical_utf8` e sha256 por evento |
| tools/check_fd_fx01_digests.py | verificador stdlib; não é teste de produto |

## O que o Codex já fechou e esta pasta não reabre

HIGH-01, HIGH-02, NEW-HIGH-01, NEW-HIGH-02, NEW-MEDIUM-02, MEDIUM-01, MEDIUM-02, MEDIUM-03, MEDIUM-04, MEDIUM-05. As páginas 03, 04, 05 e 06 repetem o invariante fechado só para o pacote não depender de edição da v0.3.

## O que esta pasta propõe, sem se declarar fechado

| ID no parecer v0.3 | Proposta v0.4 | Status do autor |
|---|---|---|
| NEW-HIGH-04 | fatia e root no settlement; zero movimento se a fatia não comporta | CANDIDATE |
| NEW-HIGH-03 | predicado e FK até Reservation; O37 por elo | CANDIDATE |
| NEW-MEDIUM-01 | `command_commit` antes do CAS | CANDIDATE |
| HIGH-03 | união de preâmbulo, ACK, payloads, crosswalk | CANDIDATE |
| NEW-MEDIUM-04 | os dois nomes saem de `observation` e vão para configuração | CANDIDATE |
| NEW-MEDIUM-05 | JSON separado, vetores e verificador | CANDIDATE; a checagem estática não é PASS |
| NEW-MEDIUM-03 | microfone = clamp(eco + humano) | CANDIDATE |
| NEW-MEDIUM-06 | unique parcial `(organization_id, project_id, session_id)` | CANDIDATE |
| LOW-01 | pessoa PENDING, effort UNSTATED, DoR NOT MET | OPEN BLOCKING DoR |

## Decisões do Founder

APPROVED, não reabertas: AQ-01, AQ-02, AQ-03, AQ-05, AQ-06, AQ-07, AQ-08, AQ-10, AQ-11.
DEFERRED ou UNDECIDED: AQ-04, AQ-09, AQ-12.
AQ-07 continua exigindo full-duplex natural no MVP. Half-duplex não é equivalente. Não há downgrade no handshake de erro.

## Gates que permanecem

FDP-14 PENDING. FDP-15 PENDING. Incorporação na baseline PENDING. BUILD-00 não iniciado. 91 oráculos v1.7 NOT RUN. 36 CMP-O NOT RUN. CMP-FD-O01..O40 NOT RUN. CMP-FD-O41..O52 NOT RUN. CMP-O-28 não é CMP-FD-O28.

O teto de builds de produto não foi fundido no teto conversacional. Fundir os dois seria decisão humana nova, não reabertura de AQ-10.
