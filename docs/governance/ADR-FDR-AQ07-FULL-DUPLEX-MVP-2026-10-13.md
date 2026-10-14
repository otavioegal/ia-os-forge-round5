# ADR-FDR-AQ07 — Conversação full-duplex obrigatória no MVP do IA OS Forge

**Data:** 13/10/2026  
**Autoridade:** decisão expressa do Founder nesta conversa.  
**Estado da decisão:** **APROVADA — AQ-07 FECHADA POR DELIBERAÇÃO HUMANA**, ainda não incorporada nem auditada como delta normativo de engenharia.  
**Registro-fonte:** `docs/planning/conversational-mvp-v0.3/CMP-AQ-FOUNDER-DECISIONS.md` e `CMP-OPEN-QUESTIONS.md` (permanecem imutáveis como fotografia da versão auditada).  
**Baseline estável:** IA OS Forge v1.7 `0c42373d583dec420348efd7bc0b8c6228a66f47` — PASS documental histórico.  
**Delta auditado:** CMP v0.3 `f404abc1b4a90f01a12266e3e56a65df277258dd` — PASS WITH CONDITIONS, HIGH-01 fechado documentalmente.  
**Não autoriza:** integrar a decisão diretamente na baseline, aprovar FDP-14/FDP-15, escolher fornecedor, contratar API, executar software/staging ou iniciar BUILD-00.

## Decisão do Founder (AQ-07)

**Jarvis, todos os agentes conversacionais disponibilizados no Forge e a Sala de Conselho Técnico devem permitir conversa natural FULL-DUPLEX na primeira versão testável do MVP.** A proposta anterior de `half-duplex STT/TTS + barge-in` como experiência suficiente foi **REJEITADA** pelo Founder. Voz **não** é etapa pós-MVP.

FULL-DUPLEX significa **entrada de voz e saída de áudio simultâneas durante a mesma sessão**: o usuário pode iniciar fala enquanto o agente fala, interromper, esclarecer ou redirecionar sem esperar o fim da resposta. A interface pode adaptar agentes cujo raciocínio de base seja textual por meio de um gateway de áudio bidirecional, mantendo a mesma experiência de voz para TODOS os interlocutores oferecidos. Não pressupõe que cada modelo subjacente suporte áudio nativo.

A decisão é sobre a experiência obrigatória, não é uma escolha de provider/SDK, contrato comercial nem SLA de latência aprovado.

## Consequências para engenharia — propostas a detalhar e submeter ao Codex

1. **CMP-01 / UX:** estados com escuta e fala simultâneas; sessão de áudio iniciada e encerrada explicitamente; transcrição parcial/final e fala interrompível; pessoa consegue intervir sem botão por turno; modo Conselho identifica agente que fala e preserva controle de turnos/ata.
2. **CMP-02 / contratos:** evoluir `cmp.speech.v0` ou definir contrato versionado compatível para stream bidirecional, sinalização de interrupção, cancelamento de geração/áudio, acknowledgements, sequência de frames, jitter/packet-loss, controle de eco, VAD e finalização de turnos. Não degradar silenciosamente a half-duplex como implementação padrão do MVP.
3. **Fronteira universal de voz:** para agentes text-backed, gateway mantém captura contínua autorizada durante a sessão, STT incremental, TTS cancelável e arbitragem com respostas textuais. Todos os agentes habilitados à conversa recebem o MESMO contrato de interação. Cada papel mantém suas capabilities e privilégios separados.
4. **Conselho Técnico:** múltiplos agentes podem discutir, mas quem fala é identificado; prioridade à intervenção do Founder; não fabricar acordo, custo ou parecer. Paralelismo de mídia de entrada/saída não concede paralelo ilimitado de chamadas pagas dos agentes.
5. **CMP-03 / segurança:** concessão explícita para o microfone continua obrigatória. Um microfone ativo **dentro de sessão iniciada e consentida** não equivale a escuta de fundo sempre ativa com aplicativo inativo. Política para ativação, push-to-talk inicial e always-on fora da sessão permanece AQ-08 PENDENTE.
6. **Privacy:** classificação pré-egress, áudio bruto não retido por default sujeito a AQ-06; pipeline de áudio/tokens minimizado; dados confidenciais/restritos não podem ir para provider externo sem política expressa — AQ-05 ainda PENDENTE.
7. **CMP-04 e FDP-16A:** eventos e custo por session/turn/provider/model, dedupe/retry e um único ledger; manter hard gates autenticados independentemente de comando falado. Streaming e interrupção não significam que o provider não cobrou: continuar usando provas e estados de settlement/HELD/CONFLICT.
8. **Revisor independente:** Codex conversacional por voz é read-only e NÃO executa review formal; os controles de `review_run_id`, processo/instância/credencial separados e CMP-O-28 continuam vinculantes.
9. **Acessibilidade e fallback:** texto permanece alternativo; indisponibilidade momentânea de voz pode exibir modo texto com erro recuperável, mas não autoriza retirar FULL-DUPLEX do produto MVP.
10. **Testabilidade futura:** especificar oráculos negativos e positivos para (a) capturar usuário falando enquanto TTS toca, (b) interrupção simultânea/echo sem perda de contexto, (c) escolha/troca de agentes, (d) Conselho com fala humana no meio da fala de um agente, (e) áudio/consentimento revoked, (f) sem duplo débito ou bypass, (g) latência/qualidade só após medição; oráculos mantidos NOT RUN até BUILD.

## Decisões que ESTE ato não tomou

AQ-01, AQ-02, AQ-03, AQ-05, AQ-06, AQ-08, AQ-10, AQ-11: **PENDENTES**. 
AQ-04, AQ-09, AQ-12: **DIFERÍVEIS COM GUARDAS**, não aprovadas. 
FDP-14 e FDP-15, a consolidação da baseline e o BUILD-00: **PENDENTES**.

## Critério de integração

O Grok deve especificar delta full-duplex conforme esta decisão e as deliberações AQ restantes, preservando as fontes auditadas. O Codex deve auditar a ampliação do contrato/UX/oráculos e a compatibilidade com v1.7. O Founder aprova expressamente a baseline de implementação em gate separado. Este ADR registra a decisão de produto, **não** é PASS do novo desenho de engenharia.

**Atenção:** os documentos `conversational-mvp-v0.3/` continuam como fotografia auditada que descreve AQ-07 aberta e half-duplex proposto. Esta ADR posterior **prevalece para a decisão do Founder**, mas não os reescreve retroativamente.
