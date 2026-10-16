# Candidata v1.8 — revisão documental do Forge

**Estado:** CANDIDATE FOR CODEX REVIEW. Não é PASS. Não é READY FOR BUILD. Não autoriza BUILD-00.
**Não fecha finding.** Não converte NOT RUN, PARTIAL ou OPEN em aprovação.
**Parent desta pasta:** o commit que já contém a v0.16. Esta pasta não reescreve a v1.7, os pareceres, as atas, os ADRs nem as versões anteriores.
**Escopo:** IA OS Forge. O Founder Operating System continua de fora.

## O que esta pasta é

O parecer Round 5 reprovou a prontidão documental da v1.2. As rodadas 6 a 10 escreveram a correção na baseline v1.7. O Codex, no Round 10, deu PASS documental àquela baseline. Isso não é aprovação do Founder e não é licença para construir.

Esta candidata não cria outra baseline. Ela junta, com caminho e seção verificáveis:

- onde cada achado do Round 5 foi corrigido, ou por que continua aberto;
- a ligação das 41 histórias com a fonte, o aceite e o teste;
- a experiência de conversa do Jarvis, que a v1.7 não narrava em linguagem de uso;
- a leitura correta dos índices que ficaram desatualizados;
- só as decisões que ainda dependem de uma pessoa.

## Arquivos

| Arquivo | Uso |
|---|---|
| 01-REGISTRO-DOS-ACHADOS.md | Achado por achado |
| 02-MATRIZ-HISTORIA-TESTE.md | Fonte, história, aceite e teste |
| 03-EXPERIENCIA-JARVIS.md | Conversa, sala, voz, interrupção, passagem e falhas |
| 04-O-QUE-O-FOUNDER-PRECISA-APROVAR.md | Só decisões humanas, em linguagem simples |
| 05-VALIDACAO-DOCUMENTAL.md | O que foi conferido e o que não foi testado |
| 06-LEITURA-DOS-INDICES.md | O que os índices antigos dizem e o que já mudou |
| 07-LIMITES.md | O que esta pasta não faz |
| tools/check_documentary.py | Conferência estrutural, só leitura |

Nenhum documento escrito nesta pasta está aprovado só por existir.
