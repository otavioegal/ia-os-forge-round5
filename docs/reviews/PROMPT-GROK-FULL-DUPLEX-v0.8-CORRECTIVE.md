# PROMPT CORRETIVO GROK — FULL-DUPLEX v0.8

## Mandato e baseline
Repositório: https://github.com/otavioegal/ia-os-forge-round5
SHA imutável auditado: 1a71dfa44fc2c88174c113e5c68eddc18d6cfad3
Parecer obrigatório: docs/reviews/PARECER-CODEX-FULL-DUPLEX-v0.7-2026-10-15.md
Veredito Codex: FAIL DOCUMENT-ONLY.
Leia integralmente parecer, pacote v0.7, v0.6, v0.5, baseline FDP-16A v1.7, CMP v0.3, ata Founder e histórico dos pareceres. Não confunda checker estático com execução de oráculos. Crie SOMENTE pasta aditiva docs/planning/conversational-full-duplex-v0.8/ e preserve todos os arquivos anteriores e hashes históricos. Não inicie BUILD-00, migrations, deploy, provider, gastos ou alterações de flags. Não declare PASS nem feche findings sem parecer independente.

## FD07-05 PARTIAL — sequência negativa e efeitos de todos os negativos
Adicionar fixture FX03-NEGATIVE-SEQUENCE com n=-1, stream alocado, ACK_REGRESSION, zero escrita, high-water idêntico, zero dinheiro, mic fechado. Inclua ID em REQUIRED. Checker deve conferir zero_effect, zero_new_effect, zero_money, opens_mic e opaque em TODAS as linhas negativas (zero, futuro, regressão, duplicata, unallocated, mismatch, ambos null). Mutação de qualquer campo declarado deve gerar erro não zero específico. Documente matriz de códigos, estado inicial/final, efeito e oráculo. Não apenas acrescentar campo sem validá-lo.

## FD07-06 OPEN — isolamento por stream e receiver
Estender fixture com session_id, ack_stream_id e receiver_participant_id, ao menos 2 streams alocados e 2 receivers; high-water por chave {session_id, ack_stream_id, receiver_participant_id} dentro do tenant organization_id/project_id. Operações intercaladas sobre trios distintos; verificador mantém mapa de estados e prova que apenas a chave alvo mudou. Negativos cross-stream, receiver errado, tenant errado e stream não alocado; 404 opaco quando aplicável; nenhum lock/efeito cruzado. Testes de mutação que fazem falhar se uma outra chave for alterada. Preserve ack_of_sequence e ack_stream_id como par: ambos null => NO_ACK, XOR null => 422 ACK_SCOPE_MISMATCH antes de unallocated, sem inferência pelo stream_id do evento.

## FD07-07 OPEN — concorrência monotônica
Preservar norma SQL da v0.6: unique física tenant-composta, INSERT/ON CONFLICT, SELECT FOR UPDATE e UPDATE guardado por :n > peer_ack_high_water; commit serializado e releitura do perdedor. Adicionar especificação executável FUTURA de teste PostgreSQL de 2 transações concorrentes com barreira real e as duas ordens, n=1 e n=2; final=2, nunca 2->1; perdedor ACK_REGRESSION ou ACK_DUPLICATE. Outra race com trios distintos prova ausência de lock compartilhado indevido. Enquanto testes não forem executados, marcar NOT RUN e não confundir com replay sequencial de fixture. Nenhuma migration real.

## FD07-08 PARTIAL — replay e efeitos observáveis
Estender contrato/fixture com identidade durável de ACK (event_id/command_id conforme baseline), outbox/audit/idempotency se aplicáveis, sem inventar ledger novo. Repetir mesmo ACK com mesma identidade e identidade distinta; provar high-water estável, nenhum movimento financeiro, nenhuma abertura de mic e nenhum efeito de transporte duplicado. Checker deve conferir zero_new_effect=true e contadores observáveis, e distinguir teste estático de oráculo transacional NOT RUN. Definir idempotência dentro da transação e crash/rollback.

## FD07-09 PARTIAL — cadeia de pareceres
Não inventar que Codex auditou v0.5/v0.6. Buscar nos arquivos históricos apenas pareceres realmente existentes com SHA e veredito; se ausentes, corrigir a rastreabilidade da v0.8 dizendo claramente 'v0.5/v0.6 candidatos, sem parecer independente incorporado'. Nunca modificar v0.5/v0.6/v0.7. Gerar manifest SHA-256 verificável dos arquivos históricos e comparação contra SHA base, somente leitura. Não falsificar aprovação.

## HIGH-03, NEW-MEDIUM-06 e LOW-01
HIGH-03 permanece PARTIAL até fechar evidências documentais e ter oráculos de concorrência executados em fase autorizada. NEW-MEDIUM-06 foi CLOSED documentalmente pelo Codex v0.7: preservar Opção B, null ativo tratado antes de unique index e predicado correto; migration NOT RUN. LOW-01 permanece OPEN BLOCKING DoR: owner pessoa PENDING, effort UNSTATED, DoR NOT MET até decisão humana. Preservar todos findings CLOSED e AQs aprovadas (01/02/03/05/06/07/08/10/11) e deferred (04/09/12).

## Entrega e gates
Pacote v0.8 com índice, norma de ACK, fixtures positivas/negativas, checker estático autocontido, oráculos O84+ ou identificadores não conflitantes, matriz de traceabilidade, disposition por finding, change report, consistency report, migration design se necessário, e manifest histórico. Explicitar se novos oráculos são apenas especificações NOT RUN. Flag forge.conversation.delta.v4 OFF. FDP-14/FDP-15 e BUILD-00 pendentes. Nenhuma chamada real de provider. Se executar somente checagens estáticas permitidas, registrar comando, ambiente, exit code e escopo PASS_FIXTURE_ONLY sem afirmar PASS de produto. Ao finalizar, publicar commit aditivo e SHA completo como CANDIDATE FOR CODEX REVIEW, para auditoria independente em clone read-only.
