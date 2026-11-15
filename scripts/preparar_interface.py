"""Set locale before React mounts, only in a project-owned Streamlit installation."""
import re
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
MARKER='<meta name="observa-locale" content="pt-BR-no-translate">'

def localize_html(source):
    match=re.search(r'<html\b[^>]*>',source,flags=re.I)
    if match is None or not re.search(r'<head\b[^>]*>',source,flags=re.I):
        raise ValueError('Template HTML do Streamlit não reconhecido; não foi modificado.')
    tag=match.group()
    for name,value in [('lang','pt-BR'),('translate','no')]:
        pattern=rf'\s{name}\s*=\s*(?:"[^"]*"|\x27[^\x27]*\x27|[^\s>]+)'
        tag=re.sub(pattern,'',tag,flags=re.I)
        tag=tag[:-1]+f' {name}="{value}">'
    source=source[:match.start()]+tag+source[match.end():]
    if MARKER not in source:
        source=re.sub(r'(<head\b[^>]*>)',lambda m:m.group()+'\n'+MARKER+'\n<meta name="google" content="notranslate">',source,count=1,flags=re.I)
    return source

def main():
    import streamlit
    target=(Path(streamlit.__file__).parent/'static/index.html').resolve()
    if not target.is_relative_to(ROOT):
        print('Instalação fora do projeto: template mantido. Use um ambiente virtual dentro do projeto ou desative a tradução no navegador.')
        return
    source=target.read_text(encoding='utf-8');updated=localize_html(source)
    if source!=updated:
        backup=target.with_name('index.observa-original.html')
        if not backup.exists():backup.write_text(source,encoding='utf-8')
        target.write_text(updated,encoding='utf-8')
    print('Interface preparada: pt-BR, tradução automática desativada no documento.')

if __name__=='__main__':main()
