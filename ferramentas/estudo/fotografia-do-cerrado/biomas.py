# Rodar (precisa do shapely: python3 -m venv /tmp/v && /tmp/v/bin/pip install shapely): baixar nesta pasta
#   https://github.com/ipeaGIT/geobr/releases/download/v1.7.0/biomes_2019_simplified.gpkg (IBGE 2019, pelo geobr/Ipea)
#   https://raw.githubusercontent.com/codeforgermany/click_that_hood/main/public/data/brazil-states.geojson (como br-estados.geojson)
# e /tmp/v/bin/python biomas.py. Sai o biomas.svg (para o guia-pt.py) e o estados-cerrado.json.
# Mapa dos biomas do Brasil (IBGE 2019, via geobr/Ipea) com o Cerrado em destaque, e quanto de cada estado é Cerrado.
import sqlite3, json, math, pathlib
from shapely import wkb
from shapely.geometry import shape, mapping
from shapely.ops import transform  # noqa: avisa que vai mudar de nome, mas funciona
AQUI = pathlib.Path(__file__).resolve().parent
db = sqlite3.connect(AQUI / 'biomes_2019_simplified.gpkg')
biomas = {}
for nome, g in db.execute("select name_biome, geom from biomes_2019_simplified"):
    env = {0:0,1:32,2:48,3:48,4:64}[(g[3] >> 1) & 7]
    biomas[nome] = wkb.loads(bytes(g[8+env:]))
estados = {f['properties']['sigla']: shape(f['geometry']).buffer(0) for f in json.load(open(AQUI / 'br-estados.geojson'))['features']}

# área: projeção sinusoidal (de áreas iguais), em km²
R = 6371.0
sin = lambda x, y, z=None: (math.radians(x) * R * math.cos(math.radians(y)), math.radians(y) * R)
area = lambda g: transform(sin, g).area
cer = biomas['Cerrado']
print('Cerrado km²:', round(area(cer)))
fatia = {}
for s, g in estados.items():
    a = area(g); c = area(g.intersection(cer))
    if c / a > 0.005: fatia[s] = (round(c), round(100 * c / a))
print(sorted(fatia.items(), key=lambda kv: -kv[1][0]))
json.dump(fatia, open(AQUI / 'estados-cerrado.json', 'w'))

# desenho: equirretangular com correção do cosseno da latitude do meio do Brasil
LON0, LAT1 = -74.5, 5.6
K = 9.0; C = math.cos(math.radians(-14))
xy = lambda x, y, z=None: ((x - LON0) * K * C, (LAT1 - y) * K)
def caminho(g, tol):
    g = transform(xy, g).simplify(tol, preserve_topology=True)
    polis = g.geoms if g.geom_type == 'MultiPolygon' else [g]
    out = []
    for p in polis:
        for anel in [p.exterior, *p.interiors]:
            pts = list(anel.coords)
            if len(pts) < 4: continue
            out.append('M' + 'L'.join(f'{x:.0f} {y:.0f}' for x, y in pts[:-1]) + 'Z')
    return ''.join(out)
ORDEM = ['Amazônia', 'Caatinga', 'Mata Atlântica', 'Pampa', 'Pantanal', 'Cerrado']
IDS = {'Amazônia': 'amazonia', 'Caatinga': 'caatinga', 'Mata Atlântica': 'mata-atlantica', 'Pampa': 'pampa', 'Pantanal': 'pantanal', 'Cerrado': 'cerrado'}
partes = [f'<path class="bioma bioma-{IDS[n]}" data-bioma="{IDS[n]}" d="{caminho(biomas[n], 1.2)}"/>' for n in ORDEM]
contorno_estados = ''.join(caminho(g, 1.5) for g in estados.values())
x1, y1 = xy(-34.5, -34.0)
svg = (f'<svg class="mapa-biomas" viewBox="0 0 {x1:.0f} {y1:.0f}" role="img" aria-labelledby="biomas-titulo">'
       f'<title id="biomas-titulo">Mapa dos biomas do Brasil: o Cerrado ocupa o centro do país, entre a Amazônia, a Caatinga, a Mata Atlântica e o Pantanal</title>'
       + ''.join(partes) + f'<path class="estados" d="{contorno_estados}"/></svg>')
open(AQUI / 'biomas.svg', 'w').write(svg)
print(f'{x1:.0f}x{y1:.0f}', len(svg) // 1024, 'KB')
