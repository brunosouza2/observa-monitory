# Preparação da entrega — 16/11/2026

**Estado:** pacote técnico e material de apresentação preparados; conferência humana dos áudios e passagem ao grupo pendentes de confirmação. Gravação, publicação e submissão permanecem em 17/11.

## Executado nesta rodada

| Tarefa | Resultado e evidência |
| --- | --- |
| T16.1 — preparar conferência das referências | [Procedimento de escuta](../testes/revisao-audio-16-11.md), com arquivos, textos e classes esperadas. Bruno confirmou disponibilidade para ouvir; isso ainda não é confirmação do conteúdo. |
| T28 — revisão técnica do relatório | Escopo explícito, arquitetura implementada, métricas preservadas, diferença entre modelo final e avaliação externa, erro de A04, confirmação manual de 15/11 e reprodução documentados no [relatório](../relatorios/relatorio-tecnico.md). PDF gerado com dez páginas; fechamento das referências de áudio pendente. |
| T29 — preparar roteiro e demonstrações | [Roteiro de 12–13 minutos](../apresentacao/roteiro-video.md), cenários e falas, divisão proposta entre os colegas e [guia de passagem interna](../apresentacao/guia-do-grupo.md). |
| T31 — acesso e reprodução na máquina escolhida | Bruno confirmou que a apresentação será neste computador. Repositório público respondeu HTTP 200 sem autenticação; `main` remoto conferido. Os quatro cenários da demonstração passaram no ambiente local já preparado, com AppTest. |
| Evidências selecionadas | [Quatro sessões JSON/HTML](../../reports/entrega/README.md) com fontes reduzidas ao nome do arquivo, indicação de geração automatizada e hashes no manifesto. Nenhuma mídia ou peso foi incluído. |
| Verificações de código | 28 testes unitários passaram em 16/11. Os hashes de fontes congeladas da versão original foram preservados. |

## Como interpretar a reprodução

O fluxo local processou calibração, consulta correta distinta, desvio com fala afirmativa e erro conhecido de transcrição. A confirmação do terceiro cenário foi acionada automaticamente pelo script; não é confirmação humana nem avaliação de qualidade. A exportação JSON/HTML foi verificada quanto ao conteúdo. Downloads reais em Chrome e abertura manual dos arquivos já tinham sido conferidos em 15/11; não foram repetidos como parte desta rodada de AppTest.

A verificação usou a instalação e caches existentes. Não demonstra instalação limpa em outro computador. Acessibilidade pública foi conferida pelo endereço do repositório; não substitui a conferência final do vídeo e dos arquivos antes da submissão.

O F1 0,79 continua sendo o agregado da avaliação personalizada retrospectiva em 126 consultas, com oito apoios excluídos. O painel usa o modelo final ajustado nos dados conhecidos. Na repetição 6 de PM_001, há sinalização no painel, mas falso negativo na predição externa; a distinção está descrita no relatório e roteiro.

## O que depende de Bruno e do grupo

1. **Bruno:** ouvir A05–A08 e confirmar se as palavras coincidem com os roteiros. Se houver diferença, registrar o texto efetivamente ouvido e revisar a conclusão do áudio, preservando o resultado original.
2. **Bruno:** abrir o PDF e conferir apresentação e legibilidade; o conteúdo técnico já foi revisado.
3. **Bruno + colegas:** fazer a passagem da solução com o guia, definir quem opera/narra e confirmar que conseguem seguir os cenários (T30). A preparação do documento não conclui a passagem humana.

## Mantido para 17/11

Ensaio cronometrado, gravação de até 15 minutos, publicação YouTube/Vimeo, inclusão do link definitivo em `configs/entrega.json`, README e relatório regenerado, conferência de acesso e submissão antes de **23h59, horário de Brasília**. Não há submissão automática ao portal nesta rodada.
