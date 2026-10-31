# Rodar: baixar o br-estados.geojson (link abaixo) para esta pasta e python3 mapa.py; o SVG sai em mapa.svg, para colar no
# modelo/expedicoes.html no lugar do <svg class="mapa">. Fonte: https://raw.githubusercontent.com/codeforgermany/click_that_hood/main/public/data/brazil-states.geojson
# Gera o SVG do mapa "Onde ficam os parques" (Guia do Cerrado, 31/10/2026).
# Contorno dos estados: IBGE, via Code for America (click_that_hood, licença MIT).
import json, math, pathlib
d = json.load(open(pathlib.Path(__file__).resolve().parent / 'br-estados.geojson'))
LON0, LON1, LAT0, LAT1 = -56.5, -43.5, -20.5, -10.5   # o recorte do Centro-Oeste
K = 46                                                 # px por grau de latitude
C = math.cos(math.radians(-15.5))
def xy(lon, lat): return ((lon - LON0) * K * C, (LAT1 - lat) * K)
W, H = xy(LON1, LAT0)

def rdp(pts, eps):
    if len(pts) < 3: return pts
    a, b = pts[0], pts[-1]; dmax, idx = 0, 0
    for i in range(1, len(pts) - 1):
        p = pts[i]
        num = abs((b[1]-a[1])*p[0] - (b[0]-a[0])*p[1] + b[0]*a[1] - b[1]*a[0]); den = math.hypot(b[0]-a[0], b[1]-a[1]) or 1
        if num / den > dmax: dmax, idx = num / den, i
    if dmax > eps: return rdp(pts[:idx+1], eps)[:-1] + rdp(pts[idx:], eps)
    return [a, b]

def caminho(geom, proj, eps, caixa=None):
    polis = geom['coordinates'] if geom['type'] == 'MultiPolygon' else [geom['coordinates']]
    partes = []
    for poli in polis:
        for anel in poli:
            if caixa:
                lons = [p[0] for p in anel]; lats = [p[1] for p in anel]
                if max(lons) < caixa[0] or min(lons) > caixa[1] or max(lats) < caixa[2] or min(lats) > caixa[3]: continue
            todos = [proj(*p) for p in anel]
            meio = len(todos) // 2   # anel fechado: começo e fim iguais; simplifica em duas metades
            pts = rdp(todos[:meio + 1], eps)[:-1] + rdp(todos[meio:], eps)
            if len(pts) < 3: continue
            partes.append('M' + 'L'.join(f'{x:.0f} {y:.0f}' for x, y in pts) + 'Z')
    return ''.join(partes)

estados = []
for f in d['features']:
    sig = f['properties']['sigla']
    c = caminho(f['geometry'], xy, 1.2, (LON0 - .5, LON1 + .5, LAT0 - .5, LAT1 + .5))
    if c: estados.append((sig, c))

# o Brasil pequeno, para localizar o recorte
k2 = 3.2; c2 = math.cos(math.radians(-15))
def xy2(lon, lat): return ((lon + 74) * k2 * c2, (6 - lat) * k2)
brasil = ''.join(caminho(f['geometry'], xy2, 1.6) for f in d['features'])
bx0, by0 = xy2(LON0, LAT1); bx1, by1 = xy2(LON1, LAT0)
bw, bh = xy2(-34.5, -34)

ROTULOS = {'GO': (-50.3, -16.4), 'DF': (-47.75, -15.95), 'MT': (-54.8, -13.0), 'MS': (-54.6, -19.9), 'MG': (-45.6, -17.8), 'TO': (-48.6, -11.3), 'BA': (-44.6, -12.4)}
PARQUES = [('veadeiros', 'Chapada dos Veadeiros', -47.68, -14.05, 'esquerda'), ('brasilia', 'Parque Nacional de Brasília', -48.0, -15.65, 'esquerda'),
           ('emas', 'Parque Nacional das Emas', -52.88, -18.15, 'direita')]

def svg_estados():
    out = []
    for sig, c in estados:
        cls = 'estado destaque' if sig in ('GO', 'DF') else 'estado'
        out.append(f'<path class="{cls}" d="{c}"/>')
    for sig, (lon, lat) in ROTULOS.items():
        x, y = xy(lon, lat)
        out.append(f'<text class="sigla{" sigla-df" if sig == "DF" else ""}" x="{x:.0f}" y="{y:.0f}" text-anchor="middle">{sig}</text>')
    for id_, nome, lon, lat, lado in PARQUES:
        x, y = xy(lon, lat)
        tx, anchor = (x + 15, 'start') if lado == 'direita' else (x - 15, 'end')
        out.append(f'<a href="#{id_}" class="parque" aria-label="{nome}: ver a expedição"><circle cx="{x:.1f}" cy="{y:.1f}" r="22" class="alvo"/>'
                   f'<circle cx="{x:.1f}" cy="{y:.1f}" r="7" class="ponto"/><text x="{tx:.1f}" y="{y + 6:.1f}" text-anchor="{anchor}">{nome}</text></a>')
    return ''.join(out)

mini = (f'<g class="mini" transform="translate({W - bw * 0.62 - 8:.0f} {H - bh * 0.62 - 8:.0f}) scale(.62)">'
        f'<rect class="mini-fundo" x="-6" y="-6" width="{bw + 12:.0f}" height="{bh + 12:.0f}" rx="8"/>'
        f'<path class="mini-brasil" d="{brasil}"/><rect class="mini-recorte" x="{bx0:.1f}" y="{by0:.1f}" width="{bx1 - bx0:.1f}" height="{by1 - by0:.1f}"/></g>')
svg = (f'<svg class="mapa" viewBox="0 0 {W:.0f} {H:.0f}" role="group" aria-labelledby="mapa-titulo">'
       f'<title id="mapa-titulo">Mapa do Centro-Oeste com os três parques: a Chapada dos Veadeiros e o Parque Nacional das Emas, em Goiás, e o Parque Nacional de Brasília, no Distrito Federal</title>'
       f'{svg_estados()}{mini}</svg>')
open(pathlib.Path(__file__).resolve().parent / 'mapa.svg', 'w').write(svg)
print(f'{W:.0f}x{H:.0f}', len(svg) // 1024, 'KB', [s for s, _ in estados])
