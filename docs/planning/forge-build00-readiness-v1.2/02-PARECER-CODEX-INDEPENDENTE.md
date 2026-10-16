# Parecer independente do Codex — página de decisão v1.2

**Commit revisado:** cc7110bf001b273b97de483d130772d5cdde0fa2
**Parent:** a5af11c2e291560d0e2dc12cec32de1daade07c0
**Escopo:** leitura dos dois arquivos novos da v1.2 e comparação com os registros citados abaixo.
**Resultado:** REVISÃO NECESSÁRIA. Não é PASS, não declara prontidão, não autoriza BUILD-00 e não fecha findings anteriores.

## O que confere

- A v1.2 apresenta as duas regras como recomendações pendentes de decisão, sem afirmar que foram aprovadas.
- O caminho preferido AIOX e o fallback FORGE_DIRECT correspondem à história F-013 do registro FDP-19A v1.7. O fallback limita os efeitos a NONE ou INTERNAL e exclui deploy.release e efeitos EXTERNAL.
- A v1.2 mantém separada a autorização para começar BUILD-00.
- As decisões FDP-14, FDP-15 e a base v1.7 continuam referenciadas no registro de encerramento, sem reescrita dos documentos anteriores.

## Pontos que precisam ficar explícitos antes de levar a página ao Founder

1. **A regra de execução por agentes cobre as histórias e os spikes?** A recomendação fala em dispensar nomes humanos por história. O FDP-20 v1.3 também deixa pendente a atribuição dos nove spikes do BUILD-00. A página deve dizer se a regra proposta inclui esses spikes. Mesmo que inclua, isso não calibra horas nem autoriza executá-los.
2. **Quem decide os detalhes de implementação?** A página diz que Claude Code coordena e que detalhes dentro da base aceita não precisam voltar ao Founder. Não afirma diretamente se Claude Code decide quando houver discordância técnica com AIOX dentro desse escopo. Se essa é a recomendação, deve ser escrita; se não, deve dizer que o trabalho para.
3. **Os demais gates humanos continuam?** A frase “aprovando só o que é de alto impacto” pode parecer uma lista completa. A página deve esclarecer que as duas recomendações não removem controles já previstos, incluindo a aprovação humana específica de cada publicação em produção descrita em FDP-18 v1.3 e FDP-19A v1.7, história F-029.

## Estado

As três pendências acima impedem considerar a página pronta para decisão. Nomes de pessoas e horas calibradas continuam pendentes. A aprovação das recomendações, se vier, não autoriza BUILD-00. Nenhum teste de produto, spike, banco, migração, fornecedor ou implantação foi executado nesta revisão.
