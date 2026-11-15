"""Functional examples, not an independent performance evaluation."""
import json
from pathlib import Path
from streamlit.testing.v1 import AppTest

app=AppTest.from_file(str(Path(__file__).resolve().parents[1]/'app.py'),default_timeout=90).run()
app.selectbox[2].set_value('A01').run()
for repetition,status in [('1','calibracao'),('2','referencia'),('6','desvio')]:
    app.selectbox[1].set_value(repetition).run()
    app.button[0].click().run(timeout=90)
    assert not app.exception,app.exception
    session=app.session_state['result']
    assert session['video']['repetitions'][0]['status']==status
    assert session['video']['calibration']['id']=='PM_001-rep-1'
    assert session['audio']['analysis']['attention']=='nao'
    print('Functional development example OK:',repetition,status)
next(x for x in app.button if x.label=='Confirmar recebimento do alerta').click().run(timeout=90)
assert not app.exception,app.exception
session=app.session_state['result'];folder=Path('reports/sessions');saved=json.loads((folder/(session['id']+'.json')).read_text(encoding='utf-8'))
assert saved['acknowledged_utc'] is not None
html=(folder/(session['id']+'.html')).read_text(encoding='utf-8')
assert session['id'] in html and saved['acknowledged_utc'] in html
assert len(app.get('download_button'))==2
print('Both exported files contain session and acknowledgement; both download controls present.')
