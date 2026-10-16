# CMP-FD-00 v0.16 — Jornadas de uso do Forge

**Estado:** CANDIDATE FOR CODEX REVIEW. Não é PASS. O autor não fecha finding e não pede decisão nova ao Founder.
**Parent previsto:** `f016b1a4a32b460ee9948c2dc71f171a9146e61a` (v0.15). Este pacote não reescreve esse commit nem nenhum arquivo anterior.
**Escopo:** IA OS Forge. Não é o Founder Operating System. Não há banco, sessão, código nem memória compartilhada com ele.
**Não executado e não autorizado:** código de produto, teste, PostgreSQL, migration, deploy, provider, gasto, BUILD-00. FDP-14 e FDP-15 continuam pendentes. `forge.conversation.delta.v4` continua desligada.

## Para quem vai usar

O Founder já decidiu que o Forge conversa com o Jarvis e com qualquer agente, em texto e em voz, no jeito full-duplex, e que existe uma Sala de Conselho Técnico. Este pacote conta como isso aparece no uso. Onde um detalhe de mecanismo ainda não estava fechado, há uma proposta marcada para o Codex. Isso não é uma pergunta de volta ao Founder.

## Para quem vai revisar

| Arquivo | O que contém |
|---|---|
| CMP-FD-01 | O que já está aprovado e o que ainda é proposta |
| CMP-FD-02 | Jornada da conversa individual, texto e voz |
| CMP-FD-03 | Jornada da Sala de Conselho Técnico |
| CMP-FD-04 | Jeito natural: rapidez sem número inventado, contexto, interrupção, retomada e quem fala |
| CMP-FD-05 | O que acontece quando a pessoa fala enquanto o agente ainda responde |
| CMP-FD-06 | Troca de agente e continuidade só do contexto autorizado |
| CMP-FD-07 | Telas, estados, erros e o que fazer sem voz ou sem conexão |
| CMP-FD-08 | O que o Founder consegue conferir sem conhecimento técnico. Não foi executado |
| CMP-FD-09 | Rastreio entre decisão aprovada e requisito proposto |
| CMP-FD-10 | Findings e bloqueios, todos preservados |
| CMP-FD-11 | Limites, fontes e o que este pacote não altera |

A fotografia antiga `docs/planning/conversational-mvp-v0.3/CMP-01-PRD-UX-JOURNEYS.md` ainda descreve meia-duplex e AQ-07 aberta. Ela não é reescrita. Para a decisão humana, prevalecem a ata `docs/governance/ATA-FOUNDER-AQS-CONVERSATIONAL-2026-10-13.md` e o ADR `docs/governance/ADR-FDR-AQ07-FULL-DUPLEX-MVP-2026-10-13.md`.

Não há checker nesta pasta. Não houve oráculo. `PASS_FIXTURE_ONLY` da v0.15 não é aceitação deste uso. 508/2443 não provam produto. 480/2239 continuam rejeitados.
