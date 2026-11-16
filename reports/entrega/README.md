# Evidências selecionadas para a entrega

Estas saídas reais do painel foram produzidas por `scripts/preparar_demonstracao.py`, com os modelos locais e os exemplos conhecidos de desenvolvimento. Os nomes de fonte foram reduzidos ao nome do arquivo. Não contêm vídeo, gravação de voz ou pesos dos modelos.

**Natureza das evidências:** verificações funcionais automatizadas. A confirmação de recebimento do terceiro cenário foi feita pelo script, acionando o botão da aplicação. Esses registros não são avaliações humanas, novos testes independentes ou comprovação de envio a uma equipe médica.

| Caso | Entradas | Resultado verificado | JSON | HTML |
| --- | --- | --- | --- | --- |
| Referência | PM_001, repetição 1, A01 | Calibração, sem escore; fala nao | [01](01-calibracao.json) | [01](01-calibracao.html) |
| Execução distinta correta | PM_001, repetição 2, A01 | Sem desvio sinalizado; fala nao | [02](02-sem-desvio.json) | [02](02-sem-desvio.html) |
| Desvio e relato de dor | PM_001, repetição 6, A02 | Desvio; fala sim; recebimento confirmado automaticamente | [03](03-alerta-confirmado.json) | [03](03-alerta-confirmado.html) |
| Erro conhecido da transcrição | PM_001, repetição 2, A04 | Texto original e aviso preservados; contexto_passado | [04](04-erro-conhecido-audio.json) | [04](04-erro-conhecido-audio.html) |

O [manifesto](verificacao-16-11.json) registra ambiente, hashes dos pesos e do classificador, resultados e limites da verificação. Estes JSON/HTML são exemplos para inspeção; o HTML no GitHub pode precisar ser baixado para abrir no navegador.

Para conferir a exportação, compare o `id` entre JSON e HTML do caso 03 e procure `acknowledged_utc`, que deve conter data e hora. Em `evidence_metadata`, veja a identificação de confirmação automatizada. Em `alert`, `aligned` e `combined` são falsos porque as fontes são independentes.

As métricas de desempenho vêm de [reference-metrics.json](../v2/reference-metrics.json), e não destes quatro exemplos. A mesma repetição 6 que o painel final sinaliza foi um falso negativo na predição externa do participante; o modelo final e o modelo avaliado fora do treino têm contextos de ajuste diferentes.

Os registros humanos anteriores continuam preservados localmente em `reports/feedback`; o resumo está em [fechamento-15-11.md](../../docs/acompanhamento/fechamento-15-11.md). Downloads reais em navegador e confirmação manual foram verificados em 15/11, separadamente destas evidências automatizadas.

Regerar neste computador: `& .tools/python/python.exe scripts/preparar_demonstracao.py`. Em outro ambiente preparado: `python scripts/preparar_demonstracao.py`. Os IDs e horários mudarão; o script valida os resultados esperados antes de exportar.
