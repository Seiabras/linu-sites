"""Traz o Linu novo do app (linupedia, em ~/Documentos/projetos/LinuPedia/meu-app-idiomas) para o site, como o app
fez em 24/10/2026 (“O Linu novo em todo lugar”). Rode de novo quando o Linu mudar no app:

    python3 ferramentas/linu-do-app.py [pasta do app]

- img/linu/linu-frente.png e linu-costas.png: o Linu parado do mapa do linuhub (172 × 190);
- img/linu/linu-lado.png: os 4 passos de lado numa folha só (688 × 190), desenhados para a direita;
- img/linu/linu-contato.png: o Linu do contato em 4 poses (552 × 190): acenando, acenando de olho fechado, feliz e
  comemorando, para o aceno e o pulinho do js/movimento.js;
- img/linu-pixel.png: o Linu acenando (138 × 190), na página de erro e nas páginas de projeto;
- img/linu-logo.png (128 px), icone-180.png e icone-32.png: a logo e os ícones do app.
Tudo na cor padrão. Depois, rode o ferramentas/gerar-imagens.mjs para refazer a imagem de compartilhar.
"""
import sys
from pathlib import Path
from PIL import Image

APP = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.home() / 'Documentos/projetos/LinuPedia/meu-app-idiomas'
IMG = Path(__file__).resolve().parent.parent / 'public/img'
HUB = APP / 'assets/pixel/linuhub/linu-novo'

SOMBRA = 22  # as últimas 22 linhas do quadro do linuhub são a sombra do chão (scripts/arte/linuhub-linu-novo.py)


def abrir(caminho):
    return Image.open(caminho).convert('RGBA')


def sem_sombra(im):
    """Tira a sombra do chão que vem desenhada nos quadros de costas e de lado (cinza, com um contorno mais claro); no
    app ela não combina com a do Linu de frente (preta) e trocava de cor quando ele andava. O site desenha uma sombra só,
    igual em todas as poses (.cena-linu::before). Sai o cinza (pouca cor, nem o escuro do corpo nem o branco da barriga)
    que encosta na sombra, a partir da cor que mais aparece nas linhas de baixo, só nas 22 linhas do chão."""
    px = im.load()
    w, h = im.size
    cinza = lambda r, g, b: max(r, g, b) - min(r, g, b) <= 28 and 70 <= (r + g + b) / 3 <= 215
    fila = [(x, y) for y in range(h - 4, h) for x in range(w) if px[x, y][3] and cinza(*px[x, y][:3])]
    visto = set(fila)
    while fila:
        x, y = fila.pop()
        px[x, y] = (0, 0, 0, 0)
        for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
            if 0 <= nx < w and h - SOMBRA <= ny < h and (nx, ny) not in visto:
                r, g, b, a = px[nx, ny]
                if a and cinza(r, g, b):
                    visto.add((nx, ny))
                    fila.append((nx, ny))
    return im


def no_quadro(im, largura):
    """Põe um desenho de 138 de largura no meio do quadro do linuhub (172), como o app faz."""
    quadro = Image.new('RGBA', (largura, im.height))
    quadro.paste(im, ((largura - im.width) // 2, 0))
    return quadro


def salvar(im, destino):
    destino.parent.mkdir(parents=True, exist_ok=True)
    im.save(destino, optimize=True)
    print(destino.relative_to(IMG.parent), im.size)


# de frente, o app usa o Linu “olhando” com a sombra por cima: aqui vai o “olhando”, sem ela
salvar(no_quadro(abrir(APP / 'assets/pixel/linu-novo/olhando-padrao.png'), abrir(HUB / 'frente-padrao.png').width), IMG / 'linu/linu-frente.png')
salvar(sem_sombra(abrir(HUB / 'costas-padrao.png')), IMG / 'linu/linu-costas.png')
passos = [sem_sombra(abrir(HUB / f'anda-lado-{n}-padrao.png')) for n in range(1, 5)]
folha = Image.new('RGBA', (passos[0].width * 4, passos[0].height))
for i, passo in enumerate(passos):
    folha.paste(passo, (i * passo.width, 0))
salvar(folha, IMG / 'linu/linu-lado.png')
salvar(abrir(APP / 'assets/pixel/linu-novo/acenando-padrao.png'), IMG / 'linu-pixel.png')
poses = [abrir(APP / f'assets/pixel/linu-novo/{n}-padrao.png') for n in ('acenando', 'acenando-piscando', 'feliz', 'comemorando')]
contato = Image.new('RGBA', (poses[0].width * len(poses), poses[0].height))
for i, pose in enumerate(poses):
    contato.paste(pose, (i * pose.width, 0))
salvar(contato, IMG / 'linu/linu-contato.png')
salvar(abrir(APP / 'assets/logo/linu-logo.png').resize((128, 128), Image.LANCZOS), IMG / 'linu-logo.png')
icone = abrir(APP / 'public/apple-touch-icon.png')
salvar(icone.convert('RGB'), IMG / 'icone-180.png')
salvar(icone.resize((32, 32), Image.LANCZOS).convert('RGB'), IMG / 'icone-32.png')
