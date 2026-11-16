# Guia para apresentar o Observa

Objetivo de hoje, 16/11: Bruno explicar a solução aos dois colegas, conferir a divisão de falas e deixar a demonstração pronta para gravar em 17/11. O [roteiro do vídeo](roteiro-video.md) define telas, falas e duração.

## Explicação em linguagem simples

O programa recebe um vídeo de exercício e uma gravação de fala. No vídeo, localiza articulações, calcula medidas de uma repetição completa e compara com uma execução correta de referência. Na fala, transforma áudio em texto e procura expressões de atenção, considerando alguns casos de negação e passado. Reúne as evidências em uma sessão que pode ser revisada, confirmada e exportada.

Nos exemplos, **PM_001** identifica um vídeo do dataset. **Repetição completa** escolhe uma execução dentro dele, usando os intervalos anotados. **Repetição 1** é a referência de calibração; **repetição 2** é um exemplo correto distinto; **repetição 6** é um exemplo incorreto. **A01–A04** identificam nossas gravações de calibração, combinadas com o vídeo para a demonstração.

**Referência do dataset** é o gabarito da repetição analisada. **Execução correta usada para calibração** é o movimento de apoio fornecido ao modelo. São informações com funções diferentes. O modelo não recebe o gabarito da consulta para decidir a classe.

## Etapas da explicação interna — aproximadamente 30 minutos

1. **5 minutos:** abrir o painel e explicar os controles e a referência de calibração.
2. **10 minutos:** Bruno demonstra repetição 1/A01, repetição 2/A01 e repetição 6/A02, confirma o alerta e abre JSON/HTML.
3. **5 minutos:** mostrar A03, o erro conhecido de A04 e os números do relatório técnico.
4. **10 minutos:** cada colega executa ou narra pelo menos uma parte do roteiro. Ajustar a divisão e anotar dúvidas.

## Verificação pelos colegas

- Conseguimos explicar o problema e as duas modalidades em uma frase.
- Sabemos por que a referência não conta como acerto.
- Conseguimos executar os cenários sem trocar o gabarito pelo resultado do modelo.
- Conseguimos confirmar o recebimento e mostrar a confirmação no arquivo exportado.
- Sabemos que as fontes dos exemplos são independentes e o protótipo não envia mensagens à equipe médica.
- Sabemos explicar F1, precisão, recall, os 21 desvios perdidos e a limitação do áudio.
- Sabemos onde estão código, relatório técnico e instruções de reprodução.

Bruno deve confirmar a realização dessa passagem para encerrar **T30**. A existência deste guia não comprova que os colegas já foram preparados. O ensaio cronometrado e a gravação permanecem nas tarefas de 17/11.

## Perguntas prováveis

| Pergunta | Resposta curta |
| --- | --- |
| Por que usar uma referência da mesma pessoa? | Medidas absolutas variaram entre participantes; a referência permite comparar a execução com um apoio personalizado. Ela é uma entrada adicional exigida pelo protocolo atual. |
| Como medimos se funcionou? | Comparamos predições fora do treino da pessoa com rótulos anotados, excluindo as oito referências. Para áudio, comparamos a transcrição com os roteiros e as regras com classes esperadas. |
| Por que o painel pode acertar um caso que o experimento errou? | O modelo final do painel foi ajustado nos dados de desenvolvimento completos; as métricas usam modelos que deixam a pessoa avaliada fora do ajuste. |
| É tempo real? | Processa arquivos gravados. Os tempos na linha de eventos são posições nos arquivos. |
| É diagnóstico ou detector de alteração vocal? | Produz sinalizações experimentais de movimento e conteúdo falado. Não avalia doença por voz nem substitui avaliação profissional. |
| Por que não Azure? | O recorte atualizado informado pelo grupo permite execução local. Pose e transcrição são executadas em CPU com pesos locais. |
| O clone já tem tudo para executar? | Tem código, configurações e evidências. Dependências, pesos, vídeos e gravações próprias exigem preparação conforme o README. |

## Entrega final de 17/11

Gravar até 15 minutos; publicar no YouTube ou Vimeo com acesso por link; informar o endereço definitivo para inclusão no README e no relatório; conferir a reprodução do vídeo e o acesso ao repositório; submeter no portal antes de **17/11/2026 às 23h59, horário de Brasília**. Guardar a confirmação da submissão.
