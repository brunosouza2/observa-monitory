"""Inference conditional on a separate, explicitly correct calibration repetition."""
import numpy as np
from .movement_v2 import FEATURES


def classify(summary,artifact,reference=None):
    result={**summary,'deviation_score':None,'status':'insuficiente'}
    if summary.get('features') is None:
        return {**result,'reason':'Cobertura de pose insuficiente.'}
    if reference is None or reference.get('features') is None:
        return {**result,'reason':'É necessária uma execução correta de referência da mesma pessoa e vista.'}
    observed=np.asarray(summary['features'],dtype=float)
    baseline=np.asarray(reference['features'],dtype=float)
    if observed.shape!=(len(FEATURES),) or baseline.shape!=observed.shape or not np.isfinite(observed).all() or not np.isfinite(baseline).all():
        return {**result,'reason':'Medidas inválidas na execução ou referência.'}
    delta=observed-baseline;values=np.concatenate([delta,np.abs(delta)])
    if artifact['input_size']!=len(values):raise ValueError('Modelo e medidas incompatíveis.')
    if artifact['kind']=='logistic':
        z=(values-artifact['mean'])/artifact['scale']
        score=float(1/(1+np.exp(-np.clip(np.dot(z,artifact['coef'])+artifact['intercept'],-50,50))))
    else:
        probabilities=[]
        for tree in artifact['trees']:
            node=0
            while tree['children_left'][node]!=-1:
                node=tree['children_left'][node] if values[tree['feature'][node]]<=tree['threshold'][node] else tree['children_right'][node]
            probabilities.append(tree['deviation_probability'][node])
        score=float(np.mean(probabilities))
    return {**summary,'deviation_score':score,'status':'desvio' if score>=artifact['threshold'] else 'referencia',
            'reference_id':reference.get('id'),'decision_threshold':artifact['threshold']}
