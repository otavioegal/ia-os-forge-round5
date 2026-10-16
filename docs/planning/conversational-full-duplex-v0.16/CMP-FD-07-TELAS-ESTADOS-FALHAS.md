# CMP-FD-07 v0.16 — Telas, estados e falhas

**Estado:** PROPOSTA. Nomes de tela não são uma promessa de que a tela já exista. Não é PASS. Não foi testada.

## Quatro lugares

**REQ-TELA-01.** Proposta herdada da jornada antiga, sem reescrevê-la:

| Lugar | Para que serve |
|---|---|
| Conversar | Jarvis e conversa de um para um |
| Conselho | Sala com vários agentes |
| Agentes | Quem existe neste projeto e o que cada um pode fazer, em linguagem simples |
| Evidências | Abrir uma fonte real, ou dizer que não há |

Em todos os lugares de conversa ficam visíveis: campo de texto, microfone, ligar ou desligar a voz de saída, interromper, o texto da conversa e o nome de quem fala.

## Estados que a pessoa distingue

**REQ-TELA-02.** Um estado não se disfarça de outro.

| Estado | O que a pessoa vê | Som |
|---|---|---|
| Pronto | Dá para escrever ou começar a voz. O nome do agente está na tela | Calado |
| Precisa permitir o microfone | Texto liberado. Pedido claro de permissão | Sem captura |
| Ouvindo | "Ouvindo", só dentro da conversa iniciada | Captura local |
| Ouvindo e falando | Os dois ao mesmo tempo. É o full-duplex | Captura e voz do agente |
| Pensando | Nome de quem pensa. Não é só uma roda | Calado ou voz já cortada |
| Falando | Texto acompanhando a fala e o nome antes | Voz daquele turno |
| Interrompido | O que já foi dito permanece, marcado | Som do agente parado |
| Só texto | Faixa dizendo por que a voz não está disponível | Sem fingir que a voz saiu do produto |
| Sem conexão | O que já está na tela fica. O que pode não ter ido fica marcado | Sem resposta inventada |
| Recusado | O motivo está escrito | Sem sucesso falso |
| Sem orçamento | Aquele passo pago não segue | Sem saldo inventado |
| Confirmação à parte | Folha separada da bolha da conversa | A fala não aperta o confirmar |

## Quando a voz ou a conexão faltam

- Sem permissão de microfone: texto segue; a tela pede a permissão; a voz continua sendo parte do produto. **REQ-TELA-03.**
- Voz caída: faixa com o motivo e "Tentar a voz de novo". Microfone e alto-falante continuam na tela. A conversa segue por texto. **REQ-TELA-04.** Cumpre DEC-TEXTO. Tentar de novo não apaga o fio. Se o Forge não sabe se o serviço já cobrou, o botão não dispara outra chamada; ele diz que é preciso conferir. Proposta alinhada à regra já existente de reserva incerta, sem segundo significado escondido no mesmo botão.
- Sem conexão: nada é mostrado como resposta terminada se não chegou. Ao voltar, a pessoa continua a mesma conversa aberta, sem cobrança nova automática. **REQ-TELA-05.**
- Conteúdo confidencial ou restrito: não sai para voz de fora. A tela explica e deixa seguir em texto dentro do Forge. **REQ-TELA-06.** Cumpre DEC-SIGILO.
- Áudio bruto não fica guardado. A tela não promete gravação. **REQ-TELA-07.** Cumpre DEC-AUDIO. O que a organização guarda de transcrição, e por quanto tempo, continua regra da organização antes de uso real, não um número inventado aqui.
- "Mostrar fontes" abre a evidência daquela fala ou escreve que não há. Não completa status nem porcentagem. **REQ-TELA-08.**
- "Eu aprovo", "pode gastar" ou "pode publicar", em voz ou em texto, não executam o ato. Abre a confirmação separada. A frase falada não é o botão. **REQ-TELA-09.** Cumpre DEC-GRAVE.
- Pausar, fechar ou sair desliga a escuta. Não há escuta em segundo plano. **REQ-TELA-10.** Cumpre DEC-SESSAO.
- Sem orçamento: a tela diz que o passo pago parou. Não mostra saldo fabricado. **REQ-TELA-11.** Cumpre DEC-TETO.
- Recusa: o motivo fica no texto. **REQ-TELA-12.**

Lista vazia de agentes não ganha nomes inventados. Pessoa fora do projeto não entra na conversa.

Nenhuma informação de que o Founder precise está só no áudio. O texto da conversa permanece visível durante a fala.
