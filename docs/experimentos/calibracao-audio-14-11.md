# Calibração de áudio ? 14/11/2026

Recebidos A01.m4a a A08.m4a. Apenas A01 a A04 foram decodificados e transcritos. A05 a A08 permanecem reservados.

Referências: textos dos roteiros; ainda não conferidos por escuta independente. WER mede divergência em relação a esses roteiros. Normalização: minúsculas, remoção de pontuação e espaços repetidos; acentos preservados.

| Modelo CPU int8 | WER | Processamento dos 4 arquivos |
| --- | --- | --- |
| Whisper base multilingual | 17.86% | 2.82 s |
| Whisper small multilingual | 7.14% | 6.95 s |

Tempos de uma execução, incluindo decodificação e VAD; carregamento inicial registrado separadamente no JSON.

## Transcrições com small

- A01: Estou confortável e consigo continuar o exercício.
- A02: Sinto dor no braço quando levanto a mão.
- A03: Não estou sentindo dor no braço.
- A04: Ontem sentidor, mas agora estou bem.

Escolha provisória: small preservou a expressão de dor em A02 e reduziu a divergência nos roteiros de calibração. A04 ainda uniu duas palavras. Isso não mede detecção de sintomas: as regras de contexto e negação ainda precisam ser implementadas.

Os quatro áudios são insuficientes para estimar generalização. Fixar configuração e regras antes de executar a partição de teste.

Reprodução: `.tools/python/python.exe scripts/avaliar_audio.py --partition calibracao --model small`. O script exige pesos locais e não consulta cloud.
