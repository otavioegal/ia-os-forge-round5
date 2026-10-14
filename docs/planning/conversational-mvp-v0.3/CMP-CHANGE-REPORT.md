# Relatório de mudança — DELTA CONVERSATIONAL-MVP v0.3

**Estado:** DELTA CONVERSATIONAL-MVP v0.3 — CANDIDATE FOR CODEX REVIEW. Não é PASS. Não autoriza BUILD-00. Nenhum teste de software foi executado.

## O que não mudou

- `docs/planning/conversational-mvp/` em relação a `cad1ac6d6bb8a970165ebd17ce1bff13d98af806`.
- `docs/planning/conversational-mvp-v0.2/` em relação a `99474da514419a26ac8471c50c33697ade2a1cde`.
- Baseline v1.7 e o SHA `0c42373d583dec420348efd7bc0b8c6228a66f47`.
- Pareceres, inclusive o parecer CMP v0.2 e o prompt v0.3.
- 13 histórias CMP-S01..CMP-S13. Nenhuma história nova.
- 36 oráculos CMP-O-01..CMP-O-36. Nenhum id novo. Todos NOT RUN.
- Contratos fechados pelo parecer v0.2: schemas STT/TTS, tabela de retry, atribuição de custo, consentimento text-only. Os arquivos CMP-01 a CMP-04 desta pasta diferem da v0.2 só no carimbo de versão, salvo o ponteiro de evidência de AC-9 em CMP-06.
- Um único protocolo de dinheiro. Voz continua obrigatória no MVP.

## O que a v0.3 emenda

Só o HIGH-01 residual. CMP-O-28 passa a fixar, na fixture, `BUILDER_RUNTIME_ID`, `BUILDER_PROCESS_ID`, `BUILDER_AGENT_INSTANCE_ID` e `BUILDER_CREDENTIAL_FINGERPRINT`, além dos marcadores de scratch, verdict, cache, actor e tool state.

O PASS exige ids de runtime, processo e instância diferentes, e fingerprint de credencial do reviewer emitido fora do LLM. O FAIL cobre reutilização desse processo, runtime, instância ou credencial mesmo quando o actor registrado é `codex_reviewer` e os marcadores saíram do prompt. Uma frase do modelo não vale como attestation.

CMP-S11 acompanha essa fixture. A tabela AQ não decide nada.

## Fora deste diff

Os pontos editoriais do parecer v0.2 (ordem de §7.2 e a frase “provider_id ou capability” em CMP-O-31) não foram mexidos, para não reabrir findings fechados.
