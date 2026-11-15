import argparse
import json
import time
from pathlib import Path

parser = argparse.ArgumentParser(description='Ensaio local dos modelos; nao classifica exercicios nem diagnostica sintomas.')
parser.add_argument('--video')
parser.add_argument('--audio')
parser.add_argument('--language', default='pt')
parser.add_argument('--model', default='models/whisper-base')
parser.add_argument('--output', default='reports/ensaio-local.json')
args = parser.parse_args()
result = {}
if args.video:
    from ultralytics import YOLO
    start = time.perf_counter()
    model = YOLO('models/yolov8n-pose.pt')
    frames = visible = 0
    for prediction in model.predict(args.video, stream=True, device='cpu', verbose=False):
        frames += 1
        visible += int(prediction.keypoints is not None and len(prediction.keypoints) > 0)
        if frames == 1:
            prediction.save(filename='reports/primeiro-quadro-pose.jpg')
    result['video'] = {'source': args.video, 'frames': frames, 'frames_with_pose': visible, 'seconds': time.perf_counter() - start}
if args.audio:
    from faster_whisper import WhisperModel
    start = time.perf_counter()
    model = WhisperModel(args.model, device='cpu', compute_type='int8', local_files_only=True)
    segments, info = model.transcribe(args.audio, language=args.language, vad_filter=True)
    result['audio'] = {'source': args.audio, 'language': args.language, 'segments': [{'start': s.start, 'end': s.end, 'text': s.text} for s in segments], 'seconds': time.perf_counter() - start}
if not result:
    parser.error('Forneca --video ou --audio.')
output = Path(args.output)
output.parent.mkdir(parents=True, exist_ok=True)
output.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps(result, ensure_ascii=False, indent=2))
