# DELTA CONVERSATIONAL-MVP v0.1 — índice do pacote

**Estado:** DELTA CONVERSATIONAL-MVP v0.1 — CANDIDATE FOR CODEX REVIEW. DRAFT / NOT APPROVED / NOT READY FOR BUILD / NO BUILD-00 AUTHORIZATION.
**Não é PASS.** Não é parecer do Codex. Não é aprovação do Founder. Não autoriza BUILD-00.
**Nenhum teste de software foi executado.** Nenhum staging. Nenhuma API paga. Nenhum provider de voz foi escolhido ou contratado.
**Baseline intocada:** v1.7, SHA auditado `0c42373d583dec420348efd7bc0b8c6228a66f47`, PASS DOCUMENTAL somente daquele SHA no parecer Round 10. Este delta não reabre NEW-MEDIUM-12 nem reescreve os 91 oráculos, as 41 histórias, os 17 P0 ou os 11 estados Task.
**FDP-14 e FDP-15:** continuam pendentes de deliberação humana. Citá-los não os aprova.

## Língua

Contratos técnicos CMP-01 a CMP-06 estão em inglês, no mesmo registro dos FDP normativos. Este índice, as questões abertas, os riscos e o relatório de consistência estão em português.

## O que este pacote é

Especificação aditiva da decisão funcional `docs/governance/FOUNDER-DECISION-JARVIS-VOICE-ALL-AGENTS-MVP-2026-10-13.md`. A seção de fases e a pergunta aberta sobre voz do addendum foram substituídas por essa decisão. Os demais princípios do addendum permanecem: fato versus inferência versus sugestão, Codex read-only, fala não autoriza efeito irreversível, minimização, conselho como workflow, “mostrar evidência” abre registro real.

Três modalidades são obrigatórias no primeiro MVP testável e não podem ser adiadas:

1. Jarvis por voz e por texto.
2. Conversa 1:1 por voz e por texto com todos os agentes oferecidos, na mesma interface. A mesma interface não iguala permissões.
3. Conselho Técnico multiagente por voz e por texto, com identidade de turno, divergência, interrupção, ata e evidências.

## Arquivos

| Arquivo | Papel |
|---|---|
| [CMP-01-PRD-UX-JOURNEYS.md](CMP-01-PRD-UX-JOURNEYS.md) | Jornadas, telas, compositor universal, falhas, acessibilidade |
| [CMP-02-SYSTEM-ARCHITECTURE.md](CMP-02-SYSTEM-ARCHITECTURE.md) | Sessão, turno, contexto, router, STT/TTS, idempotência, fallback |
| [CMP-03-SECURITY-PRIVACY-AND-REVIEW-INDEPENDENCE.md](CMP-03-SECURITY-PRIVACY-AND-REVIEW-INDEPENDENCE.md) | Escopo, consentimento, classificação, gates, reviewer |
| [CMP-04-OBSERVABILITY-EVIDENCE-AND-COST.md](CMP-04-OBSERVABILITY-EVIDENCE-AND-COST.md) | Eventos, origem, evidência, custo sem números inventados |
| [CMP-05-ADDITIVE-STORIES-AND-ORACLES.md](CMP-05-ADDITIVE-STORIES-AND-ORACLES.md) | Histórias CMP-S e oráculos CMP-O, todos NOT RUN |
| [CMP-06-TRACEABILITY-AND-IMPACT.md](CMP-06-TRACEABILITY-AND-IMPACT.md) | Impacto FDP-11/13/14/15/16/17/19/19A e classificação das decisões |
| [CMP-OPEN-QUESTIONS.md](CMP-OPEN-QUESTIONS.md) | Questões substantivas submetidas ao Founder |
| [CMP-RISKS.md](CMP-RISKS.md) | Ameaças e mitigação proposta |
| [CMP-CONSISTENCY-REPORT.md](CMP-CONSISTENCY-REPORT.md) | Verificação documental deste delta, não veredito Codex |

Verificador read-only: `tools/check_conversational_mvp_consistency.py`. Ele não executa produto, provider, banco ou staging, e não emite PASS de Codex.

## Autoridade

- A única tabela normativa de oráculos da baseline fechada continua sendo `docs/planning/FDP-TRACEABILITY-MATRIX-v1.7-CANONICAL.md`.
- Os oráculos CMP-O são suplementares. Não substituem, não renumeram e não emendam essa tabela.
- O único protocolo de dinheiro continua sendo FDP-16A v1.7 seções 8A a 8A.3. Este delta não cria um segundo ledger.
- FDP-11 não está neste repositório como documento normativo. A lacuna está em CMP-06. CMP-01 é proposta, não cláusula histórica recuperada.

## Fora deste pacote

Implementação, BUILD-00, escolha de fornecedor de voz, aprovação de FDP-14, aprovação de FDP-15, aprovação geral do Founder, correção editorial LOW-01, e qualquer alteração dos pareceres já publicados.
