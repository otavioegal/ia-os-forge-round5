# ATA DE DELIBERAÇÃO DO FOUNDER — IA OS Forge — AQs conversacionais

**Data:** 13/10/2026. **Ato:** aprovação expressa do Founder nesta conversa.
**Antecedentes:** [AQ-07 full-duplex](ADR-FDR-AQ07-FULL-DUPLEX-MVP-2026-10-13.md), [pacote de oito recomendações](FOUNDER-AQ-REMAINING-EIGHT-DECISION-PACK-2026-10-13.md), parecer independente [CMP v0.3](../reviews/PARECER-CODEX-CMP-v0.3-2026-10-13.md).
**Status:** DECISÕES HUMANAS REGISTRADAS; adequação dos contratos técnicos ainda requer revisão Codex.
**Referência auditada:** CMP v0.3 `f404abc1b4a90f01a12266e3e56a65df277258dd` (PASS WITH CONDITIONS). Baseline v1.7 `0c42373d583dec420348efd7bc0b8c6228a66f47` (PASS documental histórico).

## Resolução humana expressa

O Founder declarou: “Aprovo expressamente as oito recomendações AQ-01, AQ-02, AQ-03, AQ-05, AQ-06, AQ-08, AQ-10 e AQ-11 conforme o pacote publicado no GitHub. Registre a ata de aprovação, preserve as questões diferíveis, prossiga com a especificação do full-duplex e revisão independente, sem autorizar BUILD-00.”

| AQ | DECISÃO APROVADA | Condição de aplicação |
|---|---|---|
| AQ-01 | Papel específico `conversation_router` reserva gastos somente pelo gateway/transação do ledger v1.7, sem fingir ser `coding_engine` | Delimitar capability e autorização no catálogo; não conceder gasto externo antes dos contratos e gates |
| AQ-02 | Uma Task-âncora por sessão conversacional, fora do DAG de build, com `task_id` obrigatório | Proibidas capabilities de deploy, terminal e vault à âncora |
| AQ-03 | `speech.transcribe` e `speech.synthesize` como capabilities TOOL, dentro das três famílias do FDP-15 | Contrato de áudio bidirecional acrescentado por versão, sem quarta família não aprovada |
| AQ-05 | PUBLIC / INTERNAL / CONFIDENTIAL / RESTRICTED; projeto não é PUBLIC por padrão; CONFIDENTIAL/RESTRICTED não são enviados para speech externo | Política fora do LLM, aplicada previamente ao egress e ao fallback |
| AQ-06 | Áudio bruto DO_NOT_STORE por padrão; transcrição sob política organizacional explícita, sem retenção indefinida | Período, exclusão e base aplicável definidos na configuração antes de produção |
| AQ-08 | Iniciar a sessão de voz por ação expressa e consentimento; depois permitir escuta contínua APENAS na sessão ativa full-duplex; sem escuta de fundo | Ao pausar, revogar, fechar ou perder o escopo/consentimento: cessar captura e transporte |
| AQ-10 | Teto monetário único no ledger v1.7, `spent + reserved <= limit`; sem segundo ledger, meeting fee oculta ou duplo débito | Custos por operação e prova conclusiva; em incerteza, HELD/reconciliação |
| AQ-11 | Biometria de voz FORA do MVP; gravações/fala não autenticam nem concedem autorização de alto impacto | Hard gates exigem autenticação e confirmação em canal próprio |

**AQ-07 — JÁ APROVADA:** FULL-DUPLEX natural no MVP, todos agentes expostos, Jarvis e Conselho Técnico; áudio bidirecional simultâneo e interrupção, sem half-duplex como substituto.

**AQ-04, AQ-09 e AQ-12 — DIFERÍVEIS, NÃO DECIDIDAS:** respectivamente (a) provedor/modelo sujeito a deny-by-default e classificação, (b) sem compartilhamento implícito de banco/código/memória com Founder OS, (c) sem prova ingerível de fornecedor, reserva HELD sem recibo fictício. Não selecionar fornecedor por esta ata.

## Limites de autoridade

Esta ata **não aprova FDP-14 ou FDP-15**, **não integra automaticamente o CMP à baseline v1.7**, **não autoriza BUILD-00**, **não aprova contratação, deploy, credenciais, testes de software ou gastos**. Aprovação de decisões de produto e arquitetura não substitui revisão independente dos contratos, schemas, oráculos e integração financeira.

Estado das questões após este ato: nove resolvidas pelo Founder (AQ-01/02/03/05/06/07/08/10/11), três diferíveis ainda não decididas (AQ-04/09/12).
