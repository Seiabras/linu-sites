"""Transforma as páginas de um site de estudo (sitios/<site>/*.html) em modelos com {{chave}} no lugar de cada texto e
grava o português em ferramentas/estudo/<site>/textos/pt-BR.json. Roda uma vez por site (ou de novo depois de mudar o
HTML em português); depois, as traduções e o ferramentas/gerar-estudo.mjs fazem o resto.

    python3 ferramentas/estudo/extrair.py fotografia-do-cerrado

Cada bloco de texto (um elemento que só tem texto e marcação de dentro da frase, como <strong>, <a> e <mark>) vira uma
chave inteira, para a frase ser traduzida de uma vez; o mesmo texto repetido em várias páginas usa a mesma chave."""
import json, re, sys
from html.parser import HTMLParser
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
site = sys.argv[1]
ORIGEM = RAIZ / 'sitios' / site
DESTINO = RAIZ / 'ferramentas' / 'estudo' / site
DENTRO_DA_FRASE = {'a', 'b', 'strong', 'em', 'i', 'mark', 'span', 'br', 'small', 'abbr', 'code', 'sup', 'sub', 'q', 'cite', 'time'}
VAZIOS = {'br', 'img', 'input', 'meta', 'link', 'hr', 'source', 'area', 'col', 'wbr'}
ATRIBUTOS = ('alt', 'title', 'aria-label', 'placeholder', 'data-escuro', 'data-claro')
LETRA = re.compile(r'[A-Za-zÀ-ú]')


class Leitor(HTMLParser):
    def __init__(self, texto):
        super().__init__(convert_charrefs=False)
        self.texto = texto
        self.inicio_linha = [0]
        for m in re.finditer('\n', texto):
            self.inicio_linha.append(m.end())
        self.pilha = []
        self.blocos = []

    def pos(self):
        linha, coluna = self.getpos()
        return self.inicio_linha[linha - 1] + coluna

    def handle_starttag(self, tag, attrs):
        if self.pilha:
            self.pilha[-1]['filhos_bloco'] |= tag not in DENTRO_DA_FRASE
        if tag in VAZIOS:
            return
        fim_da_tag = self.texto.index('>', self.pos()) + 1
        self.pilha.append({'tag': tag, 'dentro': fim_da_tag, 'filhos_bloco': False, 'texto': False})

    def handle_startendtag(self, tag, attrs):
        if self.pilha:
            self.pilha[-1]['filhos_bloco'] |= tag not in DENTRO_DA_FRASE

    def handle_data(self, data):
        if LETRA.search(data):
            for e in self.pilha:
                e['texto'] = True

    def handle_endtag(self, tag):
        if tag in VAZIOS:
            return
        while self.pilha:
            e = self.pilha.pop()
            if e['tag'] == tag:
                break
        if e['tag'] in ('script', 'style'):
            return
        if e['texto'] and not e['filhos_bloco'] and e['tag'] not in DENTRO_DA_FRASE - {'a', 'span', 'q', 'strong', 'b', 'em'}:
            self.blocos.append((e['dentro'], self.pos()))
        # um bloco com filhos de bloco não vira chave; os filhos viram (o pai fica marcado para os avós)
        if self.pilha and (e['filhos_bloco'] or e['tag'] not in DENTRO_DA_FRASE):
            self.pilha[-1]['filhos_bloco'] = True


chaves = {}
por_texto = {}


def chave(pagina, texto):
    limpo = ' '.join(texto.split())
    if limpo in por_texto:
        return por_texto[limpo]
    n = len(chaves) + 1
    k = f"{pagina.replace('-', '_')}_{n:03d}"  # o gerador só aceita letras, números e _ nas chaves
    chaves[k] = limpo
    por_texto[limpo] = k
    return k


(DESTINO / 'modelo').mkdir(parents=True, exist_ok=True)
for arquivo in sorted(ORIGEM.glob('*.html')):
    pagina = arquivo.stem
    texto = arquivo.read_text(encoding='utf-8')
    leitor = Leitor(texto)
    leitor.feed(texto)
    # os blocos mais de dentro primeiro não acontecem: um bloco só tem filhos de dentro da frase; tira os que estão
    # dentro de outro bloco e troca de trás para a frente, para as posições valerem
    blocos = sorted(set(leitor.blocos))
    finais = [b for b in blocos if not any(o != b and o[0] <= b[0] and b[1] <= o[1] for o in blocos)]
    for ini, fim in sorted(finais, reverse=True):
        miolo = texto[ini:fim]
        if not LETRA.search(re.sub(r'<[^>]+>', '', miolo)):
            continue
        lead = re.match(r'\s*', miolo).group(0)
        tail = re.search(r'\s*$', miolo).group(0)
        texto = texto[:ini] + lead + '{{' + chave(pagina, miolo.strip()) + '}}' + tail + texto[fim:]
    def atributo(m):
        nome, valor = m.group(1), m.group(2)
        if '{{' in valor or not LETRA.search(valor):
            return m.group(0)
        return f'{nome}="{{{{{chave(pagina, valor)}}}}}"'
    texto = re.sub(r'\b(' + '|'.join(ATRIBUTOS) + r')="([^"]*)"', atributo, texto)
    texto = re.sub(r'(<meta name="description" content=")([^"]*)(")', lambda m: m.group(1) + '{{' + chave(pagina, m.group(2)) + '}}' + m.group(3), texto)
    # o idioma, os arquivos (na pasta de cada idioma, um nível abaixo) e os idiomas no rodapé
    texto = texto.replace('<html lang="pt-BR">', '<html lang="{{lang}}">')
    texto = re.sub(r'(href|src)="((?:css|js|img|fontes)/[^"]*)"', r'\1="{{raiz}}\2"', texto)
    texto = texto.replace('</head>', '{{alternativas}}\n<script type="application/json" id="textos-estudo">{{textos_js}}</script>\n</head>', 1)
    texto = re.sub(r'(<footer class="rodape">\s*<div class="container">)', r'\1\n            {{idiomas}}', texto, count=1)
    (DESTINO / 'modelo' / arquivo.name).write_text(texto, encoding='utf-8')
    corpo = re.sub(r'<script.*?</script>|<!--.*?-->|\{\{[a-z0-9_]+\}\}', '', texto, flags=re.S)
    sobra = [t.strip() for t in re.split(r'<[^>]+>', corpo) if LETRA.search(t)]
    print(f'{arquivo.name}: sobrou {sobra}' if sobra else f'{arquivo.name}: ok')

(DESTINO / 'textos').mkdir(exist_ok=True)
saida = DESTINO / 'textos' / 'pt-BR.json'
js = json.loads(saida.read_text())['js'] if saida.exists() else {}
saida.write_text(json.dumps({'textos': chaves, 'js': js}, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(len(chaves), 'chaves em', saida.relative_to(RAIZ))
