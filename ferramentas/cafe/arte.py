"""Kit de arte da API de imagens (04/11/2026): leva a tentativa aprovada de cada pedido para os arquivos do site.

Copiado igual em cada projeto (como o linu-modelo); o que muda de um projeto para o outro fica no `saidas.json`.
O original mora em `linuarquivos/modelos/ferramentas/arte/`; mudou lá, copie de novo (o README diz onde está cada cópia).

  <projeto>/arte/                    um pedido por pasta: pedido.md (o prompt e os anexos), as tentativas api-*.png
  <projeto>/arte/aprovadas.json      {"<pedido>": "<a tentativa que ficou>"}
  <projeto>/arte/aprovadas/          a cópia da aprovada em WebP (a que vai para o git; as tentativas não vão)
  <projeto>/arte/saidas.json         que arquivo sai de cada pedido (abaixo)

  python3 arte.py <pasta arte/>       (precisa do Pillow)

O saidas.json tem "raiz" (a pasta do site, a partir da pasta arte/) e uma lista de "regras"; vale a primeira cujo
"padrao" (expressão regular, com grupos nomeados) casa com o nome do pedido. Os grupos entram no "destino", junto com
{largura} e, nas folhas, {parte}. "trocar" troca o valor de um grupo (ex.: {"m": {"n": "noite", "d": "dia"}}).

  tipo "imagem": "proporcao" ("16:9", "4:3" ou null para manter a do corte), "corte" opcional ([x0, y0, x1, y1] em
                 frações, tirado antes da proporção), "larguras" ({"1600": teto em bytes}), "qualidade" ([início,
                 passo, mínimo]: baixa de passo em passo até caber no teto).
  tipo "folha":  as expressões de uma pessoa lado a lado, em fundo magenta (#FF00FF). O magenta vira transparente, a
                 folha é cortada pelas colunas vazias, na ordem de "partes" ({"<nome>": [partes]}), e cada figura vai
                 apoiada embaixo e centrada numa "caixa" ([largura, altura]), em WebP com "qualidade" fixa.
"""
import io, json, os, re, sys
from PIL import Image


def sem_magenta(img):
    """Fundo magenta para transparente, com a borda suave e sem o halo rosado."""
    img = img.convert('RGBA')
    px = img.load()
    w, h = img.size
    for y in range(h):
        for x in range(w):
            r, g, b, _ = px[x, y]
            m = min(r, b) - g  # quanto de magenta: alto no fundo, baixo no desenho
            if m > 150:
                px[x, y] = (0, 0, 0, 0)
            elif m > 60:
                a = int(255 * (150 - m) / 90)
                tira = m - 60  # tira o rosa que vazou na borda
                px[x, y] = (max(0, r - tira), g, max(0, b - tira), a)
    return img


def colunas(img, n):
    """As faixas de colunas com desenho; junta as mais próximas até sobrarem n."""
    w, h = img.size
    alfa = img.getchannel('A').load()
    cheia = [sum(1 for y in range(0, h, 2) if alfa[x, y] > 40) > h * 0.01 for x in range(w)]
    faixas, ini = [], None
    for x, c in enumerate(cheia + [False]):
        if c and ini is None:
            ini = x
        elif not c and ini is not None:
            faixas.append([ini, x]); ini = None
    faixas = [f for f in faixas if f[1] - f[0] > w * 0.02]
    while len(faixas) > n:
        i = min(range(len(faixas) - 1), key=lambda i: faixas[i + 1][0] - faixas[i][1])
        faixas[i:i + 2] = [[faixas[i][0], faixas[i + 1][1]]]
    if len(faixas) != n:
        raise SystemExit(f'achei {len(faixas)} figuras, esperava {n}')
    return faixas


