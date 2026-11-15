# Relatório técnico — rodada experimental de 14/11/2026

## 1. Objetivo e estado da entrega

Protótipo de revisão multimodal de um exercício de reabilitação, executado localmente. As entradas são vídeo e áudio; texto é uma saída da transcrição. O recorte local com duas modalidades segue a orientação do grupo, registrada no planejamento. O PDF original permanece em context/.

A solução estima pose, resume medidas por repetição, classifica possíveis desvios, transcreve a fala e aplica regras textuais. O painel reúne evidências e permite confirmar um alerta e exportar os resultados. O funcionamento é sobre arquivos gravados, sem garantia de tempo real.

Estado: fluxo implementado e primeira avaliação realizada. A qualidade de classificação do movimento ainda é insuficiente: F1 0.389 no teste e resultado inferior à referência simples de sinalizar tudo. A entrega é experimental, com essa limitação explícita. Publicação do vídeo de apresentação e revisão humana final ainda pendentes.

## 2. Dados, seleção e separação

Vídeo: REHAB24-6, exercício 1 (abdução do braço direito), câmera 17, vista frontal. Foram baixadas oito gravações por intervalos HTTP do ZIP oficial e verificada a integridade por tamanho e CRC. Fonte: https://zenodo.org/records/13305826. Os termos indicados são de uso acadêmico ou pesquisa não comercial, com citação do trabalho dos autores.

Treino: participantes 1, 2, 3 e 4 (PM_001, PM_012, PM_023, PM_032), 51 repetições. Validação: participantes 5 e 7 (PM_039, PM_122), 41 repetições. Teste: participantes 8 e 9 (PM_109, PM_114), 42 repetições. Os grupos não compartilham pessoas. As repetições e rótulos são fornecidos pela base. O protótipo depende desses intervalos ou de delimitação manual em arquivos próprios.

Áudio: oito gravações em português fornecidas pelo usuário. A01–A04 serviram à calibração; A05–A08 à primeira avaliação reservada depois do registro das regras e configuração. As referências são os roteiros esperados, ainda sem verificação independente por escuta. Esta é uma limitação da métrica WER apresentada.

Os exemplos combinam vídeo público e fala própria, portanto são cenários compostos de fontes independentes. Uma gravação própria com fala no mesmo vídeo permite utilizar um relógio comum. Arquivos grandes, pesos e gravações próprias ficam fora do Git.

## 3. Arquitetura e execução

Python 3.11, OpenCV, Ultralytics YOLOv8n-Pose, NumPy, scikit-learn, faster-whisper, jiwer e Streamlit. Versões exatas em requirements-lock.txt. O ambiente portátil está em .tools/python, fora do Git.

Fluxo: vídeo -> seleção da pessoa e estimativa de pose -> medidas por quadro -> resumo da repetição -> classificador. Áudio -> Whisper small -> transcrição original e tempos dos segmentos -> regras de expressões de atenção. Os dois caminhos alimentam os eventos da sessão, o painel e o relatório.

A interface é servida somente em 127.0.0.1:8501. Inferência em CPU e pesos locais; internet é necessária para preparação, não para chamadas de inferência. Uploads e resultados ficam em reports/uploads e reports/sessions. O estado de confirmação do alerta é persistido. A exportação oferece JSON estruturado e HTML legível. Feedback manual fica em reports/feedback.

As fontes e seus hashes permitem relacionar as saídas à execução. Extração de pose usa cache identificado pelo hash do vídeo e parâmetros. A reprodução de métricas verifica hashes do protocolo e dos arquivos do experimento congelado.

## 4. Modelos e decisões

YOLOv8n-Pose pré-treinado estima articulações COCO. Seleciona-se a maior pessoa inicialmente e a mais próxima do centro anterior nos quadros seguintes. Deslocamentos incompatíveis e articulações com baixa confiança impedem medidas. Essa heurística ainda pode falhar com múltiplas pessoas.

Amostragem: um quadro a cada seis, origem a 30 FPS, resultando em aproximadamente 5 FPS para medidas. Confiança mínima de articulação: 0,35. Cobertura mínima: 65%, com pelo menos cinco amostras válidas por intervalo. Medidas: percentil 90 de abdução do ombro, amplitude entre percentis 90 e 10, percentil 10 do ângulo do cotovelo, percentil 90 de inclinação do tronco, assimetria de ombros normalizada pelo torso e duração. Coordenadas são projeções 2D, sensíveis à câmera.

Classificador: regressão logística com características padronizadas, C=1, classes balanceadas e semente 42. Ajuste das estatísticas e pesos somente no treino. Limiar 0.35, escolhido dentre 11 valores entre 0,25 e 0,75 por F1 na validação. O escore é estatístico e não representa probabilidade de risco clínico. Configuração final em configs/movement-model.json.

