"""A versão de cada arquivo pelo conteúdo (07/11/2026): põe ?v=<8 letras do hash> em todo src, href e data-piscar
local das páginas (menos nas fontes, que o CSS pede sem versão), para o navegador baixar de novo só o que mudou.

    python3 versao-arquivos.py <pasta do site> [página.html ...] [--conferir]

Por quê: o Caddy dos sites manda guardar /img, /css, /js e /fontes por 7 dias. Sem a versão no endereço, quem já
visitou continua vendo a imagem ou o CSS velho por até uma semana depois de publicar. Com o hash, o endereço muda
quando o arquivo muda, e só nesse caso. Sem página na linha de comando, pega todos os .html da pasta (sem descer).
--conferir só diz se alguma página está desatualizada (o Actions roda assim e reprova).
O original mora em linuarquivos/modelos/ferramentas/; cada site tem uma cópia em ferramentas/.
"""
import hashlib
import re
import sys
from pathlib import Path

# As fontes (.woff2) ficam de fora: o CSS pede a fonte sem versão (url(...) não passa por aqui), e o <link rel="preload">
# tem de pedir o mesmo endereço, senão o navegador baixa a fonte duas vezes. Uma ?v= que já esteja numa fonte sai.
ATRIBUTO = re.compile(r'\b(src|href|data-piscar)="([^"#?]+?\.(?:png|jpg|jpeg|webp|gif|svg|css|js|ico))(\?v=[^"]*)?"')
FONTE = re.compile(r'\b(href)="([^"#?]+?\.woff2)\?v=[^"]*"')


def versao(arquivo):
    return hashlib.sha256(arquivo.read_bytes()).hexdigest()[:8]


def carimbar(pasta, pagina):
    texto = pagina.read_text(encoding='utf-8')
    faltam = []

    def trocar(m):
        attr, caminho, _ = m.groups()
        if caminho.startswith(('http:', 'https:', '//', 'data:', 'mailto:')):
            return m.group(0)
        alvo = (pasta / caminho.lstrip('/')) if caminho.startswith('/') else (pagina.parent / caminho)
        if not alvo.is_file():
            faltam.append(caminho)
            return m.group(0)
        return f'{attr}="{caminho}?v={versao(alvo)}"'

    return texto, FONTE.sub(r'\1="\2"', ATRIBUTO.sub(trocar, texto)), faltam


def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    if not args:
        sys.exit(__doc__)
    pasta = Path(args[0]).resolve()
    paginas = [Path(p).resolve() for p in args[1:]] or sorted(pasta.glob('*.html'))
    atrasadas = 0
    for pagina in paginas:
        antes, depois, faltam = carimbar(pasta, pagina)
        for f in faltam:
            print(f'  {pagina.name}: {f} não existe')
        if depois != antes:
            atrasadas += 1
            if '--conferir' not in sys.argv:
                pagina.write_text(depois, encoding='utf-8')
                print(f'  {pagina.name}: versões atualizadas')
    if '--conferir' in sys.argv:
        print('As versões dos arquivos estão em dia.' if not atrasadas else
              f'{atrasadas} página(s) com versão velha. Rode: python3 ferramentas/versao-arquivos.py .')
        sys.exit(1 if atrasadas else 0)


if __name__ == '__main__':
    main()
