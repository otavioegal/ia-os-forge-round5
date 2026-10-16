# CMP-FD-03 v0.16 — Sala de Conselho Técnico

**Estado:** PROPOSTA de jornada. A existência da sala e a voz full-duplex nela estão aprovadas (DEC-SALA, DEC-DUPLEX). Não é PASS. Não foi testada.

A sala é uma conversa conduzida, não um acordo automático entre máquinas.

## Como a pessoa usa

1. Abre a aba **Conselho**.
2. Escolhe pelo menos dois agentes que já existem na lista do projeto.
3. Diz o assunto falando ou escrevendo. **REQ-SALA-01.**
4. Vê o assunto, quem está na sala e quem está falando agora. **REQ-SALA-02.** Cumpre a identificação aprovada no ADR.
5. Ouve um agente por vez. O nome escrito e o nome falado antes da frase são o mesmo texto, por exemplo "Arquiteto." Semelhança de voz não identifica ninguém. **REQ-SALA-03.** Proposta de mecanismo; a obrigação de saber quem fala é aprovada.
6. Pode falar no meio, pedir que um agente nomeado fale em seguida, ou pedir a ata. **REQ-SALA-05.** A prioridade da fala humana no meio da fala de um agente é aprovada no ADR. O pedido nominal e a ata são proposta.
7. Se dois agentes discordam, os dois lados continuam na tela. A sala não escreve "o conselho concorda" por cima da discordância. **REQ-SALA-04.** Cumpre o ADR: não fabricar acordo.
8. A ata diz quem falou o quê. Onde não há fonte, diz que não há evidência. A ata não substitui uma decisão humana nem um parecer do Codex. **REQ-SALA-06.** Proposta.
9. Abrir o microfone da sala não põe todos os agentes para trabalhar e gastar ao mesmo tempo. **REQ-SALA-07.** Cumpre o ADR: mídia simultânea não é fan-out livre de chamadas pagas.
10. O Codex na sala pode falar em leitura. Não há botão de "pedir parecer formal" nesse fio. Revisão formal continua outro caminho, separado. **REQ-SALA-08.** Cumpre DEC-CODEX.

## O que falha a sala

- Um parágrafo só, sem nome de quem falou.
- Várias vozes de agente ao mesmo tempo, sem dar para saber quem é quem.
- Uma ata que apaga divergência ou que se apresenta como decisão do Founder.
- A sala escutando depois de encerrada.

O compositor é o mesmo da conversa individual: texto, microfone, voz de saída, interromper e ver quem fala. Cumpre DEC-COERENTE.
