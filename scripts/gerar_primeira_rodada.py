"""Generate a local review report from calibration data only."""
import base64
import html
import json
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from src.attention import analyze

def escape(value):
    return html.escape(str(value))

report=json.loads((ROOT/'reports/audio-calibracao-small.json').read_text(encoding='utf-8'))
if report['partition'] != 'calibracao':
    raise ValueError('Esta rodada aceita apenas calibracao.')
sections=[]
results=[]
for item in report['results']:
    if item['id'] not in {'A01','A02','A03','A04'}:
        raise ValueError('Audio reservado nao permitido nesta rodada.')
    analysis=analyze(item['transcript'])
    results.append({'id':item['id'],**analysis,'expected_attention':item['expected_attention']})
    evidence='; '.join(f"{e['expression']}: {e['status']} ({e['context']})" for e in analysis['evidence']) or 'Nenhuma expressao prevista encontrada.'
    notes=' '.join(analysis['review_notes'])
    audio='../'+item['file'].replace('\\','/')
    sections.append(f'''<article><h2>{escape(item['id'])}</h2>
    <audio controls preload="none" src="{escape(audio)}"></audio>
    <p><strong>Transcricao original:</strong> {escape(item['transcript'])}</p>
    <p><strong>Roteiro de referencia:</strong> {escape(item['reference'])}</p>
    <p><strong>Atencao:</strong> {escape(analysis['attention'])} | <strong>Esperado:</strong> {escape(item['expected_attention'])} | WER: {item['wer']:.1%}</p>
    <p><strong>Evidencias:</strong> {escape(evidence)}</p><p>{escape(notes)}</p>
    <p>Confira: a gravacao corresponde ao roteiro? A transcricao preservou o sentido? A classificacao faz sentido?</p></article>''')
images=[]
for name,label in [('primeiro-quadro-pose-correto.jpg','Trecho com rotulo correto'),('primeiro-quadro-pose.jpg','Trecho com rotulo incorreto')]:
    path=ROOT/'reports'/name
    if path.exists():
        encoded=base64.b64encode(path.read_bytes()).decode()
        images.append(f'<h3>{label}</h3><img alt="Quadro com pose estimada" src="data:image/jpeg;base64,{encoded}">')
page='''<!doctype html><html lang="pt-BR"><meta charset="utf-8"><title>Primeira rodada local</title>
<style>body{font:17px system-ui;max-width:1000px;margin:40px auto;padding:0 20px;line-height:1.6;background:#f5f7fa;color:#15253b}article{background:white;padding:20px;margin:20px 0;border:1px solid #ccd4df;border-radius:8px}img{max-width:100%}audio{width:100%}</style>
<h1>Primeira rodada — 14/11</h1><p>Relatorio local de revisao. Apenas A01–A04 foram usados; A05–A08 permanecem reservados.</p>
<p>Ouça cada gravacao, compare o texto e anote divergencias. WER compara com o roteiro, que ainda precisa ser conferido pela escuta. As regras sao limitadas a dor, falta de ar e alguns contextos de negacao/passado.</p>
<p>Legenda: <strong>sim</strong> = relato atual sinalizado; <strong>nao</strong> = sem expressao atual prevista; <strong>contexto_passado</strong> = mencao anterior. Isso nao e diagnostico.</p>
'''+''.join(sections)+'''<h2>Inspecao de pose</h2><p>Os rotulos abaixo pertencem ao dataset. A classificacao automatica de exercicios ainda nao foi implementada. Confira se as articulacoes acompanham a pessoa principal e observe deteccoes indevidas na borda.</p>'''+''.join(images)+'''<h2>Seu retorno</h2><p>Informe o ID do audio e o problema, se houver. Para o video, diga se a pessoa e as articulacoes estao visiveis. Se o audio nao tocar no navegador, abra o arquivo correspondente em data/recordings.</p></html>'''
(ROOT/'reports/primeira-rodada.html').write_text(page,encoding='utf-8')
(ROOT/'reports/atencao-calibracao.json').write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf-8')
print('Relatorio criado: reports/primeira-rodada.html')
for result in results:
    print(result['id'],result['attention'],result['expected_attention'])
