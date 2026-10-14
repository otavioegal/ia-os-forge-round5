# Prompt Grok — DELTA CONVERSATIONAL-MVP v0.2 — Fechamento dirigido do Codex

**Repositório:** https://github.com/otavioegal/ia-os-forge-round5
**Commit original do delta auditado:** cad1ac6d6bb8a970165ebd17ce1bff13d98af806
**Parecer independente obrigatório:** docs/reviews/PARECER-CODEX-CMP-v0.1-2026-10-13.md
**Meta:** DELTA CONVERSATIONAL-MVP v0.2 — CANDIDATE FOR CODEX REVIEW. Não autodeclare PASS.

Leia integralmente o parecer independente, todos os arquivos CMP-00 a CMP-06, riscos, questões abertas, decisão funcional do Founder e contratos baseline v1.7. Corrija somente os findings HIGH-01, MEDIUM-01/02/03 e LOW-01 listados. Não reabra a baseline v1.7, que recebeu PASS documental histórico no SHA 0c42373d583dec420348efd7bc0b8c6228a66f47. Não autorize BUILD-00 nem execute software.

## HIGH-01 — independência real do reviewer
Formal review por Codex requer novo review_run_id, principal distinto do Builder, runtime/contexto independente e memória reconstruída exclusivamente a partir de entradas admitidas pelo gate. Proibir transferência de estado oculto, cache, conversation session, score, review candidate/verdict e tool state do Builder. Distinga Codex consultado em chat read-only de Codex executando revisão formal. Ampliar CMP-O-28 ou criar oracle com fixture adversarial incluindo scratch marker, score/verdict, session/cache e credencial/actor id do Builder; PASS somente se tudo estiver ausente do review formal e o principal auditado for independente. Nenhum bypass via Conselho ou Jarvis.

## MEDIUM-01 — STT/TTS
Produzir contratos versionados e provider-agnostic input/output/error para speech.transcribe e speech.synthesize, transcript partial/final, audio encoding, mime/formato, idioma, streaming, cancelamento confirmado, negociação de versão e taxonomia de erros retryable/terminal. Atualizar oráculos para demonstrar validade, falha, cancelamento e fallback a texto, sem eliminar voz do MVP.

## MEDIUM-02 — Retry depois de dispatch
Harmonizar CMP-01:141, CMP-02:223 e oráculos CMP-O-15/16/29 com tabela de resultado por: antes do dispatch, chamada recebida com resultado incerto, falha conclusiva/no-effect, HELD pendente de reconciliação e efeito conclusivo. Proibir redespacho em resultado incerto; definir quando nova tentativa pede nova operação/turn e quando apenas replay retorna resultado. Não criar segundo ledger, não enfraquecer FDP-16A, não fabricar comprovante.

## MEDIUM-03 — custos rastreáveis
Atualizar CMP-O-31 ou adicionar oracle com dois providers/models, várias operações por sessão e turn. Exigir atribuição por session_id, turn_id, agent_id, model_id/provider_id ou capability de voz, somas por sessão exclusivamente derivadas de operações reais, distinção de estimativa e custo confirmado, sem tarifa de Conselho oculta ou dupla cobrança.

## LOW-01 — consentimento
Resolver consent_id non-null versus início text-only: optar por nullable com validação ou registro explícito de consentimento NEGADO/NÃO-CONCEDIDO, ou separar consentimento de mic de política de retenção. Nunca captar áudio/STT sem consentimento válido.

## Questões de Founder e governança
As 12 AQ devem continuar visíveis, sem autoaprovação. AQ-01/02/03/05/06/07/08/10/11 precisam de decisão do Founder antes da integração normativa; AQ-04/09/12 podem ficar deferidas sob deny-by-default/HELD. Produza quadro executivo de decisões, com recomendação e riscos, mas não marque como decisão humana já tomada. Não escolha fornecedor nem gastos.

Entregue pacote CMP v0.2 em nova subpasta ou versionamento aditivo rastreável, preservando v0.1 e os pareceres históricos intactos, com status index, change report, finding closure, matrix e consistency report. Preserve os 13 stories e 34 oracles originais, acrescentando só o mínimo necessário. Tudo NOT RUN. Faça commit no GitHub e informe SHA. O Codex auditará de modo independente.
