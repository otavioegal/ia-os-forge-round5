# Prompt oficial Grok — DELTA CONVERSATIONAL-MVP v0.1

Repositório: https://github.com/otavioegal/ia-os-forge-round5
Papel: Grok, builder DOCUMENTAL. Entrega: DELTA CONVERSATIONAL-MVP v0.1 — CANDIDATE FOR CODEX REVIEW, nunca PASS.

Leia antes de alterar: `docs/governance/FOUNDER-DECISION-JARVIS-VOICE-ALL-AGENTS-MVP-2026-10-13.md`, `docs/governance/ADDENDUM-CONVERSATIONAL-COUNCIL-JARVIS-2026-10-13.md`, `docs/governance/IMPACT-ASSESSMENT-CONVERSATIONAL-MVP-2026-10-13.md`, `docs/reviews/PARECER-CODEX-ROUND10-2026-10-13.md`, baseline normativa v1.7, fontes históricas FDP-13/14/15 e, se encontrada, fonte verificável FDP-11. Se FDP-11 não estiver presente, documente lacuna; não invente conteúdo ou aprovações.

## Decisão funcional obrigatória
No MVP já testável, o Founder terá: (1) Jarvis com voz natural e texto; (2) conversa 1:1 com TODOS os agentes oferecidos, voz e texto com interface universal; (3) Conselho Técnico multiagente por voz e texto, com identidade de cada turno, divergências, interrupção, ata e evidências. São três modalidades obrigatórias e não podem ser adiadas. Mesma experiência de interface NÃO significa iguais permissões.

## Artefatos a entregar em docs/planning/conversational-mvp/
- CMP-01-PRD-UX-JOURNEYS.md: telas de ponta a ponta, contexto, seleção de agente, Conselho, mic, áudio, transcrição, interrupção, estados de falha e acessibilidade;
- CMP-02-SYSTEM-ARCHITECTURE.md: sessão/turno, context builder, router, orquestração, adaptação STT/TTS, áudio, provedor agnóstico, idempotência e fallback seguro;
- CMP-03-SECURITY-PRIVACY-AND-REVIEW-INDEPENDENCE.md: escopos org/projeto, voice spoofing, consentimento/retenção, classificação de dados, injeção por voz, hard gates e Codex reviewer independente;
- CMP-04-OBSERVABILITY-EVIDENCE-AND-COST.md: eventos/traces por turno, origem de respostas, citações de evidência, medição real versus estimativa e custos de voz/conselho;
- CMP-05-ADDITIVE-STORIES-AND-ORACLES.md: histórias CMP adicionais e oráculos positivos e negativos para TODAS as capacidades, com fixture, passos, PASS/FAIL e estado NOT RUN;
- CMP-06-TRACEABILITY-AND-IMPACT.md: impacto documentado em FDP-11/13/14/15/16/17/19/19A, rastreabilidade desde o pedido do Founder até UX, API, agente, permissão, teste e custo;
- índice do pacote, open questions, risks e consistency report.

## Restrições
1. Preserve integralmente a baseline v1.7 e seus 91 oráculos, 41 histórias, 17 P0 e 11 estados Task. NÃO renumere nem sobrescreva; use IDs prefixados CMP para adições. Históricos e parecer Codex Round10 intocados.
2. A fala não substitui autenticação/confirmacão formal para gasto, deploy, segredos ou operação destrutiva. Jarvis não eleva privilégios de ninguém. Codex pode explicar achados por voz, mas não comprometer sua avaliação independente.
3. Não inventar resultados, percentuais de progresso, custos medidos ou evidências. Caso não existam, declarar inexistentes.
4. Reutilizar conceitos do Conselho Consultivo/Founder OS sem acoplamento indevido. Minimizar áudio armazenado; opção de texto acessível e fallback em incidentes, sem excluir voz do MVP.
5. Provider de voz não escolhido nem contratado sem governança. Model Router e fallback respeitam classificação de dados e orçamento. OpenRouter opcional.
6. Desenvolver como especificação, NÃO implementar software, testar providers, gastar com APIs ou fazer deploy.
7. Gerar relatório de verificação documental e commit não destrutivo no GitHub, informando SHA. Após entrega, Codex auditará o delta independentemente.
8. FDP-14/FDP-15 continuam pendentes de deliberação do Founder; não autorizar BUILD-00.

Critério de aceitação: cada funcionalidade da decisão do Founder deve estar ligada a um fluxo, um contrato, uma política, um oracle e evidência futura. Evite reabrir o Round10; revisão isolada do incremento conversacional.
