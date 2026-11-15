"""Versioned features; the frozen v1 module and evaluation remain unchanged."""
import numpy as np
from .movement import summarize as summarize_v1, FEATURES as V1_FEATURES

FEATURES=V1_FEATURES+['active_elbow_p10','active_elbow_median','active_trunk_p90',
    'active_asymmetry_p90','active_fraction','active_bent_fraction','abduction_speed_p90',
    'peak_relative_time','active_elbow_range']


def summarize(rows,start,end,min_coverage=0.65):
    result=summarize_v1(rows,start,end,min_coverage)
    if result['features'] is None:return result
    valid=[r for r in rows if start<=r['time']<=end and r['valid']]
    if any(not all(np.isfinite(r[k]) for k in ['time','abduction','elbow','trunk','shoulder_asymmetry']) for r in valid):
        return {**result,'features':None,'status':'insuficiente'}
    ab=np.array([r['abduction'] for r in valid]);times=np.array([r['time'] for r in valid])
    active=[r for r in valid if r['abduction']>=0.6*max(ab)]
    elbows=np.array([r['elbow'] for r in active])
    dt=np.diff(times);velocity=np.abs(np.diff(ab))/np.maximum(dt,1e-6)
    features=[np.percentile(elbows,10),np.median(elbows),np.percentile([r['trunk'] for r in active],90),
        np.percentile([r['shoulder_asymmetry'] for r in active],90),len(active)/len(valid),
        np.mean(elbows<140),np.percentile(velocity,90),
        (times[int(np.argmax(ab))]-start)/max(end-start,1e-6),np.percentile(elbows,90)-np.percentile(elbows,10)]
    return {**result,'features':result['features']+[float(x) for x in features]}


def classify(summary,artifact):
    if summary['features'] is None:return {**summary,'status':'insuficiente','deviation_score':None}
    if artifact['features']!=FEATURES:raise ValueError('Ordem de medidas v2 incompatível.')
    values=np.asarray(summary['features'],dtype=float)
    if len(values)!=len(FEATURES) or not np.isfinite(values).all():
        return {**summary,'status':'insuficiente','features':None,'deviation_score':None}
    if artifact['kind']=='forest':
        probabilities=[]
        for tree in artifact['trees']:
            node=0
            while tree['children_left'][node]!=-1:
                node=tree['children_left'][node] if values[tree['feature'][node]]<=tree['threshold'][node] else tree['children_right'][node]
            probabilities.append(tree['deviation_probability'][node])
        score=float(np.mean(probabilities))
    else:
        z=(values[:6]-artifact['mean'])/artifact['scale']
        score=float(1/(1+np.exp(-np.clip(np.dot(z,artifact['coef'])+artifact['intercept'],-50,50))))
    return {**summary,'deviation_score':score,'status':'desvio' if score>=artifact['threshold'] else 'referencia'}
