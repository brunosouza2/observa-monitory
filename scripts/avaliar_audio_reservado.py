"""Frozen evaluation of the reserved audio partition, without changing rules."""
import hashlib,json,subprocess,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from src.attention import analyze
protocol=json.loads(Path('configs/audio-protocol.json').read_text())
if hashlib.sha256(Path('src/attention.py').read_bytes()).hexdigest()!=protocol['attention_sha256']:raise ValueError('Audio rules differ from frozen protocol')
subprocess.run([sys.executable,'scripts/avaliar_audio.py','--partition','teste','--model','small'],check=True)
r=json.loads(Path('reports/audio-teste-small.json').read_text(encoding='utf-8'))
for item in r['results']:
    item['analysis']=analyze(item['transcript'])
r['attention_accuracy']=sum(item['analysis']['attention']==item['expected_attention'] for item in r['results'])/len(r['results'])
r['protocol']=protocol
r['warning']='Tiny held-out set, script reference not yet independently verified by listening.'
Path('reports/audio-teste-small.json').write_text(json.dumps(r,ensure_ascii=False,indent=2),encoding='utf-8')
print('Attention accuracy against script:',r['attention_accuracy'])
