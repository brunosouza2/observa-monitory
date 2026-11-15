"""Local Streamlit interface. No cloud inference or remote account required."""
import csv,hashlib,json,os,sys,threading
from datetime import datetime,timezone
from pathlib import Path
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT));os.chdir(ROOT)
os.environ['HF_HUB_OFFLINE']='1';os.environ['YOLO_CONFIG_DIR']=str(ROOT/'.tools/yolo')
import cv2
import pandas as pd
import streamlit as st
from src.movement import extract,select_person
from src.movement_v2 import summarize,FEATURES
from src.reference_model import classify
from src.session import transcribe,new_session,save_session,html_report
from src.browser_locale import LOCALE_GUARD

st.set_page_config(page_title='Observa | Monitoramento multimodal',page_icon='🔎',layout='wide')
st.html(LOCALE_GUARD,unsafe_allow_javascript=True)
st.title('Observa · revisão multimodal')
st.caption('Protótipo local de reabilitação • vídeo e fala • evidências para revisão humana')
st.warning('Análise experimental: o movimento é comparado com uma execução correta de referência da mesma pessoa. As sinalizações precisam de conferência humana.')

@st.cache_resource
def resources():
    from ultralytics import YOLO
    from faster_whisper import WhisperModel
    return YOLO('models/yolov8n-pose.pt'),WhisperModel('models/whisper-small',device='cpu',compute_type='int8',local_files_only=True),threading.Lock()

def uploaded_path(upload):
    if upload is None:return None
    data=upload.getvalue();folder=Path('reports/uploads');folder.mkdir(parents=True,exist_ok=True)
    path=folder/(hashlib.sha256(data).hexdigest()+Path(upload.name).suffix.lower());path.write_bytes(data)
    return path

config=json.loads(Path('configs/video-protocol.json').read_text(encoding='utf-8-sig'))
artifact_path=Path('configs/movement-reference-v2.json')
if not artifact_path.exists():
    st.info('O classificador de movimento ainda está em preparação. Execute a preparação descrita no README.');st.stop()
artifact=json.loads(artifact_path.read_text(encoding='utf-8'))
references=json.loads(Path('configs/movement-references-v2.json').read_text(encoding='utf-8'))
mode=st.sidebar.radio('Entrada',['Exemplos de desenvolvimento','Meus arquivos'])
st.sidebar.info('Exercício suportado: elevação lateral do braço direito, de frente. Para arquivo próprio, informe o intervalo de uma repetição completa.')
video_path=audio_path=reference_path=None;aligned=False;start=0.;end=None;expected=None;calibration=None;reference_start=0.;reference_end=5.
if mode=='Exemplos de desenvolvimento':
    c1,c2=st.columns(2)
    names=['Sem vídeo']+[v for v in config['train']+config['validation'] if list(Path('data/samples').glob(f'{v}-Camera17*.mp4'))]
    selected=c1.selectbox('Vídeo de exercício',names,index=1 if len(names)>1 else 0)
    if selected!='Sem vídeo':
        video_path=list(Path('data/samples').glob(f'{selected}-Camera17*.mp4'))[0]
        rows=[r for r in csv.DictReader(open('data/samples/Segmentation.csv'),delimiter=';') if r['video_id']==selected]
        rep=c1.selectbox('Repetição completa',[r['repetition_number'] for r in rows],index=1 if len(rows)>1 else 0);row=next(r for r in rows if r['repetition_number']==rep)
        start=int(row['first_frame'])/30;end=int(row['last_frame'])/30;expected='correta' if row['correctness']=='1' else 'incorreta'
        calibration=references.get(selected)
        if calibration:
            c1.info('Execução correta usada para calibração: '+calibration['id']+'. Essa execução não é contada na avaliação do modelo.')
    selected_audio=c2.selectbox('Áudio de calibração',['Sem áudio','A01','A02','A03','A04'],index=2)
    if selected_audio!='Sem áudio':audio_path=next(Path('data/recordings').glob(selected_audio+'.*'))
    st.warning('Exemplos combinam fontes independentes. Cada tempo pertence ao seu arquivo; não há correlação clínica entre vídeo e fala.')
else:
    c1,c2=st.columns(2)
    upload_v=c1.file_uploader('Vídeo do exercício',type=['mp4','mov','avi'])
    upload_a=c2.file_uploader('Gravação da fala',type=['m4a','wav','mp3','flac'])
    video_path=uploaded_path(upload_v);audio_path=uploaded_path(upload_a)
    if video_path:
        start=float(c1.number_input('Início da repetição (s)',min_value=0.,value=0.,step=.1))
        end=float(c1.number_input('Fim da repetição (s)',min_value=.1,value=5.,step=.1))
        if st.checkbox('Usar a fala do próprio vídeo (mesmo relógio)',value=False):audio_path=video_path;aligned=True
        reference_upload=c1.file_uploader('Vídeo de referência correta da mesma pessoa e vista',type=['mp4','mov','avi'])
        reference_path=uploaded_path(reference_upload)
        reference_start=float(c1.number_input('Início da referência (s)',min_value=0.,value=0.,step=.1))
        reference_end=float(c1.number_input('Fim da referência (s)',min_value=.1,value=5.,step=.1))
        c1.caption('A execução de referência precisa ser confirmada como correta por você. Sem ela, o painel mostra medidas, mas não classifica o movimento.')
