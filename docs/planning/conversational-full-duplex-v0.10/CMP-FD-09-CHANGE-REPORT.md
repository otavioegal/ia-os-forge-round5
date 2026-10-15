# CMP-FD-09 v0.10 — Change report

**Estado:** PROPOSTA. Não é PASS. Não edita v0.1 a v0.9, baseline, CMP, ata, ADR nem parecer.

NEW-MEDIUM-09: cada parecer de v0.1 a v0.9 é lido do blob do commit em que existe. O checker confere path, SHA auditado, rótulo e veredito. v0.5 e v0.6 continuam ausência legítima. A lista de prompts presentes e a de ausentes são conferidas com `git ls-tree`. Troca de SHA, veredito, path, omissão, prompt inventado, parecer inventado e promoção do v0.2 são rejeitadas. O veredito do v0.2 fica NOT_VERIFIED porque os dois textos do arquivo discordam.

NEW-LOW-02: o schema externo exige todos os campos obrigatórios. A ausência devolve `FAIL_SCHEMA` antes do processamento. A remoção de cada campo obrigatório é testada, junto com as mutações de valor já existentes.

FD07-07 e HIGH-03 não são fechados. Não há PostgreSQL. O replay, o 404 de tenant, o par null, `n < 0` e a monotonicidade da v0.9 permanecem.
