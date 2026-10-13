# IA OS Forge — Prompt oficial Grok Round 8
## Correção direcionada: semântica de prova financeira e autenticidade da reconciliação

**Repositório:** https://github.com/otavioegal/ia-os-forge-round5  
**Parecer independente, leitura obrigatória:** `docs/reviews/PARECER-CODEX-ROUND7-2026-10-13.md`  
**Baseline auditada:** v1.4, commit `decef2809b61d3f1fe84bef74a5162d782cc6231`  
**Parecer publicado:** commit `916d7025b1618087660aa3d66efa6d5b56ad47b5`  
**Saída:** v1.5 — ROUND 8 — CANDIDATE FOR CODEX REVIEW.

Você é o Grok, BUILDER DOCUMENTAL. Não audite seu próprio trabalho como se fosse o Codex. Leia integralmente o parecer e examine FDP-16A §8A, F-015 em FDP-19A, matriz canônica LEDGER-01…12 e os relatórios Round7. Compare com fontes FDP-12/13 e documentos históricos antes de editar. Preserve todos os demais findings fechados, os 17 P0 e a arquitetura previamente estabelecida.

### Correção HIGH-01 / NEW-HIGH-08 — provas financeiras contraditórias
O Codex constatou que LEDGER-08 permite que ReleaseReservation vença sobre RecordReceipt válido simplesmente por timing de lock. Corrija a semântica: ordem de lock garante exclusão mútua, **não** determina veracidade. Especifique representação durável de evidências de receipt e de no-effect, com identificadores, valor real, moeda, provider, operação e estado de verificação. Defina quando no-effect pode ser considerado conclusivo, como preservar receipt válido, como reconhecer evidência conflitante/tardia e como bloquear decisão na presença de contradição. Não permita estado RELEASED definitivo com receipt autenticado que demonstra custo real. Use bloqueio para investigação segura quando a precedência não puder ser estabelecida sem inventar gasto ou apagar prova. Resolva crash, evento tardio, repetição, retry, terminalidade e a integridade `spent_minor + reserved_minor <= budget_limit_minor`; não permita redespacho automático.

Revise o oráculo LEDGER-08 com disputa **semanticamente conflitante**, não apenas dois comandos em concorrência. Adicione negativos que rejeitam conclusão incorreta e garantem preservação de evidências, estado e auditoria. Especifique tratamento de `pending_actual_minor` ou equivalente para custo conhecido bloqueado por budget, de modo consistente com outros estados.

### Correção NEW-HIGH-07 / NEW-HIGH-09 — confiança de evidências
Não basta um `evidence_ref` apontando para texto com digest e author class security_operator. Defina um contrato tipado da evidência com `operation_id`, `provider_id`, `receipt/provider_ref`, moeda, valor, marca temporal, origem, tipo de prova, hash, cadeia de proveniência e verificação de vínculo. Identifique quem/qual serviço pode capturar a prova; se o provider não fornece atestado verificável, defina classificação de confiança e procedimento explícito para casos sem prova conclusiva, sem presumir assinatura que não existe. Separe captor, aprovador e confirmador, e não aceite conteúdo arbitrário criado pelo aprovador como prova de efeito/no-effect. Delimite validação independente, privilégio mínimo, sessão com autenticação forte e frescor, política fora do LLM, escopo org/project e trilha íntegra. Mantenha o humano aprovando e o system aplicando efeito monetário somente após autorização válida. Não habilite coding_engine, adapter ou reviewer a fazer reconciliação financeira.

### MEDIUM — ciclo de autorizações e custo pendente
Defina no catálogo, tipos, máquina de estados e oráculos o comportamento de replay com mesmo `command_id`, duplicata com command_id novo, conflito de decisão ou `evidence_ref`, expiração/revogação de permissão, Confirm não autorizado, segundo Apply (mesmo e novo command_id) e transação/auditoria únicas. Estabeleça estrutura tipada e imutável para receipts/custo real pendente quando `actual > estimate`, inclusive conflito posterior.

### Metadados
Corrija em `docs/reviews/ROUND7-CHANGE-REPORT-2026-10-13.md` a identificação ambígua de “commit auditado”: `4e57839` é o commit da baseline Round 6; a baseline Round 7 efetivamente revisada pelo Codex foi `decef2809b61d3f1fe84bef74a5162d782cc6231`. Preserve o relatório histórico original se a política impedir edição, usando errata datada em vez de sobrescrever fonte histórica.

### Entrega e critérios
- Produza v1.5 somente dos documentos afetados, com ponteiros normativos coerentes e matriz canônica única; registre explicitamente documentos v1.3/v1.4 não modificados.
- Preserve a baseline v1.4 e os pareceres históricos em `historical/round7/`, sem alterações retroativas.
- Atualize F-015, FDP-16A e matriz LEDGER-08/11/12 e crie oráculos adicionais se indispensáveis; cada oracle deve ter fixture, passos, PASS/FAIL positivos e negativos e evidências requeridas.
- Produza `docs/planning/FDP-ROUND8-STATUS-INDEX.md`, `docs/reviews/ROUND8-FINDING-CLOSURE-2026-10-13.md`, change report, consistency report e open pendencies.
- Verifique 41 histórias, 17 P0, compatibilidade dos 11 estados Task, links e histórico. Faça verificações documentais, NÃO testes de software/staging; mantenha NOT RUN.
- Não infira aprovação FDP-14, FDP-15 ou Founder. Não autorize BUILD-00.
- Faça commit não destrutivo no repositório e informe SHA; se o push for impossível, entregue patch/pacote e explique.
- Marque tudo **ROUND 8 — CANDIDATE FOR CODEX REVIEW**. É proibido declarar PASS próprio.

Seu objetivo é fechar as lacunas apontadas, **sem reabrir decisões já aceitas nem transformar o planejamento em um ciclo infinito**. O Codex fará auditoria independente sobre o SHA entregue.
