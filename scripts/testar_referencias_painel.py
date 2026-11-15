"""Regression: dataset reference remains visible even when speech evidence is empty."""
from pathlib import Path
from streamlit.testing.v1 import AppTest
app=AppTest.from_file(str(Path(__file__).resolve().parents[1]/'app.py'),default_timeout=90).run()
app.selectbox[2].set_value('A01').run()
for repetition,expected in [('1','correta'),('6','incorreta')]:
    app.selectbox[1].set_value(repetition).run()
    app.button[0].click().run(timeout=90)
    assert not app.exception,app.exception
    session=app.session_state['result']
    assert session['video']['expected_dataset_label']==expected
    assert session['audio']['analysis']['evidence']==[]
    assert session['audio']['expected_script_label']=='nao'
    assert any(x.value==f'**Referência do dataset:** {expected}' for x in app.markdown)
    assert any('Nenhuma expressão de atenção prevista' in x.value for x in app.info)
    assert any('Resultado esperado da fala:' in x.value for x in app.markdown)
    print('Reference and empty-evidence display OK:',repetition,expected)
