"""Browser QA over CDP in an isolated Chrome profile; no personal profile access."""
import json,time
from pathlib import Path
import requests
from websockets.sync.client import connect

ROOT=Path(__file__).resolve().parents[1]
tabs=requests.get('http://127.0.0.1:9223/json/list',timeout=10).json()
target=next(tab for tab in tabs if tab.get('type')=='page' and tab.get('url','').startswith('http://127.0.0.1:8502'))
events=[];counter=0
with connect(target['webSocketDebuggerUrl'],max_size=32*1024*1024) as socket:
    def call(method,params=None):
        global counter
        counter+=1;ident=counter
        socket.send(json.dumps({'id':ident,'method':method,'params':params or {}}))
        while True:
            item=json.loads(socket.recv(timeout=120))
            if item.get('id')==ident:
                if 'error' in item:raise RuntimeError(item['error'])
                return item.get('result',{})
            events.append(item)
    def evaluate(expression):
        result=call('Runtime.evaluate',{'expression':expression,'returnByValue':True,'awaitPromise':True})
        if 'exceptionDetails' in result:raise RuntimeError(result['exceptionDetails'])
        return result.get('result',{}).get('value')
    def wait(expression,timeout=90):
        deadline=time.monotonic()+timeout
        while time.monotonic()<deadline:
            if evaluate(expression):return
            time.sleep(.3)
        raise TimeoutError(expression)
    def click(label):
        expr='''(() => {const b=Array.from(document.querySelectorAll('button')).find(b=>b.innerText.trim()===LABEL);if(!b)throw Error('Button not found');b.click();return true;})()'''.replace('LABEL',json.dumps(label))
        evaluate(expr)
    call('Runtime.enable');call('Page.enable')
    call('Browser.setDownloadBehavior',{'behavior':'allow','downloadPath':str(ROOT/'.tools/browser-downloads'),'eventsEnabled':True})
    wait("document.body.innerText.includes('Processar sessão')")
    locale=evaluate("({lang:document.documentElement.lang,translate:document.documentElement.getAttribute('translate'),google:document.querySelector('meta[name=google]')?.content})")
    assert locale=={'lang':'pt-BR','translate':'no','google':'notranslate'},locale
    print('Locale guard active:',locale,flush=True)
    click('Processar sessão')
    wait("Array.from(document.querySelectorAll('h3')).some(x=>x.innerText.startsWith('Sessão '))",120)
    wait("document.body.innerText.includes('Confirmar recebimento do alerta')",120)
    session_id=evaluate("Array.from(document.querySelectorAll('h3')).find(x=>x.innerText.startsWith('Sessão ')).innerText.split(' ')[1]")
    click('Confirmar recebimento do alerta')
    wait("document.body.innerText.includes('Recebimento registrado em')")
    click('Baixar JSON');click('Baixar relatório HTML')
    deadline=time.monotonic()+30
    folder=ROOT/'.tools/browser-downloads'
    while time.monotonic()<deadline:
        json_files=list(folder.glob(f'sessao-{session_id}*.json'));html_files=list(folder.glob(f'sessao-{session_id}*.html'))
        if json_files and html_files:break
        time.sleep(.2)
    else:raise TimeoutError('Downloads not completed')
    downloaded=json.loads(json_files[0].read_text(encoding='utf-8'));html=html_files[0].read_text(encoding='utf-8')
    assert downloaded['id']==session_id and downloaded['acknowledged_utc']
    assert downloaded['acknowledged_utc'] in html and session_id in html
    # Downloads should not cause an application rerun or change session.
    assert evaluate("Array.from(document.querySelectorAll('h3')).find(x=>x.innerText.startsWith('Sessão ')).innerText.split(' ')[1]")==session_id
    # Drain browser messages through a final evaluation round trip.
    evaluate('document.readyState')
    errors=[e for e in events if e.get('method')=='Runtime.exceptionThrown']
    if errors:raise AssertionError(json.dumps(errors,ensure_ascii=False))
    report={'browser':'isolated headless Chrome','locale':locale,'session_id':session_id,'acknowledgement':downloaded['acknowledged_utc'],
            'json_downloaded':True,'html_downloaded':True,'runtime_exceptions':errors,
            'limitation':'No access to user profile; cannot reproduce pre-existing translated DOM. Initial metadata and normal rerenders verified.'}
    (ROOT/'reports/browser-qa.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(report,ensure_ascii=True),flush=True)
