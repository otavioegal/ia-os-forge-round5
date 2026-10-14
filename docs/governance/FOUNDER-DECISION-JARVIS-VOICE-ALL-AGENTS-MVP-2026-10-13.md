# DECISÃO DO FOUNDER — Jarvis por voz e conversação com todos os agentes no MVP

**Data:** 2026-10-13
**Estado:** DECISÃO FUNCIONAL EXPRESSAMENTE APROVADA PELO FOUNDER — requisito obrigatório de escopo do MVP; especificação técnica e testes ainda pendentes.
**Precedência:** SUBSTITUI a seção de fases e a pergunta aberta sobre voz do documento `ADDENDUM-CONVERSATIONAL-COUNCIL-JARVIS-2026-10-13.md`. Preserva demais princípios do addendum.
**Baseline técnica de referência:** v1.7, SHA `0c42373d583dec420348efd7bc0b8c6228a66f47`, PASS DOCUMENTAL do Codex Round 10. A decisão é uma extensão ainda não auditada; não altera retroativamente essa baseline nem aprova FDP-14/FDP-15 ou BUILD-00.

## Escopo obrigatório do MVP

1. **Jarvis por voz na primeira versão testável**: entrada por microfone, saída por voz natural, opção de texto, transcrição visível, interrupção do áudio, retomada de contexto de conversa e consulta a dados reais do projeto.
2. **Paridade de conversação para TODOS os agentes disponibilizados no Forge**: mesmo padrão funcional de texto e voz, sem agentes “somente texto” por conveniência técnica. O usuário escolhe o agente por nome/papel; conversa diretamente em voz ou texto e pode alternar o interlocutor preservando contexto autorizado.
3. **Conselho Técnico multiagente por texto E voz**: o usuário convoca, acompanha e interrompe sessões de discussão com Builder, Arquiteto, Codex, Segurança, Coordenador ou outros agentes registrados; turnos e identidade de quem fala devem permanecer explícitos, inclusive em áudio. O usuário pode intervir, perguntar a um agente específico e solicitar conclusão ou ata.
4. **Jarvis como porta de entrada universal**: capaz de conversar, localizar um especialista, convidá-lo à sessão, transferir-lhe o turno e sintetizar a resposta, sem atribuir indevidamente ao revisor independente conclusões não emitidas.
5. **Proposta de UX**: um único padrão de microfone/alto-falante, controle texto/voz, seleção de agente, transcrição e evidências, reutilizado nas três modalidades; ergonomia compatível com desktop e, quando houver frontend móvel, responsiva.

## Critérios de aceitação que deverão gerar histórias e oráculos

- Selecionar qualquer agente registrado como conversável e executar pergunta/resposta por voz e por texto.
- Trocar agente mantendo apenas o contexto permitido para seu papel, organização e projeto.
- Sessão de Conselho com pelo menos dois agentes, identificação inequívoca de cada resposta, interrupção do usuário e ata com fontes.
- Jarvis convoca ou transfere a pergunta ao agente indicado, com indicação auditável de origem da resposta.
- Em falha de STT/TTS ou indisponibilidade de provider, degradar com segurança para texto e oferecer retentativa; **não tratar fallback eventual como retirada do requisito de voz do MVP**.
- Comando “mostrar evidência” retorna artefato real ou declara não haver evidência. Nunca inventar status, testes ou percentuais.
- Privacidade: consentimento de microfone, política de retenção configurável, mínimo acesso a áudio/transcrições e política de classificação de dados para prestadores de voz.
- Segurança: hard gates de gastos, deploy, credenciais, operação destrutiva e dados sensíveis permanecem sujeitos a autenticação e confirmação específicas; falar “aprovo” sem confirmação segura não elimina o gate.
- Independência: Codex pode conversar e esclarecer parecer, mas no papel de reviewer continua isolado do Builder e não pode ser levado por uma sessão do Conselho a assinar uma avaliação conflitante com sua análise registrada.
- Custos de voz e de reuniões multiagentes são contabilizados por sessão/modelo/provider, com limites e prevenção de chamadas duplicadas.

## Deltas documentais necessários antes do BUILD-00

- FDP-11: fluxo de telas 1:1, Conselho e Jarvis; componente universal de voz/texto, interrupção, turnos e evidências.
- FDP-14: observabilidade de conversas, sessões de voz, invocação de agentes, tempos e custos; registrar rastros com minimização de dados.
- FDP-15: contratos de STT/TTS e áudio de baixa latência, provider agnóstico, modo degradado para texto, idempotência e custo.
- FDP-16: roteamento de turnos, delegação entre agentes, contexto e isolamento do reviewer; participação da Sala Técnica.
- FDP-13: autenticação, consentimento, privacy-by-design, capability gating e prevenção de abuso de comandos falados.
- Backlog e matriz: novas histórias e oráculos para as funcionalidades MVP; análise de custo e faseamento detalhado **sem postergar voz para um incremento futuro**.

A elaboração dos deltas e sua revisão independente são autorizadas enquanto planejamento, sem executar BUILD, testar software, chamar APIs pagas ou colocar sistemas em produção. Se o delta gerar nova questão arquitetural substantiva, submeter decisão específica ao Founder; não reabrir os findings históricos já fechados sem evidência de regressão.

## Critério de sucesso do produto

O Founder consegue entrar no Forge, iniciar Jarvis por voz, conversar com qualquer agente individualmente usando a mesma interface, reunir um Conselho Técnico por voz, ouvir e ler turnos identificados, questionar evidências e encerrar a sessão — tudo no MVP, mantendo auditoria e hard gates.

**Não confundir:** decisão funcional aprovada ≠ documento FDP-14/FDP-15 formalmente aprovado ≠ BUILD-00 autorizado ≠ produto implementado.
