# IA OS Forge — Pacote executivo de decisão do Founder
**Estado:** PROPOSTA PARA DELIBERAÇÃO — NENHUMA APROVAÇÃO PRESUMIDA  
**Data:** 2026-10-13  
**Baseline auditada:** v1.7, SHA `0c42373d583dec420348efd7bc0b8c6228a66f47`  
**Parecer independente:** `docs/reviews/PARECER-CODEX-ROUND10-2026-10-13.md` — PASS **documental**; LOW-01 editorial não bloqueante  
**Escopo deste documento:** apresentar os gates do Founder; não é deliberação e não autoriza BUILD-00.

## 1. Três deliberações distintas

**D-01: FDP-14 v1.0 — Observability & Evaluation Architecture.** Texto-fonte preservado em `historical/round4/docs/source-material/chat-extracts/FDP-14-v1.0__msg080.md`, status DRAFT → REVIEW e validação do Founder pendente. Proposta: confirmar seus princípios e decisões, como padrão OpenTelemetry, logs estruturados com redação de dados sensíveis, rastreabilidade por project/task/attempt, custos estimados versus confirmados, métricas de autonomia, evidências para status de Ready for Human Test, avaliação de modelos sem LLM como única autoridade e proibição de percentuais inventados. Essa confirmação não afirma que telemetria esteja implementada ou metrificada.

**D-02: FDP-15 v1.0 — Integration / Adapter Specification.** Texto-fonte preservado em `historical/round4/docs/planning/FDP-15-v1.0-INTEGRATION-ADAPTER-SPECIFICATION.md`, status DRAFT → REVIEW e aprovação do Founder pendente. Proposta: aprovar os contratos ForgeContract → Adapter → Provider; três famílias Engine/Model/Tool; capability registry; fronteira de segredos, idempotência estável por operação, health, fallback sujeito à classificação de dados, testes por doubles e anti-lock-in; OpenRouter opcional e AIOX não exclusivo. **Pontos explicitamente propostos no próprio FDP-15**: eventuais deltas de esquema em Capability Registry (§12); registro persistido da idempotência (§21); alternativa registrada ou ausência documentada para capabilities críticas (§29.9); confirmar Google/WhatsApp no backlog do MVP conforme caso de uso (§47). Não converter automaticamente PROPOSTA em aprovação anterior: registrar decisão do Founder no gate.

**D-03: baseline documental consolidada v1.7 — Round 10.** O Codex confirmou PASS DOCUMENTAL no SHA acima, com 91 oráculos especificados (NOT RUN), 41 histórias, 17 P0 históricos e 11 estados Task. A aprovação do Founder, se concedida, apenas congela a referência documental para preparação operacional; não dispensa evidências de implementação, testes, segurança nem outros gates.

## 2. Resumo sem linguagem técnica

- **FDP-14:** “Como a plataforma provará o que os agentes fizeram, quanto custou e se funcionou?”
- **FDP-15:** “Como a plataforma conversará com outros serviços sem entregar a eles o controle do sistema?”
- **v1.7:** “Os documentos técnicos passaram na auditoria; posso aceitá-los como referência oficial para preparar a construção?”

## 3. Decisões a colher do Founder

| Gate | Alternativas | Situação atual |
|---|---|---|
| FDP-14 | APROVAR / APROVAR COM RESSALVAS / DEVOLVER PARA AJUSTES | PENDENTE |
| FDP-15, incluindo suas PROPOSTAS identificadas | APROVAR / APROVAR COM RESSALVAS e decisões por proposta / DEVOLVER PARA AJUSTES | PENDENTE |
| Baseline v1.7 SHA `0c42373…` | APROVAR COMO BASELINE DOCUMENTAL / DEVOLVER PARA AJUSTES | PENDENTE |
| BUILD-00 | AUTORIZAÇÃO EM ATO SEPARADO, posterior | NÃO AUTORIZADO |

**Critério:** não deduzir aprovação de silêncio, continuação da conversa, parecer de Codex ou publicação em GitHub. Registrar declaração expressa e ressalvas em ata/ADR identificável, vinculada ao SHA. Evitar atribuir ao Founder aprovação de versões diferentes sem nova decisão.

## 4. Pré-requisitos para uma futura autorização de BUILD-00

- Aprovação ou resolução formal de FDP-14/FDP-15 e da baseline v1.7.
- Responsável, esforço e timebox das histórias planejadas: DoR operacional permanece NOT MET.
- Delimitação explícita de ambiente de trabalho/sandbox, orçamento, permissões, segredos, execução autônoma e hard gates.
- Plano de construção e de verificação com Builder Claude Code, auditoria independente Codex e framework Synkra AIOX; preservar separação de responsabilidades.
- Testes, staging, produção e efeitos externos têm gates próprios; nenhum oráculo foi executado até este registro.

## 5. Próximo ato proposto

Apresentar D-01, D-02 e D-03 ao Founder; registrar decisões expressas. Após isso, produzir um **BUILD-00 PRE-FLIGHT** operacional, sem iniciar coding/deploy automaticamente. O finding LOW-01 no FDP-17 v1.7 é apenas correção editorial futura; a baseline aprovada documentalmente pelo Codex permanece identificada pelo SHA auditado.

**Fontes:** `docs/reviews/PARECER-CODEX-ROUND10-2026-10-13.md`; `historical/round4/docs/source-material/chat-extracts/FDP-14-v1.0__msg080.md`; `historical/round4/docs/planning/FDP-15-v1.0-INTEGRATION-ADAPTER-SPECIFICATION.md`; `docs/reviews/ROUND10-OPEN-PENDENCIES-2026-10-13.md`.
