import argparse,csv,json,sys,hashlib
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from src.movement import extract,summarize,FEATURES
from ultralytics import YOLO

parser=argparse.ArgumentParser();parser.add_argument('--partition',choices=['train','validation','test'],required=True);args=parser.parse_args()
config=json.loads(Path('configs/video-protocol.json').read_text(encoding='utf-8-sig'))
annotations=list(csv.DictReader(open('data/samples/Segmentation.csv'),delimiter=';'))
partitions={p:{r['person_id'] for r in annotations if r['video_id'] in config[p]} for p in ['train','validation','test']}
assert not(partitions['train']&partitions['validation'] or partitions['train']&partitions['test'] or partitions['validation']&partitions['test'])
model=YOLO('models/yolov8n-pose.pt'); output=[]
for name in config[args.partition]:
    paths=list(Path('data/samples').glob(f'{name}-Camera17*.mp4'))
    if not paths:raise FileNotFoundError(name)
    video=extract(paths[0],model,config)
    for row in annotations:
        if row['video_id']!=name:continue
        summary=summarize(video['measurements'],int(row['first_frame'])/30,int(row['last_frame'])/30,config['min_coverage'])
        output.append({'video_id':name,'person_id':row['person_id'],'repetition':row['repetition_number'],'expected_deviation':1-int(row['correctness']),'video_sha256':video['sha256'],**summary})
    print(name,'repetitions',len([r for r in output if r['video_id']==name]),'seconds',round(video['processing_seconds'],2),flush=True)
Path(f'reports/video-{args.partition}.json').write_text(json.dumps({'partition':args.partition,'features':FEATURES,'protocol_sha256':hashlib.sha256(Path('configs/video-protocol.json').read_bytes()).hexdigest(),'rows':output},indent=2),encoding='utf-8')
