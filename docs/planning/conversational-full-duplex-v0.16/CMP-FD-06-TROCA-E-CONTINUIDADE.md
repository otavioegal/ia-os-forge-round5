# CMP-FD-06 v0.16 — Troca de agente e contexto autorizado

**Estado:** PROPOSTA de passagem. A continuidade é só do que já é autorizado. Não é PASS. Não foi testada.

"Contexto autorizado" significa: esta conversa, este projeto, e o que o papel daquele agente já pode ver. Não significa copiar tudo.

## Troca direta

1. Na conversa aberta, a pessoa escolhe outro agente da lista.
2. A tela diz quem sai e quem entra. **REQ-PASSA-01.**
3. O agente que entra recebe de novo só o pacote permitido. O mesmo fio de conversa não conserva segredo do agente anterior. **REQ-PASSA-02.**
4. Ficam de fora outro projeto, outra organização, segredo, rascunho particular do agente anterior e qualquer coisa do Founder OS. **REQ-PASSA-03.** Cumpre DEC-SIGILO e DEC-FORGE.
5. Se houver um recado de passagem, ele aparece como resumo, com o rótulo Conclusão, não como cópia das notas escondidas. **REQ-PASSA-04.** Proposta.
6. A troca não aumenta o que o agente pode fazer. O Jarvis não empresta permissão. **REQ-PASSA-05.** Cumpre DEC-GASTO e a regra de que a experiência igual não é poder igual.

## Pedir um especialista ao Jarvis

1. A pessoa pede, por voz ou por texto, que o Jarvis chame um agente pelo nome. **REQ-PASSA-06.**
2. O convite não é a resposta.
3. A fala seguinte é do especialista, com o nome dele.
4. Se o Jarvis resumir depois, o resumo aponta as falas de origem. Ele não atribui ao Codex uma frase que o turno do Codex não disse. **REQ-PASSA-07.** Cumpre DEC-CODEX.

## Retomar

Pausar ou fechar desliga a escuta. O texto já mostrado dessa conversa continua disponível quando a pessoa volta ao mesmo fio, se a sessão ainda existe. Isso não importa memória de outro projeto.

Se a sessão foi encerrada de verdade, a pessoa começa outra. A tela não finge que a conversa antiga ainda está aberta.

A âncora financeira da conversa não vira tarefa de build, não publica e não abre terminal nem cofre. A pessoa não precisa ver essa âncora. O efeito visível é: conversar não dispara obra nem gasto fora do teto já existente.
