from pathlib import Path
from streamlit.testing.v1 import AppTest
app=AppTest.from_file(str(Path(__file__).resolve().parents[1]/'app.py'),default_timeout=90).run()
assert not app.exception,app.exception
print('Initial controls:',[(x.label,x.value) for x in app.selectbox])
app.button[0].click().run(timeout=90)
assert not app.exception,app.exception
print('Session metrics:',[(x.label,x.value) for x in app.metric])
print('Buttons:',[x.label for x in app.button])
assert any(x.label=='Confirmar recebimento do alerta' for x in app.button)
next(x for x in app.button if x.label=='Confirmar recebimento do alerta').click().run(timeout=90)
assert not app.exception,app.exception
assert app.session_state['result']['acknowledged_utc'] is not None
print('ACK saved:',app.session_state['result']['id'])


next(x for x in app.radio if x.label.startswith('Como ficou')).set_value('Concordo com o resultado').run()
app.text_area[0].set_value('[Teste automatizado] Verifica persistencia; nao e avaliacao humana.').run()
next(x for x in app.button if x.label.startswith('Salvar')).click().run()
assert not app.exception,app.exception
assert list(Path('reports/feedback').glob(app.session_state['result']['id']+'-*.json'))
print('Feedback persisted.')
next(x for x in app.selectbox if x.label=='Avaliação do movimento').set_value('Falso alerta: execução correta sinalizada').run()
next(x for x in app.selectbox if x.label=='Avaliação da fala').set_value('Transcrição e contexto corretos').run()
next(x for x in app.button if x.label.startswith('Salvar')).click().run()
assert not app.exception,app.exception
latest=sorted(Path('reports/feedback').glob(app.session_state['result']['id']+'-*.json'))[-1]
import json
record=json.loads(latest.read_text(encoding='utf-8'))
assert record['movement_assessment']=='Falso alerta: execução correta sinalizada'
assert record['speech_assessment']=='Transcrição e contexto corretos'
print('Separate movement/audio feedback persisted.')
