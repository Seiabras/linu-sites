# O mapa das cinco regiões do Brasil (1/11/2026) para o filtro "Onde você mora?" do Pica ou Não Pica?.
# Junta os estados do br-estados.geojson (o mesmo do Guia do Cerrado) por região, simplifica e grava regioes.svg,
# que o guia-pt.py lê. Rodar só se quiser refazer o desenho: python3 regioes.py
import json, math, pathlib
from shapely.geometry import shape
from shapely.ops import unary_union

AQUI = pathlib.Path(__file__).resolve().parent
GEO = AQUI.parent / 'fotografia-do-cerrado' / 'br-estados.geojson'
REGIOES = {
    'N': ('Norte', 'AC AM AP PA RO RR TO'), 'NE': ('Nordeste', 'AL BA CE MA PB PE PI RN SE'),
    'CO': ('Centro-Oeste', 'DF GO MS MT'), 'SE': ('Sudeste', 'ES MG RJ SP'), 'S': ('Sul', 'PR RS SC'),
}
estados = {f['properties']['sigla']: shape(f['geometry']).buffer(0) for f in json.load(open(GEO))['features']}
x0, x1, y0, y1 = -74.1, -34.7, -33.8, 5.3
k = math.cos(math.radians(14))
largura = 400
esc = largura / ((x1 - x0) * k)
altura = round((y1 - y0) * esc)
def pt(x, y): return f'{(x - x0) * k * esc:.1f},{(y1 - y) * esc:.1f}'
def caminho(g):
    partes = []
    polys = getattr(g, 'geoms', [g])
    for p in polys:
        if p.area < 0.3: continue
        for anel in [p.exterior]:
            c = list(anel.coords)
            partes.append('M' + ' L'.join(pt(x, y) for x, y in c) + 'Z')
    return ''.join(partes)
paths = []
for sig, (nome, ufs) in REGIOES.items():
    g = unary_union([estados[u] for u in ufs.split()]).simplify(0.12, preserve_topology=True)
    c = g.centroid
    paths.append(f'<path class="regiao" data-regiao="{sig}" d="{caminho(g)}"><title>{nome}</title></path>')
svg = f'<svg class="mapa-regioes" viewBox="0 0 {largura} {altura}" width="{largura}" height="{altura}" role="img" aria-label="Mapa das cinco regiões do Brasil">{"".join(paths)}</svg>'
(AQUI / 'regioes.svg').write_text(svg + '\n')
print('regioes.svg', len(svg), 'bytes')
