"""Local audio/video session and export, preserving provenance."""
import html,json,uuid,hashlib
from datetime import datetime,timezone
from pathlib import Path
from .attention import analyze
from .movement import extract,summarize,classify

def transcribe(path,model):
    segments,_=model.transcribe(str(path),language='pt',vad_filter=True,beam_size=5)
    segments=[{'start':s.start,'end':s.end,'text':s.text.strip()} for s in segments]
    text=' '.join(s['text'] for s in segments)
    return {'sha256':hashlib.sha256(Path(path).read_bytes()).hexdigest(),'language':'pt','vad_filter':True,'beam_size':5,'source':str(path),'model':'Whisper small multilingual CPU int8','transcript':text,'segments':segments,'analysis':analyze(text),'status':'transcrito' if text else 'sem_fala'}

def combine(video,audio,aligned=False):
    events=[]
    if video:
        for r in video['repetitions']:
            if r['status']=='desvio':events.append({'modality':'video','start':r['start'],'end':r['end'],'message':'Desvio no movimento','evidence':dict(zip(video['feature_names'],r['features']))})
    if audio:
        for s in audio['segments']:
            evidence=analyze(s['text'])
            if evidence['attention']=='sim':events.append({'modality':'audio','start':s['start'],'end':s['end'],'message':'Expressao de atencao na fala','evidence':s['text']})
    events.sort(key=lambda r:r['start'])
    multimodal=aligned and any(v['modality']!=a['modality'] and max(v['start'],a['start'])<=min(v['end'],a['end'])+5 for v in events for a in events)
    return {'events':events,'aligned':aligned,'combined':multimodal,'priority':'revisar_evidencias_conjuntas' if multimodal else 'revisar_eventos' if events else 'sem_eventos_previstos','note':'Proximidade temporal nao demonstra causalidade.' if aligned else 'Fontes independentes: cenario composto, sem sincronizacao clinica.'}

def new_session(video=None,audio=None,aligned=False):
    return {'id':uuid.uuid4().hex[:12],'created_utc':datetime.now(timezone.utc).isoformat(),'video':video,'audio':audio,'alert':combine(video,audio,aligned),'acknowledged_utc':None}

def html_report(session):
    safe=html.escape(json.dumps(session,ensure_ascii=False,indent=2))
    return '<!doctype html><html lang="pt-BR"><meta charset="utf-8"><title>Relatorio da sessao</title><style>body{font:16px system-ui;max-width:1000px;margin:40px auto;padding:20px}pre{white-space:pre-wrap;overflow-wrap:anywhere;background:#f2f5f8;padding:20px}</style><h1>Relatorio multimodal local</h1><p>Evidencias experimentais para revisao humana; sem diagnostico. Tempos relativos as fontes gravadas.</p><pre>'+safe+'</pre></html>'

def save_session(session):
    folder=Path('reports/sessions');folder.mkdir(parents=True,exist_ok=True)
    path=folder/f"{session['id']}.json";path.write_text(json.dumps(session,ensure_ascii=False,indent=2),encoding='utf-8')
    path.with_suffix('.html').write_text(html_report(session),encoding='utf-8')
    return path
