# Segunda rodada de teste — painel integrado

## Iniciar

**Atualização de 15/11:** este roteiro descreve a versão anterior. Para o painel atual, siga [teste-15-11.md](teste-15-11.md): PM_001, repetição 1 passou a ser a referência de calibração e não é classificada como consulta.

Na raiz do projeto, execute:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\iniciar-painel.ps1
```

Acesse http://127.0.0.1:8501 no navegador. O terminal precisa permanecer aberto; encerre com Ctrl+C. A interface executa os modelos no computador.

## Testar os exemplos

1. Mantenha “Exemplos de desenvolvimento”. Selecione PM_001, repetição 1 e áudio A02. Clique em “Processar sessão”. A primeira execução carrega os modelos; aguarde.
2. Confira a pessoa selecionada no quadro, os ângulos no gráfico e a transcrição. Em Movimento, “Resultado” é a decisão do programa e “Referência do dataset” é o gabarito, agora sempre visível abaixo do resultado. PM_001, repetição 1: correta; repetição 6: incorreta.
3. Em Fala, compare “Classificação textual” com “Resultado esperado da fala”. Troque A02 por A03 e processe novamente. A negação deve ser preservada. Com A04, confira o contexto passado e o aviso sobre “sentidor”. Em “Contexto e evidências”, a ausência de expressões previstas agora aparece explicada em texto.
4. Confira os eventos. Se houver alerta, clique em “Confirmar recebimento do alerta”. Baixe JSON e HTML e verifique se a confirmação aparece nos arquivos.
5. Registre “Avaliação do movimento” e “Avaliação da fala” separadamente, além das observações. A avaliação geral é opcional se uma modalidade já foi avaliada. Os registros ficam em `reports/feedback`.

Os vídeos e áudios dos exemplos são de fontes independentes. O painel os reúne em uma sessão composta e não afirma que se referem à mesma pessoa ou ao mesmo relógio.

## Testar arquivo próprio (opcional)

Na opção “Meus arquivos”, envie um vídeo frontal curto com uma repetição completa de elevação lateral do braço direito, informando início/fim em segundos. Você pode enviar áudio separado ou selecionar “Usar a fala do próprio vídeo”. Somente essa última opção considera as fontes sincronizadas.

Não é necessário provocar dor ou realizar movimentos desconfortáveis. A fala pode ser uma encenação. A análise só contempla o exercício especificado e não deve ser interpretada como avaliação clínica.

## O que já sabemos

- Áudio reservado A05–A08: quatro transcrições coincidiram com os roteiros; as quatro classificações textuais também. O gabarito ainda precisa ser conferido por escuta humana.
- Movimento: no primeiro teste independente, o classificador errou frequentemente e ficou abaixo da referência simples de sinalizar tudo em F1. Portanto, avalie principalmente a seleção da pessoa, a qualidade das medidas e o funcionamento do fluxo. Não assuma que o resultado do classificador é correto.
- Repetições vêm de intervalos anotados no dataset ou informados manualmente. A segmentação automática ainda não existe.

Envie o ID da sessão, sua observação e os passos para reproduzir qualquer falha. Os arquivos de feedback podem apoiar o próximo desenvolvimento, mas não serão apresentados como um novo teste independente.
