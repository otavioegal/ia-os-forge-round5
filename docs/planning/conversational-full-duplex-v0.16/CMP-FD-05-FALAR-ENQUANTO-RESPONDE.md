# CMP-FD-05 v0.16 — Falar enquanto o agente responde

**Estado:** a possibilidade de falar por cima está APROVADA (DEC-DUPLEX). O comportamento abaixo é PROPOSTA de como isso aparece. Não é PASS. Não foi testado.

Vale para o Jarvis, para cada agente e para a sala.

## O que a pessoa percebe

1. O agente ainda está falando. A pessoa começa a falar. **REQ-CORTE-01.** Aprovado.
2. O som do agente para na saída local assim que a fala da pessoa é reconhecida como fala, não como ruído. O texto que já apareceu fica na tela, marcado como interrompido. Nada disso é apagado. **REQ-CORTE-02.** Proposta.
3. A frase nova segue na mesma conversa. O agente responde a ela. A pessoa não é obrigada a repetir o que já estava entendido. **REQ-CORTE-03.** Cumpre a retomada aprovada.
4. O som da própria voz do agente não é tratado como se a pessoa tivesse falado. **REQ-CORTE-04.** Proposta. Sem isso, o agente se interromperia sozinho.
5. Um estalo ou um ruído curto não apaga a resposta. Uma fala da pessoa, sim. **REQ-CORTE-05.** Proposta. O limiar exato não é escolha do Founder.
6. Parar o som na caixa de som não significa que o serviço de fora confirmou o cancelamento, nem que o custo foi zero. Se o gasto ficou incerto, a conversa não finge que não houve cobrança. **REQ-CORTE-06.** Cumpre DEC-TETO e a regra já escrita de reserva incerta. A pessoa vê um aviso simples se isso bloquear o passo seguinte, não um extrato técnico.
7. O botão Interromper existe e faz o mesmo corte para quem não usa a voz. Ele não é o único caminho. **REQ-CORTE-07.**

## O que não acontece

- A pessoa espera a frase inteira porque o produto está em "vez do agente".
- A resposta some e a conversa recomeça vazia.
- O eco do alto-falante vira uma pergunta nova.
- O cancelamento do áudio é apresentado como estorno já confirmado.

Na sala, a fala da pessoa tem prioridade sobre o agente que está falando. Os outros agentes não começam a falar todos juntos por causa do corte.
