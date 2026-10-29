"""Traz o Linu novo do app (linupedia, em ~/Documentos/projetos/LinuPedia/meu-app-idiomas) para o site, como o app
fez em 24/10/2026 (“O Linu novo em todo lugar”). Rode de novo quando o Linu mudar no app:

    python3 ferramentas/linu-do-app.py [pasta do app]

- img/linu/linu-frente.png e linu-costas.png: o Linu parado do mapa do linuhub (172 × 190, com a sombra);
- img/linu/linu-lado.png: os 4 passos de lado numa folha só (688 × 190), desenhados para a direita;
- img/linu-pixel.png: o Linu acenando (138 × 190), no contato, na página de erro e nas páginas de projeto;
- img/linu-logo.png (128 px), icone-180.png e icone-32.png: a logo e os ícones do app.
Tudo na cor padrão. Depois, rode o ferramentas/gerar-imagens.mjs para refazer a imagem de compartilhar.
"""
import sys
from pathlib import Path
from PIL import Image

APP = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.home() / 'Documentos/projetos/LinuPedia/meu-app-idiomas'
IMG = Path(__file__).resolve().parent.parent / 'public/img'
HUB = APP / 'assets/pixel/linuhub/linu-novo'


def abrir(caminho):
    return Image.open(caminho).convert('RGBA')


def salvar(im, destino):
    destino.parent.mkdir(parents=True, exist_ok=True)
    im.save(destino, optimize=True)
    print(destino.relative_to(IMG.parent), im.size)


salvar(abrir(HUB / 'frente-padrao.png'), IMG / 'linu/linu-frente.png')
salvar(abrir(HUB / 'costas-padrao.png'), IMG / 'linu/linu-costas.png')
passos = [abrir(HUB / f'anda-lado-{n}-padrao.png') for n in range(1, 5)]
folha = Image.new('RGBA', (passos[0].width * 4, passos[0].height))
for i, passo in enumerate(passos):
    folha.paste(passo, (i * passo.width, 0))
salvar(folha, IMG / 'linu/linu-lado.png')
salvar(abrir(APP / 'assets/pixel/linu-novo/acenando-padrao.png'), IMG / 'linu-pixel.png')
salvar(abrir(APP / 'assets/logo/linu-logo.png').resize((128, 128), Image.LANCZOS), IMG / 'linu-logo.png')
icone = abrir(APP / 'public/apple-touch-icon.png')
salvar(icone.convert('RGB'), IMG / 'icone-180.png')
salvar(icone.resize((32, 32), Image.LANCZOS).convert('RGB'), IMG / 'icone-32.png')
