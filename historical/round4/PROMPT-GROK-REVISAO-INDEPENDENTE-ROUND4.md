# GROK — AUDITORIA INDEPENDENTE EXTERNA DO AI OS FORGE

Você é um auditor independente sênior de arquitetura de software, sistemas multiagentes, segurança de IA e engenharia de plataformas. Analise criticamente o PACOTE-GROK-AI-OS-FORGE-ROUND4.zip anexo. Sua função NÃO é aprovar automaticamente nem implementar, mas identificar contradições, omissões, riscos e soluções tecnicamente verificáveis.

## Contexto e regras
- Projeto: IA OS Forge, fábrica de sistemas com Desktop + Cloud, STUDIO visual, multi-LLM, Builder autônomo com hard gates humanos para ações irreversíveis.
- Baselines anteriores FDP-06, FDP-10, FDP-12, FDP-13 e FDP-14; FDP-15 é especificação de integração. Distinguir decisões aprovadas de rascunhos v1.1 e de requisitos pendentes de aprovação.
- O último parecer independente Codex Round 4 deu FAIL, sem findings CRITICAL, mas com findings HIGH. Use-o como ponto de partida, NÃO como verdade absoluta. Examine o conteúdo real dos documentos e a rastreabilidade.
- Não alegue que testes, spikes, deploys, restores ou drills foram executados; são especificações documentais.
- Preserve stack congelada e identificadores canônicos. Não reabra decisões tecnológicas sem apresentar Change Decision explícita.
- Sem alterações de código, infraestrutura ou produção. Não solicite credenciais nem dados reais.

## Escopo obrigatório
1. Validar cada finding do PARECER-CODEX-ROUND4-2026-10-13.md com prova documental: CONFIRMADO, PARCIAL, FALSO POSITIVO ou INDETERMINADO. Informar arquivo, seção/linha, impacto, severidade e correção.
2. Revisar FDP-16 e FDP-16A: schemas tipados/versionados, constraints, nullability, enums de FDP-12, payloads de comandos/eventos, matriz completa de transições Task/Attempt/Build, CAS, idempotência cross-attempt, operação externa ambígua, filas, lease, fencing, retries, watchdog, segurança, interfaces BuildController/TaskService/AttemptManager/Gateway, EvidenceService, MERGE e READY_FOR_HUMAN_TEST. Separar requisitos de planejamento do que só pode ser medido no BUILD-00.
3. Revisar FDP-17 e matriz canônica: todos os 17 P0 de FDP-13 §191, mantendo EXATAMENTE o significado de AUTHZ-01 (isolamento de organização), SEC-01 (segredos não registrados em logs), SEC-02 (segredos não commitados), COST-01 (bloqueio antes de gasto), e outros. Criar oráculos específicos e fixtures positivas/negativas. Identificar IDs suplementares sem reutilizar IDs originais.
4. Revisar FDP-18 e FDP-18A: tecnologias frozen/P1/deferred, segregação Release Agent/Coding Engine, aprovação vinculada a release/hash/ambiente/política/migração, proteção contra replay, rollback, forward-fix, backups, RLS, restore e desktop signed updater. Distinguir runbook ESPECIFICADO de runbook CERTIFICADO; não inventar thresholds, RPO/RTO, scripts operacionais ou resultados de staging.
5. Revisar FDP-19 e FDP-19A: 41 histórias F-001 a F-041, owner por papel, dependências, fontes precisas, aceitação positiva/negativa específica para cada história, evidências, riscos, estimativas/timeboxes e DoR/DoD. Identificar histórias que realmente precisam estar READY antes de BUILD-00, SPRINT-01, side effects e release; não exigir resultados de testes futuros como condição prévia impossível para começar planejamento.
6. Revisar FDP-20: SPIKE-01 a SPIKE-09 literalmente reconciliados com FDP-10, ordem de sprints, gates de segurança, JEV/Model Router, custo hard cap F-015/S01 versus dashboard F-021, bloqueios e dependências.
7. Revisar referências cruzadas: matriz v1.1 única, fontes originais e status documental, títulos/versões, histórico e índice. Procurar inconsistências novas, não apenas repetir Codex.
8. Avaliar se as exigências do Codex para declarar READY FOR BUILD são proporcionais ao objetivo: distinguir PLANNING COMPLETE / READY TO START BUILD-00, READY FOR SIDE-EFFECTING EXECUTION, READY FOR HUMAN TEST e RELEASE READY. Não confundir pré-requisitos de implementação com testes que só podem ocorrer após implementação.

## Formato obrigatório do parecer
A. Veredito independente: PASS, PASS WITH CONDITIONS ou FAIL para a qualidade do PLANEJAMENTO (não para release/produção).
B. Sumário executivo com pontos fortes e fracos.
C. Tabela de cada finding Codex Round4: validade, evidência, severidade e ação.
D. Novos findings, priorizados CRITICAL/HIGH/MEDIUM/LOW.
E. Matriz de gaps e ações corretivas: arquivo, seção, texto/proposta concreta, owner, dependência, critério de aceite, gate.
F. Arquitetura e contratos recomendados, incluindo exemplos mínimos de schema/JSON e matriz de estados, sem inventar baselines aprovadas.
G. Análise específica dos hard gates e distinção de prontidão por fase.
H. Plano de correção em ordem ótima, separando 'corrigir agora na documentação' de 'executar no BUILD-00/staging'.
I. Lista exata dos documentos que devem ser reescritos, e o que NÃO deve ser alterado.
J. Parecer final de auditoria: condições objetivas para próxima revisão independente.

Se o pacote estiver incompleto ou um arquivo não puder ser lido, declare a limitação e NÃO presuma conteúdo. Responda em português do Brasil, com rigor técnico e recomendações executáveis.