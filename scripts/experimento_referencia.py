"""Exploratory personalized protocol: one explicitly correct support repetition per person.

Support labels are inputs to calibration, never hidden ground-truth labels of queries.
Support repetitions are excluded from every reported evaluation metric.
"""
import json,sys,hashlib
from pathlib import Path
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import LeaveOneGroupOut
from sklearn.metrics import f1_score
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from scripts.experimento_movimento_v2 import metrics

NAMES=['reference_logistic','reference_forest']
def create(name):
    if name=='reference_logistic':return make_pipeline(StandardScaler(),LogisticRegression(C=0.3,class_weight='balanced',random_state=42,max_iter=1000))
    return RandomForestClassifier(n_estimators=100,max_depth=4,min_samples_leaf=3,class_weight='balanced',random_state=42,n_jobs=1)

def vector(features,reference):
    delta=np.array(features)-reference
    return np.concatenate([delta,np.abs(delta)])

def export_references(references):
    """Build runtime calibration inputs from the same supports used in evaluation."""
    return {row['video_id']:{
        'id':row['video_id']+'-rep-'+row['repetition'],
        'person_id':person,
        'source_sha256':row['video_sha256'],
        'start':row['start'],'end':row['end'],'features':row['features'],
        'provenance':'dataset-labelled correct support, excluded from evaluation',
    } for person,row in references.items()}

def choose(X,y,groups):
    scores={}
    for name in NAMES:
        scores[name]=float(np.mean([f1_score(y[test],create(name).fit(X[train],y[train]).predict(X[test]),zero_division=0) for train,test in LeaveOneGroupOut().split(X,y,groups)]))
    return max(NAMES,key=lambda n:scores[n]),scores

def main():
    # The v2 report includes geometry-only features computed before this experiment.
    data=json.loads(Path('reports/v2/movement-metrics.json').read_text())['predictions']
    references={}
    for person in sorted(set(r['person_id'] for r in data)):
        reference=next(r for r in data if r['person_id']==person and r['expected_deviation']==0)
        references[person]=reference
    queries=[r for r in data if r is not references[r['person_id']]]
    assert len(queries)+len(references)==len(data)
    X=np.array([vector(r['features'],references[r['person_id']]['features']) for r in queries]);y=np.array([r['expected_deviation'] for r in queries]);g=np.array([r['person_id'] for r in queries])
    predicted=np.zeros(len(y),dtype=int);folds=[]
    for train,test in LeaveOneGroupOut().split(X,y,g):
        name,scores=choose(X[train],y[train],g[train]);model=create(name).fit(X[train],y[train]);predicted[test]=model.predict(X[test])
        folds.append({'person_id':str(g[test][0]),'selected':name,'inner_scores':scores,'samples':len(test),**metrics(y[test],predicted[test])});print(folds[-1],flush=True)
    name,scores=choose(X,y,g);model=create(name).fit(X,y)
    report={'protocol':'Retrospective personalized nested subject CV; one correct support per person excluded from queries; offline files; not an untouched test',
            'references':references,'samples':len(queries),'nested':metrics(y,predicted),'always_alert':metrics(y,np.ones(len(y))),
            'folds':folds,'final_candidate':name,'final_inner_scores':scores,'predictions':[{**r,'prediction':int(p)} for r,p in zip(queries,predicted)]}
    artifact={'version':'reference-v2','candidate':name,'threshold':0.5,'requires_reference':True,'input_size':30,'features_code_sha256':hashlib.sha256(Path('src/movement_v2.py').read_bytes()).hexdigest()}
    if name=='reference_logistic':
        scaler,logistic=model.steps[0][1],model.steps[1][1];artifact.update(kind='logistic',mean=scaler.mean_.tolist(),scale=scaler.scale_.tolist(),coef=logistic.coef_[0].tolist(),intercept=float(logistic.intercept_[0]))
    else:
        trees=[]
        for estimator in model.estimators_:
            t=estimator.tree_;v=t.value[:,0,:];trees.append({'children_left':t.children_left.tolist(),'children_right':t.children_right.tolist(),'feature':t.feature.tolist(),'threshold':t.threshold.tolist(),'deviation_probability':(v[:,1]/v.sum(axis=1)).tolist()})
        artifact.update(kind='forest',trees=trees)
    Path('reports/v2/reference-metrics.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    Path('configs/movement-reference-v2.json').write_text(json.dumps(artifact,indent=2),encoding='utf-8')
    Path('configs/movement-references-v2.json').write_text(json.dumps(export_references(references),indent=2),encoding='utf-8')
    print('SUMMARY',json.dumps({k:v for k,v in report.items() if k not in ['references','predictions','folds']}),flush=True)

if __name__=='__main__':main()
