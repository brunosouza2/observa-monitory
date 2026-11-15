"""One predeclared domain glossary; calibration-only comparison, original text retained."""
import csv,json,re,time
from pathlib import Path
from faster_whisper import WhisperModel
from jiwer import process_words

prompt='Vocabulário de reabilitação: exercício, braço, dor, falta de ar, movimento.'
config={'version':'audio-v2','initial_prompt':prompt,'language':'pt','beam_size':5,'vad_filter':True,
        'design':'single general glossary, calibration only; no per-file reference or expected class in prompt'}
Path('configs/audio-candidate-v2.json').write_text(json.dumps(config,ensure_ascii=False,indent=2),encoding='utf-8')
model=WhisperModel('models/whisper-small',device='cpu',compute_type='int8',local_files_only=True)
normalize=lambda t:re.sub(r'\s+',' ',re.sub(r'[^\w\s]','',t.lower())).strip()
results=[]
for row in csv.DictReader(Path('data/scenarios/roteiros-audio.csv').open(encoding='utf-8-sig')):
    if row['particao']!='calibracao':continue
    source=next(Path('data/recordings').glob(row['id']+'.*'));start=time.perf_counter()
    segments,_=model.transcribe(str(source),language='pt',beam_size=5,vad_filter=True,initial_prompt=prompt)
    text=' '.join(s.text.strip() for s in segments);score=process_words(normalize(row['texto']),normalize(text))
    results.append({'id':row['id'],'source':str(source),'reference':row['texto'],'transcript':text,'wer':score.wer,
                    'errors':score.substitutions+score.deletions+score.insertions,'words':len(normalize(row['texto']).split()),'seconds':time.perf_counter()-start})
    print(row['id'],text,flush=True)
report={'config':config,'wer':sum(r['errors'] for r in results)/sum(r['words'] for r in results),'results':results}
Path('reports/v2/audio-glossary-calibration.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print('WER',report['wer'])
