# Arquitetura implementada

```mermaid
flowchart TD
    V[Vídeo gravado e intervalo de uma repetição] --> P[OpenCV e YOLOv8n-Pose em CPU]
    P --> M[Qualidade da pose e 15 medidas 2D]
    R[Execução correta da mesma pessoa e vista] --> D[Diferenças assinadas e absolutas: 30 entradas]
    M --> D
    D --> C[Regressão logística personalizada em JSON]
    M --> Q[Abstenção se a pose for insuficiente]
    R --> Q2[Abstenção se não houver referência adequada]
    C --> E[Eventos de movimento com tempo e evidência]
    A[Áudio gravado] --> W[Whisper small local em CPU int8]
    W --> T[Transcrição original e segmentos]
    T --> L[Regras de expressões, negação e passado]
    L --> E2[Eventos de fala com tempo e evidência]
    E --> S[Sessão e origem das fontes]
    E2 --> S
    Q --> S
    Q2 --> S
    S --> I[Streamlit: pose, medidas, fala e eventos]
    I --> H[Confirmação de recebimento pelo usuário]
    H --> J[Persistência e exportação JSON e HTML]
    I --> F[Feedback separado de movimento e fala]
```

Sem referência correta disponível, o caminho de classificação se encerra em abstenção. Na consulta que se sobrepõe à própria referência, a saída é **calibração**, sem escore.

Os exemplos usam vídeo do REHAB24-6 e áudios próprios independentes. A aplicação mantém essa origem explícita. Somente ao selecionar a fala contida no próprio vídeo usa um relógio comum e combina eventos de modalidades diferentes próximos em até cinco segundos.

Dados e modelos são preparados com internet; o processamento usa arquivos e pesos locais. O fluxo de alerta termina no painel, na confirmação e nos relatórios. A implementação não contém envio de notificações a destinatários externos.

O diagrama também é incluído no PDF pelo [gerador do relatório](../../scripts/gerar_relatorio_tecnico.py). Os métodos e resultados estão no [relatório técnico](relatorio-tecnico.md).
