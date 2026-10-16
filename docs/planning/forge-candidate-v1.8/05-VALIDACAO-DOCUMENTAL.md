# 05 — Validação documental

**Estado:** relato do autor. Não é auditoria independente. Não é PASS. Não é teste de produto.

## Ambiente

- Sistema: Linux no ambiente de escrita deste pacote.
- Python: 3.10.22.
- Comando: `python3 -B tools/check_documentary.py --repo <cópia somente leitura das fontes>`.
- `PYTHONDONTWRITEBYTECODE` não foi necessário além de `python3 -B`. Nenhum arquivo de bytecode foi escrito nas fontes.
- Fontes lidas no SHA `d33617fbbef40343cd59c0f37dfe2910cea87f1e`, antes de publicar esta pasta. Se o parent publicado for outro, a publicação deve ter sido abortada.

## Saída

```
DOCUMENTARY_STRUCTURE_CHECK
stories=41/41
oracle_rows=91
LOW-01_stale_sentence_still_in_FDP-17_line_31=yes
tests_executed=no
postgresql=not_used
problems=0
RESULT STRUCTURE_ONLY
NOT_PRODUCT_PASS
NOT_READY_FOR_BUILD
FINDINGS_NOT_CLOSED_BY_THIS_CHECK
```

Exit code: 0.

O checker conferiu, só lendo texto: 41 histórias, separação de fonte, aceite positivo e negativo, 91 linhas de oráculo, passos e estado NOT RUN, métodos do adaptador, AIOX sem ser a única porta, testes DEPLOY-02 a DEPLOY-12, LEDGER-01 a LEDGER-18, HANDOFF-01, ambiente como identidade, estados finais da operação, lista do pronto-para-teste, a frase velha da linha 31 do FDP-17 ainda presente, e os arquivos de uso da v0.16.

## O que não foi testado

- PostgreSQL, migration, concorrência real, provider, deploy, gasto e BUILD-00.
- Os 91 oráculos da matriz v1.7.
- ACE-01 a ACE-14 da experiência de conversa.
- Spikes, ensaios de recuperação, drills de classe B e C.
- Suficiência semântica de cada frase de aceite além da estrutura conferida. Isso fica para o Codex.
- Nenhum finding foi fechado por este comando.
