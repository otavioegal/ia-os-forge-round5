# 03 — Experiência Jarvis no plano

**Estado:** o comportamento de produto já está aprovado. Esta página só mostra onde o plano descreve o uso. Não pede para escolher de novo. Não é PASS. Nada disso foi testado no produto.

As decisões aprovadas estão na ata `docs/governance/ATA-FOUNDER-AQS-CONVERSATIONAL-2026-10-13.md` e no ADR `docs/governance/ADR-FDR-AQ07-FULL-DUPLEX-MVP-2026-10-13.md`. A narrativa de uso, em linguagem simples, está na pasta `docs/planning/conversational-full-duplex-v0.16/`. A v1.7 do Forge não repetia essa narrativa. Esta candidata faz o vínculo. Não edita a v0.16.

Há dois tipos de passagem. Os dois existem. Um não substitui o outro.

| O que a pessoa vê | Onde está | Que teste escrito existe | Estado do teste |
|---|---|---|---|
| Conversar com um agente, por voz ou por texto | v0.16, CMP-FD-02 | ACE-01 e ACE-02 | NOT RUN |
| Sala de Conselho, com nome de quem fala | v0.16, CMP-FD-03 | ACE-03 e ACE-04 | NOT RUN |
| A mesma experiência para todos os agentes | v0.16, CMP-FD-02 e CMP-FD-04 | ACE-01 e ACE-02 | NOT RUN |
| Falar enquanto o agente ainda responde, e continuar a conversa | v0.16, CMP-FD-04 e CMP-FD-05 | ACE-05 | NOT RUN |
| Trocar de agente levando só o contexto permitido | v0.16, CMP-FD-06 | ACE-06 e ACE-07 | NOT RUN |
| Voz ou rede indisponível, sem a voz sair do produto | v0.16, CMP-FD-07 | ACE-08, ACE-09, ACE-10 e ACE-14 | NOT RUN |
| Pedido grave falado não se executa sozinho | v0.16, CMP-FD-07 | ACE-11 | NOT RUN |
| A escuta para quando a conversa pausa ou fecha | v0.16, CMP-FD-07 | ACE-12 | NOT RUN |
| Uma tarefa de obra passa de uma tentativa a outra sem ganhar poder e sem checkpoint falso | F-016, F-027, FDP-16A seção 10 | HANDOFF-01 e ENG-02 | NOT RUN |
| Dinheiro incerto espera uma pessoa; ninguém chuta o custo | F-015, FDP-16A seções 8A.2 e 8C | LEDGER-05, LEDGER-11 e LEDGER-12 | NOT RUN |

## Como isso aparece no uso

Você abre uma conversa com o Jarvis ou com outro agente do projeto. Pode escrever ou falar. A resposta aparece em texto e, se a voz estiver ligada, também é falada. O nome de quem fala fica na tela.

Se você falar no meio da resposta, o som para, o que já foi dito permanece, e a conversa segue na sua frase nova. Não é preciso esperar a vez.

Na sala, você vê o assunto, quem está presente e quem fala agora. Discordância não é apagada por uma frase de que todos concordaram.

Quando você chama outro agente, ele recebe só o que já pode ver deste projeto e desta conversa. Não leva outro projeto, segredo, nem memória de outro sistema. Na obra, a passagem de uma tentativa de trabalho para a próxima é outra coisa: a tentativa anterior termina, o ponto salvo precisa bater, e a nova tentativa não ganha permissão extra.

Se a voz cair, você continua por texto e pode tentar a voz de novo. Se a rede cair, a tela não inventa o final. Se o custo de uma chamada ficar incerto, o Forge para e pede uma pessoa autorizada. Dizer "eu aprovo" em voz não publica e não gasta.

## O que não está neste vínculo

Os ACE da v0.16 não entram na matriz dos 17 controles P0. Não substituem HANDOFF-01. Não foram executados. Não escolhem fornecedor de voz. Não medem milissegundos. Não autorizam BUILD-00.
