# Ensaio de viabilidade — 14/11/2026

Escopo executado: preparação local e primeiro teste de pose e transcrição. Este registro não representa avaliação final do projeto.

## Ambiente

- Python portátil 3.11.9 dentro de `.tools/python`.
- Windows, oito processadores lógicos e aproximadamente 15,8 GiB de memória física, conforme consulta pelo Python.
- Inferência em CPU. Versões instaladas em `requirements-lock.txt`.
- `pip check`: nenhuma dependência incompatível reportada.
- Scripts compilados com `compileall` sem erro de sintaxe.

## Dados e observações

Obtidas duas entradas do ZIP oficial REHAB24-6 por HTTP Range, verificando CRC, sem precisar baixar 2,7 GB. Arquivos PM_000/Camera17 e PM_039/Camera17, exercício 1: abdução do braço. As anotações e sua descrição estão em `data/samples`.

Foram recortados 60 quadros a partir do início de uma repetição correta do PM_000 e de uma incorreta do PM_039. São trechos parciais de dois segundos usados para verificar inferência, e não unidades completas para avaliação da correção. As anotações selecionadas estão em `reports/amostras-anotacoes.json`.

| Ensaio | Resultado | Duração de execução |
| --- | --- | --- |
| Pose no trecho com rótulo correto | Pose presente em 60 de 60 quadros | 5,49 s |
| Pose no trecho com rótulo incorreto | Pose presente em 60 de 60 quadros | 5,85 s |
| Transcrição em português | Frase sintética transcrita localmente | 1,38 s |
| Transcrição de teste em inglês | Áudio oficial de teste transcrito localmente | 1,31 s |

Tempos de uma execução, incluindo carregamento do modelo e outras operações do script. Não são benchmark robusto nem latência em tempo real. A pose nesses trechos não acompanhou os 30 quadros/s de origem na configuração inicial.

O quadro anotado foi inspecionado visualmente. A pessoa principal recebeu articulações plausíveis; também houve uma detecção adicional de baixa confiança na borda. Será necessário selecionar a pessoa de interesse e filtrar qualidade ao implementar medidas.

## Áudio em português

Usado Windows SpeechSynthesizer, voz Microsoft Maria Desktop pt-BR, para gerar localmente a frase de teste:

> Durante o exercício eu senti dor no braço. Agora estou melhor.

Whisper base, CPU int8, retornou:

> Durante o exercício eu sentidor no braço, agora estou melhor.

WER: 18,18%, após remoção de pontuação e conversão para minúsculas. Uma única frase sintética verifica instalação e revela um erro de segmentação de palavras; não mede qualidade em consultas reais. O resultado estruturado está em `reports/ensaio-audio-portugues.json`.

## Próximas etapas

- Gravar os oito roteiros em `data/scenarios/roteiros-audio.csv`, preservando os quatro casos de teste para avaliação posterior.
- Extrair repetições completas e escolher um subconjunto com separação por participante.
- Implementar seleção da pessoa, medidas e regras de movimento.
- Comparar base e small na calibração se a qualidade de transcrição exigir.
- Integrar painel e relatório final conforme o planejamento.

Preparação e execução dos primeiros modelos concluídas. Classificação do exercício, regras textuais, interface e avaliação agregada ainda pendentes.
