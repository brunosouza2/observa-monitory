"""Exercise real demo scenarios and export selected, media-free evidence.

These are functional development checks, not independent performance metrics.
Run from the repository root with the project's Python interpreter.
"""
import hashlib
import importlib.metadata
import json
import platform
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from streamlit.testing.v1 import AppTest
from src.session import html_report

OUTPUT = ROOT / 'reports/entrega'
CASES = [
    ('01-calibracao', '1', 'A01', 'calibracao', 'nao'),
    ('02-sem-desvio', '2', 'A01', 'referencia', 'nao'),
    ('03-alerta-confirmado', '6', 'A02', 'desvio', 'sim'),
    ('04-erro-conhecido-audio', '2', 'A04', 'referencia', 'contexto_passado'),
]


def file_sha256(path):
    digest = hashlib.sha256()
    with path.open('rb') as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b''):
            digest.update(chunk)
    return digest.hexdigest()


def select(app, label, value):
    next(control for control in app.selectbox if control.label == label).set_value(value).run()
    assert not app.exception, app.exception


def public_session(session):
    """Keep the actual output while removing local paths; never embed media."""
    result = json.loads(json.dumps(session))
    for key in ('video', 'audio'):
        if result.get(key):
            result[key]['source'] = Path(result[key]['source']).name
    result['evidence_metadata'] = {
        'kind': 'automated_functional_development_check',
        'source_paths': 'basenames_only',
        'acknowledgement': 'automated_button_click_when_present',
        'not_independent_performance_evaluation': True,
        'contains_raw_media': False,
    }
    return result


def main():
    if Path.cwd().resolve() != ROOT:
        raise SystemExit('Execute este script a partir da raiz do projeto.')
    OUTPUT.mkdir(parents=True, exist_ok=True)
    app = AppTest.from_file(str(ROOT / 'app.py'), default_timeout=120).run()
    assert not app.exception, app.exception
    select(app, 'Vídeo de exercício', 'PM_001')
    cases = []
    for name, repetition, audio, movement, speech in CASES:
        select(app, 'Repetição completa', repetition)
        select(app, 'Áudio de calibração', audio)
        next(button for button in app.button if button.label == 'Processar sessão').click().run(timeout=120)
        assert not app.exception, app.exception
        session = app.session_state['result']
        assert session['video']['model_version'] == 'reference-v2'
        assert session['video']['repetitions'][0]['status'] == movement
        assert session['video']['calibration']['id'] == 'PM_001-rep-1'
        assert session['audio']['analysis']['attention'] == speech
        if movement == 'calibracao':
            assert session['video']['repetitions'][0]['deviation_score'] is None
        if name == '03-alerta-confirmado':
            next(button for button in app.button if button.label == 'Confirmar recebimento do alerta').click().run(timeout=120)
            assert not app.exception, app.exception
            session = app.session_state['result']
            assert session['acknowledged_utc']
            assert len(app.get('download_button')) == 2
            assert not session['alert']['aligned'] and not session['alert']['combined']
            assert {event['modality'] for event in session['alert']['events']} == {'video', 'audio'}
        if audio == 'A04':
            assert session['audio']['analysis']['review_notes'], 'O erro conhecido precisa continuar visível.'
        public = public_session(session)
        json_path = OUTPUT / (name + '.json')
        html_path = OUTPUT / (name + '.html')
        json_path.write_text(json.dumps(public, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        html_path.write_text(html_report(public), encoding='utf-8')
        assert public['id'] in html_path.read_text(encoding='utf-8')
        cases.append({
            'case': name, 'video': 'PM_001', 'repetition': repetition,
            'audio': audio, 'movement_status': movement, 'speech_status': speech,
            'acknowledged_utc': public['acknowledged_utc'],
            'json': json_path.name, 'html': html_path.name,
            'json_sha256': hashlib.sha256(json_path.read_bytes()).hexdigest(),
        })
        print(name + ': OK', flush=True)

    # Exact source/weight fingerprints describe this demonstration environment.
    model_paths = [ROOT / 'models/yolov8n-pose.pt'] + sorted((ROOT / 'models/whisper-small').glob('*'))
    weights = {str(path.relative_to(ROOT)).replace('\\', '/'): file_sha256(path)
               for path in model_paths if path.is_file()}
    result = {
        'checked_utc': datetime.now(timezone.utc).isoformat(),
        'kind': 'same_machine_functional_reproduction',
        'python': platform.python_version(), 'platform': platform.platform(),
        'packages': {name: importlib.metadata.version(name) for name in
                     ('streamlit', 'ultralytics', 'faster-whisper', 'scikit-learn', 'jiwer')},
        'classifier_sha256': hashlib.sha256((ROOT / 'configs/movement-reference-v2.json').read_bytes()).hexdigest(),
        'weights_sha256': weights, 'cases': cases,
        'limitations': [
            'Known development examples; not an independent performance test.',
            'AppTest checks processing and export content, not an actual browser download.',
            'Uses existing local installation and caches; not a clean installation check.',
            'Acknowledgement in these examples is automated, not human feedback.',
            'No raw recordings, videos or model weights included.',
        ],
    }
    (OUTPUT / 'verificacao-16-11.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print('Evidências funcionais em reports/entrega; nenhuma mídia copiada.', flush=True)


if __name__ == '__main__':
    main()
