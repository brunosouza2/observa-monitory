# Preparação e reprodução

**Método estabilizado em 15/11; preparação da entrega em 16/11:** os passos abaixo preservam o experimento original. Depois dos caches, execute `scripts/experimento_movimento_v2.py` e `scripts/experimento_referencia.py`. O painel atual usa `configs/movement-reference-v2.json`, condicionado a uma referência correta. Protocolo e resultados em [rodada-15-11.md](../experimentos/rodada-15-11.md); teste manual em [teste-15-11.md](../testes/teste-15-11.md).

Os scripts devem ser executados a partir da raiz do projeto. Os comandos abaixo usam o Python portátil já preparado neste computador. Em outro computador, instale Python 3.11, crie um ambiente virtual e use `python -m pip install -r requirements-lock.txt`. O Python portátil e os pesos não são versionados.

1. Obtenha os pesos de pose e Whisper conforme README.
2. Baixe os vídeos com `python scripts/obter_videos.py --videos PM_001 PM_012 PM_023 PM_032 PM_039 PM_122 PM_109 PM_114`.
3. Para reproduzir as medidas, use `python scripts/extrair_movimento.py --partition train`, depois `validation` e `test`. A extração guarda um cache por hash da fonte e parâmetros.
4. O classificador congelado está em `configs/movement-model.json`. `python scripts/treinar_movimento.py --evaluate-test` compara esse artefato com a partição de teste sem reajustá-lo. O script verifica a assinatura dos arquivos que definem o experimento.
5. Para novo treinamento, use uma cópia limpa dos resultados anteriores e preserve o relatório da primeira avaliação. O comando `python scripts/treinar_movimento.py` utiliza exclusivamente treino e validação e se recusa a reajustar depois que há métricas de teste nesse diretório.
6. Para áudio, `python scripts/avaliar_audio_reservado.py` usa parâmetros e regras registrados em `configs/audio-protocol.json`. As referências ainda devem ser conferidas pelo usuário por escuta.
7. Abra o painel com `powershell -NoProfile -ExecutionPolicy Bypass -File .\iniciar-painel.ps1`. Ele fica somente em `http://127.0.0.1:8501`. Encerrar com Ctrl+C no terminal.

O protótipo processa arquivos gravados; não há garantia de processamento em tempo real. Arquivos próprios podem conter apenas uma repetição, ou um intervalo informado manualmente. A classificação só se destina ao exercício e vista definidos no protocolo.

## Conferir a demonstração de 16/11 neste computador

Bruno confirmou que este será o computador da demonstração. Com a instalação, modelos e dados já presentes:

```powershell
& .tools/python/python.exe scripts/preparar_demonstracao.py
& .tools/python/python.exe scripts/gerar_relatorio_tecnico.py
```

O primeiro comando processa os quatro cenários e verifica a referência, classes, transcrição/contexto, confirmação e conteúdo exportado. Grava saídas selecionadas em `reports/entrega`; não copia mídia bruta. É uma verificação funcional por AppTest com caches locais e confirmação automática identificada. Não é teste independente, instalação limpa ou novo teste de download no navegador.

Para uma instalação em ambiente virtual, use `python` no lugar de `.tools/python/python.exe`. Prepare o idioma com `python scripts/preparar_interface.py` e inicie com `python -m streamlit run app.py --server.address 127.0.0.1`. O inicializador PowerShell da raiz usa especificamente o Python portátil deste computador.

As métricas e configurações treinadas estão versionadas e podem ser inspecionadas sem pesos ou dados brutos. Para executar a demonstração, o clone precisa de dependências, pesos, vídeos e das gravações A01–A04. Se não tiver as gravações, use **Meus arquivos** com áudio próprio; isso não reproduz exatamente os quatro cenários acima.

A revisão humana das referências A05–A08 está descrita em [revisao-audio-16-11.md](../testes/revisao-audio-16-11.md). O resultado original de áudio é preservado; eventual confirmação posterior é documentada separadamente.
