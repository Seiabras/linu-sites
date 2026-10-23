# Uso: python3 ferramentas/corrigir-porta-estacao.py <dia.png> <noite.png> <saida.png>
# (feito para assets/pixel/abrigo-estacao-{noite,sol-da-meia-noite}.png do linupedia; a noite do site é a mesma do app)
"""Tira o retângulo da porta e da escotilha nas versões de noite e de sol da meia-noite da estação.
O recolorido pintou a paisagem de fora num retângulo inteiro, por cima da cortina e do batente: aqui,
dentro desses retângulos, o que na imagem de dia não é paisagem volta a ser a imagem de dia recolorida
pela mesma conta (ajustada na parede ao lado)."""
import sys
from PIL import Image
import numpy as np
dia_p, luz_p, saida = sys.argv[1:4]
d = np.asarray(Image.open(dia_p).convert('RGB')).astype(float)
src = Image.open(luz_p).convert('RGBA'); n = np.asarray(src).astype(float); a = n[..., 3:]; n = n[..., :3]
ys, xs = np.mgrid[0:d.shape[0], 0:d.shape[1]]
caixas = [(33, 38, 67, 178), (71, 48, 95, 89)]  # porta e escotilha (x0, y0, x1, y1)
amostra = (xs >= 68) & (xs < 120) & ~((xs >= 70) & (xs < 95) & (ys >= 45) & (ys < 92))
M = np.linalg.lstsq(np.c_[d[amostra], np.ones(amostra.sum())], n[amostra], rcond=None)[0]
pred = (np.c_[d.reshape(-1, 3), np.ones(d.shape[0] * d.shape[1])] @ M).reshape(d.shape)
R, G, B = d[..., 0], d[..., 1], d[..., 2]
paisagem = (B - R >= 6) & ((R + G + B) / 3 > 120)
out = n.copy()
for x0, y0, x1, y1 in caixas:
    m = (xs >= x0) & (xs < x1) & (ys >= y0) & (ys < y1) & ~paisagem
    out[m] = pred[m]
Image.fromarray(np.concatenate([np.clip(np.rint(out), 0, 255), a], -1).astype(np.uint8), 'RGBA').save(saida, optimize=True)
