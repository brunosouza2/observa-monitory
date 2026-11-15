"""Evaluate a declared partition without reading audio from the reserved partition."""
import argparse
import csv
import hashlib
import json
import platform
import re
import time
from pathlib import Path

from faster_whisper import WhisperModel
from faster_whisper.audio import decode_audio
from jiwer import process_words


def normalize(text):
    return re.sub(r"\s+", " ", re.sub(r"[^\w\s]", "", text.lower())).strip()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--partition', choices=['calibracao', 'teste'], default='calibracao')
    parser.add_argument('--model', choices=['base', 'small'], default='base')
    args = parser.parse_args()
    rows = list(csv.DictReader(Path('data/scenarios/roteiros-audio.csv').open(encoding='utf-8-sig')))
    selected = [row for row in rows if row['particao'] == args.partition]
    inputs = []
    for row in selected:
        matches = [p for p in Path('data/recordings').iterdir() if p.is_file() and p.stem.upper() == row['id']]
        if len(matches) != 1:
            raise ValueError(f"Expected one recording for {row['id']}, found {len(matches)}")
        inputs.append((row, matches[0]))
    start = time.perf_counter()
    model = WhisperModel(f'models/whisper-{args.model}', device='cpu', compute_type='int8', local_files_only=True)
    load_seconds = time.perf_counter() - start
    results = []
    for row, path in inputs:
        start = time.perf_counter()
        audio = decode_audio(str(path), sampling_rate=16000)
        segments, info = model.transcribe(audio, language='pt', vad_filter=True, beam_size=5)
        segments = [{'start': s.start, 'end': s.end, 'text': s.text.strip()} for s in segments]
        hypothesis = ' '.join(s['text'] for s in segments)
        metrics = process_words(normalize(row['texto']), normalize(hypothesis))
        results.append({
            'id': row['id'], 'file': str(path), 'sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
            'reference': row['texto'], 'reference_status': 'script_expected_not_independently_verified',
            'expected_attention': row['atencao'], 'transcript': hypothesis, 'segments': segments,
            'duration_seconds': len(audio)/16000, 'processing_seconds': time.perf_counter()-start,
            'wer': metrics.wer, 'substitutions': metrics.substitutions, 'deletions': metrics.deletions,
            'insertions': metrics.insertions, 'reference_words': len(normalize(row['texto']).split()),
        })
        print(f"{row['id']}: {hypothesis}", flush=True)
    words = sum(r['reference_words'] for r in results)
    report = {'partition': args.partition, 'model': f'Whisper {args.model} multilingual', 'device': 'cpu',
              'compute_type': 'int8', 'language': 'pt', 'vad_filter': True, 'beam_size': 5,
              'normalization': 'lowercase, remove punctuation, collapse whitespace; preserve accents',
              'platform': platform.platform(), 'model_load_seconds': load_seconds,
              'wer': sum(r['substitutions']+r['deletions']+r['insertions'] for r in results)/words,
              'reference_words': words, 'results': results}
    output = Path('reports') / f'audio-{args.partition}-{args.model}.json'
    output.parent.mkdir(exist_ok=True)
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f"WER against script: {report['wer']:.2%}; saved to {output}")


if __name__ == '__main__':
    main()
