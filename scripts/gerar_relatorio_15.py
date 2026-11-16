"""Current report with preserved v1 results and explicitly exploratory v2 protocol."""
import json,os,textwrap
from pathlib import Path
os.environ.setdefault('MPLCONFIGDIR',str(Path('.tools/matplotlib').resolve()))
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.patches import FancyBboxPatch


def architecture_figure():
    fig, ax = plt.subplots(figsize=(8.27, 11.69))
    ax.set(xlim=(0, 10), ylim=(0, 14)); ax.axis('off')
    ax.text(5, 13.5, 'Arquitetura implementada · execução local', ha='center', fontsize=15, weight='bold')
    def box(x, y, label, color='#e5f1f5', width=4):
        ax.add_patch(FancyBboxPatch((x, y), width, 1.2, boxstyle='round,pad=0.08', facecolor=color, edgecolor='#316578'))
        ax.text(x+width/2, y+.6, label, ha='center', va='center', fontsize=10)
    def arrow(start, end):
        ax.annotate('', xy=end, xytext=start, arrowprops={'arrowstyle':'->', 'color':'#316578', 'lw':1.6})
    box(.3, 11.3, 'Vídeo + intervalo da repetição')
    box(5.7, 11.3, 'Áudio gravado')
    box(.3, 9.2, 'OpenCV + YOLOv8n-Pose\nQualidade e 15 medidas 2D')
    box(5.7, 9.2, 'Whisper small · CPU int8\nTexto original + segmentos')
    box(.3, 6.9, 'Referência correta da mesma pessoa\nDiferenças: 30 entradas\nRegressão logística em JSON')
    box(5.7, 6.9, 'Regras textuais\nExpressões, negação e passado')
    box(1.4, 4.5, 'Sessão: fontes, tempos e eventos\nFontes independentes ficam explícitas', width=7.2)
    box(1.4, 2.3, 'Streamlit · revisão humana\nConfirmação e exportação JSON / HTML', width=7.2)
    for x in (2.3, 7.7):
        arrow((x, 11.3), (x, 10.4)); arrow((x, 9.2), (x, 8.1)); arrow((x, 6.9), (5, 5.7))
    arrow((5, 4.5), (5, 3.5))
    ax.text(5, 1.4, 'Pose ou referência insuficiente: abstenção. Sobreposição ao apoio: calibração.', ha='center', fontsize=9)
    ax.text(5, .8, 'Arquivos gravados; sem diagnóstico ou envio a destinatários externos.', ha='center', fontsize=9)
    fig.tight_layout()
    return fig

