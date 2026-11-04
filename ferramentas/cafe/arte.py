"""As fotos do Café Aurora e da Padaria Aurora (geradas pela API de imagens do Google, 04/11/2026) para o site.

  ferramentas/cafe/arte/aprovadas.json diz qual tentativa de cada pedido ficou (arte/<pedido>/api-*.png). Saem, em WebP:
  - cardápio (n1…n6 de noite, d1…d6 de dia), 4:3: sitios/cafe-aurora/img/cardapio/<noite|dia>-<n>-{400,720}.webp
  - abertura (n-abertura, d-abertura), 16:9: sitios/cafe-aurora/img/abertura-<noite|dia>-{800,1600}.webp
  - origem (n-origem, d-origem), 4:5: sitios/cafe-aurora/img/origem-<noite|dia>-{480,800}.webp
  A tentativa aprovada também fica guardada, menor, em arte/aprovadas/ (as outras não vão para o git).

  python3 ferramentas/cafe/arte.py          (precisa do Pillow)
"""
import io, json, os, re, sys
from PIL import Image

AQUI = os.path.dirname(os.path.abspath(__file__))
ARTE = os.path.join(AQUI, 'arte')
SITIO = os.path.normpath(os.path.join(AQUI, '..', '..', 'sitios', 'cafe-aurora', 'img'))
# largura: teto em bytes (as diretrizes pedem até 200 KB por imagem; o cardápio fica bem abaixo)
TAMANHOS = {
    'cardapio': ((4, 3), {400: 28_000, 720: 60_000}),
    'abertura': ((16, 9), {800: 70_000, 1600: 170_000}),
    'origem': ((4, 5), {480: 45_000, 800: 95_000}),
}


def destino(pedido):
    m = re.match(r'([nd])(\d)-', pedido)
    if m:
        return 'cardapio', os.path.join(SITIO, 'cardapio', f'{"noite" if m[1] == "n" else "dia"}-{m[2]}')
    m = re.match(r'([nd])-(abertura|origem)$', pedido)
    if m:
        return m[2], os.path.join(SITIO, f'{m[2]}-{"noite" if m[1] == "n" else "dia"}')
    sys.exit(f'pedido sem destino: {pedido}')


def recortar(img, prop):
    w, h = img.size
    a = prop[0] / prop[1]
    if w / h > a:
        nw = round(h * a); return img.crop(((w - nw) // 2, 0, (w - nw) // 2 + nw, h))
    nh = round(w / a); return img.crop((0, (h - nh) // 2, w, (h - nh) // 2 + nh))


def webp(img, caminho, teto):
    q = 82
    while True:
        buf = io.BytesIO(); img.save(buf, 'WEBP', quality=q, method=6)
        if buf.tell() <= teto or q <= 40: break
        q -= 4
    open(caminho, 'wb').write(buf.getvalue())
    return buf.tell(), q


def main():
    aprovadas = json.load(open(os.path.join(ARTE, 'aprovadas.json'), encoding='utf-8'))
    os.makedirs(os.path.join(ARTE, 'aprovadas'), exist_ok=True)
    os.makedirs(os.path.join(SITIO, 'cardapio'), exist_ok=True)
    for pedido, arquivo in sorted(aprovadas.items()):
        origem = os.path.join(ARTE, pedido, arquivo)
        guardada = os.path.join(ARTE, 'aprovadas', pedido + '.webp')
        if os.path.exists(origem):
            Image.open(origem).convert('RGB').save(guardada, 'WEBP', quality=90, method=6)
        elif not os.path.exists(guardada):
            sys.exit(f'{pedido}: falta {arquivo}')
        tipo, base = destino(pedido)
        prop, larguras = TAMANHOS[tipo]
        img = recortar(Image.open(origem if os.path.exists(origem) else guardada).convert('RGB'), prop)
        for largura, teto in larguras.items():
            altura = round(largura * prop[1] / prop[0])
            tam, q = webp(img.resize((largura, altura), Image.LANCZOS), f'{base}-{largura}.webp', teto)
            print(f'{os.path.relpath(base, SITIO)}-{largura}.webp  {tam // 1024} KB (q {q})')


if __name__ == '__main__':
    main()
