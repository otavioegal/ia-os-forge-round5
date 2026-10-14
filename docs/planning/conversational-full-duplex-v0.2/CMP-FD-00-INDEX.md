# CMP-FD-00 v0.2 — Índice do pacote corretivo full-duplex

**Estado de entrega:** CANDIDATE FOR CODEX REVIEW.
**Este pacote não é PASS.** Nenhum finding deste ciclo é declarado fechado pelo autor.
**Não autoriza** BUILD-00, FDP-14, FDP-15, integração à baseline v1.7, contratação, credencial, staging, deploy ou execução de software.

## O que este diretório é

Versão corretiva **aditiva** depois do FAIL documental Codex sobre o pacote v0.1. Os arquivos auditados não são reescritos.

| Fonte congelada | SHA | O que permanece |
|---|---|---|
| Baseline v1.7 | `0c42373d583dec420348efd7bc0b8c6228a66f47` | PASS documental histórico. Contratos históricos não editados. |
| CMP v0.3 | `f404abc1b4a90f01a12266e3e56a65df277258dd` | PASS WITH CONDITIONS. Fotografia intacta, inclusive o texto que ainda descrevia half-duplex. |
| Pacote full-duplex v0.1 auditado | `97ee817ca8262b3a0bae996c510b935435b2e575` | FAIL DOCUMENT-ONLY. Não é reaberto como se tivesse passado. |
| Parecer | `docs/reviews/PARECER-CODEX-FULL-DUPLEX-v0.1-2026-10-13.md` | Imutável. |
| Prompt corretivo | `docs/reviews/PROMPT-GROK-FULL-DUPLEX-v0.2-CORRECTIVE.md` | Imutável. |
| Ata do Founder | `docs/governance/ATA-FOUNDER-AQS-CONVERSATIONAL-2026-10-13.md` | Imutável. Nove decisões não são reabertas. |
| ADR AQ-07 | `docs/governance/ADR-FDR-AQ07-FULL-DUPLEX-MVP-2026-10-13.md` | Imutável. Prevalece como decisão de produto full-duplex. As AQ que o ADR ainda listava como pendentes foram resolvidas **depois**, pela ata, não por este pacote. |

Parent de trabalho lido: `c43fad4bbdd74c8157d6c1b424f0311c3c1d011c` (parecer e prompt já arquivados). Este diretório é o único acréscimo pretendido.

## Mapa

| Arquivo | Função |
|---|---|
| [CMP-FD-01-LEDGER-DELTA.md](CMP-FD-01-LEDGER-DELTA.md) | Delta normativo proposto de FDP-16A/FDP-15. HIGH-01. |
| [CMP-FD-02-MEDIA-CONTRACT.md](CMP-FD-02-MEDIA-CONTRACT.md) | Schema `cmp.media.duplex.v1` e crosswalk com `cmp.speech.v0`. HIGH-03. |
| [CMP-FD-03-LIFECYCLE.md](CMP-FD-03-LIFECYCLE.md) | Máquinas de playback, TTS, modelo e ledger. MEDIUM-01. |
| [CMP-FD-04-POLICY-SECURITY-PRIVACY.md](CMP-FD-04-POLICY-SECURITY-PRIVACY.md) | Consent epoch, trust boundary, classificação. MEDIUM-02 e MEDIUM-03. |
| [CMP-FD-05-UX.md](CMP-FD-05-UX.md) | UX simultânea e proveniência. MEDIUM-04. |
| [CMP-FD-06-OBSERVABILITY.md](CMP-FD-06-OBSERVABILITY.md) | Pontos de medição sem SLA. MEDIUM-05. |
| [CMP-FD-07-STORIES-ORACLES-FIXTURES.md](CMP-FD-07-STORIES-ORACLES-FIXTURES.md) | Histórias, fixtures e oráculos. HIGH-02 e LOW-01. |
| [CMP-FD-08-TRACEABILITY.md](CMP-FD-08-TRACEABILITY.md) | Rastro AQ, findings, oráculos e contratos. |
| [CMP-FD-09-CHANGE-REPORT.md](CMP-FD-09-CHANGE-REPORT.md) | O que mudou e o que não foi tocado. |
| [CMP-FD-10-FINDING-DISPOSITION.md](CMP-FD-10-FINDING-DISPOSITION.md) | Mapa de correção. Fechamento **não** declarado. |
| [CMP-FD-11-OPEN-QUESTIONS.md](CMP-FD-11-OPEN-QUESTIONS.md) | AQ diferíveis e gates pendentes. |
| [CMP-FD-12-CONSISTENCY-REPORT.md](CMP-FD-12-CONSISTENCY-REPORT.md) | Checagens documentais do autor. Não é auditoria. |

## Decisões humanas — não reabertas

| ID | Estado neste pacote |
|---|---|
| AQ-01, AQ-02, AQ-03, AQ-05, AQ-06, AQ-07, AQ-08, AQ-10, AQ-11 | APPROVED pelo Founder, na ata e, para AQ-07, também no ADR. |
| AQ-04, AQ-09, AQ-12 | DEFERRED / UNDECIDED. |
| FDP-14, FDP-15, consolidação da baseline, BUILD-00 | PENDING. |

Aprovação humana não é aprovação técnica. O desenho abaixo é proposta para revisão independente.

## Oráculos que este pacote não executa

| Conjunto | IDs | Estado |
|---|---|---|
| v1.7 | 91 oráculos históricos | NOT RUN. Não renumerados. |
| CMP v0.3 | CMP-O-01 .. CMP-O-36 | NOT RUN. Evidence ABSENT. CMP-O-28 não é substituído. |
| Full-duplex v0.1 | CMP-FD-O01 .. CMP-FD-O12 | NOT RUN. Evidence ABSENT. IDs preservados. O texto de aceite é corrigido aqui. |
| Novos | CMP-FD-O13 .. CMP-FD-O34 | NOT RUN. Evidence ABSENT. Sem colisão com os doze anteriores nem com CMP-O-28. |

## Pedido de auditoria

Solicita-se revisão Codex independente, somente leitura, documental, sobre este diretório e o encaixe no ledger v1.7 e no CMP v0.3. O revisor não deve tratar este índice como evidência de PASS, de teste executado ou de autorização de BUILD-00.
