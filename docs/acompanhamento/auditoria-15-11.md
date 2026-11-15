# Auditoria das tarefas de 15/11

O objetivo é concluir o bloco de domingo do cronograma, incluindo a conferência manual indicada. O escopo não foi reduzido às verificações automáticas.

| Requisito de hoje | Evidência inspecionada | Estado |
| --- | --- | --- |
| T14: investigar erros do movimento | Medidas por pessoa, coeficientes originais e `docs/experimentos/rodada-15-11.md` | Concluído tecnicamente. |
| T15: implementar e avaliar uma abordagem delimitada | `scripts/experimento_referencia.py`, protocolos em `configs`, métricas em `reports/v2/reference-metrics.json` | Concluído tecnicamente; avaliação exploratória condicional a um apoio correto, sem alegação de teste novo. |
| Preservar o experimento original | Teste de hashes dos arquivos congelados de v1 e resultados originais | Verificado. |
| Evitar pontuar a própria referência | Suportes excluídos das consultas; teste de conjuntos disjuntos e teste de calibração no painel | Verificado. |
| Reproduzir os artefatos usados no painel | Exportação conjunta do modelo e apoios no script do experimento; igualdade dos apoios exportados e armazenados | Verificado. |
| T16: conferir referências A01–A04 | Resposta de Bruno em 15/11: nenhuma diferença adicional percebida além de A04 | Concluído para a calibração. Referências A05–A08 ficam na revisão final de 16/11. |
| Tratar o erro conhecido de áudio | Glossário testado e não adotado; texto original e aviso preservados | Concluído como investigação, sem prometer correção automática. |
| Fluxo técnico de interface e relatórios | Testes de processamento, gabaritos, calibração, confirmação persistida, arquivos exportados e controles de download | Verificado automaticamente. |
| T26.1: usuário baixar/abrir JSON e HTML e conferir confirmação | Bruno confirmou explicitamente em 15/11: “Sim, confirmei o alerta e abri os dois arquivos”. | Concluído. |
| T27: conferir a rodada com Bruno | Quatro feedbacks humanos novos confirmam calibração, execução correta, incorreta e fala. O erro de interface foi tratado e Bruno confirmou “Tudo está funcionando depois das alterações”. | Concluído na rodada atual. |

28 testes unitários passaram na execução mais recente. Foram recebidos quatro feedbacks humanos novos, preservados e relacionados às sessões em `docs/operacao/correcao-navegador-15-11.md`. Registros explicitamente automatizados não foram contados como revisão do usuário. O fluxo e os downloads reais foram verificados em Chrome isolado e, posteriormente, Bruno confirmou a abertura dos arquivos na sua própria conferência.

## Conclusão da auditoria

A implementação, a avaliação delimitada, as correções e a conferência manual previstas para 15/11 estão concluídas. As confirmações humanas encerraram T26.1 e T27. O registro final está em `docs/acompanhamento/fechamento-15-11.md`; revisão final dos entregáveis e preparação do grupo continuam em 16/11, e publicação/submissão em 17/11.
