# Revisão manual — 14/11/2026

Recebidas cinco avaliações de Bruno em `reports/feedback`. Foi excluído desta revisão o registro identificado explicitamente como teste automatizado. Os registros originais foram preservados.

## Sessões recebidas

| Sessão | Entrada | Avaliação geral registrada | Divergência observável nos resultados |
| --- | --- | --- | --- |
| `0e51b2116935` | PM_001, repetição 1 + A01 | Concordo com o resultado | Movimento sinalizou desvio, mas o dataset indica execução correta. Fala classificada como `nao`. |
| `fe6b6bb78b27` | PM_001, repetição 6 + A01 | Concordo com o resultado | Movimento não sinalizou desvio, mas o dataset indica execução incorreta. Fala classificada como `nao`. |
| `daabc2c54ac6` | PM_001, repetição 1 + A02 | Concordo com o resultado | Mesmo falso alerta de movimento da primeira sessão. Fala classificada como `sim`. |
| `faa7cec4520f` | PM_001, repetição 1 + A03 | Concordo com o resultado | Mesmo falso alerta de movimento. Fala classificada como `nao`, com negação identificada. |
| `60749846a690` | PM_001, repetição 1 + A04 | Houve erro na transcrição ou no contexto | Mesmo falso alerta de movimento. Transcrição uniu `senti dor` em `sentidor`; contexto classificado como passado. |

No comentário de A04, o usuário identificou a grafia percebida como “sentido” e confirmou a frase pretendida “Ontem senti dor, mas agora estou bem”. O texto efetivamente salvo pelo reconhecedor é “Ontem sentidor, mas agora estou bem”. A correção auxiliar já existente sinalizou a possível união de palavras, sem alterar a transcrição original ou o cálculo de WER.

## Interpretação

As quatro escolhas gerais “Concordo” não permitem atribuir aprovação específica ao vídeo, à fala ou à interface. Não serão contabilizadas como validação humana da correção dos movimentos. As divergências do vídeo são comparações objetivas com os rótulos, sem alterar a opinião registrada pelo usuário.

Há duas repetições distintas de vídeo nesses cinco testes. Repetir a mesma execução com áudios diferentes não cria quatro novos exemplos independentes de movimento. Para as duas repetições observadas, houve um falso alerta e um desvio não detectado. Os cinco testes manuais não substituem a avaliação reservada de 42 repetições.

O erro de A04 é de transcrição; a classificação `contexto_passado` permaneceu coerente com o roteiro, por meio de uma regra auxiliar explícita. Não é necessário regravar para mascarar o erro do modelo.

## Ações

- Concluído: receber e relacionar os cinco feedbacks às sessões, preservando os originais.
- Concluído: acrescentar avaliações específicas de movimento e de fala ao formulário, mantendo a avaliação geral por compatibilidade.
- Pendente: investigar por que as medidas e o classificador confundem repetições corretas e incorretas.
- Pendente: avaliar melhoria de transcrição na próxima rodada de desenvolvimento, preservando a evidência original de A04.
- Pendente: conferir exportação e confirmação de alertas; os cinco registros, por si só, não comprovam esses testes.

Não solicitar uma nova rodada igual apenas para preencher os novos campos. A informação já recebida é suficiente para iniciar a investigação técnica. Os dados e erros desta revisão são agora exemplos de desenvolvimento.
