"""Desenha o Linu de lado, andando para a direita, em pixel art: 4 quadros de 52 × 61 numa folha só
(public/img/linu/linu-lado.png, 208 × 61). A grade, a paleta e o olho feliz são os do Linu de frente
do app (LinuLingo, assets/pixel/linu/). Cada pixel é decidido no centro dele (sem suavizar), depois
vem o sombreado em faixas e o contorno.

    python3 ferramentas/desenhar-linu-lado.py
"""
import math
from pathlib import Path
from PIL import Image

W, H = 52, 61
CONTORNO = (31, 42, 68)
AZUL = [(30, 40, 69), (36, 47, 79), (45, 59, 95), (52, 65, 99), (62, 78, 118)]  # da sombra à luz
BRANCO = [(206, 193, 211), (229, 235, 242), (243, 246, 250), (248, 250, 252)]
BOCHECHA = (232, 176, 196)
BICO = (31, 42, 68)
PE = [(190, 160, 186), (214, 190, 210)]
OLHO = (31, 42, 68)


def elipse(x, y, cx, cy, rx, ry, ang=0.0):
    c, s = math.cos(ang), math.sin(ang)
    dx, dy = x - cx, y - cy
    u, v = dx * c + dy * s, -dx * s + dy * c
    return (u / rx) ** 2 + (v / ry) ** 2


def quadro(f):
    """f = 0..3: passo com o pé da frente adiante, passagem, passo com o outro pé, passagem."""
    sobe = 1 if f in (1, 3) else 0              # na passagem o corpo sobe um pixel
    passo = {0: 1, 1: 0, 2: -1, 3: 0}[f]          # quanto o pé da frente está adiante
    asa = {0: 0.22, 1: 0.0, 2: -0.22, 3: 0.0}[f]  # a nadadeira balança ao contrário do pé
    oy = -sobe
    px = {}

    def pinta(x, y, cor):
        if 0 <= x < W and 0 <= y < H:
            px[(x, y)] = cor

    # pés (por baixo de tudo): o de trás um tom mais escuro
    for lado, d in ((-1, -passo), (1, passo)):
        cx = 26 + d * 6 + (1 if lado > 0 else -2)
        ergue = 1 if d < 0 and passo else 0  # o pé de trás sai do chão
        for y in range(54, 61):
            for x in range(W):
                if elipse(x + .5, y + .5 + ergue, cx + 2, 58.3, 5.5, 2.4) <= 1:
                    pinta(x, y, PE[1] if lado > 0 else PE[0])

    for y in range(H):
        for x in range(W):
            X, Y = x + .5, y + .5 - oy
            corpo = elipse(X, Y, 25, 41, 15, 16.5, -0.08) <= 1
            cabeca = elipse(X, Y, 27, 21, 14, 13.5) <= 1
            if not (corpo or cabeca):
                continue
            # rosto branco na frente da cabeça, com o “boné” escuro por cima e por trás
            rosto = cabeca and elipse(X, Y, 33.5, 25, 8.5, 8.2) <= 1 and Y > 17
            barriga = corpo and elipse(X, Y, 30, 43, 9.5, 14) <= 1 and Y > 30
            if rosto or barriga:
                # o branco sombreia para baixo e para trás
                t = (Y - 20) / 40 + (30 - X) / 30
                cor = BRANCO[3] if t < .3 else BRANCO[2] if t < .7 else BRANCO[1] if t < 1.05 else BRANCO[0]
            else:
                # o azul pega luz do alto, à frente
                if cabeca:
                    t = (X - 27) / 14 * .5 - (Y - 21) / 13.5 * .7
                else:
                    t = (X - 25) / 15 * .4 - (Y - 41) / 16.5 * .5
                cor = AZUL[4] if t > .55 else AZUL[3] if t > .25 else AZUL[2] if t > -.1 else AZUL[1] if t > -.45 else AZUL[0]
            pinta(x, y, cor)

    # a barbicha: a linha fina que passa por baixo do rosto
    for x in range(25, 41):
        y = round(29 + oy + 0.0018 * (x - 33) ** 4 / 10 + 0.06 * (x - 33) ** 2)
        if (x, y) in px and px[(x, y)] in BRANCO:
            pinta(x, y, CONTORNO)

    # olho feliz (um arco, como o de frente) e a bochecha
    for x, y in ((33, 22), (34, 21), (35, 21), (36, 22)):
        pinta(x, y + oy, OLHO)
    for x, y in ((35, 25), (36, 25), (37, 25)):
        pinta(x, y + oy, BOCHECHA)

    # bico: sai do rosto para a frente
    for x, y in ((41, 22), (41, 23), (41, 24), (42, 23), (42, 24), (43, 23), (43, 24), (44, 24), (42, 25), (41, 25)):
        pinta(x, y + oy, BICO)
    pinta(42, 23 + oy, (70, 82, 115))

    # nadadeira: presa no ombro, balançando; a borda escura separa ela do corpo
    asa_px = set()
    for y in range(H):
        for x in range(W):
            X, Y = x + .5, y + .5 - oy
            if elipse(X, Y, 23.5 - 6 * math.sin(asa), 42, 3.4, 11, 0.38 + 1.3 * asa) <= 1 and Y > 31:
                asa_px.add((x, y))
    for x, y in asa_px:
        borda = any(v not in asa_px for v in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)))
        t = (x - 23) / 4 - (y - 40) / 11
        pinta(x, y, CONTORNO if borda else AZUL[3] if t > .6 else AZUL[1])

    img = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    for (x, y), cor in px.items():
        img.putpixel((x, y), cor + (255,))
    # contorno: todo pixel pintado que encosta no vazio (os pés, de rosa, têm contorno próprio mais claro)
    a = img.copy()
    for (x, y), cor in px.items():
        viz = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
        if any(v not in px for v in viz):
            a.putpixel((x, y), ((150, 120, 150) if cor in PE else CONTORNO) + (255,))
    # contorno da nadadeira por dentro do corpo, do lado de trás
    return a


folha = Image.new('RGBA', (W * 4, H), (0, 0, 0, 0))
for f in range(4):
    folha.alpha_composite(quadro(f), (W * f, 0))
saida = Path(__file__).resolve().parent.parent / 'public/img/linu/linu-lado.png'
folha.save(saida, optimize=True)
print(saida)
