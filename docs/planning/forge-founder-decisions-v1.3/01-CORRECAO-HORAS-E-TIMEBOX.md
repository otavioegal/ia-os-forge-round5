# Correção — horas de trabalho e timebox de calendário

**Data:** 22 de outubro de 2026  
**Corrige a leitura de:** `docs/planning/forge-founder-decisions-v1.2/01-DECISAO-CALIBRACAO-E-PLANO.md`

As decisões do Founder não mudam.

## O que continua aprovado

- As faixas da v1.1 foram aceitas como calibração de esforço para o planejamento.
- O plano escrito foi aprovado como READY FOR BUILD.
- O BUILD-00 não foi autorizado.

## O que estava errado

O registro v1.2 disse que a decisão também resolvia os timeboxes de calendário e que a prontidão operacional deixava de estar bloqueada por nome, hora ou timebox. Isso foi além da decisão e além da base.

## A leitura correta

As faixas da v1.1 são horas de trabalho ativo. O próprio texto diz que não são dias de calendário. Não incluem espera, aprovação humana nem dependência externa.

A base trata duas coisas como pendências distintas: horas de pessoa e timebox de calendário. Fonte: FDP-19 v1.7. A decisão aceitou as horas de esforço. Não criou data, prazo nem timebox de calendário.

Por isso:

- a pendência de horas de esforço, para o planejamento, está encerrada pelas faixas aceitas;
- a pendência de timebox de calendário continua aberta. Nenhuma data foi inventada;
- READY FOR BUILD aceita o plano escrito. Não declara que cada história está operacionalmente pronta para execução;
- a base ainda impede marcar uma história como pronta para execução enquanto o timebox de calendário estiver pendente. Essa frase não foi reescrita e continua valendo.

O texto antigo do FDP-19A e do FDP-20 não foi alterado. Para as horas de esforço, o registro v1.2 prevalece. Para o timebox de calendário, a base continua prevalecendo.

## O que esta correção não faz

- Não reverte o sim das faixas nem o READY FOR BUILD.
- Não autoriza o BUILD-00.
- Não fecha findings.
- Não cria responsável, data ou prazo.
- Não executa teste, spike, banco, migração, fornecedor ou implantação.
