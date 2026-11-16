# Roteiro do vídeo — Observa

**Duração planejada: 12 a 13 minutos; limite do desafio: 15 minutos.** Publicar no YouTube ou Vimeo como público ou não listado. A demonstração será feita no computador de Bruno, com dados e modelos já preparados.

**Plano atualizado em 16/11:** Bruno fará a apresentação sozinho, operando o painel e narrando os blocos abaixo. Essa é a organização atual da gravação; o trabalho continua sendo o projeto do grupo.

## Preparação antes de gravar

1. Leia o [guia do apresentador](guia-apresentador.md). Abra o [relatório técnico](../relatorios/relatorio-tecnico.pdf) e o [repositório](https://github.com/brunosouza2/observa-monitory).
2. Na raiz do projeto, execute `powershell -NoProfile -ExecutionPolicy Bypass -File .\iniciar-painel.ps1`. Abra http://127.0.0.1:8501 e mantenha a tradução automática desativada.
3. Processe uma sessão de ensaio para carregar os modelos. O cache pode acelerar as seguintes; não apresente esse tempo como uma medição de inferência nova.
4. Deixe acessíveis a [arquitetura](../relatorios/arquitetura.md), as figuras de resultados e os [exemplos exportados](../../reports/entrega/README.md).
5. Feche abas e notificações pessoais. Use zoom que permita ler os campos. Grave a tela e a narração com teste prévio de som.

## Fala e telas

| Tempo | Tela e ação | Fala sugerida — Bruno |
| --- | --- | --- |
| 0:00–1:00 | Título do projeto e painel | “O Observa é um protótipo local para revisar um exercício de reabilitação por vídeo e fala. Escolhemos elevação lateral do braço direito, de frente. As saídas ajudam a revisar evidências; não fazem diagnóstico.” |
| 1:00–2:00 | Diagrama de arquitetura | “YOLO estima articulações, calculamos medidas e comparamos a repetição com uma execução correta da mesma pessoa. Whisper transcreve a fala, e regras identificam expressões como dor e falta de ar, com negação e contexto passado. Os resultados chegam ao painel e aos relatórios.” |
| 2:00–3:00 | **Exemplos de desenvolvimento** → PM_001 → repetição 1 → A01 → **Processar sessão** | “A primeira repetição é a referência correta fornecida para calibração. O painel informa ‘Execução usada para calibração’, sem escore. Ela não entra como acerto nas métricas.” |
| 3:00–4:15 | PM_001 → repetição 2 → A01 → **Processar sessão**; mostrar pose, gráfico e fala | “Esta é uma repetição diferente da referência. Neste exemplo não foi sinalizado desvio. ‘Referência do dataset’ é o gabarito usado para conferir a saída. Na fala, A01 não contém os termos de atenção previstos.” |
| 4:15–6:15 | PM_001 → repetição 6 → A02 → **Processar sessão** | “Agora temos um exemplo com possível desvio e a frase ‘Sinto dor no braço quando levanto a mão’. A transcrição é preservada e a regra sinaliza ‘sim’. Vídeo e áudio aqui vêm de fontes independentes: é um cenário composto, sem sincronização clínica.” |
| 6:15–7:30 | **Eventos e resposta** → **Confirmar recebimento do alerta** → **Baixar JSON** e **Baixar relatório HTML** | “O painel reúne os eventos e permite registrar recebimento. Essa confirmação não é aprovação do resultado nem conduta médica. O JSON contém o horário em ‘acknowledged_utc’; o HTML mostra o mesmo ID e as evidências.” Abra um dos arquivos baixados. |
| 7:30–8:30 | PM_001 → repetição 2 → A03 → **Processar sessão** | “Em ‘Não estou sentindo dor no braço’, o termo aparece negado. A classificação esperada é ‘nao’. O sistema considera contexto, dentro de regras limitadas.” |
| 8:30–9:30 | PM_001 → repetição 2 → A04 → **Processar sessão** | “Também preservamos erros: em A04, ‘senti dor’ foi unido como ‘sentidor’. A transcrição original continua visível e há um aviso de revisão. A interpretação auxiliar reconhece o contexto passado; isso não corrige artificialmente a métrica de transcrição.” |
| 9:30–11:30 | Matriz de confusão personalizada, comparação com sinalizar tudo e tabela de protocolos do relatório | “Na avaliação personalizada retrospectiva foram 126 consultas de oito pessoas, com oito referências excluídas. O F1 agregado foi 0,79, precisão 0,92 e recall 0,69: ainda perdemos 21 desvios e tivemos quatro falsos alertas. O F1 do primeiro teste foi 0,39 em outro protocolo; não são medidas diretamente comparáveis. Os exemplos do painel são conhecidos e usam o modelo final treinado nos dados de desenvolvimento.” |
| 11:30–12:30 | Resultados de áudio e limitações | “Nos quatro áudios reservados originais houve WER zero contra os roteiros, confirmados por escuta pelo próprio autor das gravações em 16/11. A amostra é pequena e controlada. A04 mostra que outros áudios podem falhar. Não detectamos fadiga ou disartria por características da voz.” |
| 12:30–13:00 | README e relatório técnico no GitHub | “O repositório contém código, modelos estatísticos em JSON, resultados, evidências selecionadas e instruções para baixar pesos e dados. O processamento é local sobre arquivos gravados. Os próximos passos são testar novos participantes, ampliar a avaliação e melhorar os desvios não detectados.” |

Se o tempo exceder 13 minutos no ensaio, reduza a navegação de A03 e a leitura da arquitetura. Preserve a demonstração de alerta/exportação, as métricas e as limitações.

Ao apresentar sozinho, termine cada frase antes de mudar de tela. Durante o processamento, explique a entrada selecionada ou faça uma pausa. Se gravar em blocos e editar as esperas, mantenha a ordem das ações e identifique eventuais cortes; o tempo do vídeo editado não é uma medição do processamento.

## Afirmações que precisam de precisão

- **F1 0,79** é resultado exploratório retrospectivo, condicionado à referência correta da mesma pessoa e vista. Não é acurácia e não é probabilidade de risco clínico.
- **Recall 0,69** significa que 47 dos 68 desvios anotados foram detectados nessa avaliação; 21 foram perdidos. **Precisão 0,92** significa que 47 das 51 sinalizações corresponderam a desvios anotados.
- **PM_001, repetição 6:** o painel final sinaliza desvio. Na predição externa, sem treinar nas consultas dessa pessoa, esse mesmo exemplo foi um falso negativo. Isso ilustra por que acertos na demonstração não substituem as métricas.
- **Áudio:** a análise identifica o conteúdo da transcrição, não alterações acústicas indicativas de doença. ‘nao’ significa ausência de expressão afirmativa prevista pelas regras.
- **Local e duas modalidades:** esse é o recorte atualizado informado por Bruno. O PDF original foi preservado; não apresentar integração Azure, terceira frente de sinais vitais ou tempo real como funcionalidades implementadas.
- **Alerta:** o fluxo demonstrado termina no painel, com confirmação persistida. Não existe envio implementado a hospital, médico, e-mail ou celular.
- **Dois documentos:** o relatório da sessão é a saída automática JSON/HTML; o relatório técnico explica arquitetura, experimentos, resultados e limitações.

## Se houver falha durante a gravação

Pare a tomada, registre a mensagem e refaça o trecho depois de corrigir. Para continuar a explicação, abra os exemplos em `reports/entrega`, identificando-os como saídas previamente geradas por verificação automatizada. Identifique a origem da saída e da confirmação ao mostrá-las.

Se o modelo exibir algo diferente da tabela, confira primeiro as entradas e clique novamente em **Processar sessão**. O resultado abaixo dos controles pertence à última sessão processada.
