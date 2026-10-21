"""Confere, antes de publicar, que todo arquivo local que as páginas de public/ usam (src, href, srcset,
url() do CSS) existe de verdade. Sai com erro e a lista do que falta.

    python3 deploy/conferir-pagina.py
"""
import re
import sys
from pathlib import Path
from urllib.parse import urlsplit, unquote

PUBLIC = Path(__file__).resolve().parent.parent / 'public'
faltando = []


def conferir(origem, ref):
    partes = urlsplit(ref)
    if partes.scheme or partes.netloc or ref.startswith(('#', 'mailto:', 'tel:', 'data:')):
        return
    caminho = unquote(partes.path)
    if not caminho or caminho in ('.', './'):
        return
    alvo = (PUBLIC / caminho.lstrip('/')) if caminho.startswith('/') else (origem.parent / caminho)
    if alvo.is_dir():
        alvo = alvo / 'index.html'
    elif not alvo.exists():
        alvo = alvo.with_name(alvo.name + '.html')  # como o try_files do Caddy: /projetos/x serve x.html
    if not alvo.resolve().is_file():
        faltando.append(f'{origem.relative_to(PUBLIC)}: {ref}')


for pagina in PUBLIC.rglob('*.html'):
    html = pagina.read_text(encoding='utf-8')
    html = re.sub(r'<!--.*?-->', '', html, flags=re.S)  # o que está comentado não conta
    for ref in re.findall(r'\s(?:src|href)="([^"]+)"', html):
        conferir(pagina, ref)
    for srcset in re.findall(r'\ssrcset="([^"]+)"', html):
        for item in srcset.split(','):
            conferir(pagina, item.strip().split(' ')[0])
for css in PUBLIC.rglob('*.css'):
    for ref in re.findall(r'url\(["\']?([^"\')]+)', css.read_text(encoding='utf-8')):
        conferir(css, ref)

if faltando:
    print('Arquivos que não existem:\n  ' + '\n  '.join(faltando))
    sys.exit(1)
print('Todos os arquivos usados pelas páginas existem.')