def main():
    Path('docs/relatorios').mkdir(parents=True,exist_ok=True)
    old=json.loads(Path('reports/video-test-metrics.json').read_text())
    generic=json.loads(Path('reports/v2/movement-metrics.json').read_text())
    report=json.loads(Path('reports/v2/reference-metrics.json').read_text())
    audio=json.loads(Path('reports/audio-teste-small.json').read_text(encoding='utf-8'))
    glossary=json.loads(Path('reports/v2/audio-glossary-calibration.json').read_text(encoding='utf-8'))
    delivery=json.loads(Path('configs/entrega.json').read_text(encoding='utf-8'))
    revision=delivery['report_revision']
    review_path=Path('reports/audio-revisao-manual-16-11.json')
    review=json.loads(review_path.read_text(encoding='utf-8')) if review_path.exists() else {}
    reviewed=(review.get('status')=='confirmed_by_listening'
              and set(review.get('verified_ids',[]))=={'A05','A06','A07','A08'}
              and all(review.get('recording_sha256',{}).get(item['id'])==item['sha256'] for item in audio['results']))
    audio_review=('Em 16/11, Bruno confirmou por escuta que A05–A08 coincidem com os roteiros. A revisão foi feita pelo próprio autor das gravações; não é anotação independente e cega. O registro posterior está em reports/audio-revisao-manual-16-11.json; o resultado original de 14/11 foi preservado.' if reviewed else 'As referências de A05–A08 ainda devem ser conferidas por escuta antes do fechamento final. O procedimento está em docs/testes/revisao-audio-16-11.md; o WER informado continua sendo calculado contra os roteiros.')
    presentation=delivery.get('presentation_url') or 'pendente de gravação e publicação em 17/11/2026'
    m=report['nested'];baseline=report['always_alert'];macro=sum(f['f1'] for f in report['folds'])/len(report['folds'])
    sections=[('1. Problema e escopo', '''O Observa é um protótipo local de revisão multimodal de um exercício de reabilitação: vídeo e áudio. O texto é saída da transcrição. O recorte segue a orientação do grupo de executar localmente e contemplar duas frentes. O PDF do desafio original está em context/.

A aplicação estima articulações, calcula medidas por repetição e compara o movimento com uma referência correta da mesma pessoa e vista. Em paralelo, transcreve fala em português, identifica expressões de atenção e alguns contextos de negação e passado. Reúne evidências, registra confirmação de recebimento e exporta relatórios JSON/HTML.

O objetivo é demonstrar processamento, avaliação e integração rastreável. A solução é experimental e opera sobre arquivos gravados. Não demonstra diagnóstico, benefício clínico ou garantia de tempo real. A segmentação das repetições é fornecida pelo dataset ou informada manualmente.

O PDF original menciona cloud e outras frentes. O escopo atualizado informado pelo grupo permite execução local e duas modalidades. O áudio é analisado pelo conteúdo transcrito, sem classificador de alterações acústicas, fadiga ou disartria. Não foram implementados Azure, sinais vitais, prescrições ou envio de notificações a destinatários externos. A detecção de desvios de movimento é supervisionada pelos rótulos da base, e não uma detecção não supervisionada de anomalias.'''),
    ('2. Dados e histórico do experimento',f'''Vídeo: REHAB24-6, exercício 1, câmera 17, vista frontal, oito participantes e 134 repetições. Os vídeos foram obtidos por intervalos HTTP do arquivo oficial e verificados por tamanho e CRC. Fonte: https://zenodo.org/records/13305826. Os termos indicados são de uso acadêmico ou pesquisa não comercial, com citação dos autores.

Em 14/11, o experimento original separou pessoas: treino 1–4 (51 repetições), validação 5 e 7 (41), teste 8 e 9 (42). A regressão logística original obteve F1 {old['f1']:.3f} no teste, abaixo da referência de sinalizar tudo. Seus artefatos e resultados foram preservados sem alterações. A revisão manual identificou, entre outros, falso alerta na repetição 1 de PM_001 e desvio perdido na repetição 6.

Em 15/11, todos esses exemplos passaram a ser dados de desenvolvimento. Os novos experimentos são retrospectivos; não possuem um novo teste inédito. Essa distinção impede apresentar a diferença entre F1 de protocolos diferentes como ganho confirmado de generalização.

Áudio: oito gravações próprias em português, A01–A04 para calibração e A05–A08 na avaliação reservada de 14/11. Referências são os roteiros em data/scenarios/roteiros-audio.csv. Em 15/11 o usuário confirmou não ter percebido divergências adicionais na calibração, além do erro conhecido em A04. {audio_review}'''),
    ('3. Arquitetura e modelos', '''Execução em Python 3.11 com OpenCV, YOLOv8n-Pose, NumPy, scikit-learn, faster-whisper, jiwer e Streamlit. Versões em requirements-lock.txt. Inferência em CPU, com pesos locais. Internet é necessária para obter dependências, dados e modelos; não há API de cloud no processamento.

Vídeo: um quadro a cada seis, aproximadamente 5 FPS de uma origem de 30 FPS, resolução de inferência 640. Seleciona-se inicialmente a maior pessoa e depois a mais próxima do centro anterior. Articulações necessárias devem ter confiança mínima 0,35. Exige-se cobertura de 65% e pelo menos cinco amostras válidas no intervalo. A ausência de pose ou referência produz abstenção.

As seis medidas originais foram ampliadas para quinze: amplitude e percentis de abdução, cotovelo, inclinação do tronco, assimetria de ombros e duração, com medidas adicionais na fase elevada, velocidade e posição temporal do pico. A fase elevada é definida por abdução maior ou igual a 60% do máximo observado na repetição. As medidas são projeções 2D, sensíveis à perspectiva.

No protocolo personalizado, o vetor de entrada reúne diferenças assinadas e absolutas entre as quinze medidas da execução e da referência correta, totalizando trinta características. O artefato final escolhido é regressão logística padronizada, C=0,3, classes balanceadas e limiar 0,5. Exportação em JSON sem pickle, com inferência verificada contra scikit-learn. O escore não é probabilidade clínica.

Áudio: Whisper small multilíngue via faster-whisper, CPU int8, idioma pt, VAD e beam_size=5. Regras explícitas para dor, falta de ar, negação próxima e passado. A transcrição original é preservada; a hipótese auxiliar sentidor -> senti dor é acompanhada de aviso, sem alterar WER.'''),
    ('4. Protocolo de avaliação de 15/11', '''Primeiro foram comparadas regras lineares e florestas genéricas com validação aninhada por participante. Como essa tentativa não superou a referência simples em F1, foi registrado um segundo protocolo, personalizado, com uma execução correta de apoio por pessoa.

A referência é a primeira repetição anotada como correta de cada participante. É uma entrada explícita de calibração, não uma previsão e não um rótulo oculto da consulta. As oito referências são excluídas das métricas, restando 126 consultas. O uso exige que uma execução correta da mesma pessoa e vista esteja disponível. Sem essa condição, o resultado não se aplica.

Laço externo: deixar uma pessoa inteira de fora por vez. Laço interno: comparar regressão logística e floresta apenas entre as pessoas restantes, selecionando pela média de F1 por participante. Padronização e ajuste de pesos ocorrem dentro de cada treino. O participante externo fornece somente sua referência correta de apoio, excluída da avaliação; seus rótulos de consulta não entram no ajuste.

Depois da avaliação, o modelo de demonstração é treinado com todas as consultas de desenvolvimento e referências. Os resultados mostrados no painel são testes funcionais sobre exemplos conhecidos; não são as predições fora de treino usadas nas métricas. O experimento é retrospectivo, planejado após observar a limitação de v1, e requer confirmação futura com novos participantes.

Nos exemplos PM_001, a repetição 1 é apoio. O painel a marca como calibração e não a classifica; intervalos próprios que se sobreponham à referência também são marcados assim. A repetição 2 permite inspecionar uma execução correta distinta. A repetição 6 é sinalizada pelo modelo final do painel, mas foi falso negativo na predição externa sem ajuste nas consultas dessa pessoa. É um exemplo concreto da diferença entre demonstração e avaliação.'''),
    ('5. Resultados medidos',f'''Resultado original de 14/11: F1 {old['f1']:.3f} em 42 repetições de duas pessoas não usadas no treino original. Mantido em reports/video-test-metrics.json.

Experimento genérico retrospectivo de 15/11: F1 {generic['nested']['f1']:.3f} em 134 repetições. A referência de sinalizar tudo obteve F1 {generic['always_alert']['f1']:.3f}. Essa tentativa não foi adotada como melhoria principal.

Experimento personalizado retrospectivo: 126 consultas de oito pessoas, mais oito referências de calibração não pontuadas. F1 agregado {m['f1']:.3f}; precisão {m['precision']:.3f}; recall {m['recall']:.3f}; acurácia {m['accuracy']:.3f}. F1 médio entre participantes {macro:.3f}. Matriz [TN, FP; FN, TP]: {m['confusion_matrix']}. A referência de sinalizar tudo obteve F1 {baseline['f1']:.3f} neste mesmo conjunto de consultas.

Ainda houve 21 desvios perdidos e quatro falsos alertas. O participante 3 teve F1 zero; a variação entre pessoas deve ser mostrada. Portanto, o resultado é uma evidência exploratória condicional, não validação clínica ou garantia para uma pessoa nova. O protocolo, a quantidade de consultas e a calibração adicional diferem do primeiro teste de 14/11.

Áudio reservado de 14/11: quatro arquivos, {audio['reference_words']} palavras de referência, WER {audio['wer']:.2%} em relação aos roteiros e concordância das classes textuais {audio['attention_accuracy']:.0%} (4/4). A normalização remove pontuação, ignora maiúsculas e compacta espaços, preservando acentos. Amostra pequena e de um contexto de gravação. O glossário geral testado em 15/11 não melhorou A04: WER de calibração {glossary['wer']:.2%}, com a união sentidor ainda presente. O glossário não foi adotado.

Verificações de código incluem 28 testes de geometria, contexto, qualidade, metadados de idioma, preservação dos artefatos v1, exclusão das referências das métricas, ausência do rótulo da consulta na decisão, reprodução das referências e igualdade entre JSON e scikit-learn. Os 28 passaram novamente em 16/11. O teste do painel cobre análise, confirmação persistida e feedback separado. Em 15/11, um Chrome isolado verificou metadados ativos, processamento, confirmação e downloads reais de JSON/HTML sem exceções JavaScript. Bruno confirmou também o recebimento e a abertura dos dois arquivos na aba pessoal após o tratamento do conflito de tradução automática. A reprodução funcional de 16/11 está em reports/entrega/verificacao-16-11.json.'''),
    ('6. Fluxo de alerta, revisão e limitações', '''As duas modalidades produzem eventos com tempo relativo à fonte e evidência. Fontes independentes são identificadas como cenário composto e não geram uma alegação de sincronização clínica. Somente quando o áudio vem do próprio vídeo usa-se o mesmo relógio para combinar eventos próximos em uma janela de cinco segundos. Proximidade não demonstra causalidade.

O usuário confirma recebimento do alerta e pode baixar JSON e HTML. A confirmação não significa aprovação do classificador ou conduta médica. Os relatórios registram ID, parâmetros, referência, transcrição original, medidas, eventos e horário de confirmação. Feedback de movimento e fala é separado, preservando registros anteriores.

Limitações: oito participantes no vídeo, gravações controladas, projeção 2D, seleção heurística da pessoa, intervalos anotados ou manuais, referência correta assumida, falso negativo ainda frequente e texto com regras restritas. O usuário precisa fornecer uma referência adequada em arquivos próprios; o programa não verifica identidade ou qualidade clínica dessa referência.

Ensaios iniciais de pose levaram cerca de 5,5–5,9 s por trecho de 60 quadros, incluindo inicialização; não demonstram tempo real a 30 FPS. Máquina de desenvolvimento: Windows, oito processadores lógicos e aproximadamente 15,8 GiB de memória. Cache reutiliza medidas já extraídas e deve ser distinguido de tempo de inferência novo.

Próxima investigação: novos participantes reservados, qualidade de pose, detecção de compensações e segmentação automática. Novas decisões orientadas pelos erros já observados tornam esses exemplos dados de desenvolvimento, não um teste independente renovado.'''),
    ('7. Reprodução e preparação da entrega', f'''Repositório público: {delivery['repository_url']}. Abrir o painel neste computador: powershell -NoProfile -ExecutionPolicy Bypass -File .\\iniciar-painel.ps1. URL local: http://127.0.0.1:8501. Instruções de teste: docs/testes/teste-15-11.md. Checklist: TAREFAS.md.

Reproduzir experimentos: python scripts/experimento_movimento_v2.py e depois python scripts/experimento_referencia.py, com caches de pose já obtidos. A obtenção e a extração originais estão em docs/operacao/reproducao.md. Resultados novos em reports/v2; artefatos em configs/movement-reference-v2.json e configs/movement-references-v2.json. Gerar este documento: python scripts/gerar_relatorio_tecnico.py.

O relatório original foi arquivado em docs/historico/relatorio-tecnico-14-11.md e .pdf. Nenhum resultado original é substituído pelas novas métricas. Não comparar 0,39 e 0,79 como se o teste, a calibração e as pessoas de treino fossem idênticos.

Em outro computador, instalar Python 3.11 e dependências fixadas, baixar os oito vídeos selecionados, YOLOv8n-Pose e Whisper small conforme README. Gravações pessoais precisam ser fornecidas separadamente ou substituídas por uploads próprios. O clone contém código, configurações, relatório e resultados, mas não dados brutos, pesos ou ambiente Python. A reprodução de 16/11 usa a instalação local já preparada e caches existentes; não comprova instalação limpa em outra máquina.

Evidências selecionadas em reports/entrega: calibração, consulta correta distinta, possível desvio com fala afirmativa e confirmação, e erro conhecido de transcrição com aviso. Há JSON/HTML e manifesto de ambiente e hashes. São verificações funcionais automatizadas: a confirmação nelas foi acionada pelo script, sem representar feedback humano. Os arquivos não incluem mídia bruta. Regenerar com python scripts/preparar_demonstracao.py.

Roteiro e preparação dos colegas: docs/apresentacao/roteiro-video.md e docs/apresentacao/guia-do-grupo.md. A demonstração será neste computador. A passagem interna e o ensaio pelo grupo exigem confirmação humana. Publicar vídeo de até 15 minutos no YouTube ou Vimeo e conferir acesso. Link da apresentação: {presentation}. Prazo de submissão: 17/11/2026, às 23h59, horário de Brasília.

Fontes: REHAB24-6 — https://zenodo.org/records/13305826; YOLOv8 — https://docs.ultralytics.com/models/yolov8/; faster-whisper — https://github.com/SYSTRAN/faster-whisper; scikit-learn LeaveOneGroupOut — https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.LeaveOneGroupOut.html. As fontes possuem seus próprios termos e licenças.''')]
    illustrations='\n\n## Figuras\n\n- [Arquitetura implementada](arquitetura.md) (diagrama também incluído no PDF).\n\n![Matriz de confusão personalizada: 54 TN, 4 FP, 21 FN e 47 TP](../../reports/v2/figures/matriz-personalizada.png)\n\n![F1 no mesmo protocolo: personalizado e sinalizar tudo](../../reports/v2/figures/comparacao-personalizada.png)\n'
    Path('docs/relatorios/relatorio-tecnico.md').write_text(f'# Relatório técnico — revisão de {revision}\n\n'+'\n\n'.join('## '+t+'\n\n'+b for t,b in sections)+illustrations,encoding='utf-8')
    folder=Path('reports/v2/figures');folder.mkdir(exist_ok=True)
    fig,ax=plt.subplots(figsize=(7,5));matrix=m['confusion_matrix'];ax.imshow(matrix,cmap='Blues');ax.set_xticks([0,1],['Correta','Desvio']);ax.set_yticks([0,1],['Correta','Desvio']);ax.set_xlabel('Predição fora do treino da pessoa');ax.set_ylabel('Rótulo');ax.set_title('Exploratório personalizado · 126 consultas')
    for i,row in enumerate(matrix):
        for j,value in enumerate(row):ax.text(j,i,str(value),ha='center',va='center',fontsize=23,color='white' if value>max(max(r) for r in matrix)/2 else 'black')
    fig.tight_layout();fig.savefig(folder/'matriz-personalizada.png',dpi=150)
    fig2,ax=plt.subplots(figsize=(7,4));bars=ax.bar(['Procedimento personalizado','Sinalizar tudo'],[m['f1'],baseline['f1']],color=['#176b89','#b65b30']);ax.bar_label(bars,labels=[f"{m['f1']:.3f}",f"{baseline['f1']:.3f}"],padding=4);ax.set_ylim(0,1);ax.set_ylabel('F1 agregado');ax.set_title('Mesmo protocolo: 8 apoios excluídos, 126 consultas');fig2.tight_layout();fig2.savefig(folder/'comparacao-personalizada.png',dpi=150)
    with PdfPages('docs/relatorios/relatorio-tecnico.pdf') as pdf:
        pdf.infodict()['Title']='Observa — relatório técnico'
        pdf.infodict()['Subject']=f'Revisão de {revision}; vídeo e áudio, execução local'
        page_number=0
        for title,body in sections:
            lines=[]
            for p in body.split('\n\n'):lines+=textwrap.wrap(p,width=102)+['']
            for offset in range(0,len(lines),51):
                page_number+=1
                page=plt.figure(figsize=(8.27,11.69));page.text(.08,.95,title,fontsize=15,weight='bold');page.text(.08,.91,f'Observa · revisão de {revision} · experimental',fontsize=9,color='#566');page.text(.08,.87,'\n'.join(lines[offset:offset+51]),fontsize=9.1,va='top',linespacing=1.5);page.text(.92,.035,str(page_number),ha='right',fontsize=9);pdf.savefig(page);plt.close(page)
        diagram=architecture_figure()
        diagram.savefig('reports/entrega/arquitetura.png',dpi=130)
        diagram.text(.92,.035,str(page_number+1),ha='right',fontsize=9)
        fig.set_size_inches(8.27,11.69)
        fig.axes[0].set_position([.15,.30,.70,.50])
        fig.text(.08,.95,'Matriz de confusão · protocolo personalizado',fontsize=15,weight='bold')
        fig.text(.08,.91,'Oito pessoas · avaliação retrospectiva · apoios excluídos',fontsize=9,color='#566')
        fig.text(.10,.20,'54 execuções corretas sem alerta; 4 falsos alertas.\n47 desvios detectados; 21 desvios perdidos.\nClasse positiva: desvio anotado no dataset.',fontsize=10,linespacing=1.5)
        fig.text(.92,.035,str(page_number+2),ha='right',fontsize=9)
        fig2.set_size_inches(8.27,11.69)
        fig2.axes[0].set_position([.12,.38,.80,.37])
        fig2.text(.08,.95,'Comparação dentro do mesmo protocolo',fontsize=15,weight='bold')
        fig2.text(.08,.91,'F1 agregado sobre as mesmas 126 consultas',fontsize=9,color='#566')
        fig2.text(.10,.24,'A referência simples sinaliza desvio em todas as consultas.\nA comparação acima usa os mesmos dados e oito apoios excluídos.\nO F1 original de 0,39 pertence a outro protocolo.\nA diferença entre protocolos não mede ganho independente.',fontsize=10,linespacing=1.5)
        fig2.text(.92,.035,str(page_number+3),ha='right',fontsize=9)
        pdf.savefig(diagram);pdf.savefig(fig);pdf.savefig(fig2)
    plt.close('all');print(f'Relatório de {revision} e figuras gerados; histórico preservado.')

if __name__=='__main__':main()
