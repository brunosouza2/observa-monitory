"""Pose measurements for frontal right-arm abduction, with quality abstention."""
import hashlib
import json
import math
import time
from pathlib import Path
import cv2
import numpy as np

FEATURES=['abduction_p90','abduction_range','elbow_p10','trunk_p90','shoulder_asymmetry_p90','duration']

def angle(a,b,c):
    u=np.asarray(a)-b; v=np.asarray(c)-b
    norm=np.linalg.norm(u)*np.linalg.norm(v)
    return None if norm<1e-8 else float(np.degrees(np.arccos(np.clip(np.dot(u,v)/norm,-1,1))))

def measure(points,confidence,minimum=0.35):
    required=[5,6,8,10,11,12]
    if any(confidence[i]<minimum for i in required): return None
    ls,rs,re,rw,lh,rh=[points[i] for i in required]
    shoulder=(ls+rs)/2; hip=(lh+rh)/2; torso=np.linalg.norm(hip-shoulder)
    if torso<10:return None
    abduction=angle(rh,rs,re); elbow=angle(rs,re,rw)
    if abduction is None or elbow is None:return None
    tilt=float(np.degrees(np.arccos(np.clip((hip[1]-shoulder[1])/torso,-1,1))))
    return {'abduction':abduction,'elbow':elbow,'trunk':tilt,'shoulder_asymmetry':float(abs(ls[1]-rs[1])/torso)}

def select_person(boxes,previous=None):
    if not len(boxes):return None
    centers=(boxes[:,:2]+boxes[:,2:])/2
    if previous is None:
        return int(np.argmax((boxes[:,2]-boxes[:,0])*(boxes[:,3]-boxes[:,1])))
    return int(np.argmin(np.linalg.norm(centers-previous,axis=1)))

def extract(video,model,config,cache=True):
    video=Path(video)
    signature=hashlib.sha256(video.read_bytes()).hexdigest()
    settings={k:config[k] for k in ['sample_stride','image_size','keypoint_confidence']}
    key=hashlib.sha256((signature+json.dumps(settings,sort_keys=True)+'pose-features-v1').encode()).hexdigest()
    cached=Path('reports/features')/f'{key}.json'
    if cache and cached.exists():return json.loads(cached.read_text(encoding='utf-8'))
    cap=cv2.VideoCapture(str(video)); fps=cap.get(cv2.CAP_PROP_FPS); total=int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    if not cap.isOpened() or not math.isfinite(fps) or fps<=0:raise ValueError('Video invalido ou FPS ausente.')
    if total/fps>600:raise ValueError('Use videos de ate 10 minutos nesta versao.')
    start=time.perf_counter(); rows=[];previous=None; frame_id=0
    try:
        while True:
            ok=cap.grab()
            if not ok:break
            if frame_id%config['sample_stride']==0:
                ok,frame=cap.retrieve()
                if not ok:break
                prediction=model.predict(frame,device='cpu',imgsz=config['image_size'],verbose=False)[0]
                boxes=prediction.boxes.xyxy.cpu().numpy()
                idx=select_person(boxes,previous)
                values=None
                if idx is not None and prediction.keypoints is not None:
                    center=(boxes[idx,:2]+boxes[idx,2:])/2
                    if previous is None or np.linalg.norm(center-previous)<0.25*np.hypot(frame.shape[0],frame.shape[1]):
                        previous=center
                        points=prediction.keypoints.xy[idx].cpu().numpy()
                        confidence=prediction.keypoints.conf[idx].cpu().numpy()
                        values=measure(points,confidence,config['keypoint_confidence'])
                rows.append({'frame':frame_id,'time':frame_id/fps,'valid':values is not None,**(values or {})})
            frame_id+=1
    finally:cap.release()
    result={'source':str(video),'sha256':signature,'fps':fps,'frames':frame_id,'duration':frame_id/fps,'processing_seconds':time.perf_counter()-start,'settings':settings,'measurements':rows}
    cached.parent.mkdir(parents=True,exist_ok=True)
    cached.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    return result

def summarize(rows,start,end,min_coverage=0.65):
    selected=[r for r in rows if start<=r['time']<=end]
    valid=[r for r in selected if r['valid']]
    coverage=len(valid)/len(selected) if selected else 0
    result={'start':start,'end':end,'coverage':coverage,'status':'insuficiente','features':None}
    if coverage<min_coverage or len(valid)<5:return result
    ab=[r['abduction'] for r in valid]
    result['features']=[float(np.percentile(ab,90)),float(np.percentile(ab,90)-np.percentile(ab,10)),float(np.percentile([r['elbow'] for r in valid],10)),float(np.percentile([r['trunk'] for r in valid],90)),float(np.percentile([r['shoulder_asymmetry'] for r in valid],90)),float(end-start)]
    result['status']='medido'
    return result

def classify(summary,artifact):
    if summary['features'] is None:return {**summary,'status':'insuficiente','deviation_score':None}
    if artifact['features']!=FEATURES:raise ValueError('Ordem de medidas incompativel.')
    z=(np.array(summary['features'])-artifact['mean'])/artifact['scale']
    score=float(1/(1+np.exp(-np.clip(np.dot(z,artifact['coef'])+artifact['intercept'],-50,50))))
    return {**summary,'deviation_score':score,'status':'desvio' if score>=artifact['threshold'] else 'referencia'}
