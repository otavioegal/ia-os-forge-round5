# IA OS Forge — Impacto controlado do Jarvis e Conselho de Agentes no MVP
**Data:** 2026-10-13  
**Estado:** ANÁLISE DE IMPACTO PARA ESPECIFICAÇÃO; NÃO É NOVA BASELINE APROVADA.  
**Decisão funcional vinculante:** `FOUNDER-DECISION-JARVIS-VOICE-ALL-AGENTS-MVP-2026-10-13.md` (voz e texto com todos os agentes, 1:1, Conselho e Jarvis na primeira versão testável).  
**Baseline fechada:** v1.7, SHA `0c42373d583dec420348efd7bc0b8c6228a66f47`; PASS DOCUMENTAL Codex R10. Sem mudança retroativa e sem BUILD-00.

## Inventário verificado e limite de fonte
- Normativos v1.7: `docs/planning/FDP-16-v1.7-AIOX-EXECUTION-ENGINES.md`, `FDP-16A-v1.7-EXECUTION-CONTRACTS.md`, `FDP-17-v1.7-TESTING-STRATEGY.md`, `FDP-19-v1.7-PRODUCT-BACKLOG.md`, `FDP-19A-v1.7-STORY-ACCEPTANCE-REGISTER.md`, matriz de oráculos v1.7.
- Fontes históricas disponíveis: FDP-13 v1.0 e FDP-14 v1.0 (extratos), FDP-15 v1.0 (documento em histórico round4).
- **FDP-11 não aparece como arquivo normativo isolado nesta árvore**; Grok deve recuperar fonte original verificável, ou marcar lacuna e elaborar delta proposto sem fabricar cláusulas históricas. Não editar o snapshot original.
- FDP-14/FDP-15 seguem pendentes de aprovação humana, independentemente da decisão funcional sobre voz.

## Delta esperado por domínio
| Área | Inclusão planejada | Controle verificável |
|---|---|---|
| UX / FDP-11 | Jornada inicial Jarvis, seletor de agente universal, mic/alto-falante/transcrição/interrupção, Conselho com turnos explícitos | fluxos de telas e estados acessíveis; equivalência funcional texto/voz |
| Observabilidade / FDP-14 | session_id, turn_id, actor/agent, mode, timestamps, consumo STT/TTS/LLM, handoffs, custo, evidência e motivo de recusa | trilha que não registra áudio/prompts sensíveis indiscriminadamente; métricas sem percentuais inventados |
| Integrações / FDP-15 | Speech-to-Text, Text-to-Speech e sessão áudio, via adapters desacoplados de fornecedor | contratos versionados, timeouts, idempotência, fallback texto e custos/privacidade |
| Execução / FDP-16 | Router de conversação 1:1/Conselho/Jarvis, passagens de contexto autorizadas, delegação de turnos | agente/reviewer não recebe capacidades externas por intermédio de voz ou Jarvis |
| Segurança / FDP-13 | consentimento e retenção; acesso de áudio/transcrições por escopo; gates autenticados, prompt-injection verbal e logs redigidos | mensagem falada não é autorização automática para gasto, produção ou segredo |
| Backlog / FDP-19/19A | novas histórias como incremento separado, sem renumerar F-001…F-041 | histórias com DoR/DoD, dependências, owner pendente e oráculos específicos |
| Matriz / FDP-17 | oráculos positivos/negativos de fala, texto, conselho, interrupção, proteção de contexto e evidência | casos completos **NOT RUN**; não afirmar software testado |

## MVP inegociável da decisão do Founder
1. Todos os agentes oferecidos ao usuário têm interface uniforme de **voz e texto** (não apenas Jarvis); se um agente não puder receber diretamente voz, a interface universal deve realizar STT/TTS e encaminhar texto sob o mesmo regime de acesso. Não confundir uniforme com acesso uniforme a ferramentas.
2. Jarvis é orquestrador conversacional e pode transferir/convocar agentes; o usuário consegue interromper/retomar a interação e verificar a identidade da fonte.
3. Sala de Conselho suporta discussões multiagente também em voz, com turnos identificáveis, intervenção humana, ata e evidências.
4. Não apresentar saída hipotética ou parecer de agente como resultado de execução/prova documental.

## Ameaças / decisões de arquitetura para revisão
- Exfiltração de conteúdo de outros projetos por troca de interlocutor ou contexto de sessão.
- Contaminação do revisor independente pelo Builder durante Conselho ou explicação por Jarvis.
- Voz confundida com autorização formal; impersonação de usuário por áudio gravado.
- Custos e duplicação de chamadas por retentativa de STT/TTS ou discussões multiagente.
- Uso de prestador de voz externo para dados classificados ou armazenamento de áudio sem consentimento.
- Degradação de áudio: fallback para texto **não descaracteriza requisito de voz no MVP**; deve ser erro recuperável/indisponibilidade e não escopo removido.
- Latência, interrupção e estabilidade: números-alvo propostos, jamais apresentados como SLA medido.

## Plano de entrega documental
1. Grok prepara **pacote DELTA CONVERSATIONAL-MVP v0.1**, sem sobrescrever v1.7: Impact Assessment, UX Flow, API/Adapter voice contracts, agent/turn governance, privacy/security threat model, backlog aditivo e matriz de oráculos suplementar.
2. Validar correspondência com as fontes: classificar itens herdados vs novidade aprovada vs propostas de implementação; conflitos marcados para decisão Founder.
3. Codex audita **somente o delta**, compatibilidade com os contratos baseline e oráculos; relatório com PASS/PASS WITH CONDITIONS/FAIL apenas do incremento.
4. Gate humano sobre FDP-14/FDP-15 e inclusão da versão consolidada, separado da autorização operacional BUILD-00.

**Sem construir, sem usar provedores externos ou paid voice, sem executar testes de produto nesta fase.**
