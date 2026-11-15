"""Regras limitadas e explicaveis; nao produzem diagnostico."""
import re
import unicodedata


def analyze(text):
    normalized = ''.join(c for c in unicodedata.normalize('NFD', text.lower()) if unicodedata.category(c) != 'Mn')
    corrections = []
    if re.search(r'\bsentidor\b', normalized):
        normalized = re.sub(r'\bsentidor\b', 'senti dor', normalized)
        corrections.append('Possivel uniao de palavras: sentidor -> senti dor. Confira o audio.')
    evidence = []
    for clause in re.split(r'[.!?;,]|\b(?:mas|porem)\b', normalized):
        for match in re.finditer(r'\b(?:dor|falta de ar)\b', clause):
            before = clause[:match.start()].split()[-6:]
            if 'nao' in before or 'sem' in before:
                status = 'negado'
            elif any(word in before for word in ['ontem','antes','senti','sentia']):
                status = 'passado'
            else:
                status = 'atual'
            evidence.append({'expression': match.group(), 'context': clause.strip(), 'status': status})
    status = 'sim' if any(e['status']=='atual' for e in evidence) else 'contexto_passado' if any(e['status']=='passado' for e in evidence) else 'nao'
    return {'attention': status, 'evidence': evidence, 'review_notes': corrections, 'original_text': text}
