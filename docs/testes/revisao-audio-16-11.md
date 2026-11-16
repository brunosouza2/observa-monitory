# Conferência das referências de áudio — 16/11/2026

Esta revisão encerra T16.1. Ela confere se o que foi realmente gravado coincide com os roteiros usados na avaliação. Não exige nova gravação, novo treinamento ou novo teste independente.

## Onde encontrar

- **Referências:** [roteiros-audio.csv](../../data/scenarios/roteiros-audio.csv), linhas A05–A08, coluna `texto`. Abra no VS Code ou em outro editor de texto.
- **Gravações:** pasta local `data/recordings`, arquivos `A05.m4a` a `A08.m4a`. Abra pelo Explorador de Arquivos e ouça no reprodutor de áudio.
- **O que o modelo transcreveu:** [audio-teste-small.json](../../reports/audio-teste-small.json), lista `results`, campos `reference`, `transcript` e `analysis.attention` de cada ID.

As gravações pessoais não estão no GitHub. Este procedimento deve ser feito neste computador. O seletor **Áudio de calibração** do painel oferece somente A01–A04; A05–A08 são os arquivos da avaliação reservada original e não aparecem nesse seletor.

## O que conferir

| Arquivo para ouvir | Referência, coluna `texto` | Classificação esperada, coluna `atencao` | Motivo |
| --- | --- | --- | --- |
| A05.m4a | Gostaria de parar porque estou sentindo dor. | sim | Relato afirmativo de dor. |
| A06.m4a | Hoje estou bem e não sinto falta de ar. | nao | A expressão está negada. |
| A07.m4a | Estou com falta de ar durante o movimento. | sim | Relato afirmativo de falta de ar. |
| A08.m4a | O exercício terminou e estou confortável. | nao | Nenhuma expressão prevista de atenção. |

1. Ouça cada arquivo antes de olhar a transcrição do modelo, se possível.
2. Compare as palavras faladas com a referência acima. Pontuação e maiúsculas não alteram esta conferência.
3. Se houver diferença, escreva o ID e as palavras efetivamente ouvidas, incluindo omissões ou acréscimos. Não substitua automaticamente o roteiro pela saída do modelo.
4. Informe ao Codex se as quatro referências coincidem ou quais precisam de correção. A conclusão será registrada separadamente do resultado original de 14/11.

Os quatro textos reconhecidos coincidiram com os roteiros na execução original. O WER zero foi calculado contra esses roteiros; a escuta humana ainda precisa ser confirmada. A conferência feita pelo próprio autor das gravações não equivale a uma anotação independente e cega por outro avaliador.
