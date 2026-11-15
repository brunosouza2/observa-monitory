# Acompanhamento da entrega

Atualizado em **15/11/2026**, após concluir a rodada técnica e receber a confirmação manual do alerta, downloads e recuperação da interface.

**Prazo: 17/11/2026, às 23h59 (Brasília).** Escopo: vídeo e áudio/transcrição, com execução local.

Este é o checklist principal do projeto. O [planejamento](docs/planejamento/planejamento-fase-4.md) explica as decisões; este arquivo mostra o estado atual. A tabela “Onde estamos” preserva as datas originais; “Cronograma atualizado” orienta o trabalho restante. A cada rodada de trabalho, atualizar estados, evidências e próximas ações.

## Onde estamos

| Etapa | Data original | Estado atual | O que falta para encerrar |
| --- | --- | --- | --- |
| 1. Preparar ambiente e amostras | Sábado, 14/11 | Concluída | — |
| 2. Implementar análises e avaliar | Domingo, 15/11 | Concluída na rodada atual | Manter as limitações experimentais documentadas. |
| 3. Integrar e preparar a entrega | Segunda, 16/11 | Integração e testes concluídos; material final para 16/11 | Revisão final do relatório, roteiro, apresentação interna e repositório remoto. |
| 4. Gravar e publicar a apresentação | Terça, 17/11, manhã/tarde | A fazer | Ensaiar, gravar, publicar e conferir acesso. |
| 5. Conferir e submeter | Terça, 17/11, antes de 23h59 | A fazer | Validar links e arquivos e efetuar a entrega. |

**Estado técnico:** o resultado original de F1 0,39 foi preservado. A comparação personalizada teve F1 0,79 em 126 consultas, com oito referências corretas excluídas, em avaliação retrospectiva por participante. É um protocolo diferente, não um ganho confirmado no mesmo teste independente. A nova versão está integrada e conferida por Bruno. A recuperação da interface, a confirmação do alerta e a abertura dos dois relatórios foram confirmadas em 15/11.

## Próximas ações, em ordem

Os pacotes de 14/11 e 15/11 estão concluídos. A próxima etapa é a estabilização e revisão final dos entregáveis em 16/11, mantendo as limitações conhecidas no relatório.

### Cronograma atualizado a partir do estado real

| Data | Trabalho | Responsáveis propostos | Resultado para encerrar o dia |
| --- | --- | --- | --- |
| **14/11, sábado — realizado** | Ambiente, dados, modelos, primeira implementação das análises, painel, avaliação inicial, relatório experimental e testes manuais. | Codex + Bruno | Primeira rodada concluída, feedback registrado e problemas conhecidos listados. |
| **15/11, domingo — concluído** | Investigação, novo protocolo, comparação personalizada, correções de interface, validação manual e confirmação de alerta/exportação concluídos (T14/T15/T16/T26.1/T27). | Codex + Bruno | Rodada encerrada; evidências em docs/acompanhamento/fechamento-15-11.md. |
| **16/11, segunda — estabilização e material final** | Encerrar alterações de escopo, revisar relatório/PDF e figuras (T28), fechar roteiro e demonstrações (T29), apresentar ao grupo (T30), conferir repositório remoto e máquina da apresentação (T31). | Bruno + Codex + grupo, conforme cada tarefa. | Código e material estáveis; colegas preparados; exemplos reproduzíveis e entregáveis revisados. |
| **17/11, terça — apresentação e entrega** | Ensaiar, gravar, publicar e conferir o vídeo; inserir link definitivo; revisar acesso e submeter (T32–T39). | Grupo: gravação/publicação; Bruno: conferência e submissão; Codex: apoio à documentação. | Vídeo de até 15 minutos, repositório e relatório acessíveis; submissão antes de 23h59, com margem. |

O bloco de 15/11 foi encerrado. Priorizar a revisão final e estabilização em 16/11 para preservar a gravação e a submissão.

### Ação imediata

1. **Bruno + Codex, 16/11:** revisar referências de A05–A08 e o relatório técnico final (T16.1/T28).
2. **Bruno + Codex, 16/11:** fechar roteiro e demonstrações para os colegas (T29).
3. **Grupo + Codex, 16/11:** conferir reprodução na máquina da apresentação e acesso ao repositório; apresentar a solução ao grupo (T30/T31).

