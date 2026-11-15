"""Create two 60-frame smoke-test excerpts; not complete evaluation repetitions."""
import csv
from pathlib import Path
import cv2
rows=list(csv.DictReader(open('data/samples/Segmentation.csv',encoding='utf-8-sig'),delimiter=';'))
for video_id,label,output in [('PM_000','1','ensaio-pose.mp4'),('PM_039','0','ensaio-pose-incorreto.mp4')]:
    candidates=list(Path('data/samples').glob(f'{video_id}-Camera17*.mp4'))
    if not candidates:
        raise FileNotFoundError(video_id)
    row=next(r for r in rows if r['video_id']==video_id and r['correctness']==label)
    cap=cv2.VideoCapture(str(candidates[0]))
    if not cap.isOpened():
        raise RuntimeError(f'Cannot open {candidates[0]}')
    cap.set(cv2.CAP_PROP_POS_FRAMES,int(row['first_frame']))
    writer=cv2.VideoWriter(str(Path('data/samples')/output),cv2.VideoWriter_fourcc(*'mp4v'),30,(int(cap.get(3)),int(cap.get(4))))
    if not writer.isOpened():
        raise RuntimeError('Cannot create output video')
    count=0
    try:
        for _ in range(60):
            ok,frame=cap.read()
            if not ok: break
            writer.write(frame)
            count+=1
    finally:
        writer.release()
        cap.release()
    if count!=60:
        raise RuntimeError(f'Incomplete excerpt: {count}')
    print(output,count)