if st.button('Processar sessão',type='primary',disabled=video_path is None and audio_path is None):
    try:
        with st.spinner('Processando localmente em CPU…'):
            pose,speech,lock=resources()
            with lock:
                video=None
                if video_path:
                    data=extract(video_path,pose,config)
                    if end is None:end=data['duration']
                    if end<=start or end>data['duration']+0.1:raise ValueError('Confira os limites da repetição e a duração do vídeo.')
                    if reference_path:
                        reference_data=extract(reference_path,pose,config)
                        if reference_end<=reference_start or reference_end>reference_data['duration']+0.1:raise ValueError('Confira os limites da referência.')
                        calibration={'id':'referencia-fornecida-pelo-usuario','source_sha256':reference_data['sha256'],**summarize(reference_data['measurements'],reference_start,reference_end,config['min_coverage'])}
                    summary=classify(summarize(data['measurements'],start,end,config['min_coverage']),artifact,calibration)
                    same_reference=calibration and calibration['source_sha256']==data['sha256'] and max(calibration['start'],start)<min(calibration['end'],end)
                    if same_reference and summary['features'] is not None and calibration.get('features') is not None:
                        summary={**summary,'status':'calibracao','deviation_score':None,'reason':'Esta execução sobrepõe a referência de calibração; não é uma predição avaliada.'}
                    video={'model_version':'reference-v2','decision_threshold':artifact['threshold'],'calibration':calibration,'classifier_artifact_sha256':hashlib.sha256(artifact_path.read_bytes()).hexdigest(),'source':str(video_path),'sha256':data['sha256'],'exercise':'abducao_braco_direito_frontal','feature_names':FEATURES,'repetitions':[summary],'processing_seconds':data['processing_seconds'],'measurements':[r for r in data['measurements'] if start<=r['time']<=end],'expected_dataset_label':expected}
                audio=transcribe(audio_path,speech) if audio_path else None
                if audio and mode=='Exemplos de desenvolvimento':
                    scripts=list(csv.DictReader(Path('data/scenarios/roteiros-audio.csv').open(encoding='utf-8-sig')))
                    reference=next((row for row in scripts if row['id']==selected_audio),None)
                    if reference:
                        audio['expected_script_label']=reference['atencao']
                        audio['script_reference']=reference['texto']
            session=new_session(video,audio,aligned);save_session(session)
            st.session_state['result']=session
    except Exception as error:
        st.error(f'Não foi possível processar: {error}')

session=st.session_state.get('result')
if session and session.get('video') and session['video'].get('classifier_artifact_sha256')!=hashlib.sha256(artifact_path.read_bytes()).hexdigest():
    st.info('A versão do modelo mudou desde esta sessão. Clique em Processar sessão para obter um resultado atualizado; o registro anterior permanece salvo.')
    session=None
