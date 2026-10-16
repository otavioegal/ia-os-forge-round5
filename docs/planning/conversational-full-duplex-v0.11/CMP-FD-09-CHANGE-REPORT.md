# CMP-FD-09 v0.11 — Change report

**Estado:** PROPOSTA. Não é PASS. Não edita v0.1 a v0.10, baseline, CMP, ata, ADR nem parecer.

NEW-MEDIUM-09: o parecer v0.2 não é editado e nenhum dos dois vereditos é escolhido. CMP-FD-16 propõe uma errata futura, com blob e SHA-256, pendente de aprovação humana. Até lá, NOT_VERIFIED. O campo `bytes` de cada path é comparado ao tamanho do blob. v0.5 e v0.6 continuam ausência legítima. As listas de prompts presentes e ausentes são as do parent.

NEW-LOW-02 e NEW-LOW-03: o schema externo declara tipo e cardinalidade. `rollback_model`, `interleave`, `sequential_replay` e os dois replays compostos são validados antes da decisão. Há mutação de ausência e de tipo para os campos declarados, inclusive aninhados. Lista vazia e tamanhos desiguais de `commit_order` e `expected_steps` devolvem `FAIL_SCHEMA`.

FD07-07 e HIGH-03 não são fechados. Não há PostgreSQL.
