"""Retrospective nested subject CV. Never replaces first untouched-holdout results."""
import hashlib,json,sys
from pathlib import Path
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import f1_score,precision_score,recall_score,accuracy_score,confusion_matrix
from sklearn.model_selection import LeaveOneGroupOut
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from src.movement_v2 import summarize,FEATURES,classify

def create(name):
    if name=='logistic_v1':return make_pipeline(StandardScaler(),LogisticRegression(C=1,class_weight='balanced',random_state=42,max_iter=1000))
    return RandomForestClassifier(n_estimators=100,max_depth=3 if name=='forest_depth3' else 6,min_samples_leaf=3,class_weight='balanced',random_state=42,n_jobs=1)

def columns(X,name):return X[:,:6] if name=='logistic_v1' else X

def choose(X,y,groups,names):
    scores={}
    for name in names:
        fold_scores=[]
        for train,test in LeaveOneGroupOut().split(X,y,groups):
            model=create(name).fit(columns(X[train],name),y[train])
            fold_scores.append(f1_score(y[test],model.predict(columns(X[test],name)),zero_division=0))
        scores[name]=float(np.mean(fold_scores))
    return max(names,key=lambda name:scores[name]),scores

def metrics(y,pred):
    return {'f1':float(f1_score(y,pred,zero_division=0)),'precision':float(precision_score(y,pred,zero_division=0)),
            'recall':float(recall_score(y,pred,zero_division=0)),'accuracy':float(accuracy_score(y,pred)),
            'confusion_matrix':confusion_matrix(y,pred,labels=[0,1]).tolist()}

def main():
    protocol=json.loads(Path('configs/video-protocol-v2.json').read_text(encoding='utf-8-sig'))
    caches={r['sha256']:r for p in Path('reports/features').glob('*.json') for r in [json.loads(p.read_text(encoding='utf-8'))]}
    rows=[]
    for partition in ['train','validation','test']:
        for row in json.loads(Path(f'reports/video-{partition}.json').read_text())['rows']:
            source=caches[row['video_sha256']]
            summary=summarize(source['measurements'],row['start'],row['end'])
            rows.append({**row,**summary})
    valid=[r for r in rows if r['features'] is not None]
    X=np.array([r['features'] for r in valid]);y=np.array([r['expected_deviation'] for r in valid]);groups=np.array([r['person_id'] for r in valid])
    predictions=np.zeros(len(y),dtype=int);baseline=np.zeros(len(y),dtype=int);folds=[]
    for train,test in LeaveOneGroupOut().split(X,y,groups):
        assert not set(groups[train])&set(groups[test])
        name,scores=choose(X[train],y[train],groups[train],protocol['candidates'])
        model=create(name).fit(columns(X[train],name),y[train]);predictions[test]=model.predict(columns(X[test],name))
        old=create('logistic_v1').fit(X[train,:6],y[train]);baseline[test]=old.predict(X[test,:6])
        folds.append({'person_id':str(groups[test][0]),'selected':name,'inner_scores':scores,'samples':len(test),**metrics(y[test],predictions[test])})
        print(folds[-1],flush=True)
    name,scores=choose(X,y,groups,protocol['candidates']);model=create(name).fit(columns(X,name),y)
    artifact={'version':'v2','features':FEATURES,'candidate':name,'threshold':0.5,'training_persons':sorted(set(groups)),
              'evaluation':'Retrospective nested subject CV; final artifact fitted on all development data.',
              'protocol_sha256':hashlib.sha256(Path('configs/video-protocol-v2.json').read_bytes()).hexdigest(),
              'features_code_sha256':hashlib.sha256(Path('src/movement_v2.py').read_bytes()).hexdigest()}
    if name=='logistic_v1':
        scaler,logistic=model.steps[0][1],model.steps[1][1]
        artifact.update(kind='logistic',mean=scaler.mean_.tolist(),scale=scaler.scale_.tolist(),coef=logistic.coef_[0].tolist(),intercept=float(logistic.intercept_[0]))
    else:
        trees=[]
        for estimator in model.estimators_:
            t=estimator.tree_;value=t.value[:,0,:];prob=value[:,1]/value.sum(axis=1)
            trees.append({'children_left':t.children_left.tolist(),'children_right':t.children_right.tolist(),'feature':t.feature.tolist(),'threshold':t.threshold.tolist(),'deviation_probability':prob.tolist()})
        artifact.update(kind='forest',trees=trees)
    # Ensure safe JSON inference exactly matches sklearn before making artifact available.
    expected=model.predict_proba(columns(X,name))[:,1]
    actual=np.array([classify({'features':x.tolist()},artifact)['deviation_score'] for x in X])
    if not np.allclose(actual,expected,atol=1e-10):raise ValueError('JSON model differs from sklearn')
    report={'protocol':protocol,'samples':len(rows),'classified':len(valid),'coverage':len(valid)/len(rows),'nested':metrics(y,predictions),
            'linear_same_folds':metrics(y,baseline),'always_alert':metrics(y,np.ones(len(y),dtype=int)),'folds':folds,
            'final_candidate':name,'final_inner_scores':scores,'predictions':[{**r,'prediction':int(p)} for r,p in zip(valid,predictions)]}
    Path('reports/v2').mkdir(exist_ok=True)
    Path('reports/v2/movement-metrics.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    Path('configs/movement-model-v2.json').write_text(json.dumps(artifact,indent=2),encoding='utf-8')
    print('SUMMARY',json.dumps({k:v for k,v in report.items() if k not in ['predictions','folds','protocol']}),flush=True)

if __name__=='__main__':main()