O trabalho técnico que não depende do teste manual pode continuar em paralelo. O feedback do usuário é necessário para encerrar a revisão manual, não para iniciar a investigação dos erros.

## 1. Ambiente e dados — concluída em 14/11

- [x] T01 — Fechar o recorte: execução local, vídeo e áudio.
- [x] T02 — Preparar Python e instalar dependências.
- [x] T03 — Obter pesos de pose e transcrição local.
- [x] T04 — Obter vídeos e anotações do exercício escolhido.
- [x] T05 — Executar ensaios iniciais de pose e transcrição.
- [x] T06 — Receber as oito gravações do grupo.

Evidências: [ensaio inicial](docs/experimentos/ensaio-14-11.md), [calibração de áudio](docs/experimentos/calibracao-audio-14-11.md) e `requirements-lock.txt`.

## 2. Análises e avaliação — implementação antecipada em 14/11

- [x] T07 — Separar participantes entre treino, validação e teste.
- [x] T08 — Extrair medidas de repetições completas e verificar qualidade da pose.
- [x] T09 — Implementar e congelar a primeira versão do classificador de movimento.
- [x] T10 — Implementar transcrição e regras textuais de atenção, negação e passado.
- [x] T11 — Registrar parâmetros antes de avaliar os dados reservados.
- [x] T12 — Realizar e documentar a primeira avaliação reservada de vídeo e áudio.
- [x] T13 — Verificar regras, geometria e integração com testes automatizados.
- [x] T14 — **Codex, 15/11:** investigar os erros e registrar os experimentos em [rodada-15-11.md](docs/experimentos/rodada-15-11.md).
- [x] T15 — **Codex, 15/11:** definir, implementar e avaliar tecnicamente a comparação personalizada; limitações e diferença de protocolo documentadas. A conferência manual da interface permanece em T27.
- [x] T16 — **Bruno, 15/11:** confirmar que não percebeu outras divergências em A01–A04 além do erro de A04.
- [ ] T16.1 — **Revisão final, 16/11:** conferir por escuta as referências de A05–A08 antes do fechamento do relatório.

Evidências: [protocolo de vídeo](configs/video-protocol.json), [métricas de teste de vídeo](reports/video-test-metrics.json), [métricas de teste de áudio](reports/audio-teste-small.json) e `tests/`.

**Regra de avaliação:** os testes reservados já foram utilizados. Novas alterações podem usar seus erros como desenvolvimento, mas uma repetição não será apresentada como novo teste independente. Não há nota mínima de F1 inventada para encerrar T15; a decisão deve se apoiar no experimento e na descrição honesta das limitações.

## 3. Integração e documentação — antecipada em 14/11

