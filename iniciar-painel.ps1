$ErrorActionPreference = 'Stop'
Set-Location -LiteralPath $PSScriptRoot
$env:HF_HUB_OFFLINE = '1'
$env:YOLO_CONFIG_DIR = Join-Path $PSScriptRoot '.tools\yolo'
& .tools/python/python.exe scripts/preparar_interface.py
if ($LASTEXITCODE -ne 0) { throw 'Falha ao preparar a interface. Consulte a mensagem acima.' }
& .tools/python/python.exe -m streamlit run app.py --server.address 127.0.0.1 --server.port 8501 --server.headless false
