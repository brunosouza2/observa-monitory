# Fechamento das atividades — 15/11/2026

**Estado: concluídas as tarefas previstas para 15/11.** O fechamento não significa que a entrega de 17/11 já foi submetida ou que há validação clínica.

| Tarefa de hoje | Evidência de conclusão |
| --- | --- |
| T14 — investigar os erros | Medidas por participante, inspeção dos coeficientes e experimentos documentados em `rodada-15-11.md`. |
| T15 — implementar e avaliar melhoria delimitada | Comparação personalizada, protocolo retrospectivo explícito, artefatos v2 e métricas; apoios excluídos das consultas e resultados originais preservados. |
| T16 — conferir áudios de calibração | Bruno confirmou não ter percebido outras divergências em A01–A04 além do erro conhecido de A04. |
| T27 — corrigir e conferir a rodada | Quatro avaliações humanas novas registradas, correção do conflito de tradução e confirmação de Bruno de funcionamento após as alterações. |
| T26.1 — verificar alerta e relatórios | Confirmação explícita de Bruno: “Sim, confirmei o alerta e abri os dois arquivos”. |

## Verificações técnicas

28 testes unitários passaram. Testes da aplicação verificaram calibração, consultas, gabaritos, confirmação e feedback separado. Um Chrome com perfil isolado verificou metadados de idioma, processamento, confirmação e downloads reais de JSON e HTML, sem exceções JavaScript (`reports/browser-qa.json`). O HTML e JSON continham o mesmo ID de sessão e a confirmação. Esses testes não foram contabilizados como feedback humano.

Os artefatos de v1 continuam com as assinaturas originais verificadas. O relatório atual em Markdown/PDF e as figuras foram atualizados; a versão de 14/11 foi preservada em `historico`.

## Limitações mantidas

O F1 personalizado de 0,79 decorre de outro protocolo, retrospectivo e condicionado a uma referência correta da mesma pessoa. Não substitui o F1 de 0,39 do primeiro teste nem comprova um ganho direto no mesmo teste independente. Ainda há desvios perdidos, variação entre pessoas e necessidade de revisão humana.

O erro de transcrição “sentidor” em A04 permanece documentado, com aviso e interpretação de contexto separada. Não foi ocultado nem corrigido por regravação. A tradução automática deve permanecer desativada na página para evitar alterar o DOM e os textos apresentados.

## Próxima etapa — 16/11

- Conferir referências de A05–A08 e revisar o relatório técnico final.
- Fechar o roteiro e as demonstrações para apresentação.
- Apresentar a solução aos colegas e conferir a máquina da gravação.
- Disponibilizar/conferir o repositório remoto e os arquivos finais.

Gravação, publicação do vídeo e submissão permanecem no cronograma de 17/11, antes de 23h59 (Brasília).
