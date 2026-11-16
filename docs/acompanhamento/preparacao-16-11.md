# Preparação da entrega — 16/11/2026

**Estado: preparação de 16/11 concluída no plano atual.** Pacote técnico e roteiro individual preparados, referências de áudio confirmadas por Bruno e revisão do relatório concluída. Bruno informou que fará o vídeo sozinho; a passagem interna aos colegas foi dispensada por essa decisão. Ensaio, gravação, publicação e submissão permanecem em 17/11.

## Executado nesta rodada

| Tarefa | Resultado e evidência |
| --- | --- |
| T16.1 — conferir referências por escuta | Bruno confirmou “Conferi, tudo está correto.” para A05–A08. [Registro da revisão](../../reports/audio-revisao-manual-16-11.json), com os hashes das gravações e da avaliação original. Referências mantidas. |
| T28 — revisão do relatório concluída | Escopo explícito, arquitetura implementada, métricas preservadas, diferença entre modelo final e avaliação externa, erro de A04, confirmação manual de 15/11 e revisão de áudio de 16/11 documentados no [relatório](../relatorios/relatorio-tecnico.md). PDF regenerado com dez páginas. Link definitivo do vídeo será incluído após publicação em T36. |
| T29 — preparar roteiro e demonstrações | [Roteiro individual de 12–13 minutos](../apresentacao/roteiro-video.md), cenários e falas para Bruno narrar e operar o painel; [guia do apresentador](../apresentacao/guia-apresentador.md). |
| T30 — passagem interna dispensada | Bruno informou: “Por hora, pode considerar que farei o vídeo sozinho.” A tarefa foi encerrada por mudança explícita de plano, mantendo o ensaio individual em T32. |
| T31 — acesso e reprodução na máquina escolhida | Bruno confirmou que a apresentação será neste computador. Repositório público respondeu HTTP 200 sem autenticação; `main` remoto conferido. Os quatro cenários da demonstração passaram no ambiente local já preparado, com AppTest. |
| Evidências selecionadas | [Quatro sessões JSON/HTML](../../reports/entrega/README.md) com fontes reduzidas ao nome do arquivo, indicação de geração automatizada e hashes no manifesto. Nenhuma mídia ou peso foi incluído. |
| Verificações de código | 28 testes unitários passaram em 16/11. Os hashes de fontes congeladas da versão original foram preservados. |

## Como interpretar a reprodução

O fluxo local processou calibração, consulta correta distinta, desvio com fala afirmativa e erro conhecido de transcrição. A confirmação do terceiro cenário foi acionada automaticamente pelo script; não é confirmação humana nem avaliação de qualidade. A exportação JSON/HTML foi verificada quanto ao conteúdo. Downloads reais em Chrome e abertura manual dos arquivos já tinham sido conferidos em 15/11; não foram repetidos como parte desta rodada de AppTest.

A verificação usou a instalação e caches existentes. Não demonstra instalação limpa em outro computador. Acessibilidade pública foi conferida pelo endereço do repositório; não substitui a conferência final do vídeo e dos arquivos antes da submissão.

O F1 0,79 continua sendo o agregado da avaliação personalizada retrospectiva em 126 consultas, com oito apoios excluídos. O painel usa o modelo final ajustado nos dados conhecidos. Na repetição 6 de PM_001, há sinalização no painel, mas falso negativo na predição externa; a distinção está descrita no relatório e roteiro.

## Próximas ações de Bruno

1. **Em 17/11:** ensaiar a apresentação individual com cronômetro, conferir captura da tela e áudio e gravar seguindo o roteiro (T32/T33).
2. **Antes da gravação:** abrir o PDF e verificar apresentação e legibilidade.

A confirmação dos áudios foi feita pelo próprio autor das gravações; não é anotação independente e cega. Não houve ajuste de regras, regravação ou alteração das métricas. O resultado original mantém seus avisos históricos; a revisão posterior é vinculada por hashes em arquivo separado.

## Mantido para 17/11

Ensaio cronometrado, gravação de até 15 minutos, publicação YouTube/Vimeo, inclusão do link definitivo em `configs/entrega.json`, README e relatório regenerado, conferência de acesso e submissão antes de **23h59, horário de Brasília**. Não há submissão automática ao portal nesta rodada.