def recortar(img, prop):
    if not prop:
        return img
    a, b = (int(x) for x in prop.split(':'))
    w, h = img.size
    if w / h > a / b:
        nw = round(h * a / b); return img.crop(((w - nw) // 2, 0, (w - nw) // 2 + nw, h))
    nh = round(w * b / a); return img.crop((0, (h - nh) // 2, w, (h - nh) // 2 + nh))


def webp(img, caminho, qualidade, teto=None):
    q, passo, minimo = qualidade if isinstance(qualidade, list) else (qualidade, 4, qualidade)
    while True:
        buf = io.BytesIO(); img.save(buf, 'WEBP', quality=q, method=6)
        if not teto or buf.tell() <= teto or q <= minimo: break
        q -= passo
    os.makedirs(os.path.dirname(caminho), exist_ok=True)
    open(caminho, 'wb').write(buf.getvalue())
    return buf.tell(), q


def imagem(img, regra, campos, raiz):
    if regra.get('corte'):
        x0, y0, x1, y1 = regra['corte']
        img = img.crop((round(img.width * x0), round(img.height * y0), round(img.width * x1), round(img.height * y1)))
    img = recortar(img, regra.get('proporcao'))
    for largura, teto in regra['larguras'].items():
        largura = int(largura)
        prop = regra.get('proporcao')
        altura = round(largura * int(prop.split(':')[1]) / int(prop.split(':')[0])) if prop else round(largura * img.height / img.width)
        destino = os.path.join(raiz, regra['destino'].format(largura=largura, **campos))
        tam, q = webp(img.resize((largura, altura), Image.LANCZOS), destino, regra.get('qualidade', [82, 4, 40]), teto)
        print(f'{os.path.relpath(destino, raiz)}  {tam // 1024} KB (q {q})')


def folha(img, regra, campos, raiz):
    partes = regra['partes'][campos['nome']]
    cw, ch = regra.get('caixa', [300, 360])
    img = sem_magenta(img)
    for (x0, x1), parte in zip(colunas(img, len(partes)), partes):
        fig = img.crop((x0, 0, x1, img.height))
        fig = fig.crop(fig.getbbox())
        escala = min(cw / fig.width, (ch - 8) / fig.height)
        fig = fig.resize((round(fig.width * escala), round(fig.height * escala)), Image.LANCZOS)
        tela = Image.new('RGBA', (cw, ch), (0, 0, 0, 0))
        tela.paste(fig, ((cw - fig.width) // 2, ch - fig.height), fig)
        destino = os.path.join(raiz, regra['destino'].format(parte=parte, **campos))
        tam, _ = webp(tela, destino, regra.get('qualidade', 88))
        print(f'{os.path.relpath(destino, raiz)}  {tam // 1024} KB')


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    arte = os.path.abspath(sys.argv[1])
    cfg = json.load(open(os.path.join(arte, 'saidas.json'), encoding='utf-8'))
    raiz = os.path.normpath(os.path.join(arte, cfg.get('raiz', '..')))
    aprovadas = json.load(open(os.path.join(arte, 'aprovadas.json'), encoding='utf-8'))
    os.makedirs(os.path.join(arte, 'aprovadas'), exist_ok=True)
    for pedido, arquivo in sorted(aprovadas.items()):
        regra = next((r for r in cfg['regras'] if re.match(r['padrao'], pedido)), None)
        if not regra:
            sys.exit(f'{pedido}: nenhuma regra do saidas.json serve')
        origem = os.path.join(arte, pedido, arquivo)
        guardada = os.path.join(arte, 'aprovadas', pedido + '.webp')
        if os.path.exists(origem):
            Image.open(origem).convert('RGB').save(guardada, 'WEBP', quality=90, method=6)
        elif not os.path.exists(guardada):
            sys.exit(f'{pedido}: falta {arquivo}')
        img = Image.open(origem if os.path.exists(origem) else guardada).convert('RGB')
        campos = re.match(regra['padrao'], pedido).groupdict()
        for g, tabela in regra.get('trocar', {}).items():
            campos[g] = tabela.get(campos[g], campos[g])
        (folha if regra['tipo'] == 'folha' else imagem)(img, regra, campos, raiz)


if __name__ == '__main__':
    main()
