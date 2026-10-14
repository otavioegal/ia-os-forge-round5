# IA OS Forge — Pacote de deliberação arquitetural do Founder (AQ remanescentes)

**Data:** 13/10/2026
**Estado:** **PROPOSTAS NÃO APROVADAS**, exceto AQ-07 (full-duplex) em `ADR-FDR-AQ07-FULL-DUPLEX-MVP-2026-10-13.md`.
**Fonte:** `docs/planning/conversational-mvp-v0.3/CMP-AQ-FOUNDER-DECISIONS.md`; parecer Codex CMP v0.3.
**Autoridade:** não inferir aceite das recomendações pela continuidade dos trabalhos. Deliberação expressa do Founder será registrada em documento separado.
**Limite:** não autoriza BUILD-00, contratos, provedor, teste ou alteração retroativa da baseline v1.7.

## Resumo: oito decisões ainda necessárias antes de integrar o CMP

| AQ | O que o Founder está autorizando | Recomendação conservadora | Situação |
|---|---|---|---|
| **AQ-01** | Quem tem permissão de reservar gastos quando fala com IA | Criar papel mínimo `conversation_router`, que usa a MESMA transação de reserva da v1.7; nunca fingir que é `coding_engine`; negar chamada fora do gateway | **PENDENTE** |
| **AQ-02** | Como identificar financeiramente a conversa | Uma Task-âncora por sessão, fora da execução de build, `task_id` obrigatório, sem acesso a deploy/terminal/vault | **PENDENTE** |
| **AQ-03** | Como integrar serviços de voz sem prender o Forge a fornecedor | STT/TTS como capabilities **TOOL**, mantendo famílias Engine/Model/Tool do FDP-15; contrato de streaming bidirecional em gateway sem “quarta família” informal | **PENDENTE; FDP-15 separado** |
| **AQ-05** | Que informações podem sair para serviços externos de voz | Quatro classes PUBLIC/INTERNAL/CONFIDENTIAL/RESTRICTED; nenhum dado de projeto é PUBLIC por padrão; CONFIDENTIAL/RESTRICTED não saem para speech externo; local/política autorizada para conteúdo restrito | **PENDENTE** |
| **AQ-06** | Se guardar gravações e textos das conversas | Áudio bruto não armazenado por padrão; transcrição conforme política explícita da organização, com período/eliminação definidos antes de uso real; sem retenção indefinida por omissão | **PENDENTE** |
| **AQ-08** | Como ligar o microfone na conversa full-duplex | Sessão de voz iniciada **expressamente** e apenas com consentimento; uma vez iniciada, escuta contínua **durante a sessão** para permitir interrupção natural. Microfone desligado quando sessão termina ou é pausada; não há escuta em background | **PENDENTE** |
| **AQ-10** | Como controlar orçamento de voz e conselhos | Reutilizar exclusivamente o ledger v1.7 (`spent+reserved <= limit`), sem taxa oculta, segundo ledger ou cobrança duplicada | **PENDENTE** |
| **AQ-11** | Se a voz identifica/autentica o usuário | **Não usar biometria de voz no MVP**; comando falado sozinho não aprova deploy, gasto, credencial ou mudança irreversível | **PENDENTE** |

As recomendações são **propostas técnicas**, não escolhas obrigatórias aprovadas. Há impactos em segurança, privacidade e orçamento, mas não exigem que o Founder escolha um SDK ou escreva SQL; os detalhes continuam para arquitetos/Builder e Codex.

## AQ-07 — decisão já registrada

**APROVADA:** FULL-DUPLEX natural no MVP com todos os agentes, Jarvis e Conselho Técnico; half-duplex com barge-in não basta. Essa decisão **não aprova automaticamente AQ-08**: iniciar explicitamente o microfone é opção recomendada, ainda pendente de escolha.

## Questões que podem ser adiadas (sob regras vinculantes)

- **AQ-04 — Modelo/provider conversacional:** escolher mais tarde; até então deny-by-default, classificação antes do envio, nenhum grant novo de coding engine.
- **AQ-09 — Código compartilhado com Founder OS:** adiar; não presumir código, banco, memória ou sessão compartilhada.
- **AQ-12 — Prova de custo do fornecedor:** escolha de vendor adiada; sem proof ingerível por `forge.provider_ingest` a reserva permanece HELD, sem inventar recibo nem liberar custo automaticamente.

## Ata futura da decisão

Caso o Founder confirme explicitamente as oito recomendações, criar ata com AQs individualmente marcadas **APROVADAS PELO FOUNDER**, referência a este pacote e SHA do commit. Se o Founder alterar uma recomendação, documentar exceção e análise de impacto. Não é gate de BUILD.

## Próximos passos depois da deliberação

1. Preparar delta normativo full-duplex em CMP-01/02/03/04/05/06, FDP-11 (ainda não recuperado), FDP-13/14/15/16 e protocolos financeiros quando requerido por AQ-01/AQ-02. Preservar v1.7 e v0.3.
2. Codex independente avalia somente as novas decisões, contratos, regras e oráculos. HIGH-01 e demais findings anteriores não devem reabrir sem regressão demonstrada.
3. Tratar separadamente gates FDP-14/FDP-15 e aprovação da baseline consolidada.
4. Planejar BUILD-00 preflight; nenhum desenvolvimento autorizado automaticamente.
