# Teste da primeira rodada — 14/11

Na pasta do projeto, abra um terminal PowerShell e execute:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File .\testar-primeira-rodada.ps1
```

O comando transcreve novamente apenas A01–A04 com Whisper small local e abre `reports/primeira-rodada.html`. A05–A08 permanecem reservados. A opção de execução vale somente para esse processo, sem alterar a política global do Windows. Acrescente `-NoOpen` para executar sem abrir o navegador.

Para consultar a saída existente, basta abrir o relatório HTML.

## O que verificar

1. Ouça cada áudio e confira se você leu exatamente o roteiro ou usou palavras diferentes. Se houver diferença, ajustaremos a referência manual, preservando a gravação original.
2. Compare a transcrição com o que você realmente falou e anote diferenças que alteram o sentido.
3. Confira a classificação: A01 sem expressão de atenção prevista; A02 relato atual; A03 sintoma negado; A04 contexto passado.
4. Inspecione as articulações da pessoa principal nas imagens e possíveis detecções extras na borda. A classificação automática do exercício pertence à próxima etapa.
5. Envie seu retorno com o ID e o comportamento observado. Não precisa regravar para corrigir erro do modelo.

## Resultado técnico

Regras limitadas a dor, falta de ar e alguns contextos de negação e passado. A transcrição original é preservada. O artefato `sentidor` recebe interpretação auxiliar explícita e aviso para conferência; WER continua calculada sobre a transcrição original.

Oito testes automatizados passaram, incluindo contexto misto e preservação do texto. As quatro classificações coincidiram com o roteiro de calibração. Esse resultado não é avaliação final ou validação clínica.

Fechado em 14/11: ambiente, modelos, amostras, pose, transcrição humana e pacote de revisão. As regras iniciais foram adiantadas de forma limitada para permitir essa revisão. Para 15/11 permanecem medidas em repetições completas, classificação de movimento e evolução dos relatórios. Para 16/11: painel integrado, avaliação reservada, relatório técnico e preparação do grupo.
