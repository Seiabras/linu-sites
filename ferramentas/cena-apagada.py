"""Gera public/img/abrigo-estacao-apagada.png: a estação de noite com o lampião apagado (o modo escuro
do site; no app a noite continua com o lampião aceso). A sala é a imagem de dia recolorida pela conta
que leva o dia à noite, ajustada longe do lampião (sem o halo da luz), e um pouco mais escura; o que
se vê lá fora (pela porta, pela escotilha e do lado de fora da barraca) continua o da noite, com a aurora.

    python3 ferramentas/cena-apagada.py
"""
from pathlib import Path
import numpy as np
from PIL import Image

IMG = Path(__file__).resolve().parent.parent / 'public/img'
d = np.asarray(Image.open(IMG / 'abrigo-estacao-dia.png').convert('RGB')).astype(float)
n = np.asarray(Image.open(IMG / 'abrigo-estacao-noite.png').convert('RGB')).astype(float)
H, W = d.shape[:2]
ys, xs = np.mgrid[0:H, 0:W]
R, G, B = d[..., 0], d[..., 1], d[..., 2]
paisagem = (B - R >= 6) & ((R + G + B) / 3 > 120)
fora = np.zeros((H, W), bool)
for x0, y0, x1, y1 in [(33, 38, 67, 178), (71, 48, 95, 89)]:  # porta e escotilha
    fora |= (xs >= x0) & (xs < x1) & (ys >= y0) & (ys < y1) & paisagem
for y in range(H):  # do lado de fora da barraca, até a primeira linha escura da parede
    for x in range(40):
        if d[y, x].mean() < 70:
            break
        fora[y, x] = True
longe = ((xs > 290) | (ys > 165)) & ~fora
M = np.linalg.lstsq(np.c_[d[longe], np.ones(longe.sum())], n[longe], rcond=None)[0]
sala = (np.c_[d.reshape(-1, 3), np.ones(H * W)] @ M).reshape(H, W, 3) * 0.8
out = np.where(fora[..., None], n, sala)
Image.fromarray(np.clip(out, 0, 255).astype(np.uint8)).save(IMG / 'abrigo-estacao-apagada.png', optimize=True)