if session:
    st.divider();st.subheader(f"Sessão {session['id']}")
    st.caption('O resultado abaixo corresponde às fontes registradas nesta sessão. Ao trocar as entradas, clique em Processar sessão novamente.')
    c1,c2=st.columns(2)
    with c1:
        st.subheader('Movimento')
        if session['video']:
            video=session['video'];r=video['repetitions'][0];st.caption(video['source']);st.video(str(Path(video['source']).resolve()),start_time=int(r['start']))
            st.metric('Resultado',{'desvio':'Possível desvio (experimental)','referencia':'Sem desvio sinalizado (experimental)','insuficiente':'Dados ou referência insuficientes','calibracao':'Execução usada para calibração'}[r['status']])
            if r.get('reason'):st.info(r['reason'])
            if video.get('calibration'):st.caption('Comparação com: '+video['calibration']['id'])
            reference=video.get('expected_dataset_label')
            st.markdown(f"**Referência do dataset:** {reference if reference else 'Não disponível para arquivo próprio.'}")
            st.caption('Gabarito da execução do movimento, fornecido pelo dataset. Não é o resultado do classificador.')
            st.write(f"Cobertura de pose válida: {r['coverage']:.0%}")
            if r['deviation_score'] is not None:st.write(f"Escore estatístico de desvio: {r['deviation_score']:.3f} · limiar registrado na sessão: {video.get('decision_threshold','não registrado')}")
            st.caption('Escore do classificador experimental; não é probabilidade de risco clínico.')
            chart=pd.DataFrame(video['measurements'])
            if 'abduction' in chart:st.line_chart(chart.set_index('time')[['abduction','elbow','trunk']],x_label='Tempo no vídeo (s)',y_label='Ângulo (graus)')
            if st.checkbox('Mostrar quadro com pose',value=True):
                valid=[x for x in video['measurements'] if x['valid']]
                if valid:
                    frame=max(valid,key=lambda x:x['abduction']);cap=cv2.VideoCapture(video['source']);cap.set(cv2.CAP_PROP_POS_MSEC,frame['time']*1000);ok,image=cap.read();cap.release()
                    if ok:
                        pose,_,lock=resources()
                        with lock:prediction=pose.predict(image,device='cpu',verbose=False)[0]
                        index=select_person(prediction.boxes.xyxy.cpu().numpy())
                        if index is not None:st.image(cv2.cvtColor(prediction[index].plot(),cv2.COLOR_BGR2RGB),caption='Pessoa selecionada para inspeção visual')
        else:st.info('Sem vídeo nesta sessão.')
    with c2:
        st.subheader('Fala')
        if session['audio']:
            audio=session['audio'];st.caption(audio['source']);st.audio(Path(audio['source']).read_bytes(),format={'.m4a':'audio/mp4','.mp3':'audio/mpeg','.flac':'audio/flac','.wav':'audio/wav'}.get(Path(audio['source']).suffix.lower(),'audio/mp4'))
            st.write(audio['transcript'] or 'Nenhuma fala reconhecida.')
            st.write('Classificação textual:',audio['analysis']['attention'])
            if audio.get('expected_script_label'):
                st.write('Resultado esperado da fala:',audio['expected_script_label'])
                st.caption('Gabarito do roteiro, usado apenas para comparação após a análise.')
            for note in audio['analysis']['review_notes']:st.warning(note)
            st.dataframe(audio['segments'],hide_index=True)
            with st.expander('Contexto e evidências'):
                if audio['analysis']['evidence']:
                    st.json(audio['analysis']['evidence'])
                else:
                    st.info('Nenhuma expressão de atenção prevista foi encontrada nesta fala. Isso não é uma conclusão sobre risco clínico.')
        else:st.info('Sem áudio nesta sessão.')
    st.subheader('Eventos e resposta')
    st.info(session['alert']['note'])
    if session['alert']['events']:st.dataframe(pd.DataFrame(session['alert']['events']).astype(str),hide_index=True)
    else:st.write('Nenhum evento previsto nas entradas processadas. Isso não equivale a avaliação clínica normal.')
    if session['alert']['combined']:st.warning('Evidências de duas modalidades próximas no tempo. Revisar os eventos.')
    if session['alert']['events'] and not session['acknowledged_utc']:
        if st.button('Confirmar recebimento do alerta'):
            session['acknowledged_utc']=datetime.now(timezone.utc).isoformat();save_session(session);st.rerun()
    if session['acknowledged_utc']:st.success('Recebimento registrado em '+session['acknowledged_utc'])
    c1,c2=st.columns(2)
    c1.download_button('Baixar JSON',json.dumps(session,ensure_ascii=False,indent=2),file_name=f"sessao-{session['id']}.json",mime='application/json',on_click='ignore')
    c2.download_button('Baixar relatório HTML',html_report(session),file_name=f"sessao-{session['id']}.html",mime='text/html',on_click='ignore')
    st.caption('Saída também registrada em reports/sessions. Arquivos próprios permanecem neste computador.')

    st.subheader('Registrar sua avaliação')
    feedback=st.radio('Como ficou a análise desta sessão?',['Ainda não conferi','Concordo com o resultado','Houve falso alerta de movimento','Houve desvio de movimento não detectado','Houve erro na transcrição ou no contexto','Não consegui avaliar'])
    st.caption('A avaliação geral pode envolver apenas uma parte da sessão. Registre abaixo o vídeo e a fala separadamente; não é necessário concordar com os dois.')
    movement_feedback=st.selectbox('Avaliação do movimento',['Não conferi o movimento','Concordo com o movimento','Falso alerta: execução correta sinalizada','Desvio não detectado: execução incorreta sem sinalização','Não consegui avaliar o movimento']) if session['video'] else 'Sem vídeo'
    speech_feedback=st.selectbox('Avaliação da fala',['Não conferi a fala','Transcrição e contexto corretos','Erro na transcrição','Erro no contexto ou na negação','Erro na transcrição e no contexto','Não consegui avaliar a fala']) if session['audio'] else 'Sem áudio'
    comment=st.text_area('Observações e trecho afetado')
    has_review=feedback!='Ainda não conferi' or movement_feedback not in ['Não conferi o movimento','Sem vídeo'] or speech_feedback not in ['Não conferi a fala','Sem áudio']
    if st.button('Salvar avaliação',disabled=not has_review):
        folder=Path('reports/feedback');folder.mkdir(parents=True,exist_ok=True)
        record={'session_id':session['id'],'created_utc':datetime.now(timezone.utc).isoformat(),'assessment':feedback,'movement_assessment':movement_feedback,'speech_assessment':speech_feedback,'comment':comment}
        (folder/f"{session['id']}-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S%f')}.json").write_text(json.dumps(record,ensure_ascii=False,indent=2),encoding='utf-8')
        st.success('Avaliação salva em reports/feedback. Esses registros serão dados de desenvolvimento.')
