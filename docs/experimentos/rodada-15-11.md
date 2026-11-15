# Rodada técnica de 15/11

## Investigação dos erros

A primeira versão utilizava seis medidas absolutas e uma fronteira linear. O coeficiente da abdução favorecia sinalizar amplitudes maiores, porém em alguns participantes as execuções incorretas tinham menor elevação. A duração e a geometria também variavam entre pessoas. A associação aprendida não se sustentou em outros participantes. Essa é uma explicação parcial, baseada nas medidas e coeficientes, não uma causa comprovada de todos os erros.

## Experimentos preservados

| Experimento | Protocolo | Consultas | F1 | F1 de sinalizar tudo |
| --- | --- | --- | --- | --- |
| Original, 14/11 | Primeiro teste independente | 42 | 0,389 | 0,667 |
| Genérico, 15/11 | Validação aninhada retrospectiva por pessoa | 134 | 0,641 | 0,673 |
| Personalizado, 15/11 | Validação aninhada retrospectiva por pessoa, com um apoio correto por pessoa | 126 | 0,790 | 0,701 |

Não comparar 0,39 e 0,79 como se fossem resultados no mesmo teste independente. Os oito participantes já foram estudados. A versão personalizada recebe informação adicional: uma execução correta de referência da mesma pessoa e vista. Os oito apoios foram excluídos das métricas.

O experimento genérico não melhorou o suficiente. Escolha técnica para o protótipo: comparação personalizada. A seleção de regressão logística/floresta ocorre dentro dos grupos de treino. Uma pessoa inteira fica de fora do ajuste em cada laço externo; ela fornece apenas o apoio correto explicitamente declarado. A decisão não recebe o rótulo da execução analisada.

Na versão personalizada: precisão 0,922; recall 0,691; acurácia 0,802; matriz [TN, FP; FN, TP] = [[54, 4], [21, 47]]. O F1 médio entre participantes foi aproximadamente 0,691, e o participante 3 teve F1 zero. Logo, o método ainda perde desvios e necessita de confirmação futura em novos participantes.

O modelo de demonstração é treinado nos dados de desenvolvimento completos. Os acertos do painel não são as predições fora de treino usadas para calcular essas métricas.

## Implementado

- Quinze medidas, incluindo cotovelo e tronco durante a fase elevada.
- Diferenças assinadas e absolutas em relação ao apoio, totalizando trinta entradas.
- Artefato final: regressão logística C=0,3, classes balanceadas, padronização e limiar 0,5.
- Exportação em JSON, com equivalência de inferência verificada contra scikit-learn.
- Apoio mostrado no painel e persistido na sessão. Sem apoio ou pose válida, abstenção.
- Sobreposição da consulta com o próprio apoio marcada como calibração, sem escore.
- Aviso para reprocessar sessões de modelo anterior, preservando os registros no disco.

## Áudio e revisão

Bruno confirmou não ter percebido divergências adicionais nos roteiros A01–A04, além da união “senti dor” em A04. Um glossário geral foi testado apenas na calibração: não corrigiu o erro nem reduziu WER (7,14%). Não foi adotado. Permanecem Whisper small, texto original, aviso e contexto passado.

Não é necessário regravar para esconder erro do reconhecedor. A conferência das referências de A05–A08 permanece como item da revisão final do relatório.

## Verificação e reprodução

24 testes automatizados cobrem geometria, contexto, ausência de referência, exclusão dos apoios das consultas, ausência do rótulo da consulta na decisão, igualdade de inferência JSON/scikit-learn, reprodução das referências de calibração e preservação de v1. Testes da interface verificam processamento, gabaritos, confirmação e feedback. A conferência manual de downloads pelo usuário é registrada separadamente no checklist.

Com os caches de pose disponíveis, executar:

1. `python scripts/experimento_movimento_v2.py`
2. `python scripts/experimento_referencia.py`
3. `python scripts/experimento_audio_v2.py` — tentativa não adotada.
4. `python scripts/gerar_relatorio_tecnico.py`
5. `python scripts/testar_rodada_15.py`

Resultados novos em `reports/v2`. Artefato atual em `configs/movement-reference-v2.json`; apoios em `configs/movement-references-v2.json`. Relatório de 14/11 preservado em `docs/historico`. Procedimento para o usuário: [teste-15-11.md](../testes/teste-15-11.md).
