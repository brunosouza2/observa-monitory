# Observa — monitoramento multimodal local

Protótipo de análise de exercício por vídeo e transcrição de fala em português. Desde 15/11, o movimento é comparado com uma execução correta de referência da mesma pessoa e vista. A avaliação exploratória personalizada teve F1 0,79 em 126 consultas, com oito referências excluídas. O teste original, preservado, teve F1 0,39 em outro protocolo. Esses resultados não constituem uma comparação direta no mesmo teste. As sinalizações são experimentais e exigem revisão humana.

## Acompanhar o trabalho

Repositório GitHub: [brunosouza2/observa-monitory](https://github.com/brunosouza2/observa-monitory).

Consulte [TAREFAS.md](TAREFAS.md) para ver o estado de cada etapa, as pendências, os responsáveis propostos e a próxima ação. Esse é o checklist principal; o planejamento detalha as decisões e mantém o histórico.

A documentação está organizada por finalidade no [índice de docs/](docs/README.md).

## Abrir o painel neste computador

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\iniciar-painel.ps1
```

Acesse http://127.0.0.1:8501. Mantenha o terminal aberto e encerre com Ctrl+C. O script utiliza o Python portátil em `.tools/python` e pesos locais. Não há API de cloud.

O inicializador também identifica a página como português e solicita que o navegador não a traduza. Se uma aba antiga já estiver traduzida, escolha “Mostrar original” e recarregue antes de testar. Detalhes em [correcao-navegador-15-11.md](docs/operacao/correcao-navegador-15-11.md).

Veja o [guia de 15/11](docs/testes/teste-15-11.md) para testar os exemplos, enviar arquivos, confirmar alertas e registrar feedback. O painel aceita uma repetição de elevação lateral do braço direito, vista frontal, com intervalo e execução correta de referência informados para arquivos próprios. Sem referência adequada, ele se abstém de classificar.

## Resultados e entregáveis

- [Relatório técnico em Markdown](docs/relatorios/relatorio-tecnico.md) e [PDF](docs/relatorios/relatorio-tecnico.pdf).
- [Reprodução dos experimentos](docs/operacao/reproducao.md).
- [Planejamento e estado do cronograma](docs/planejamento/planejamento-fase-4.md).
- [Roteiro do vídeo e demonstrações](docs/apresentacao/roteiro-video.md) e [guia para o grupo](docs/apresentacao/guia-do-grupo.md).
- [Evidências selecionadas de sessões JSON/HTML](reports/entrega/README.md), geradas por verificação funcional automatizada, com confirmação identificada como automática.
- Métricas e matrizes em `reports/video-*-metrics.json`; áudio reservado em `reports/audio-teste-small.json`.
- Sessões e confirmações em `reports/sessions`; feedback em `reports/feedback`.

As pastas de sessões e feedback completos são locais e não estão no GitHub. Os quatro exemplos selecionados em `reports/entrega` estão versionados, sem mídia bruta ou caminhos locais completos. A arquitetura está no [diagrama](docs/relatorios/arquitetura.md) e no PDF. Situação da preparação de 16/11: [acompanhamento](docs/acompanhamento/preparacao-16-11.md).

**Vídeo da apresentação:** pendente de gravação e publicação em 17/11. Ao receber o link definitivo do YouTube/Vimeo, atualizar `presentation_url` em `configs/entrega.json`, esta linha do README e gerar novamente o relatório técnico. A entrega só se encerra após a conferência dos links e a submissão.

Vídeo: 51 repetições de treino, 41 de validação e 42 de teste, com pessoas separadas. Áudio: A01–A04 para calibração e A05–A08 para a primeira avaliação reservada. No áudio reservado houve coincidência com os quatro roteiros. Bruno confirmou essa correspondência por escuta em 16/11; o [registro da revisão](reports/audio-revisao-manual-16-11.json) é separado da avaliação original. A conferência foi feita pelo autor das gravações, sem anotação independente e cega. Esses dados de teste já foram utilizados: futuras alterações não terão neles um teste independente novo.

## Preparar em outro computador

Instale Python 3.11, crie um ambiente virtual e execute `python -m pip install -r requirements-lock.txt`. Execute os comandos na raiz do projeto. Baixe dados e pesos antes de iniciar:

- Vídeos: `python scripts/obter_videos.py --videos PM_001 PM_012 PM_023 PM_032 PM_039 PM_122 PM_109 PM_114`. O script baixa somente entradas selecionadas do ZIP oficial e verifica tamanho e CRC.
- Pose: https://github.com/ultralytics/assets/releases/download/v8.3.0/yolov8n-pose.pt em `models/yolov8n-pose.pt`.
- Whisper: `python scripts/baixar_whisper.py --model small`.
- Gravações próprias em `data/recordings`; não são distribuídas automaticamente. Na ausência delas, use uploads próprios no painel.
- Inicie com `python -m streamlit run app.py --server.address 127.0.0.1`.

Internet é necessária para essa preparação. Pesos, vídeos grandes, uploads e gravações próprias ficam fora do Git. O classificador atual está em `configs/movement-reference-v2.json`, sem pickle; `configs/movement-model.json` preserva a primeira versão. Versões completas em `requirements-lock.txt`.

## Dados e modelos

REHAB24-6: https://zenodo.org/records/13305826. Dados de pesquisa acadêmica ou não comercial conforme os termos indicados pelos autores; cite Černek, Sedmidubsky e Budikova, REHAB24-6: Physical Therapy Dataset for Analyzing Pose Estimation Methods, SISAP 2024. Vídeos e anotações de correção e intervalos por repetição.

Modelos: YOLOv8n-Pose (https://docs.ultralytics.com/models/yolov8/) e Whisper small via faster-whisper (https://github.com/SYSTRAN/faster-whisper). Bibliotecas e pesos têm seus próprios termos e licenças. O Whisper usa os pesos públicos Systran/faster-whisper-small.

## Verificar

```powershell
& .tools/python/python.exe -c "import sys,unittest;sys.path.insert(0,'.');r=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.discover('tests'));sys.exit(not r.wasSuccessful())"
& .tools/python/python.exe scripts/testar_painel.py
```

O teste do painel usa exemplos de desenvolvimento e confirma um alerta, produzindo uma sessão local. Métricas, limitações e instruções estão no relatório técnico. Processar gravações não comprova funcionamento em tempo real nem validação clínica.

Para preparar/verificar os quatro cenários da apresentação e regerar as evidências selecionadas: `& .tools/python/python.exe scripts/preparar_demonstracao.py`. Isso usa a instalação e os dados locais; não representa uma instalação limpa. A verificação do conteúdo exportado é separada do download real em navegador já conferido em 15/11.
