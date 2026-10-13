# IA OS Forge — Addendum de decisão do fundador: Conselho Técnico Conversacional + Jarvis
**Data:** 2026-10-13
**Origem:** solicitação expressa do Founder durante revisão do gate FDP-14.
**Estado:** REQUISITO DE PRODUTO APROVADO EM PRINCÍPIO PELO FOUNDER; desenho detalhado, avaliação de impacto, oráculos e integração à baseline normativa ainda PENDENTES.
**Vínculos:** FDP-11 (UX), FDP-14 (Observability & Evaluation), FDP-16 (Execução/Agentes), FDP-13 (Segurança), FDP-15 (Integrações), Founder OS/Conselho Consultivo (referência de experiência, não dependência técnica obrigatória).
**Baseline de referência:** v1.7 SHA 0c42373d583dec420348efd7bc0b8c6228a66f47, PASS DOCUMENTAL Codex Round 10. O addendum NÃO altera o SHA auditado nem seus arquivos normativos; NÃO aprova FDP-14/15; NÃO autoriza BUILD-00.

## Decisão funcional expressa

O Founder deseja, conjuntamente, três modos de interação:

1. **Diálogo 1:1 com agentes**: selecionar Coordenador, Arquiteto, Builder, Reviewer Codex ou Segurança e conversar diretamente, com explicação em linguagem executiva, referências a evidências e indicação de incerteza.
2. **Sala de Conselho Técnico multiagente**: fundador convoca especialistas para debater alternativas, riscos, custos e pareceres; cada agente fala com identidade e papel atribuídos, registra divergências, apresenta evidências e emite recomendação consolidada, sem substituir decisão humana ou falsificar consenso.
3. **Assistente estilo Jarvis do Conselho Consultivo**: voz natural com entrada por fala e resposta falada, opção texto/voz alternável, transcrição persistida quando autorizada, interrupção de fala, perguntas de acompanhamento, acesso governado aos dados e possibilidade de convidar ou transferir a conversa a especialistas. A voz Jarvis funciona como porta de entrada do Forge, sem personificar indevidamente o Codex ou anunciar validações não realizadas.

## Requisitos e limitações arquiteturais

- FDP-14 fornece eventos, traces, métricas e evidências verificáveis; **não é sozinho uma UI de chat/voz**. FDP-11 desenha telas e jornada; FDP-16 roteia para os agentes; FDP-15 trata adaptações de speech-to-text, text-to-speech e, opcionalmente, sessões de áudio em tempo real.
- Identidade de cada agente, fonte consultada, carimbo de tempo, projeto/escopo e diferença entre fato registrado, inferência e sugestão devem permanecer claros.
- **Codex preserva auditoria independente**: o Jarvis pode explicar pareceres e consultar o Codex em modo read-only, mas não pode alterar parecer, assumir seu papel ou induzir PASS.
- Fala não equivale a autorização irreversível. Hard gates exigem confirmação explícita e autenticada no canal apropriado, inclusive deploy, gasto relevante, credenciais, dados sensíveis e alterações destrutivas. Ações de baixo risco dentro de políticas previamente aprovadas seguem sem microaprovação.
- Minimização de dados e retenção configurável de áudio/transcrições; consentimento para microfone e gravação; processamento e seleção de provider sujeitos à classificação dos dados; fallbacks de acessibilidade e operação em texto.
- A interface é assistiva e auditável: “mostrar evidência” abre registro real; “qual o status?” consulta estado, não gera percentuais inventados.
- Sala multiagente é um **workflow de orquestração**, não vários LLMs automaticamente concordando entre si. Cada participação e custo devem ser rastreados.
- Reuso de design system/experiência do Founder OS é objetivo, sujeito à análise de integração, autenticação e acoplamento. Evitar duplicação de código sem baseline compartilhada aprovada.

## UX mínima candidata

- Entrada no STUDIO: aba Conversar, abas Conselho, Agentes e Evidências.
- Menu de interlocutor (Coordenador / Builder / Arquiteto / Segurança / Codex [somente leitura em auditoria]).
- Barra única com texto, botão de microfone, áudio ligado/desligado, transcrição e “Mostrar fontes”.
- Conselho técnico: convocar especialistas, pauta, turnos, divergências e ata.
- Jarvis: ativação explícita, voz/texto sincronizados, estado de escuta/fala/ocupado e botão de interrupção.
- Qualquer comando de ação governada exibe prévia dos efeitos e o gate necessário, separada da simples conversa.

## Fases propostas para detalhamento, não cronograma aprovado

- **MVP**: conversa textual 1:1, coordenador, consulta a evidências, conselho por texto e modo texto acessível.
- **Incremento próximo**: voz Jarvis com STT/TTS, transcrição, interrupção e convite de agentes, subject to gateway/provider/cost policy.
- **Evolução**: áudio em tempo real, múltiplas vozes/perfis, sessões colaborativas e experiência convergente entre Founder OS e Forge.

**Questão de produto ainda sujeita a deliberação:** se o Jarvis por voz faz parte do MVP obrigatório ou é incremento prioritário; não presumir autorização para adiar voz. A intenção expressa do Founder é ter as três possibilidades no produto.

## Próximos gates

1. Registrar este addendum como decisão funcional do Founder sem alterar baseline Codex aprovada.
2. Elaborar análise de impacto documentada contra FDP-11/13/14/15/16, stories, oráculos, custo e LGPD/privacidade.
3. Submeter deltas normativos ao Codex independente para parecer direcionado **somente sobre a ampliação**, sem reabrir 10 rodadas fechadas.
4. O Founder delibera a inclusão na baseline de build, fase da voz, FDP-14/FDP-15 e baseline documental; BUILD-00 continua separado.

**Não é prova de implementação.** As três modalidades são capacidades requisitadas, não funcionalidades já construídas.
