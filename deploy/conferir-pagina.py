"""Confere, antes de publicar, que todo arquivo local que as páginas de public/ usam (src, href, srcset,
url() do CSS) existe de verdade, que nenhuma moeda está com preços provisórios e que as fontes de japonês, coreano e
chinês não passam de 400 KB por língua. Sai com erro e a lista do que falta.

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
    # '%23' é o '#' escrito dentro de um SVG embutido no CSS (o filter='url(#n)' do Café Aurora)
    if partes.scheme or partes.netloc or ref.startswith(('#', '%23', 'mailto:', 'tel:', 'data:')):
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

# Enquanto uma moeda usada por alguma página estiver pendente (ferramentas/pagina/precos.json), nada é publicado
import json
precos = json.loads((PUBLIC.parent / 'ferramentas' / 'pagina' / 'precos.json').read_text(encoding='utf-8'))
usadas = {m for pagina in PUBLIC.rglob('index.html') for m in re.findall(r'<html[^>]*data-moeda="([A-Z]{3})"', pagina.read_text(encoding='utf-8'))}
pendentes = [f'{moeda}: {tabela["pendente"]}' for moeda, tabela in precos.items() if moeda in usadas and isinstance(tabela, dict) and tabela.get('pendente')]
if pendentes:
    print('Preços pendentes, não publica:\n  ' + '\n  '.join(pendentes))
    sys.exit(1)

# As fontes de cada língua, somadas, ficam em até 400 KB por página (ferramentas/gerar-fontes.mjs)
LIMITE_FONTES = 400 * 1024
linguas = {}
for fonte in (PUBLIC / 'fontes').glob('noto-*.woff2'):
    lingua = fonte.stem.rsplit('-', 1)[0]
    linguas[lingua] = linguas.get(lingua, 0) + fonte.stat().st_size
pesadas = [f'{lingua}: {tamanho // 1024} KB' for lingua, tamanho in sorted(linguas.items()) if tamanho > LIMITE_FONTES]
if pesadas:
    print('Fontes acima de 400 KB por página, não publica:\n  ' + '\n  '.join(pesadas))
    sys.exit(1)

if faltando:
    print('Arquivos que não existem:\n  ' + '\n  '.join(faltando))
    sys.exit(1)
print('Todos os arquivos usados pelas páginas existem.')