Áudio: Whisper small multilíngue com faster-whisper, CPU int8, idioma pt, VAD e beam_size=5. O modelo base foi comparado apenas na calibração: WER 17,86%, contra 7,14% do small. A transcrição original é preservada.

Regras: dor e falta de ar, negação por palavras próximas e marcação limitada de contexto passado. O artefato sentidor recebe interpretação auxiliar explícita e aviso de conferência; WER não utiliza essa correção. Essas regras não interpretam toda a língua portuguesa e não diagnosticam condições médicas.

Eventos de vídeo e fala são apresentados separadamente. Só há combinação temporal quando as fontes são declaradas sincronizadas; janela de proximidade de cinco segundos. A confirmação registra recebimento, sem prescrever conduta.

## 5. Resultados e interpretação

Movimento — classe positiva: execução incorreta/desvio. Treino: F1 0.815; validação: F1 0.625; teste: F1 0.389, precisão 0.467, recall 0.333, acurácia 0.476.

No teste, foram classificadas 42 de 42 repetições, sem abstenções por cobertura. Matriz: TN=13, FP=8, FN=14, TP=7. Ter pose suficiente não implica classificação correta. A referência de sinalizar toda repetição como desvio tem F1 0.667, superior ao classificador. O desempenho não sustenta uma afirmação de monitoramento confiável. Os erros ficaram registrados e os parâmetros não foram reajustados após o teste.

Áudio reservado: 4 arquivos, 30 palavras de referência, WER 0.00%; concordância das classes textuais com o roteiro: 100%. São quatro frases de um único contexto de gravação e não uma estimativa de generalização. A escuta pelo usuário ainda deve validar as referências.

Ensaios iniciais de pose: 60 quadros em aproximadamente 5,5–5,9 segundos por trecho, incluindo inicialização. Não sustentam tempo real a 30 FPS. As extrações completas têm tempos registrados no cache. Máquina: Windows, oito processadores lógicos e aproximadamente 15,8 GiB de memória, inferência em CPU.

Verificações: testes automatizados de contexto, geometria, qualidade insuficiente, separação temporal, combinação condicionada à sincronização e escape do HTML. O teste de aplicação executou processamento, exibição de resultado e confirmação persistida. O servidor respondeu HTTP 200. Conferência visual final no navegador deve ser realizada pelo usuário.

## 6. Limitações e próximos experimentos

A primeira hipótese de classificador não generalizou bem entre participantes. O resultado desfavorável é mantido como evidência. Uma próxima versão deve investigar erro de pose, seleção da pessoa, câmera, movimentos compensatórios e representatividade das características. Mudanças baseadas nos erros já observados transformarão esses exemplos em desenvolvimento; não será correto chamar uma reavaliação deles de teste independente.

Um experimento posterior pode usar validação cruzada por participante, com seleção de parâmetros dentro de cada divisão, ou novos participantes e gravações reservadas. Também será necessário avaliar segmentação automática de repetições, falhas na estimação, iluminação, ângulos de câmera e grupos clínicos.

O texto usa regras de alcance restrito; uma negação distante ou um contexto temporal mais complexo pode produzir erro. Silêncio, ruído e expressões ausentes do vocabulário precisam de mais casos de avaliação. A amostra de oito gravações é pequena.

O sistema demonstra integração e rastreabilidade, não benefício clínico, diagnóstico, prevenção de incidentes ou conformidade para uso assistencial. O fluxo de alerta permanece uma demonstração de revisão humana.

## 7. Reprodução, evidências e apresentação

Iniciar: powershell -NoProfile -ExecutionPolicy Bypass -File .\iniciar-painel.ps1. Abrir http://127.0.0.1:8501. Guia de teste: docs/testes/teste-segunda-rodada.md. Reprodução do experimento: docs/operacao/reproducao.md.

Arquivos de evidência: reports/video-train-metrics.json, reports/video-validation-metrics.json, reports/video-test-metrics.json e reports/audio-teste-small.json. Artefatos: configs/video-protocol.json, configs/movement-model.json e configs/audio-protocol.json.

No vídeo de apresentação, demonstrar primeiro o fluxo e a inspeção das evidências, depois os números agregados e os erros. Mostrar uma execução correta que foi sinalizada indevidamente e um desvio não detectado. Explicar a diferença entre integração funcional e desempenho do classificador.

Preparar apresentação de 10–12 minutos: contexto e recorte (2 min), vídeo e medidas (3 min), transcrição e contexto (2 min), relatório e confirmação de alerta (2 min), resultados e limitações (2 min). Link da gravação: pendente de publicação pelo grupo.

Referências: REHAB24-6, https://zenodo.org/records/13305826; YOLOv8, https://docs.ultralytics.com/models/yolov8/; faster-whisper, https://github.com/SYSTRAN/faster-whisper; regressão logística, https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LogisticRegression.html. Fontes e instruções detalhadas no README.
