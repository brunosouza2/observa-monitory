# Correção da interface — 15/11

## Relato e hipótese

O usuário relatou `NotFoundError: Failed to execute 'removeChild' on 'Node'`, com rastreamento em `react-dom`, abaixo de “Contexto e evidências”. Confirmou que a tradução automática estava ativa. O momento exato de disparo não foi identificado.

O erro é compatível com o conflito documentado entre tradução da página e atualizações do DOM pelo React: https://github.com/react/react/issues/11538. Isso é a causa provável; não foi reproduzido o DOM traduzido da aba pessoal do usuário.

## Mitigação implementada

- O inicializador prepara o HTML inicial do Streamlit com `lang="pt-BR"`, `translate="no"` e metadado `notranslate`, antes de carregar o React.
- A alteração é idempotente, preserva uma cópia do template original e só escreve na instalação do Streamlit dentro deste projeto. Não modifica uma instalação global fora do projeto.
- Um script constante no app mantém os metadados de idioma. Não recebe texto de uploads nem altera funções de remoção/inserção de nós do React.
- Os downloads usam `on_click="ignore"`, evitando reconstruir o painel ao baixar um relatório.
- O usuário deve desativar a tradução da aba já aberta e recarregar. Metadados novos não desfazem um DOM que já foi traduzido.

## Verificação

28 testes unitários passaram. Foi iniciado um Chrome headless com perfil isolado em `.tools/chrome-qa`, sem acesso ao perfil pessoal. Via Chrome DevTools Protocol, foram verificados os metadados ativos, processamento de sessão, confirmação do alerta e os dois downloads reais.

O JSON baixado tinha o ID da sessão e `acknowledged_utc` preenchido; o HTML tinha o mesmo ID e horário. A sessão permaneceu a mesma após os downloads. Não houve eventos `Runtime.exceptionThrown`. Evidência em `reports/browser-qa.json` e script em `scripts/testar_navegador.py`.

Limite: esse teste verifica uma página inicialmente não traduzida, com a proteção ativa. Não prova que qualquer extensão de terceiros respeitará os metadados, nem substitui a conferência da aba do usuário depois de restaurar o texto original.

## Feedbacks recebidos

Foram encontradas quatro avaliações humanas novas, todas com concordância separada de movimento e fala:

| Sessão | Caso |
| --- | --- |
| `e26f684cfc90` | PM_001, repetição 1 + A01: calibração, fala `nao`. |
| `87dd434061b2` | PM_001, repetição 2 + A01: sem desvio, fala `nao`. |
| `5bbe00fa5f61` | PM_001, repetição 6 + A01: possível desvio, fala `nao`. |
| `abb83b3d97f2` | PM_001, repetição 6 + A02: possível desvio, fala `sim`. |

Esses registros foram preservados; não é necessário repetir as avaliações. Nessas sessões, a confirmação de alerta ainda estava nula quando inspecionada. Portanto, não se presume que o usuário já confirmou alerta ou baixou os relatórios.

## Como recuperar a aba

1. No tradutor do navegador, escolher “Mostrar original” e desativar a tradução automática para a página local.
2. Encerrar o painel com Ctrl+C e iniciar novamente pelo `iniciar-painel.ps1`.
3. Reabrir a página ou usar Ctrl+Shift+R.
4. Processar apenas PM_001, repetição 6 + A02; confirmar o alerta e testar os dois downloads.

Se o erro persistir sem tradução, registrar o ID da sessão e a ação imediatamente anterior. Não serão consideradas perdidas as avaliações só porque a interface apresentou erro; conferir primeiro os arquivos persistidos.

## Validação final do usuário

Após a recuperação, Bruno confirmou “Tudo está funcionando depois das alterações”. Em seguida confirmou explicitamente: “Sim, confirmei o alerta e abri os dois arquivos”. A correção e o fluxo de exportação foram, portanto, conferidos também pelo usuário, encerrando as pendências desta rodada de 15/11.