- [x] T17 — Implementar painel local com exemplos e arquivos próprios.
- [x] T18 — Reunir eventos das duas modalidades e explicar a origem das fontes.
- [x] T19 — Persistir confirmação de recebimento de alertas.
- [x] T20 — Exportar relatórios de sessão em JSON e HTML.
- [x] T21 — Permitir registro de feedback manual.
- [x] T22 — Testar automaticamente processamento, confirmação e persistência do feedback.
- [x] T23 — Gerar primeira versão do relatório técnico em Markdown/PDF e figuras.
- [x] T24 — Documentar instalação, reprodução e procedimento de teste.
- [x] T25 — Inicializar o repositório Git local e excluir pesos/gravações do versionamento.
- [x] T26 — **Bruno:** executar os cinco casos de análise da segunda rodada e registrar observações. Recebidas cinco avaliações, documentadas em [revisao-manual-14-11.md](docs/experimentos/revisao-manual-14-11.md).
- [x] T26.1 — **Bruno, 15/11:** confirmou explicitamente: “Sim, confirmei o alerta e abri os dois arquivos”.
- [x] T27 — **Bruno + Codex, 15/11:** rodada avaliada, problema da interface tratado e funcionamento confirmado após as alterações.
- [x] T27.1 — Esclarecer os gabaritos no painel: referência do movimento visível, resultado esperado da fala e explicação para evidências textuais vazias. Conferência concluída em 15/11.
- [x] T27.2 — Relacionar feedbacks às sessões e separar avaliação de movimento e fala no formulário. Os registros originais e a evidência do erro de transcrição foram preservados.
- [x] T27.3 — **15/11:** integrar referência correta explícita e abstenção quando não há referência ou pose suficiente; excluir apoio e intervalos sobrepostos de predições avaliadas.
- [x] T27.4 — **15/11:** testar glossário geral no áudio; não adotar, pois não melhorou A04. Preservar o erro conhecido e o aviso de revisão.
- [x] T27.5 — **15/11:** executar 28 testes unitários e testes funcionais do painel, calibração, consultas, persistência e exportação. Downloads também verificados em Chrome isolado e confirmados por Bruno em T26.1.
- [x] T27.6 — **15/11:** incluir a geração das referências de calibração no script reproduzível do experimento e verificar que reproduzem os apoios da avaliação.
- [x] T27.7 — **15/11:** receber quatro avaliações novas da versão personalizada. Calibração, repetição correta e repetição incorreta conferidas por Bruno; registros preservados em `reports/feedback`.
- [x] T27.8 — **15/11:** mitigar conflito com tradução automática confirmado no navegador, preparar idioma inicial, evitar rerun nos downloads e verificar o fluxo/downloads em Chrome isolado. 28 testes unitários passaram. Evidências em [correcao-navegador-15-11.md](docs/operacao/correcao-navegador-15-11.md).
- [x] T27.9 — **Bruno, 15/11:** confirmou “Tudo está funcionando depois das alterações”. As avaliações salvas foram preservadas.
- [ ] T28 — **A fazer · Bruno + Codex:** revisar o relatório técnico final após estabilizar a solução.
- [ ] T29 — **A fazer · Bruno + Codex:** preparar roteiro de fala e demonstrações definitivas para os colegas.
- [ ] T30 — **A fazer · Bruno + grupo:** apresentar a solução internamente e conferir que os colegas conseguem demonstrá-la.
- [ ] T31 — **A fazer · Bruno + Codex:** disponibilizar o repositório remoto para os avaliadores e conferir a reprodução dos exemplos na máquina da apresentação.
- [x] T31.1 — **15/11:** Bruno criou o repositório [observa-monitory](https://github.com/brunosouza2/observa-monitory); `origin` foi configurado e a branch local definida como `main`. Reprodução na máquina da apresentação continua pendente em T31.

Evidências: [painel](app.py), [guia de teste](docs/testes/teste-segunda-rodada.md), [relatório técnico atual](docs/relatorios/relatorio-tecnico.pdf) e [reprodução](docs/operacao/reproducao.md). O PDF é uma versão experimental, ainda sujeita à revisão final.

## 4. Apresentação — prevista para 17/11

- [ ] T32 — **Grupo:** ensaiar a apresentação com as demonstrações escolhidas.
- [ ] T33 — **Grupo:** gravar vídeo com até 15 minutos.
- [ ] T34 — **Grupo:** publicar no YouTube ou Vimeo, público ou não listado.
- [ ] T35 — **Bruno + grupo:** conferir áudio, legibilidade, duração e acesso pelo link.
- [ ] T36 — **Bruno + Codex:** inserir o link definitivo no README e no relatório técnico e regenerar o PDF.

## 5. Entrega — prevista para 17/11, com antecedência ao prazo

- [ ] T37 — **Bruno + Codex:** verificar acesso ao repositório e presença do código, relatório e instruções.
- [ ] T38 — **Bruno + grupo:** conferir os links definitivos e os entregáveis exigidos.
- [ ] T39 — **Bruno ou responsável do grupo:** efetuar a submissão antes de 23h59 e guardar a confirmação.

## Como interpretar os estados

- `[x]`: trabalho executado, com evidência indicada.
- `[ ] A fazer`: ainda falta executar.
- `[ ] Aguardando teste/revisão`: depende da conferência indicada para ser encerrado.

Não usamos percentual geral: tarefas têm tamanhos diferentes, e código implementado não equivale a qualidade validada ou entrega submetida.
