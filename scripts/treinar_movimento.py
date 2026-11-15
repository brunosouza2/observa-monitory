"""Train/validate once; evaluate frozen artifact separately on held-out people."""
import argparse,hashlib,json,sys
from datetime import datetime,timezone
from pathlib import Path
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import precision_recall_fscore_support,confusion_matrix,accuracy_score
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from src.movement import classify,FEATURES

def metrics(rows,artifact):
    eligible=[r for r in rows if r['features'] is not None]
    y=[r['expected_deviation'] for r in eligible];pred=[int(classify(r,artifact)['status']=='desvio') for r in eligible]
    p,r,f,_=precision_recall_fscore_support(y,pred,average='binary',zero_division=0)
    _,_,baseline,_=precision_recall_fscore_support(y,[1]*len(y),average='binary',zero_division=0)
    return {'samples':len(rows),'classified':len(eligible),'abstentions':len(rows)-len(eligible),'coverage':len(eligible)/len(rows),'precision':p,'recall':r,'f1':f,'accuracy':accuracy_score(y,pred),'confusion_matrix_TN_FP_FN_TP':confusion_matrix(y,pred,labels=[0,1]).tolist(),'always_alert_f1':baseline,'predictions':[{**row,**classify(row,artifact)} for row in rows]}

parser=argparse.ArgumentParser();parser.add_argument('--evaluate-test',action='store_true');args=parser.parse_args()
artifact_path=Path('configs/movement-model.json')
if args.evaluate_test:
    artifact=json.loads(artifact_path.read_text(encoding='utf-8'))
    for source,digest in artifact['frozen_sources'].items():
        if hashlib.sha256(Path(source).read_bytes()).hexdigest()!=digest:raise ValueError('Frozen protocol/code changed; do not reuse held-out test as validation')
    test=json.loads(Path('reports/video-test.json').read_text())
    result=metrics(test['rows'],artifact);result['artifact_sha256']=hashlib.sha256(artifact_path.read_bytes()).hexdigest()
    Path('reports/video-test-metrics.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    print({k:v for k,v in result.items() if k!='predictions'})
else:
    if Path('reports/video-test-metrics.json').exists():raise ValueError('Test already evaluated; preserve artifact and report')
    train=json.loads(Path('reports/video-train.json').read_text())['rows'];val=json.loads(Path('reports/video-validation.json').read_text())['rows']
    valid=[r for r in train if r['features'] is not None];X=np.array([r['features'] for r in valid]);y=[r['expected_deviation'] for r in valid]
    scaler=StandardScaler().fit(X);model=LogisticRegression(C=1.0,class_weight='balanced',random_state=42,max_iter=1000).fit(scaler.transform(X),y)
    artifact={'features':FEATURES,'mean':scaler.mean_.tolist(),'scale':scaler.scale_.tolist(),'coef':model.coef_[0].tolist(),'intercept':float(model.intercept_[0]),'threshold':0.5,'created_utc':datetime.now(timezone.utc).isoformat(),'model':'standardized logistic regression C=1 balanced; deviation is positive; no clinical probability'}
    choices=[]
    for threshold in np.linspace(.25,.75,11):
        artifact['threshold']=float(threshold);m=metrics(val,artifact);choices.append((m['f1'],-abs(threshold-.5),float(threshold)))
    artifact['threshold']=max(choices)[2]
    artifact['train_persons']=sorted(set(r['person_id'] for r in train));artifact['validation_persons']=sorted(set(r['person_id'] for r in val))
    artifact['frozen_sources']={p:hashlib.sha256(Path(p).read_bytes()).hexdigest() for p in ['configs/video-protocol.json','src/movement.py','scripts/treinar_movimento.py','reports/video-train.json','reports/video-validation.json','models/yolov8n-pose.pt']}
    artifact_path.write_text(json.dumps(artifact,indent=2),encoding='utf-8')
    for name,rows in [('train',train),('validation',val)]:
        result=metrics(rows,artifact);Path(f'reports/video-{name}-metrics.json').write_text(json.dumps(result,indent=2),encoding='utf-8');print(name,{k:v for k,v in result.items() if k!='predictions'})
