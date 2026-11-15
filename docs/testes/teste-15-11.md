# Revisão de 15/11 — comparação com referência correta

Reinicie o painel com `powershell -NoProfile -ExecutionPolicy Bypass -File .\iniciar-painel.ps1` e abra http://127.0.0.1:8501. Se já estiver aberto, encerre o processo anterior com Ctrl+C antes de iniciar novamente.

## O que mudou

O movimento agora é comparado com uma execução correta da mesma pessoa. Nos exemplos, a referência vem das anotações do dataset e aparece em “Execução correta usada para calibração”. O rótulo da repetição analisada continua sendo usado apenas como gabarito de comparação.

A repetição 1 de PM_001 é a referência de calibração. Por isso ela aparece como “Execução usada para calibração”, sem escore de classificação. Para testar uma repetição correta diferente, use a repetição 2.

## Testes funcionais de desenvolvimento

Para fechar a conferência manual de hoje, execute as três primeiras linhas da tabela, depois confira o alerta e os downloads. As duas últimas repetem casos de fala já revisados e são opcionais nesta rodada. Clique em “Processar sessão” a cada combinação.

| Vídeo de exercício | Repetição completa | Áudio de calibração | Resultado a conferir em Movimento | Classificação textual esperada |
| --- | --- | --- | --- | --- |
| PM_001 | 1 | A01 | Execução usada para calibração; não contar como acerto | nao |
| PM_001 | 2 | A01 | Sem desvio sinalizado (experimental); gabarito correta | nao |
| PM_001 | 6 | A02 | Possível desvio (experimental); gabarito incorreta | sim |
| PM_001 | 2 | A03 | Sem desvio sinalizado (experimental); gabarito correta | nao |
| PM_001 | 2 | A04 | Sem desvio sinalizado (experimental); gabarito correta | contexto_passado |

Esses são exemplos conhecidos de desenvolvimento, não novos testes independentes. O resultado agregado do experimento vem de predições feitas deixando a pessoa inteira fora do treinamento, e não dos acertos mostrados no painel.

## Onde conferir e como salvar sua avaliação

- Em **Movimento**, confira **Resultado** e **Referência do dataset**. A segunda é o gabarito da repetição; a execução usada para calibração aparece em uma mensagem separada. No primeiro teste, apenas confirme que aparece “Execução usada para calibração”. Não conte isso como classificação correta.
- Em **Fala**, ouça o áudio e confira a transcrição. Compare **Classificação textual** com **Resultado esperado da fala**.
- Nos testes de repetição 2 e 6, desça até **Registrar sua avaliação**. Em **Avaliação do movimento**, selecione “Concordo com o movimento” somente se observou o resultado esperado. Se uma execução correta gerou alerta, escolha “Falso alerta: execução correta sinalizada”; se a incorreta não gerou alerta, escolha “Desvio não detectado: execução incorreta sem sinalização”.
- Em **Avaliação da fala**, selecione “Transcrição e contexto corretos” somente se ambos estiverem corretos, ou a opção de erro correspondente. **Como ficou a análise desta sessão?** pode permanecer em “Ainda não conferi”, pois os dois campos específicos são suficientes.
- Anote diferenças em **Observações e trecho afetado**, clique em **Salvar avaliação** e espere a mensagem “Avaliação salva em reports/feedback”. Salve antes de trocar de teste.

## Fechar a conferência de exportação e alerta

1. Processe PM_001, repetição 6, com A02.
2. Na seção “Eventos e resposta”, clique em “Confirmar recebimento do alerta”. Deve aparecer “Recebimento registrado em” com data/hora.
3. Clique em “Baixar JSON”. Abra o arquivo e procure `acknowledged_utc`: deve ter data/hora, não `null`.
4. Clique em “Baixar relatório HTML”. Abra o arquivo no navegador e confira se contém o mesmo ID de sessão, as entradas, a transcrição e a confirmação.
5. Informe se os dois arquivos abriram e a confirmação ficou registrada. Caso encontre erro, envie a mensagem e o ID da sessão.

Não é necessário regravar A04: a transcrição original continua com o erro conhecido “sentidor”; o contexto é mostrado separadamente e o aviso de revisão permanece.

## Arquivos próprios

Para classificar um vídeo próprio é necessária uma referência correta da mesma pessoa, vista e exercício, com seu intervalo informado. Sem referência ou com pose insuficiente, o programa deve se abster de classificar e explicar o motivo. As gravações devem ser simuladas e os movimentos confortáveis; a solução não avalia risco clínico.
