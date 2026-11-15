param([switch]$NoOpen)
$ErrorActionPreference = 'Stop'
Set-Location -LiteralPath $PSScriptRoot
$env:HF_HUB_OFFLINE = '1'
$pythonLocal = Join-Path $PSScriptRoot '.tools\python\python.exe'
if (-not (Test-Path -LiteralPath $pythonLocal)) { throw 'Python local nao encontrado. Consulte README.md.' }
& $pythonLocal scripts/avaliar_audio.py --partition calibracao --model small
if ($LASTEXITCODE -ne 0) { throw 'Falha na transcricao. Confira a mensagem acima.' }
& $pythonLocal scripts/gerar_primeira_rodada.py
if ($LASTEXITCODE -ne 0) { throw 'Falha na geracao do relatorio.' }
if (-not $NoOpen) { Start-Process (Join-Path $PSScriptRoot 'reports\primeira-rodada.html') }

