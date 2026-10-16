# CMP-FD-02 v0.16 — Conversa individual

**Estado:** PROPOSTA de jornada. As decisões que ela cumpre estão aprovadas. Não é PASS. Não foi testada.

Lugar: aba **Conversar**, dentro de um projeto do qual a pessoa participa. Agente que não está registrado nesse projeto não aparece.

## Como começa

1. A pessoa entra no projeto e abre Conversar. **REQ-IND-01.** Proposta de rótulo do botão de voz: "Começar por voz". Apertar isso não dá poder extra a ninguém.
2. Se a voz ainda não foi permitida, a tela pede o microfone e o texto continua utilizável. Isso cumpre DEC-SESSAO e DEC-TEXTO.
3. A pessoa escreve ou fala. As duas formas valem igual. Uma não apaga a outra. **REQ-IND-02.** Cumpre DEC-COERENTE e DEC-IND.
4. O que foi dito aparece em texto na tela antes de virar pergunta fechada. **REQ-IND-04.** Proposta herdada da jornada antiga, agora em linguagem de uso.
5. O Jarvis responde sempre em texto. Se a voz estiver ligada e disponível, também fala. **REQ-IND-03.** Cumpre DEC-VOZ e DEC-TEXTO.

O Jarvis é o interlocutor inicial dessa aba. Isso não impede falar com outro agente. Não é uma palavra mágica escutando fora da conversa.

## Outro agente, a mesma conversa de um para um

1. A pessoa abre a lista e escolhe um agente pelo nome e pelo papel. **REQ-IND-05.**
2. O lugar de escrever, falar, ouvir e interromper não muda. **REQ-IND-07.** Cumpre DEC-COERENTE.
3. A resposta leva o nome desse agente. O Jarvis não assina no lugar dele. **REQ-IND-05.**
4. Quem não está na lista não é inventado. **REQ-IND-06.**

Papéis já citados na jornada antiga, como catálogo mínimo proposto e não como lista fechada nesta rodada: Coordenador, Construtor, Arquiteto, Segurança, Codex em leitura, Jarvis. Entrar outro agente no futuro é uma linha no registro, não uma segunda tela.

## O que a pessoa não deve ver

- Um modo "só texto porque este agente é mais simples".
- O Jarvis respondendo com o nome de outro.
- A conversa de outro projeto misturada nesta.
- A escuta ligada antes de "Começar por voz", ou depois de pausar e fechar.

A troca para outro agente está na CMP-FD-06. Falar por cima da resposta está na CMP-FD-05.
