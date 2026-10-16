# CMP-FD-04 v0.16 — Jeito natural da conversa

**Estado:** PROPOSTA de experiência. Não é PASS. Não foi medida.

"Estilo Jarvis" nesta pasta não é voz de cinema, marca ou biometria. É a conversa que o Founder já pediu: rápida no uso, presa ao contexto, fácil de cortar e de retomar, com nome de quem fala.

## Rápida, sem número inventado

Não há botão de "agora é a sua vez" como único modo. **REQ-NAT-01.** Cumpre DEC-DUPLEX. Meia-duplex fica rejeitada.

Enquanto o agente pensa, a tela mostra o nome de quem está pensando. Não fica muda nem usa só uma roda genérica. **REQ-NAT-06.**

Nenhum prazo em milissegundos foi aprovado. O ADR diz que a decisão não é SLA. Esta pasta não propõe 200 ms, 800 ms nem outro alvo. Não houve medição. Chamar a conversa de rápida aqui significa só isto: a pessoa não espera o fim do turno para falar, e a tela não esconde quem está trabalhando.

## Contextual

O agente usa o que já foi dito nesta conversa aberta e neste projeto, dentro do que ele pode ver. **REQ-NAT-02.**

Não entra: outro projeto, outra organização, segredo, nem memória do Founder OS. Cumpre DEC-FORGE e a guarda da AQ-09, que continua diferida.

Retomar é voltar a essa mesma conversa aberta e seguir. Não é "o agente lembra a vida inteira da pessoa". **REQ-NAT-03.**

## Fácil de interromper e retomar

O detalhe de falar por cima está na CMP-FD-05. Aqui fica o resultado para a pessoa: ela corta, o que já foi dito permanece, e a frase nova continua o mesmo fio. Não precisa recomeçar do zero nem repetir o projeto.

Há também um botão de interromper, para quem não fala por cima. O botão é acessibilidade. Sozinho, ele não cumpre o MVP. **REQ-CORTE-07**, detalhado na CMP-FD-05.

## Quem está falando

Toda fala de agente tem um nome em texto na tela. Cor não basta. **REQ-NAT-04.** Cumpre a identificação aprovada.

Se a voz estiver ligada, o áudio diz esse mesmo nome antes do conteúdo. Proposta de mecanismo já escrita na jornada antiga e mantida aqui. Voz parecida não conta como identidade. Biometria continua fora. Cumpre DEC-GRAVE.

Cada resposta mostra em palavra se é fato com fonte, conclusão, sugestão ou falta de evidência. O rótulo está no texto. Não fica só no áudio. **REQ-NAT-05.** Proposta herdada: FACT, INFERENCE, SUGGESTION, ABSENCE. A pessoa lê: Fato, Conclusão, Sugestão ou Não há evidência.

Recusa e ausência também aparecem escritas. O áudio não é o único lugar onde uma negativa existe.
