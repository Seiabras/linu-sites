# O guia do cerrado, em português (31/10/2026). Rodar depois do paginas-pt.py e antes do gerar-estudo.mjs:
#   python3 ferramentas/estudo/fotografia-do-cerrado/paginas-pt.py
#   python3 ferramentas/estudo/fotografia-do-cerrado/guia-pt.py
#   node ferramentas/gerar-estudo.mjs fotografia-do-cerrado
#
# - Troca, só na página em português, o menu de todas as páginas pelo do guia e a inicial pela do guia (as outras línguas
#   continuam como estavam, até a tradução: {{!pt-BR}} … {{/!pt-BR}} no modelo);
# - escreve as páginas novas do guia (bioma.html, paisagens.html e fontes.html), só em português;
# - marca no menu a página atual de cada uma.
# O mapa dos biomas sai do biomas.py (mesma pasta); os números de cada estado estão em estados-cerrado.json.
import json, unicodedata, pathlib, re

AQUI = pathlib.Path(__file__).resolve().parent
M = AQUI / 'modelo'
COMPARTILHADAS = ['index.html', 'galeria.html', 'expedicoes.html', 'sobre.html', 'contato.html', 'creditos.html']

# ---------------------------------------------------------------- menu e rodapé do guia (só em português)
MENU = [('index.html', 'Início'), ('bioma.html', 'O bioma'), ('paisagens.html', 'Paisagens'), ('galeria.html', 'Espécies'),
        ('expedicoes.html', 'Expedições'), ('sobre.html', 'Sobre')]
ATUAL = {'especie-': 'galeria.html'}  # as fichas ficam dentro de Espécies

def menu_pt(arquivo):
    atual = next((v for k, v in ATUAL.items() if arquivo.startswith(k)), arquivo)
    itens = ''.join(f'<li><a href="{h}"{" aria-current=\"page\"" if h == atual else ""}>{t}</a></li>' for h, t in MENU)
    return f'<ul class="menu" id="menu">{itens}</ul>'

RODAPE_PT = ' · <a href="diario.html">Diário de campo</a> · <a href="como-fotografamos.html">Como fotografamos</a> · <a href="contato.html">Contato</a> · <a href="fontes.html">Fontes</a>'

def com_menu_do_guia(s, arquivo):
    """Põe o menu do guia na página em português; nas outras línguas fica o de antes."""
    s = s.replace('{{?pt-BR}}<li><a href="diario.html">Diário</a></li>{{/pt-BR}}', '')
    s = s.replace('{{?pt-BR}}<li><a href="diario.html" aria-current="page">Diário</a></li>{{/pt-BR}}', '')
    m = re.search(r'(\{\{!pt-BR\}\})?<ul class="menu" id="menu">.*?</ul>(\{\{/!pt-BR\}\}\{\{\?pt-BR\}\}<ul class="menu" id="menu">.*?</ul>\{\{/pt-BR\}\})?', s)
    antigo = re.search(r'<ul class="menu" id="menu">.*?</ul>', m.group(0)).group(0)
    return s[:m.start()] + '{{!pt-BR}}' + antigo + '{{/!pt-BR}}{{?pt-BR}}' + menu_pt(arquivo) + '{{/pt-BR}}' + s[m.end():]

def com_rodape_do_guia(s):
    s = re.sub(r'\{\{\?pt-BR\}\} · <a href="como-fotografamos\.html">Como fotografamos</a>.*?\{\{/pt-BR\}\}', '{{?pt-BR}}' + RODAPE_PT + '{{/pt-BR}}', s)
    return s

for f in COMPARTILHADAS:
    p = M / f
    s = com_rodape_do_guia(com_menu_do_guia(p.read_text(), f))
    p.write_text(s)

# ---------------------------------------------------------------- o molde das páginas novas (cabeça e rodapé da galeria)
galeria = (M / 'galeria.html').read_text()
cabeca, resto = galeria.split('    <main id="conteudo">', 1)
rodape = resto.split('    </main>', 1)[1]
cabeca = re.sub(r'    <script src="\{\{raiz\}\}js/galeria\.js\?v=\d+" defer></script>\n', '', cabeca)
cabeca = re.sub(r'\{\{!pt-BR\}\}<ul class="menu".*?\{\{/!pt-BR\}\}', '', cabeca)
rodape = re.sub(r'\{\{!pt-BR\}\}.*?\{\{/!pt-BR\}\}', '', rodape, flags=re.S)

def pagina(arquivo, titulo, descricao, corpo, scripts=()):
    s = cabeca.replace('{{galeria_090}}', titulo).replace('{{galeria_103}}', descricao)
    s = re.sub(r'<ul class="menu" id="menu">.*?</ul>', menu_pt(arquivo), s)
    extra = ''.join(f'    <script src="{{{{raiz}}}}js/{n}" defer></script>\n' for n in scripts)
    s = s.replace('{{alternativas}}', extra + '{{alternativas}}')
    (M / arquivo).write_text(s + '    <main id="conteudo">\n' + corpo + '    </main>' + rodape)

def indice(itens):
    """O índice da página: fica parado ao lado no computador e vira uma faixa que rola de lado no celular."""
    li = ''.join(f'<li><a href="#{i}">{t}</a></li>' for i, t in itens)
    return f'<nav class="indice" aria-label="Nesta página"><p class="indice-titulo">Nesta página</p><ol>{li}</ol></nav>'

def fonte(n):
    return f'<sup class="nota"><a href="fontes.html#f{n}" aria-label="Fonte {n}">{n}</a></sup>'

# ---------------------------------------------------------------- as fontes (a página fontes.html e as notas)
FONTES = [
 (1, 'IBGE. Biomas e sistema costeiro-marinho do Brasil, compatível com a escala 1:250.000. 2019. Área do Cerrado, 1.983.017 km², nos metadados de “Limites dos Biomas” do INPE.', 'https://agenciadenoticias.ibge.gov.br/agencia-sala-de-imprensa/25798-ibge-lanca-mapa-inedito-de-biomas-e-sistema-costeiro-marinho'),
 (2, 'INPE. Limites dos Biomas (catálogo de dados, ajustado ao IBGE 2019).', 'https://data.inpe.br/geonetwork/srv/api/records/0d88678e-4cdb-44f3-9b1d-8edc00bc4122'),
 (3, 'Ipea. Pacote geobr, função read_biomes(2019): os limites do IBGE usados no mapa e nos números de cada estado.', 'https://github.com/ipeaGIT/geobr'),
 (4, 'Revista Pesquisa FAPESP. As chuvas do Cerrado (2023): média anual de 1.421 mm em 1960–1990, cerca de 5% a menos em 1991–2021, e cerca de 120 mm de junho a setembro.', 'https://revistapesquisa.fapesp.br/wp-content/uploads/2023/11/052-053_chuvas-cerrado_333novo.pdf'),
 (5, 'Embrapa. Avaliação, manejo e conservação de solos no Cerrado (1997): cerca de 90% dos solos muito ácidos e com alta saturação de alumínio.', 'https://www.alice.cnptia.embrapa.br/alice/bitstream/doc/1171496/1/Avaliacao-manejo-e-conservacao-de-solos-no-cerrado-1997.pdf'),
 (6, 'ICMBio. Colorindo o aprender: Cerrado. O fogo no Cerrado há mais de dez milhões de anos e as adaptações das plantas.', 'https://www.gov.br/icmbio/pt-br/centrais-de-conteudo/publicacoes/publicacoes-diversas/colorindo_o_aprender_cerrado.pdf'),
 (7, 'Agência FAPESP. Plantas do Cerrado combinam pelo menos duas estratégias para resistir ao fogo (estudo da Unesp na revista Flora).', 'https://agencia.fapesp.br/plantas-do-cerrado-combinam-pelo-menos-duas-estrategias-para-resistir-ao-fogo-revela-estudo/49925'),
 (8, 'Ribeiro, J. F.; Walter, B. M. T. As principais fitofisionomias do bioma Cerrado. In: Sano, S. M.; Almeida, S. P.; Ribeiro, J. F. (ed.). Cerrado: ecologia e flora. Brasília: Embrapa Informação Tecnológica, 2008. v. 1, cap. 6.', 'https://www.alice.cnptia.embrapa.br/alice/bitstream/doc/186922/1/CERRADO-Ecologia-e-flora-VOL-1-152-213.pdf'),
 (9, 'Embrapa Cerrados. Bioma Cerrado: cerradão, cerrado sentido restrito (denso, típico, ralo e rupestre) e as outras fitofisionomias.', 'https://www.embrapa.br/en/web/cerrados/colecao-entomologica/bioma-cerrado'),
 (10, 'Embrapa. Veredas (capítulo VI.3): os dois estratos da vereda e o buriti.', 'https://www.infoteca.cnptia.embrapa.br/infoteca/bitstream/doc/1176629/1/VI.3-Veredas.pdf'),
 (11, 'Ministério do Meio Ambiente. O Bioma Cerrado (página do antigo site do MMA): 11.627 espécies de plantas nativas catalogadas, número repetido por muitas fontes.', 'http://antigo.mma.gov.br/biomas/cerrado.html'),
 (12, 'Myers, N. et al. Biodiversity hotspots for conservation priorities. Nature, v. 403, p. 853–858, 2000. O Cerrado como um dos 25 hotspots do mundo, com cerca de 4.400 plantas endêmicas.', 'https://www.nature.com/articles/35002501'),
 (14, 'Governo de Goiás. Campos do Cerrado: mais de 13 mil espécies vegetais registradas no Cerrado, segundo a Flora do Brasil 2020.', 'https://goias.gov.br/camposdocerrado/?p=11'),
 (13, 'Jardim Botânico de Brasília. Flora do Cerrado: as fitofisionomias e as alturas das árvores.', 'https://www.jardimbotanico.df.gov.br/educacao-ambiental/flora-cerrado'),
]

# ---------------------------------------------------------------- O bioma
estados = json.loads((AQUI / 'estados-cerrado.json').read_text())
NOMES = {'GO': 'Goiás', 'DF': 'Distrito Federal', 'TO': 'Tocantins', 'MA': 'Maranhão', 'MS': 'Mato Grosso do Sul', 'MG': 'Minas Gerais',
         'PI': 'Piauí', 'MT': 'Mato Grosso', 'SP': 'São Paulo', 'BA': 'Bahia', 'PR': 'Paraná', 'PA': 'Pará', 'RO': 'Rondônia'}
linhas_estados = ''.join(
    f'<li><span class="estado-nome">{NOMES[s]}</span><span class="estado-pct">{pct}%</span>'
    f'<svg viewBox="0 0 100 10" preserveAspectRatio="none" aria-hidden="true"><rect class="estado-fundo" width="100" height="10"/><rect class="estado-barra" width="{pct}" height="10"/></svg></li>'
    for s, (km2, pct) in sorted(estados.items(), key=lambda kv: -kv[1][1]))
mapa_biomas = (AQUI / 'biomas.svg').read_text()
BIOMAS = [('cerrado', 'Cerrado', '23,3%'), ('amazonia', 'Amazônia', '49,5%'), ('mata-atlantica', 'Mata Atlântica', '13%'),
          ('caatinga', 'Caatinga', '10,1%'), ('pampa', 'Pampa', '2,3%'), ('pantanal', 'Pantanal', '1,8%')]
botoes_biomas = ''.join(f'<button type="button" data-bioma="{i}" aria-pressed="{"true" if i == "cerrado" else "false"}"><span class="cor-bioma cor-{i}" aria-hidden="true"></span>{n} <span class="bioma-pct">{p}</span></button>' for i, n, p in BIOMAS)

bioma = f'''        <section class="titulo-pagina guia-topo">
            <div class="container">
                <p class="guia-chapeu">Guia do cerrado</p>
                <h1>O bioma</h1>
                <p>A savana mais rica do mundo ocupa o meio do Brasil. Aqui está onde ela fica, como é o clima, por que o solo é do jeito que é e o que o fogo tem a ver com tudo isso.</p>
            </div>
        </section>
        <div class="container guia-layout">
            {indice([('onde', 'Onde fica'), ('estados', 'Estado por estado'), ('clima', 'Clima'), ('solo', 'Solo'), ('fogo', 'Fogo'), ('vida', 'Biodiversidade')])}
            <div class="guia-texto">
                <section id="onde" aria-labelledby="onde-titulo">
                    <h2 id="onde-titulo">Onde fica</h2>
                    <p>O Cerrado é o segundo maior bioma do Brasil, depois da Amazônia: são 1.983.017 km², cerca de 23,3% do país.{fonte(1)}{fonte(2)} É o único bioma que aparece em todas as regiões brasileiras, do Maranhão ao Paraná.{fonte(1)}</p>
                    <figure class="biomas-figura">
                        <div class="biomas-botoes" role="group" aria-label="Destacar um bioma no mapa">{botoes_biomas}</div>
                        {mapa_biomas}
                        <figcaption><span class="bioma-legenda" aria-live="polite">Cerrado: 23,3% do Brasil.</span> Limites dos biomas do IBGE, 2019.{fonte(1)}{fonte(3)}</figcaption>
                    </figure>
                </section>
                <section id="estados" aria-labelledby="estados-titulo">
                    <h2 id="estados-titulo">Estado por estado</h2>
                    <p>Quanto do território de cada estado é Cerrado. Goiás e o Distrito Federal são quase inteiros; em Mato Grosso, o Cerrado divide espaço com a Amazônia e o Pantanal.</p>
                    <ul class="estados-lista">{linhas_estados}</ul>
                    <p class="nota-calculo">Calculado aqui no guia, cruzando os limites do bioma (IBGE, 2019) com o contorno dos estados, numa projeção de áreas iguais. São aproximações: o total deu 1.991.688 km², 0,4% acima do número oficial.{fonte(3)}</p>
                </section>
                <section id="clima" aria-labelledby="clima-titulo">
                    <h2 id="clima-titulo">Clima: duas estações</h2>
                    <p>O ano no Cerrado se divide em dois. De outubro a abril chove, e muito; de maio a setembro quase não chove. Entre junho e setembro, o bioma inteiro recebe em média só uns 120 mm, menos do que um único mês de chuva.{fonte(4)}</p>
                    <div class="estacoes" role="img" aria-label="O ano em duas estações: chuvas de outubro a abril, seca de maio a setembro">
                        <span class="estacao-faixa chuva">Out</span><span class="estacao-faixa chuva">Nov</span><span class="estacao-faixa chuva">Dez</span><span class="estacao-faixa chuva">Jan</span><span class="estacao-faixa chuva">Fev</span><span class="estacao-faixa chuva">Mar</span><span class="estacao-faixa chuva">Abr</span><span class="estacao-faixa seca">Mai</span><span class="estacao-faixa seca">Jun</span><span class="estacao-faixa seca">Jul</span><span class="estacao-faixa seca">Ago</span><span class="estacao-faixa seca">Set</span>
                    </div>
                    <p class="estacoes-legenda"><span class="chave chuva" aria-hidden="true"></span> chuvas <span class="chave seca" aria-hidden="true"></span> seca</p>
                    <dl class="numeros-guia">
                        <div><dt>1.421 mm</dt><dd>de chuva por ano, na média de 1960 a 1990{fonte(4)}</dd></div>
                        <div><dt>cerca de 5%</dt><dd>menos chuva por ano entre 1991 e 2021{fonte(4)}</dd></div>
                        <div><dt>~120 mm</dt><dd>somando junho, julho, agosto e setembro{fonte(4)}</dd></div>
                    </dl>
                    <p>Na seca, o capim fica dourado, muitas árvores perdem parte das folhas e a umidade do ar cai muito à tarde. Na chuva, tudo rebrota em poucas semanas. Quase tudo o que vive aqui tem um jeito de atravessar os meses secos.</p>
                </section>
                <section id="solo" aria-labelledby="solo-titulo">
                    <h2 id="solo-titulo">Solo: velho, fundo e ácido</h2>
                    <p>Os solos do Cerrado são antigos, profundos e bem drenados, mas pobres em nutrientes. Cerca de 90% deles são muito ácidos e têm muito alumínio, que é tóxico para a maioria das plantas cultivadas.{fonte(5)}</p>
                    <p>As plantas nativas convivem com isso. Muitas árvores mandam raízes a vários metros de profundidade, até a água que fica guardada embaixo mesmo no auge da seca. Por isso tanta árvore do Cerrado continua verde quando o capim em volta já secou: a parte que a gente não vê é maior do que a que aparece.</p>
                </section>
                <section id="fogo" aria-labelledby="fogo-titulo">
                    <h2 id="fogo-titulo">Fogo: parte da história</h2>
                    <p>O fogo faz parte do Cerrado há mais de dez milhões de anos, e muitas espécies estão adaptadas a ele.{fonte(6)} As principais estratégias:</p>
                    <ul class="adaptacoes">
                        <li><strong>Casca grossa.</strong> A cortiça do tronco funciona como isolante e protege os tecidos vivos do calor.{fonte(6)}</li>
                        <li><strong>Partes embaixo da terra.</strong> Raízes grossas, xilopódios e rizomas guardam gemas que rebrotam depois que a parte de cima queima.{fonte(7)}</li>
                        <li><strong>As duas coisas juntas.</strong> Um estudo da Unesp mostrou que muitas árvores do Cerrado investem ao mesmo tempo em casca e em órgãos subterrâneos, e por isso aguentam queimadas de intensidades diferentes.{fonte(7)}</li>
                    </ul>
                    <p class="aviso-guia">Adaptado ao fogo não quer dizer que qualquer fogo faz bem. As queimadas muito fortes, no auge da seca, matam até árvores de casca grossa.{fonte(6)} O fogo natural é uma coisa; a queimada fora de hora, outra.</p>
                </section>
                <section id="vida" aria-labelledby="vida-titulo">
                    <h2 id="vida-titulo">Biodiversidade</h2>
                    <p>O Cerrado é considerado a savana mais rica do mundo. São mais de 11 mil espécies de plantas nativas: o Ministério do Meio Ambiente fala em 11.627 catalogadas,{fonte(11)} e a Flora do Brasil 2020, que segue somando registros, passa de 13 mil.{fonte(14)} Cerca de 4.400 delas só existem aqui.{fonte(12)}</p>
                    <p>Em 2000, um estudo publicado na Nature pôs o Cerrado entre os 25 “hotspots” do planeta: lugares com muitas espécies que só existem neles e que já perderam boa parte da vegetação original.{fonte(12)}</p>
                    <p class="mais"><a class="botao" href="paisagens.html">Conheça as 11 paisagens do Cerrado</a></p>
                </section>
            </div>
        </div>
'''
pagina('bioma.html', 'O bioma Cerrado: onde fica, clima, solo e fogo — Guia do Cerrado',
       'O Cerrado ocupa 23,3% do Brasil: onde fica, quanto de cada estado é Cerrado, as duas estações, o solo ácido e as adaptações ao fogo, com fontes.',
       bioma, scripts=['guia.js?v=1'])

# ---------------------------------------------------------------- Paisagens: as 11 fitofisionomias e o corte desenhado
P = [
 dict(id='campo-limpo', nome='Campo limpo', formacao='Campestre', cobertura='quase nenhuma árvore', altura='capim e ervas',
      texto='Um mar de capim e ervas, com raríssimos arbustos e nenhuma árvore. Aparece nas encostas, nas chapadas e em volta das veredas e das nascentes.',
      reconhecer='Dá para ver o horizonte em todas as direções. Na seca, fica dourado; logo depois das primeiras chuvas, verde.', f=[8]),
 dict(id='campo-sujo', nome='Campo sujo', formacao='Campestre', cobertura='arbustos espalhados', altura='arbustos baixos',
      texto='Capim com arbustos e subarbustos espaçados no meio, como se o campo limpo tivesse sido salpicado. Costuma estar em solos rasos ou muito pobres.',
      reconhecer='O capim domina, mas a cada poucos passos tem um arbusto. Nada passa muito da altura de uma pessoa.', f=[8]),
 dict(id='campo-rupestre', nome='Campo rupestre', formacao='Campestre', cobertura='capim e arbustos entre as pedras', altura='em geral acima de 900 m de altitude',
      texto='Vegetação de capim e arbustos crescendo entre afloramentos de rocha, nas serras e chapadas mais altas. Muitas plantas daqui só existem nessas pedras, como várias canelas-de-ema e sempre-vivas.',
      reconhecer='Pedras à mostra por todo lado, ventos fortes e plantas pequenas, de folhas duras. Comum na Chapada dos Veadeiros e na Serra do Espinhaço.', f=[8]),
 dict(id='parque-de-cerrado', nome='Parque de cerrado', formacao='Savânica', cobertura='árvores em ilhas', altura='árvores do cerrado em montinhos',
      texto='As árvores crescem agrupadas em pequenas elevações do terreno, os murundus, e entre elas fica um campo que encharca na época de chuva.',
      reconhecer='Visto de longe, parece um campo cheio de ilhas redondas de árvores, todas mais ou menos do mesmo tamanho.', f=[8]),
 dict(id='cerrado-sentido-restrito', nome='Cerrado sentido restrito', formacao='Savânica', cobertura='de 5% a 70%', altura='de 2 a 8 m, conforme o tipo',
      texto='O “cerrado” que a maioria das pessoas imagina: árvores baixas, tortas, de casca grossa, no meio de capim e arbustos. Conforme a densidade, tem quatro tipos: o denso (50% a 70% de cobertura, árvores de 5 a 8 m), o típico (20% a 50%, de 3 a 6 m), o ralo (5% a 20%, de 2 a 3 m) e o rupestre, sobre as rochas.',
      reconhecer='Troncos retorcidos, galhos tortos, marcas de queimadas antigas e muitas árvores com casca de cortiça. Pequizeiro, lobeira e pau-terra são comuns.', f=[8, 9, 13]),
 dict(id='palmeiral', nome='Palmeiral', formacao='Savânica', cobertura='uma palmeira domina', altura='altura da palmeira',
      texto='Uma única espécie de palmeira domina a paisagem: babaçu, macaúba, guariroba ou buriti, conforme o lugar e a umidade do solo.',
      reconhecer='Muitas palmeiras iguais, quase sem outras árvores entre elas.', f=[8]),
 dict(id='vereda', nome='Vereda', formacao='Savânica', cobertura='buritis no meio do campo úmido', altura='buritis altos sobre capim',
      texto='Uma faixa de campo encharcado, com os buritis alinhados no meio, onde a água do subsolo aflora. As veredas protegem nascentes e são o caminho de muita água que vai formar os rios.',
      reconhecer='Dois andares: embaixo, o capim úmido, que cobre quase tudo; em cima, os buritis. Onde tem vereda, tem água.', f=[8, 10]),
 dict(id='cerradao', nome='Cerradão', formacao='Florestal', cobertura='de 50% a 90%', altura='de 8 a 15 m',
      texto='Uma floresta de árvores do cerrado: as copas se tocam e formam um teto quase contínuo, mais fechado na chuva e mais aberto na seca. Mistura espécies do cerrado com espécies de mata.',
      reconhecer='Por fora parece mata; por dentro, os troncos ainda têm o jeito torto e a casca grossa do cerrado.', f=[9, 13]),
 dict(id='mata-seca', nome='Mata seca', formacao='Florestal', cobertura='copa contínua', altura='as maiores árvores chegam perto de 25 m',
      texto='Floresta que não depende de rio, em solos mais férteis, muitas vezes sobre calcário. Conforme o lugar, pode ficar sempre verde, perder parte das folhas ou perder quase todas na seca.',
      reconhecer='Na seca, um bosque cinzento de troncos sem folhas; na chuva, uma mata verde e fechada.', f=[8]),
 dict(id='mata-de-galeria', nome='Mata de galeria', formacao='Florestal', cobertura='as copas fecham sobre o riacho', altura='floresta alta',
      texto='Floresta que acompanha os córregos e riachos pequenos. As copas das duas margens se encontram por cima da água e formam um corredor fechado, a galeria. Fica verde o ano inteiro.',
      reconhecer='Uma faixa escura de mata seguindo o fundo do vale, no meio do cerrado aberto. Dentro, sombra e ar úmido.', f=[8]),
 dict(id='mata-ciliar', nome='Mata ciliar', formacao='Florestal', cobertura='as copas não cobrem o rio', altura='floresta alta',
      texto='Floresta das margens dos rios médios e grandes. Ao contrário da mata de galeria, as copas das duas margens não se encontram: o rio é largo demais. Parte das árvores perde folhas na seca.',
      reconhecer='Duas fileiras de mata, uma em cada margem, com o rio aberto entre elas.', f=[8]),
]

def tufo(x, y, r, cls='copa'):
    # uma copa em três volumes, mais larga do que alta, como as árvores de verdade
    return (f'<ellipse class="{cls}" cx="{x - r * .55:.0f}" cy="{y + r * .25:.0f}" rx="{r * .7:.0f}" ry="{r * .5:.0f}"/>'
            f'<ellipse class="{cls}" cx="{x + r * .55:.0f}" cy="{y + r * .25:.0f}" rx="{r * .7:.0f}" ry="{r * .5:.0f}"/>'
            f'<ellipse class="{cls}" cx="{x}" cy="{y - r * .15:.0f}" rx="{r * .8:.0f}" ry="{r * .6:.0f}"/>')
def arvore(x, chao, h, r, cls='copa'):
    if cls == 'copa seca':
        # sem folhas na seca: só os galhos
        y = chao - h + r * .6
        galhos = f'<path class="tronco fino" d="M{x} {y:.0f} l {-r * .8:.0f} {-r * .7:.0f} M{x} {y:.0f} l {r * .8:.0f} {-r * .7:.0f} M{x} {y:.0f} l {r * .1:.0f} {-r:.0f} M{x - r * .45:.0f} {y - r * .4:.0f} l {-r * .3:.0f} {-r * .5:.0f} M{x + r * .45:.0f} {y - r * .4:.0f} l {r * .35:.0f} {-r * .45:.0f}"/>'
        return f'<line class="tronco" x1="{x}" y1="{chao}" x2="{x}" y2="{y:.0f}"/>{galhos}'
    return f'<line class="tronco" x1="{x}" y1="{chao}" x2="{x}" y2="{chao - h + r * .3:.0f}"/>' + tufo(x, chao - h, r, cls)
def torta(x, chao, h, r):
    return f'<path class="tronco" d="M{x} {chao} q {r * .6:.0f} {-h * .45:.0f} {-r * .3:.0f} {-h + r * .3:.0f}"/>' + tufo(x - r * .3, chao - h, r)
def palmeira(x, chao, h):
    folhas = ''.join(f'<path class="folha" d="M{x} {chao - h} q {dx * .5:.0f} -10 {dx} {dy}"/>' for dx, dy in [(-18, 6), (-12, -8), (0, -12), (12, -8), (18, 6)])
    return f'<line class="tronco" x1="{x}" y1="{chao}" x2="{x}" y2="{chao - h}"/>{folhas}'
def capim(x0, x1, chao):
    return ''.join(f'<path class="capim" d="M{x} {chao} l -2 -7 M{x} {chao} l 0 -9 M{x} {chao} l 2 -7"/>' for x in range(x0 + 4, x1 - 2, 8))
def arbusto(x, chao, r=6):
    return f'<ellipse class="arbusto" cx="{x}" cy="{chao - r * .6:.1f}" rx="{r}" ry="{r * .7:.1f}"/>'

W, CHAO = 100, 210
def desenho(i, p):
    x0 = i * W; x1 = x0 + W; c = CHAO; m = 8  # 1 m = 8 unidades
    d = ''
    if p['id'] == 'campo-limpo': d += capim(x0, x1, c)
    elif p['id'] == 'campo-sujo': d += capim(x0, x1, c) + arbusto(x0 + 22, c) + arbusto(x0 + 55, c, 7) + arbusto(x0 + 80, c, 5)
    elif p['id'] == 'campo-rupestre':
        d += f'<path class="rocha" d="M{x0 + 6} {c} l 10 -18 l 16 -4 l 8 22 Z M{x0 + 52} {c} l 6 -26 l 18 -6 l 12 32 Z"/>' + capim(x0 + 36, x0 + 54, c) + arbusto(x0 + 44, c, 5) + arbusto(x0 + 92, c, 4)
    elif p['id'] == 'parque-de-cerrado':
        d += capim(x0, x1, c) + f'<ellipse class="murundu" cx="{x0 + 28}" cy="{c}" rx="22" ry="9"/><ellipse class="murundu" cx="{x0 + 74}" cy="{c}" rx="20" ry="8"/>'
        d += torta(x0 + 22, c - 6, 4 * m, 9) + torta(x0 + 34, c - 6, 3 * m, 8) + torta(x0 + 74, c - 5, 4 * m, 9)
    elif p['id'] == 'cerrado-sentido-restrito':
        d += capim(x0, x1, c) + torta(x0 + 16, c, 4 * m, 10) + torta(x0 + 44, c, 6 * m, 12) + arbusto(x0 + 62, c) + torta(x0 + 82, c, 3 * m, 9)
    elif p['id'] == 'palmeiral':
        d += capim(x0, x1, c) + ''.join(palmeira(x0 + dx, c, h * m) for dx, h in [(16, 8), (40, 10), (64, 9), (88, 8)])
    elif p['id'] == 'vereda':
        d += f'<path class="agua" d="M{x0} {c} h {W} v 6 h -{W} Z"/>' + capim(x0, x1, c) + palmeira(x0 + 30, c, 15 * m) + palmeira(x0 + 70, c, 13 * m)
    elif p['id'] == 'cerradao':
        d += ''.join(torta(x0 + dx, c, h * m, 16) for dx, h in [(14, 11), (38, 13), (60, 12), (84, 14)])
    elif p['id'] == 'mata-seca':
        d += arvore(x0 + 16, c, 17 * m, 16, 'copa seca') + arvore(x0 + 44, c, 21 * m, 20) + arvore(x0 + 72, c, 16 * m, 16, 'copa seca') + arvore(x0 + 92, c, 12 * m, 12)
    elif p['id'] == 'mata-de-galeria':
        # as copas das duas margens se encontram por cima do riacho
        d += f'<path class="agua" d="M{x0 + 42} {c} h 16 v 6 h -16 Z"/>' + arvore(x0 + 12, c, 14 * m, 16) + arvore(x0 + 34, c, 17 * m, 22) + arvore(x0 + 66, c, 17 * m, 22) + arvore(x0 + 90, c, 13 * m, 14)
    elif p['id'] == 'mata-ciliar':
        # o rio é largo: as copas das margens não se tocam
        d += f'<path class="agua" d="M{x0 + 30} {c} h 42 v 6 h -42 Z"/>' + arvore(x0 + 10, c, 18 * m, 12) + arvore(x0 + 22, c, 20 * m, 11) + arvore(x0 + 80, c, 19 * m, 11) + arvore(x0 + 93, c, 17 * m, 10)
    nome = p['nome'].replace('Cerrado sentido restrito', 'Cerrado s. restrito')
    return (f'<g class="trecho" data-tipo="{p["id"]}"><rect class="trecho-fundo" x="{x0}" y="0" width="{W}" height="250"/>{d}'
            f'<line class="chao" x1="{x0}" y1="{c}" x2="{x1}" y2="{c}"/><text x="{x0 + W / 2}" y="{c + 30}" text-anchor="middle">{nome}</text></g>')

grupos = [(0, 3, 'Campestres'), (3, 7, 'Savânicas'), (7, 11, 'Florestais')]
faixas = ''.join(f'<text class="grupo" x="{a * W + 6}" y="18">{n}</text><line class="divisa" x1="{b * W}" y1="0" x2="{b * W}" y2="250"/>' for a, b, n in grupos[:3])
corte = (f'<svg class="corte" viewBox="0 0 {W * len(P)} 250" aria-hidden="true" focusable="false">{faixas}'
         + ''.join(desenho(i, p) for i, p in enumerate(P)) + '</svg>')
botoes = ''.join(f'<button type="button" class="tipo" data-tipo="{p["id"]}" aria-controls="tipo-{p["id"]}" aria-pressed="false"><span class="tipo-formacao">{p["formacao"]}</span> {p["nome"]}</button>' for p in P)
SITIO_P = AQUI.parents[2] / 'sitios' / 'fotografia-do-cerrado' / 'img' / 'paisagens'
CRED_P = {c['arquivo']: c for c in json.loads((SITIO_P / 'creditos.json').read_text())}
def foto_paisagem(p):
    # uma foto salva em img/paisagens/<id>.webp e <id>-640.webp entra sozinha na ficha (NO-COMPUTADOR.md, 9.1)
    if not (SITIO_P / f"{p['id']}-640.webp").exists(): return ''
    c = CRED_P.get(f"{p['id']}.webp")
    leg = f'<figcaption>{p["nome"]}. Foto: {c["autor"]}, {c["licenca"]}.</figcaption>' if c else ''
    return (f'<figure class="paisagem-foto"><img src="{{{{raiz}}}}img/paisagens/{p["id"]}-640.webp" srcset="{{{{raiz}}}}img/paisagens/{p["id"]}-640.webp 640w, '
            f'{{{{raiz}}}}img/paisagens/{p["id"]}.webp 1000w" sizes="(max-width: 900px) 100vw, 50vw" alt="{c["alt"] if c else p["nome"]}" width="1000" height="667" loading="lazy">{leg}</figure>')
fichas = ''.join(f'''
                    <article class="paisagem" id="tipo-{p['id']}" data-tipo="{p['id']}">
                        {foto_paisagem(p)}
                        <p class="tipo-formacao">Formação {p['formacao'].lower()}</p>
                        <h2>{p['nome']}</h2>
                        <p>{p['texto']}{''.join(fonte(n) for n in p['f'])}</p>
                        <dl class="paisagem-dados"><dt>Cobertura</dt><dd>{p['cobertura']}</dd><dt>Altura</dt><dd>{p['altura']}</dd></dl>
                        <p class="paisagem-reconhecer"><strong>Como reconhecer:</strong> {p['reconhecer']}</p>
                        <p class="mais"><a href="especies.html?paisagem={p['id']}">Espécies desta paisagem →</a></p>
                    </article>''' for p in P)
paisagens = f'''        <section class="titulo-pagina guia-topo">
            <div class="container">
                <p class="guia-chapeu">Guia do cerrado</p>
                <h1>As 11 paisagens do Cerrado</h1>
                <p>“Cerrado” não é um tipo só de vegetação. Do campo sem nenhuma árvore à floresta alta na beira do rio, os botânicos José Felipe Ribeiro e Bruno Walter, da Embrapa, descrevem onze paisagens, em três grupos.{fonte(8)}</p>
            </div>
        </section>
        <section class="secao paisagens-secao">
            <div class="container">
                <figure class="corte-figura">
                    <section class="corte-rolagem" tabindex="0" aria-label="Corte desenhado das onze paisagens, do campo à mata; role de lado no celular">{corte}</section>
                    <figcaption>Do campo à mata: um corte desenhado, sem escala exata entre os trechos. Toque num trecho, ou escolha abaixo, para ler sobre ele.</figcaption>
                </figure>
                <div class="paisagens-layout">
                    <div class="tipos" role="group" aria-label="Escolha uma paisagem">{botoes}</div>
                    <div class="paisagens-fichas">{fichas}
                    </div>
                </div>
            </div>
        </section>
'''
pagina('paisagens.html', 'As 11 paisagens do Cerrado — Guia do Cerrado',
       'As onze fitofisionomias do Cerrado, de Ribeiro e Walter: campos, savanas e florestas, num corte desenhado para explorar, com fontes.',
       paisagens, scripts=['guia.js?v=1'])

# ---------------------------------------------------------------- Fontes
FONTES.sort()
lista = ''.join(f'<li id="f{n}"><span class="fonte-numero">{n}</span> {t} <a href="{u}" rel="noopener">Abrir a fonte</a></li>' for n, t, u in FONTES)
fontes = f'''        <section class="titulo-pagina guia-topo">
            <div class="container">
                <p class="guia-chapeu">Guia do cerrado</p>
                <h1>Fontes</h1>
                <p>De onde vem cada número do guia. Os números pequenos nos textos levam até aqui. Onde as fontes discordam, o guia usa a mais oficial e diz isso no texto.</p>
            </div>
        </section>
        <section class="secao">
            <div class="container texto-longo">
                <ol class="fontes-lista">{lista}</ol>
                <p class="nota-calculo">Os números de cada estado na página “O bioma” foram calculados aqui, cruzando os limites do IBGE com o contorno dos estados; são aproximações.</p>
            </div>
        </section>
'''
pagina('fontes.html', 'Fontes do guia — Guia do Cerrado', 'As fontes de cada número do guia do Cerrado: IBGE, Embrapa, ICMBio, MMA, FAPESP e artigos científicos.', fontes)

# ---------------------------------------------------------------- a inicial do guia (só em português)
p = M / 'index.html'
s = p.read_text()
if '{{!pt-BR}}' not in s.split('<main id="conteudo">')[1]:
    ini = s.index('    <main id="conteudo">\n') + len('    <main id="conteudo">\n'); fim = s.index('    </main>')
    antiga = s[ini:fim]
    s = s[:ini] + '{{!pt-BR}}\n' + antiga + '{{/!pt-BR}}\n{{?pt-BR}}\n' + '<!--INICIAL-->' + '{{/pt-BR}}\n' + s[fim:]
    # título e descrição da inicial em português
    s = re.sub(r'<title>(\{\{index_119\}\})</title>', r'<title>{{!pt-BR}}\1{{/!pt-BR}}{{?pt-BR}}Guia do Cerrado: a savana mais rica do mundo{{/pt-BR}}</title>', s)
inicial = '''        <section class="abertura">
            <img src="{{raiz}}img/abertura-seriema-ipe.webp" srcset="{{raiz}}img/abertura-seriema-ipe-640.webp 640w, {{raiz}}img/abertura-seriema-ipe.webp 1000w" sizes="100vw" alt="Seriema no campo de capim dourado, com um ipê-rosa florido ao fundo" width="1000" height="667" loading="eager" fetchpriority="high">
            <div class="faixa">
                <div class="container">
                    <p class="guia-chapeu claro">Guia do cerrado</p>
                    <h1>O cerrado, de perto</h1>
                    <p>A savana mais rica do mundo, explicada sem pressa: as paisagens, os bichos e as plantas, o clima, o fogo e a água que nasce aqui. Tudo com fonte.</p>
                    <a class="botao" href="bioma.html">Comece pelo bioma</a>
                </div>
            </div>
        </section>
        <section class="secao">
            <div class="container">
                <h2>O cerrado em três números</h2>
                <div class="fatos">
                    <div><strong>23,3%</strong>do Brasil, quase 2 milhões de km²<sup class="nota"><a href="fontes.html#f1" aria-label="Fonte 1">1</a></sup></div>
                    <div><strong>+11 mil</strong>espécies de plantas nativas<sup class="nota"><a href="fontes.html#f11" aria-label="Fonte 11">11</a></sup></div>
                    <div><strong>~4.400</strong>plantas que só existem aqui<sup class="nota"><a href="fontes.html#f12" aria-label="Fonte 12">12</a></sup></div>
                </div>
            </div>
        </section>
        <section class="secao creme">
            <div class="container">
                <h2>Explore o guia</h2>
                <div class="guia-portas">
                    <a class="porta porta-grande" href="paisagens.html"><span class="porta-chapeu">Paisagens</span><strong>Do campo limpo à mata ciliar</strong><span>As 11 paisagens do Cerrado num corte desenhado para explorar.</span></a>
                    <a class="porta" href="bioma.html"><span class="porta-chapeu">O bioma</span><strong>Onde fica, clima, solo e fogo</strong><span>E quanto de cada estado é Cerrado.</span></a>
                    <a class="porta" href="galeria.html"><span class="porta-chapeu">Espécies</span><strong>Bichos do Cerrado</strong><span>Fichas com medidas, hábitos e como fotografar.</span></a>
                    <a class="porta" href="expedicoes.html"><span class="porta-chapeu">Expedições</span><strong>Ver de perto</strong><span>Quando ir e onde ficam os parques.</span></a>
                    <a class="porta" href="fontes.html"><span class="porta-chapeu">Fontes</span><strong>De onde vem cada número</strong><span>IBGE, Embrapa, ICMBio e artigos científicos.</span></a>
                </div>
            </div>
        </section>
        <section class="secao">
            <div class="container">
                <h2>Algumas espécies</h2>
                <p class="intro">Toque para abrir a ficha de cada uma.</p>
                <div class="grade destaque">
                <article class="foto"><a href="especie-lobo-guara.html"><img src="{{raiz}}img/lobo-guara.webp" srcset="{{raiz}}img/lobo-guara-640.webp 640w, {{raiz}}img/lobo-guara.webp 1000w" sizes="(max-width: 760px) 100vw, 50vw" alt="Lobo-guará de pelagem laranja e pernas pretas andando na grama" width="1000" height="647" loading="lazy"></a><div class="legenda"><h3><a href="especie-lobo-guara.html">Lobo-guará</a></h3><p class="cientifico">Chrysocyon brachyurus</p><p>O maior canídeo da América do Sul, que come muita fruta e espalha as sementes da lobeira.</p></div></article>
                <article class="foto"><a href="especie-tamandua-bandeira.html"><img src="{{raiz}}img/tamandua-bandeira.webp" srcset="{{raiz}}img/tamandua-bandeira-640.webp 640w, {{raiz}}img/tamandua-bandeira.webp 1000w" sizes="(max-width: 760px) 100vw, 50vw" alt="Tamanduá-bandeira cinza, com a faixa preta no ombro, procurando alimento no capim" width="1000" height="667" loading="lazy"></a><div class="legenda"><h3><a href="especie-tamandua-bandeira.html">Tamanduá-bandeira</a></h3><p class="cientifico">Myrmecophaga tridactyla</p><p>Sem dentes, come formigas e cupins com uma língua de mais de meio metro.</p></div></article>
                <article class="foto"><a href="especie-arara-caninde.html"><img src="{{raiz}}img/arara-caninde.webp" srcset="{{raiz}}img/arara-caninde-640.webp 640w, {{raiz}}img/arara-caninde.webp 1000w" sizes="(max-width: 760px) 100vw, 50vw" alt="Arara-canindé azul e amarela voando de asas abertas sobre a mata" width="1000" height="772" loading="lazy"></a><div class="legenda"><h3><a href="especie-arara-caninde.html">Arara-canindé</a></h3><p class="cientifico">Ara ararauna</p><p>Faz ninho em palmeiras mortas, como o buriti das veredas.</p></div></article>
                </div>
                <p class="mais"><a href="galeria.html">Ver todas as espécies →</a></p>
            </div>
        </section>
'''
s = re.sub(r'\{\{\?pt-BR\}\}\n.*?\{\{/pt-BR\}\}\n(?=    </main>)', lambda m: '{{?pt-BR}}\n' + inicial + '{{/pt-BR}}\n', s, flags=re.S)
s = s.replace('<!--INICIAL-->', inicial)
p.write_text(s)

# ---------------------------------------------------------------- o menu certo em cada página só em português
so_pt = json.loads((AQUI / 'so-pt.json').read_text())
for f in ['bioma.html', 'paisagens.html', 'fontes.html']:
    if f not in so_pt: so_pt.append(f)
(AQUI / 'so-pt.json').write_text(json.dumps(so_pt, ensure_ascii=False, indent=2) + '\n')
for f in so_pt:
    if f == '404.html': continue
    q = M / f; t = q.read_text()
    t = re.sub(r'\{\{!pt-BR\}\}<ul class="menu".*?\{\{/!pt-BR\}\}', '', t)
    t = re.sub(r'(\{\{\?pt-BR\}\})?<ul class="menu" id="menu">.*?</ul>(\{\{/pt-BR\}\})?', menu_pt(f), t, count=1)
    t = re.sub(r'\{\{!pt-BR\}\}.*?\{\{/!pt-BR\}\}', '', t, flags=re.S)
    t = com_rodape_do_guia(t)
    q.write_text(t)
print('guia pronto:', so_pt)

# ================================================================ Espécies: o catálogo de fauna e flora (parte 2 do guia)
FONTES += [
 (15, 'Ministério do Meio Ambiente. Portaria MMA nº 148, de 7 de junho de 2022: a lista nacional de espécies ameaçadas (atualiza as portarias 443, 444 e 445 de 2014).', 'https://www.in.gov.br/en/web/dou/-/portaria-mma-n-148-de-7-de-%20%20%20%20%20%20%20%20%20%20%20%20%20%20junho-de-2022-406272733'),
 (16, 'ICMBio. SALVE, o sistema de avaliação do risco de extinção da fauna: as fichas de cada espécie.', 'https://salve.icmbio.gov.br'),
 (17, 'Lycalopex vetulus (Carnivora: Canidae). Mammalian Species, American Society of Mammalogists: o único canídeo endêmico do Cerrado, vulnerável na lista nacional.', 'https://academic.oup.com/mspecies/article/doi/10.1644/847.1/2600889'),
 (18, 'Wikipédia, com os dados da Lista Vermelha da IUCN: Mergus octosetaceus (pato-mergulhão), criticamente em perigo, menos de 250 adultos, todos no Cerrado.', 'https://en.wikipedia.org/wiki/Brazilian_merganser'),
 (19, 'Características e potencialidades dos frutos do Cerrado na indústria de alimentos. Brazilian Journal of Food Technology (SciELO): as épocas de frutificação.', 'http://www.scielo.br/j/bjft/a/F3N9GCfWzJRx77Py3ShRmRq/?lang=pt'),
 (20, 'Avaliação do risco de extinção da onça-parda Puma concolor no Brasil. Biodiversidade Brasileira (ICMBio).', 'https://revistaeletronica.icmbio.gov.br/BioBR/article/view/377'),
]
FONTES.sort()

AMEACA = {'VU': 'Vulnerável', 'EN': 'Em perigo', 'CR': 'Criticamente em perigo'}
# (id, nome, científico, grupo, reino, ameaça, paisagens, texto, foto, ficha, fontes)
ESP = [
 ('lobo-guara', 'Lobo-guará', 'Chrysocyon brachyurus', 'Mamíferos', 'fauna', 'VU', ['campo-sujo', 'cerrado-sentido-restrito'], 'O maior canídeo da América do Sul. Come muita fruta, principalmente a lobeira, e espalha as sementes.', 'lobo-guara', True, [15]),
 ('tamandua-bandeira', 'Tamanduá-bandeira', 'Myrmecophaga tridactyla', 'Mamíferos', 'fauna', 'VU', ['campo-limpo', 'campo-sujo', 'cerrado-sentido-restrito'], 'Não tem dentes: come formigas e cupins com uma língua de mais de meio metro.', 'tamandua-bandeira', True, [15]),
 ('tatu-canastra', 'Tatu-canastra', 'Priodontes maximus', 'Mamíferos', 'fauna', 'VU', ['cerrado-sentido-restrito', 'cerradao'], 'O maior tatu do mundo. As tocas enormes que ele cava viram abrigo para dezenas de outros bichos.', None, False, [15, 16]),
 ('onca-pintada', 'Onça-pintada', 'Panthera onca', 'Mamíferos', 'fauna', 'VU', ['mata-de-galeria', 'mata-ciliar', 'cerradao'], 'O maior felino das Américas. No Cerrado, vive sobretudo nas matas ao longo dos rios.', None, False, [15]),
 ('onca-parda', 'Onça-parda', 'Puma concolor', 'Mamíferos', 'fauna', 'VU', ['cerrado-sentido-restrito', 'cerradao', 'mata-de-galeria'], 'Também chamada de suçuarana. Anda muito e ocupa quase todas as paisagens; na lista nacional, as subespécies ameaçadas são vulneráveis.', None, False, [20]),
 ('veado-campeiro', 'Veado-campeiro', 'Ozotoceros bezoarticus', 'Mamíferos', 'fauna', 'VU', ['campo-limpo', 'campo-sujo'], 'O veado dos campos abertos. O Parque Nacional das Emas é um dos lugares onde ele ainda é visto em bandos.', None, False, [15, 16]),
 ('cachorro-vinagre', 'Cachorro-vinagre', 'Speothos venaticus', 'Mamíferos', 'fauna', 'VU', ['mata-de-galeria', 'cerradao'], 'Um canídeo pequeno e de pernas curtas, que caça em grupo. Raríssimo de ver.', None, False, [15, 16]),
 ('raposa-do-campo', 'Raposa-do-campo', 'Lycalopex vetulus', 'Mamíferos', 'fauna', 'VU', ['campo-limpo', 'campo-sujo', 'cerrado-sentido-restrito'], 'O único canídeo que só existe no Cerrado. Pequena, come muitos cupins e insetos.', None, False, [17]),
 ('anta', 'Anta', 'Tapirus terrestris', 'Mamíferos', 'fauna', 'VU', ['vereda', 'mata-de-galeria', 'mata-ciliar'], 'O maior mamífero terrestre do Brasil. Nada bem, vive perto da água e espalha sementes de muitas árvores.', None, False, [15]),
 ('tamandua-mirim', 'Tamanduá-mirim', 'Tamandua tetradactyla', 'Mamíferos', 'fauna', None, ['cerradao', 'mata-de-galeria', 'cerrado-sentido-restrito'], 'O primo menor do tamanduá-bandeira: sobe em árvores e se segura com a cauda.', None, False, []),
 ('ema', 'Ema', 'Rhea americana', 'Aves', 'fauna', None, ['campo-limpo', 'campo-sujo'], 'A maior ave do Brasil. Não voa, corre muito, e quem choca os ovos é o macho.', None, False, []),
 ('seriema', 'Seriema', 'Cariama cristata', 'Aves', 'fauna', None, ['campo-limpo', 'campo-sujo', 'cerrado-sentido-restrito'], 'O canto alto, que parece uma risada, é um dos sons mais típicos das manhãs do Cerrado.', 'seriema', True, []),
 ('arara-caninde', 'Arara-canindé', 'Ara ararauna', 'Aves', 'fauna', None, ['vereda', 'palmeiral'], 'Faz ninho em palmeiras mortas, como o buriti das veredas.', 'arara-caninde', True, []),
 ('tucano-toco', 'Tucano-toco', 'Ramphastos toco', 'Aves', 'fauna', None, ['cerradao', 'mata-de-galeria'], 'O maior dos tucanos: o bico oco ajuda a perder calor nos dias quentes.', 'tucano-toco', True, []),
 ('pato-mergulhao', 'Pato-mergulhão', 'Mergus octosetaceus', 'Aves', 'fauna', 'CR', ['mata-de-galeria', 'mata-ciliar'], 'Um dos patos mais raros do mundo: são menos de 250 adultos, todos em rios de água limpa e corredeira do Cerrado.', None, False, [18]),
 ('coruja-buraqueira', 'Coruja-buraqueira', 'Athene cunicularia', 'Aves', 'fauna', None, ['campo-limpo', 'campo-sujo'], 'Mora em tocas no chão e fica de pé na entrada, de dia, vigiando o campo.', None, False, []),
 ('carcara', 'Carcará', 'Caracara plancus', 'Aves', 'fauna', None, ['campo-limpo', 'campo-sujo', 'cerrado-sentido-restrito'], 'Come de tudo e aparece onde tem comida fácil, até atrás de tratores e na beira das queimadas.', None, False, []),
 ('papagaio-verdadeiro', 'Papagaio-verdadeiro', 'Amazona aestiva', 'Aves', 'fauna', None, ['cerradao', 'cerrado-sentido-restrito'], 'Anda em casais e bandos barulhentos; é dos bichos mais tirados da natureza para o comércio ilegal.', None, False, []),
 ('jiboia', 'Jiboia', 'Boa constrictor', 'Répteis', 'fauna', None, ['cerradao', 'mata-de-galeria', 'cerrado-sentido-restrito'], 'Não tem veneno: mata a presa apertando. Ajuda a controlar roedores.', None, False, []),
 ('cascavel', 'Cascavel', 'Crotalus durissus', 'Répteis', 'fauna', None, ['campo-sujo', 'cerrado-sentido-restrito'], 'Venenosa, avisa antes com o chocalho na ponta da cauda. Prefere fugir a atacar.', None, False, []),
 ('teiu', 'Teiú', 'Salvator merianae', 'Répteis', 'fauna', None, ['cerrado-sentido-restrito', 'mata-de-galeria'], 'O maior lagarto do Cerrado. Passa os meses mais frios e secos enterrado, quase sem se mexer.', None, False, []),
 ('vaga-lume-cupinzeiro', 'Vaga-lume dos cupinzeiros', 'Pyrearinus termitilluminans', 'Insetos', 'fauna', None, ['campo-limpo', 'campo-sujo'], 'Nas primeiras noites de chuva, as larvas acendem luzes verdes nos cupinzeiros para atrair insetos. As Emas são famosas pelos cupinzeiros que brilham.', None, False, []),
 ('jatai', 'Jataí', 'Tetragonisca angustula', 'Insetos', 'fauna', None, ['cerradao', 'mata-de-galeria', 'cerrado-sentido-restrito'], 'Uma das abelhas sem ferrão mais comuns. Não pica e poliniza muitas plantas. Veja o site Abelhas sem Ferrão.', None, False, []),
 ('pequi', 'Pequi', 'Caryocar brasiliense', 'Árvores', 'flora', None, ['cerrado-sentido-restrito', 'cerradao'], 'O fruto mais famoso do Cerrado. Atenção: o caroço tem espinhos finos por dentro, e não se morde.', None, False, [19]),
 ('baru', 'Baru', 'Dipteryx alata', 'Árvores', 'flora', None, ['cerradao', 'mata-seca', 'cerrado-sentido-restrito'], 'A castanha torrada é uma das mais nutritivas do Brasil. Os frutos caem na seca, quando falta comida para os bichos.', None, False, [19]),
 ('buriti', 'Buriti', 'Mauritia flexuosa', 'Palmeiras', 'flora', None, ['vereda', 'palmeiral'], 'A palmeira das veredas: onde tem buriti, tem água. Os frutos alimentam araras, antas e gente.', None, False, [19]),
 ('macauba', 'Macaúba', 'Acrocomia aculeata', 'Palmeiras', 'flora', None, ['palmeiral', 'cerradao'], 'Palmeira de tronco com espinhos e cocos amarelos, de onde se tira óleo.', None, False, []),
 ('babacu', 'Babaçu', 'Attalea speciosa', 'Palmeiras', 'flora', None, ['palmeiral'], 'Forma palmeirais imensos no norte do Cerrado. A quebra do coco é o trabalho das quebradeiras de coco do Maranhão e do Tocantins.', None, False, []),
 ('ipe-amarelo', 'Ipê-amarelo', 'Handroanthus spp.', 'Árvores', 'flora', None, ['cerrado-sentido-restrito', 'cerradao', 'mata-seca'], 'Floresce na seca, sem nenhuma folha: as árvores ficam inteiras amarelas por poucos dias.', None, False, []),
 ('lobeira', 'Lobeira', 'Solanum lycocarpum', 'Arbustos', 'flora', None, ['campo-sujo', 'cerrado-sentido-restrito'], 'A fruta-do-lobo: o lobo-guará come muito dela e espalha as sementes.', None, False, []),
 ('cagaita', 'Cagaita', 'Eugenia dysenterica', 'Árvores', 'flora', None, ['cerrado-sentido-restrito', 'cerradao'], 'Fruta ácida e suculenta. O nome científico avisa: comida em excesso, solta o intestino.', None, False, [19]),
 ('mangaba', 'Mangaba', 'Hancornia speciosa', 'Árvores', 'flora', None, ['cerrado-sentido-restrito', 'campo-sujo'], 'Fruta doce, de leite branco, que só presta bem madura.', None, False, [19]),
 ('araticum', 'Araticum', 'Annona crassiflora', 'Árvores', 'flora', None, ['cerrado-sentido-restrito'], 'Parente da fruta-do-conde, com fruto grande e perfumado.', None, False, []),
 ('jatoba', 'Jatobá-do-cerrado', 'Hymenaea stigonocarpa', 'Árvores', 'flora', None, ['cerrado-sentido-restrito', 'cerradao'], 'Dentro da vagem dura, uma farinha doce que vira bolo e mingau.', None, False, []),
 ('pau-terra', 'Pau-terra', 'Qualea grandiflora', 'Árvores', 'flora', None, ['cerrado-sentido-restrito', 'cerradao'], 'Uma das árvores mais comuns do cerrado, de flores amarelas grandes e casca grossa.', None, False, []),
 ('barbatimao', 'Barbatimão', 'Stryphnodendron adstringens', 'Árvores', 'flora', None, ['cerrado-sentido-restrito'], 'A casca, rica em taninos, é usada há muito tempo na medicina popular para cicatrizar.', None, False, []),
 ('canela-de-ema', 'Canela-de-ema', 'Vellozia spp.', 'Ervas e arbustos', 'flora', None, ['campo-rupestre'], 'Planta das pedras do campo rupestre. O “tronco” é feito de restos de folhas, que protegem do fogo e da seca.', None, False, []),
 ('sempre-viva', 'Sempre-viva', 'Comanthera elegans', 'Ervas e arbustos', 'flora', None, ['campo-rupestre'], 'Flores que secam sem perder a forma; colhidas para arranjos e artesanato na Serra do Espinhaço.', None, False, []),
 ('capim-dourado', 'Capim-dourado', 'Syngonanthus nitens', 'Ervas e arbustos', 'flora', None, ['campo-limpo', 'vereda'], 'A haste dourada vira o artesanato mais conhecido do Jalapão, no Tocantins.', None, False, []),

 # mais espécies (31/10/2026, noite): textos curtos, só com o que é bem estabelecido; sem categoria de ameaça onde não foi conferida
 ('capivara', 'Capivara', 'Hydrochoerus hydrochaeris', 'Mamíferos', 'fauna', None, ['vereda', 'mata-ciliar', 'mata-de-galeria'], 'O maior roedor do mundo. Vive em grupos perto da água e mergulha para fugir.', None, False, []),
 ('cachorro-do-mato', 'Cachorro-do-mato', 'Cerdocyon thous', 'Mamíferos', 'fauna', None, ['cerrado-sentido-restrito', 'campo-sujo', 'mata-de-galeria'], 'O canídeo mais comum do Cerrado: anda em casal, à noite, e come de tudo, de frutos a insetos.', None, False, []),
 ('tatu-peba', 'Tatu-peba', 'Euphractus sexcinctus', 'Mamíferos', 'fauna', None, ['campo-sujo', 'cerrado-sentido-restrito'], 'Tatu de pelos claros que cava muito rápido e anda de dia nos campos.', None, False, []),
 ('quati', 'Quati', 'Nasua nasua', 'Mamíferos', 'fauna', None, ['mata-de-galeria', 'cerradao'], 'Anda em bandos, com a cauda listrada em pé, revirando folhas atrás de bichinhos e frutos.', None, False, []),
 ('macaco-prego', 'Macaco-prego', 'Sapajus libidinosus', 'Mamíferos', 'fauna', None, ['cerradao', 'mata-seca', 'mata-de-galeria'], 'Usa pedras como martelo para quebrar cocos duros: um dos poucos animais que fazem isso na natureza.', None, False, []),
 ('sagui', 'Sagui-de-tufos-pretos', 'Callithrix penicillata', 'Mamíferos', 'fauna', None, ['cerradao', 'mata-de-galeria', 'cerrado-sentido-restrito'], 'Macaquinho de tufos pretos nas orelhas, comum até nas cidades do Cerrado. Come a goma que escorre das árvores.', None, False, []),
 ('jaguatirica', 'Jaguatirica', 'Leopardus pardalis', 'Mamíferos', 'fauna', None, ['mata-de-galeria', 'cerradao'], 'Felino de pelagem pintada, do tamanho de um cachorro médio. Caça à noite.', None, False, []),
 ('lontra', 'Lontra', 'Lontra longicaudis', 'Mamíferos', 'fauna', None, ['mata-ciliar', 'mata-de-galeria'], 'Nadadora de rios de água limpa: onde ela aparece, o rio está bem.', None, False, []),
 ('papagaio-galego', 'Papagaio-galego', 'Alipiopsitta xanthops', 'Aves', 'fauna', None, ['cerrado-sentido-restrito', 'campo-sujo'], 'Papagaio de cabeça amarela que vive quase só no Cerrado.', None, False, []),
 ('gralha-do-campo', 'Gralha-do-campo', 'Cyanocorax cristatellus', 'Aves', 'fauna', None, ['cerrado-sentido-restrito', 'cerradao'], 'Azul, branca e de topete, anda em bandos barulhentos. Uma das aves mais típicas do Cerrado.', None, False, []),
 ('pica-pau-do-campo', 'Pica-pau-do-campo', 'Colaptes campestris', 'Aves', 'fauna', None, ['campo-limpo', 'campo-sujo'], 'Um pica-pau que procura formigas e cupins no chão, em vez de bicar troncos.', None, False, []),
 ('beija-flor-tesoura', 'Beija-flor-tesoura', 'Eupetomena macroura', 'Aves', 'fauna', None, ['cerrado-sentido-restrito', 'cerradao'], 'Beija-flor grande, azul e verde, com a cauda aberta em tesoura. Defende as flores dele dos outros.', None, False, []),
 ('urubu-rei', 'Urubu-rei', 'Sarcoramphus papa', 'Aves', 'fauna', None, ['cerradao', 'mata-de-galeria'], 'Branco e preto, com a cabeça colorida de laranja e roxo. Plana alto atrás de carcaças.', None, False, []),
 ('curicaca', 'Curicaca', 'Theristicus caudatus', 'Aves', 'fauna', None, ['campo-limpo', 'campo-sujo'], 'Bico longo e curvo para tirar insetos do chão; o grito alto, em dupla, se ouve de longe.', None, False, []),
 ('coral', 'Cobra-coral-verdadeira', 'Micrurus spp.', 'Répteis', 'fauna', None, ['cerrado-sentido-restrito', 'mata-de-galeria'], 'Venenosa, de anéis vermelhos, pretos e brancos ou amarelos. Há falsas-corais muito parecidas: na dúvida, não mexa em nenhuma.', None, False, []),
 ('jabuti-piranga', 'Jabuti-piranga', 'Chelonoidis carbonarius', 'Répteis', 'fauna', None, ['cerradao', 'mata-seca'], 'Tartaruga de terra com manchas vermelhas nas patas e na cabeça. Come frutos caídos.', None, False, []),
 ('sapo-cururu', 'Sapo-cururu', 'Rhinella diptycha', 'Anfíbios', 'fauna', None, ['vereda', 'mata-de-galeria'], 'Sapo grande, de glândulas com veneno atrás dos olhos. Aparece em massa nas primeiras chuvas.', None, False, []),
 ('dourado', 'Dourado', 'Salminus brasiliensis', 'Peixes', 'fauna', None, ['mata-ciliar'], 'Peixe dourado e forte, que sobe os rios para desovar. Vive nos grandes rios que nascem no Cerrado.', None, False, []),
 ('cupim-de-montículo', 'Cupim de montículo', 'Cornitermes cumulans', 'Insetos', 'fauna', None, ['campo-limpo', 'campo-sujo'], 'Constrói os cupinzeiros duros dos campos, que viram casa de corujas, lagartos e vaga-lumes.', None, False, []),
 ('ipe-roxo', 'Ipê-roxo', 'Handroanthus impetiginosus', 'Árvores', 'flora', None, ['cerradao', 'mata-seca'], 'Floresce rosa-arroxeado no meio da seca, sem folhas, antes dos ipês amarelos.', None, False, []),
 ('copaiba', 'Copaíba', 'Copaifera langsdorffii', 'Árvores', 'flora', None, ['cerradao', 'mata-de-galeria'], 'O óleo que escorre do tronco é usado há muito tempo na medicina popular.', None, False, []),
 ('sucupira-branca', 'Sucupira-branca', 'Pterodon emarginatus', 'Árvores', 'flora', None, ['cerrado-sentido-restrito', 'cerradao'], 'Árvore de flores lilás e sementes aladas, usadas na medicina popular.', None, False, []),
 ('murici', 'Murici', 'Byrsonima spp.', 'Arbustos', 'flora', None, ['cerrado-sentido-restrito', 'campo-sujo'], 'Frutinhas amarelas de cheiro forte, que viram doce e licor.', None, False, []),
 ('cajuzinho', 'Cajuzinho-do-cerrado', 'Anacardium humile', 'Arbustos', 'flora', None, ['campo-sujo', 'cerrado-sentido-restrito'], 'Um cajueiro anão: quase toda a planta fica embaixo da terra, o que a protege do fogo. Por cima, só os galhos e os cajuzinhos.', None, False, []),
 ('gabiroba', 'Gabiroba', 'Campomanesia spp.', 'Arbustos', 'flora', None, ['campo-sujo', 'cerrado-sentido-restrito'], 'Parente da goiaba, com frutinhas verde-amareladas doces.', None, False, []),
 ('jenipapo', 'Jenipapo', 'Genipa americana', 'Árvores', 'flora', None, ['mata-ciliar', 'mata-de-galeria'], 'O fruto verde dá uma tinta preta usada por muitos povos indígenas para pintar o corpo.', None, False, []),
 ('guariroba', 'Guariroba', 'Syagrus oleracea', 'Palmeiras', 'flora', None, ['palmeiral', 'cerradao'], 'Palmeira de palmito amargo, ingrediente da cozinha de Goiás.', None, False, []),
 ('faveiro', 'Faveiro', 'Dimorphandra mollis', 'Árvores', 'flora', None, ['cerrado-sentido-restrito'], 'As favas são colhidas para a indústria de remédios: uma renda para muitas comunidades.', None, False, []),
 ('chuveirinho', 'Chuveirinho', 'Paepalanthus spp.', 'Ervas e arbustos', 'flora', None, ['campo-rupestre', 'campo-limpo'], 'Sempre-viva de flores brancas que se abrem como a ducha de um chuveiro.', None, False, []),
 ('lixeira', 'Lixeira', 'Curatella americana', 'Árvores', 'flora', None, ['cerrado-sentido-restrito'], 'As folhas são tão ásperas que já foram usadas como lixa.', None, False, []),
 ('pau-santo', 'Pau-santo', 'Kielmeyera coriacea', 'Árvores', 'flora', None, ['cerrado-sentido-restrito', 'campo-sujo'], 'Casca de cortiça grossa e flores brancas perfumadas na seca.', None, False, []),
 ('queixada', 'Queixada', 'Tayassu pecari', 'Mamíferos', 'fauna', 'VU', ['cerradao', 'mata-de-galeria', 'mata-seca'], 'Porco-do-mato de queixo branco que anda em bandos enormes, batendo os dentes. Precisa de grandes áreas de mata.', None, False, []),
 ('cateto', 'Cateto', 'Pecari tajacu', 'Mamíferos', 'fauna', None, ['cerradao', 'cerrado-sentido-restrito', 'mata-de-galeria'], 'O porco-do-mato menor, com um colar claro no pescoço. Anda em grupos pequenos.', None, False, []),
 ('veado-catingueiro', 'Veado-catingueiro', 'Mazama gouazoubira', 'Mamíferos', 'fauna', None, ['cerrado-sentido-restrito', 'cerradao', 'campo-sujo'], 'Veado pequeno e acinzentado, de chifres simples. O mais comum do Cerrado, mas difícil de ver.', None, False, []),
 ('paca', 'Paca', 'Cuniculus paca', 'Mamíferos', 'fauna', None, ['mata-de-galeria', 'mata-ciliar', 'vereda'], 'Roedor grande e noturno, de fileiras de pintas brancas. Vive perto da água e foge mergulhando.', None, False, []),
 ('cutia', 'Cutia', 'Dasyprocta azarae', 'Mamíferos', 'fauna', None, ['mata-de-galeria', 'cerradao', 'mata-seca'], 'Roedor de pernas finas que enterra sementes para comer depois e esquece muitas: planta árvores.', None, False, []),
 ('bugio', 'Bugio-preto', 'Alouatta caraya', 'Mamíferos', 'fauna', None, ['mata-de-galeria', 'mata-ciliar', 'cerradao'], 'O macaco do ronco. Os machos são pretos e as fêmeas, mais claras; o grito se ouve a quilômetros.', None, False, []),
 ('mao-pelada', 'Mão-pelada', 'Procyon cancrivorus', 'Mamíferos', 'fauna', None, ['mata-ciliar', 'mata-de-galeria', 'vereda'], 'Parente do guaxinim, de máscara preta e mãos sem pelo. Anda à noite na beira dos rios.', None, False, []),
 ('irara', 'Irara', 'Eira barbara', 'Mamíferos', 'fauna', None, ['mata-de-galeria', 'cerradao', 'mata-seca'], 'Carnívoro escuro, de cabeça clara, que sobe em árvores atrás de mel. O nome, em tupi, quer dizer "tomador de mel".', None, False, []),
 ('arara-azul-grande', 'Arara-azul-grande', 'Anodorhynchus hyacinthinus', 'Aves', 'fauna', None, ['palmeiral', 'vereda', 'cerradao'], 'A maior arara do mundo, toda azul, que quebra cocos duros com o bico. Vive no Pantanal e em pedaços do Cerrado.', None, False, []),
 ('joao-de-barro', 'João-de-barro', 'Furnarius rufus', 'Aves', 'fauna', None, ['campo-sujo', 'cerrado-sentido-restrito', 'parque-de-cerrado'], 'O casal constrói junto uma casa de barro em forma de forno, com um corredor por dentro.', None, False, []),
 ('bem-te-vi', 'Bem-te-vi', 'Pitangus sulphuratus', 'Aves', 'fauna', None, ['cerrado-sentido-restrito', 'mata-ciliar', 'vereda'], 'Barriga amarela, faixa branca na cabeça e o canto que diz o próprio nome. Come de tudo.', None, False, []),
 ('periquito-rei', 'Periquito-rei', 'Eupsittula aurea', 'Aves', 'fauna', None, ['cerrado-sentido-restrito', 'campo-sujo', 'mata-de-galeria'], 'Periquito verde de testa laranja, que faz o ninho dentro de cupinzeiros nas árvores.', None, False, []),
 ('anu-branco', 'Anu-branco', 'Guira guira', 'Aves', 'fauna', None, ['campo-sujo', 'campo-limpo', 'parque-de-cerrado'], 'Ave clara e despenteada, de topete laranja, que vive em grupos e divide o ninho entre várias fêmeas.', None, False, []),
 ('canario-da-terra', 'Canário-da-terra', 'Sicalis flaveola', 'Aves', 'fauna', None, ['campo-sujo', 'campo-limpo', 'cerrado-sentido-restrito'], 'O macho é amarelo-ouro, de testa laranja. Dos pássaros mais tirados da natureza pelo tráfico.', None, False, []),
 ('gaviao-carijo', 'Gavião-carijó', 'Rupornis magnirostris', 'Aves', 'fauna', None, ['cerrado-sentido-restrito', 'mata-de-galeria', 'campo-sujo'], 'O gavião mais comum do Brasil. Pousa em postes e mourões e grita alto quando voa.', None, False, []),
 ('urubu-de-cabeca-preta', 'Urubu-de-cabeça-preta', 'Coragyps atratus', 'Aves', 'fauna', None, ['campo-limpo', 'campo-sujo', 'cerrado-sentido-restrito'], 'O urubu comum, todo preto, que vive em bandos e limpa carcaças, inclusive perto das cidades.', None, False, []),
 ('morcego-beija-flor', 'Morcego-beija-flor', 'Glossophaga soricina', 'Mamíferos', 'fauna', None, ['mata-de-galeria', 'cerradao', 'cerrado-sentido-restrito'], 'Um morcego de uns 10 g que voa parado diante das flores, como um beija-flor, e toma néctar à noite.', None, False, []),
 ('jacare-de-papo-amarelo', 'Jacaré-de-papo-amarelo', 'Caiman latirostris', 'Répteis', 'fauna', None, ['mata-ciliar', 'vereda'], 'Jacaré de focinho largo e papo amarelado, dos rios e lagoas do sul do Cerrado.', None, False, []),
 ('sucuri', 'Sucuri', 'Eunectes murinus', 'Répteis', 'fauna', None, ['vereda', 'mata-ciliar'], 'A maior cobra do Brasil. Não tem veneno: vive na água e mata a presa apertando.', None, False, []),
 ('caicaca', 'Caiçaca', 'Bothrops moojeni', 'Répteis', 'fauna', None, ['mata-de-galeria', 'mata-ciliar', 'vereda'], 'A jararaca do Cerrado, das beiras de rio e de vereda. Venenosa: é das cobras que mais causam acidentes na região.', None, False, []),
 ('calango', 'Calango', 'Tropidurus spp.', 'Répteis', 'fauna', None, ['cerrado-sentido-restrito', 'campo-rupestre', 'campo-sujo'], 'O lagarto das pedras, dos muros e dos troncos, que fica parado ao sol esperando um inseto passar.', None, False, []),
 ('ra-pimenta', 'Rã-pimenta', 'Leptodactylus labyrinthicus', 'Anfíbios', 'fauna', None, ['vereda', 'mata-de-galeria'], 'Uma rã enorme, que faz o ninho numa bacia cavada na margem, cheia de espuma.', None, False, []),
 ('pacu', 'Pacu', 'Piaractus mesopotamicus', 'Peixes', 'fauna', None, ['mata-ciliar'], 'O peixe que come frutos: engole os que caem na água e espalha as sementes rio acima.', None, False, []),
 ('piranha', 'Piranha-vermelha', 'Pygocentrus nattereri', 'Peixes', 'fauna', None, ['mata-ciliar', 'vereda'], 'Peixe de dentes afiados e barriga vermelha. A fama de fera é bem maior do que o perigo.', None, False, []),
 ('sauva', 'Saúva', 'Atta spp.', 'Insetos', 'fauna', None, ['cerrado-sentido-restrito', 'campo-sujo', 'cerradao'], 'Formiga que corta folhas, não para comer, mas para cultivar um fungo dentro do formigueiro.', None, False, []),
 ('mamangava', 'Mamangava', 'Xylocopa spp.', 'Insetos', 'fauna', None, ['cerrado-sentido-restrito', 'mata-de-galeria', 'cerradao'], 'Abelha grande e preta, que faz o ninho cavando madeira seca. Poliniza o maracujá.', None, False, []),
 ('rola-bosta', 'Rola-bosta', 'Scarabaeinae', 'Insetos', 'fauna', None, ['campo-limpo', 'campo-sujo', 'cerradao'], 'Besouros que fazem bolas de esterco e as enterram: limpam o chão e adubam o solo.', None, False, []),
 ('cigarra', 'Cigarra', 'Cicadidae', 'Insetos', 'fauna', None, ['cerrado-sentido-restrito', 'cerradao', 'mata-seca'], 'O canto do fim da seca. As ninfas passam anos embaixo da terra antes de sair e cantar.', None, False, []),
 ('caraiba', 'Caraíba', 'Tabebuia aurea', 'Árvores', 'flora', None, ['cerrado-sentido-restrito', 'parque-de-cerrado', 'campo-sujo'], 'O ipê de casca de cortiça e folhas prateadas, que floresce amarelo na seca.', None, False, []),
 ('angico', 'Angico', 'Anadenanthera colubrina', 'Árvores', 'flora', None, ['mata-seca', 'cerradao'], 'Árvore de casca rica em taninos, usada há séculos para curtir couro.', None, False, []),
 ('aroeira', 'Aroeira', 'Myracrodruon urundeuva', 'Árvores', 'flora', None, ['mata-seca', 'cerradao'], 'A árvore da madeira que não apodrece. Tanto foi cortada que entrou na lista de ameaçadas.', None, False, []),
 ('sucupira-preta', 'Sucupira-preta', 'Bowdichia virgilioides', 'Árvores', 'flora', None, ['cerrado-sentido-restrito', 'cerradao'], 'Árvore de flores roxas e madeira dura e escura, das mais típicas do cerrado.', None, False, []),
 ('pimenta-de-macaco', 'Pimenta-de-macaco', 'Xylopia aromatica', 'Árvores', 'flora', None, ['cerrado-sentido-restrito', 'cerradao'], 'As sementes ardem como pimenta-do-reino e são usadas como tempero.', None, False, []),
 ('caliandra', 'Caliandra', 'Calliandra dysantha', 'Arbustos', 'flora', None, ['cerrado-sentido-restrito', 'campo-sujo'], 'Arbusto de flores que parecem pincéis vermelhos. Uma das flores-símbolo do Cerrado.', None, False, []),
 ('arnica', 'Arnica-do-cerrado', 'Lychnophora ericoides', 'Arbustos', 'flora', None, ['campo-rupestre'], 'Arbusto dos campos rupestres, usado na medicina popular e por isso muito arrancado.', None, False, []),
 ('algodaozinho', 'Algodãozinho-do-campo', 'Cochlospermum regium', 'Ervas e arbustos', 'flora', None, ['campo-sujo', 'cerrado-sentido-restrito'], 'Flores amarelas grandes e frutos que soltam paina, como algodão. A raiz grossa rebrota depois do fogo.', None, False, []),
 ('abacaxi-do-cerrado', 'Abacaxi-do-cerrado', 'Ananas ananassoides', 'Ervas e arbustos', 'flora', None, ['cerrado-sentido-restrito', 'campo-sujo'], 'Um abacaxi pequeno e azedo, nativo, que vira suco e doce.', None, False, []),
 ('tingui', 'Tingui', 'Magonia pubescens', 'Árvores', 'flora', None, ['mata-seca', 'cerradao'], 'Árvore de frutos lenhosos e sementes com asas. Já foi usada para fazer sabão.', None, False, []),
 ('bacupari', 'Bacupari-do-cerrado', 'Salacia crassifolia', 'Arbustos', 'flora', None, ['cerrado-sentido-restrito', 'campo-sujo'], 'Fruta amarela e doce, parecida com a lichia, colhida na época das chuvas.', None, False, []),
 ('jacaranda-do-cerrado', 'Jacarandá-do-cerrado', 'Dalbergia miscolobium', 'Árvores', 'flora', None, ['cerrado-sentido-restrito', 'cerradao'], 'Árvore de flores roxas, das mais típicas do cerrado.', None, False, []),
 ('orquidea-cyrtopodium', 'Sumaré', 'Cyrtopodium spp.', 'Ervas e arbustos', 'flora', None, ['campo-sujo', 'campo-limpo', 'cerrado-sentido-restrito'], 'Orquídea de chão, de flores amarelas pintadas, que floresce em massa depois das queimadas.', None, False, []),
 ('capim-flecha', 'Capim-flecha', 'Tristachya leiostachya', 'Ervas e arbustos', 'flora', None, ['campo-limpo', 'campo-sujo'], 'Capim alto dos campos das Emas, que rebrota depressa depois do fogo e domina onde cresce.', None, False, []),
 ('pau-de-tucano', 'Pau-de-tucano', 'Vochysia tucanorum', 'Árvores', 'flora', None, ['cerrado-sentido-restrito', 'cerradao', 'mata-de-galeria'], 'Árvore de cachos de flores amarelas no começo das chuvas.', None, False, []),
 ('puca', 'Puçá', 'Mouriri pusa', 'Árvores', 'flora', None, ['cerrado-sentido-restrito', 'cerradao'], 'Frutinha escura e doce, chamada de jabuticaba-do-cerrado.', None, False, []),
]

# as fichas completas das espécies sem foto (31/10/2026, noite): os números com fonte; onde as fontes divergem, o texto diz
FICHAS = {
 'onca-pintada': dict(fontes=[35, 15], abre='O maior felino das Américas e o maior predador do Cerrado. É rara e evita gente: quase tudo o que se sabe dela por aqui vem de armadilhas fotográficas e de pegadas.',
   fatos=[('Comprimento', 'de 1,7 a 2,4 m, com a cauda; os machos são maiores'), ('Peso', 'de uns 35 a mais de 100 kg, conforme a região e o sexo'), ('Come', 'capivaras, veados, queixadas, jacarés e outros bichos de porte médio'), ('Quando aparece', 'sozinha, mais à noite e ao amanhecer')],
   reconhecer=['Pintas em forma de roseta, com pintinhas dentro (a onça-parda é lisa).', 'Corpo forte, cabeça grande e patas largas.', 'Algumas são pretas, as onças-pretas: é a mesma espécie, e as rosetas aparecem contra a luz.'],
   importa='Como predador do topo, ajuda a controlar as populações de herbívoros. No Cerrado, depende das matas de galeria e ciliares para se deslocar entre as áreas de mata; é vulnerável na lista nacional.',
   escala=(2.0, 0.7, '2 m do focinho à ponta da cauda')),
 'tatu-canastra': dict(fontes=[34, 15], abre='O maior tatu do mundo, e um dos bichos mais difíceis de ver no Cerrado: passa o dia em tocas fundas e sai à noite.',
   fatos=[('Comprimento', 'cerca de 1,5 m, com a cauda'), ('Peso', 'em média 28 kg as fêmeas e 44 kg os machos, num estudo em Goiás'), ('Come', 'cupins e formigas, que ele tira cavando os montes'), ('Quando aparece', 'à noite; de dia fica na toca')],
   reconhecer=['Casco escuro com uma faixa clara na borda.', 'Uma garra enorme em cada pata da frente, feita para cavar.', 'Tocas largas, do tamanho de uma pessoa agachada, e montes de terra revirada.'],
   importa='É chamado de engenheiro do ecossistema: as tocas que ele abandona servem de abrigo para mais de cem espécies de vertebrados. É vulnerável na lista nacional.',
   escala=(1.5, 0.4, '1,5 m do focinho à ponta da cauda')),
 'anta': dict(fontes=[40, 15], abre='O maior mamífero terrestre do Brasil. Apesar do tamanho, é tímida, anda à noite perto da água e foge nadando quando se assusta.',
   fatos=[('Comprimento', 'de 1,7 a 2 m'), ('Altura', 'até cerca de 1,2 m'), ('Peso', 'até 250 a 300 kg (as fontes divergem)'), ('Come', 'frutos, folhas e brotos'), ('Quando aparece', 'à noite, perto de rios, veredas e matas')],
   reconhecer=['Um focinho curto e móvel, quase uma tromba.', 'Corpo escuro e arredondado, com uma crina curta no pescoço.', 'Os filhotes têm listras e pintas claras, que somem com a idade.'],
   importa='É uma das maiores jardineiras do Cerrado: engole frutos grandes e espalha as sementes longe, nas fezes. É vulnerável na lista nacional.',
   escala=(2.0, 1.1, '2 m de comprimento, 1,1 m de altura')),
 'veado-campeiro': dict(fontes=[36, 15], abre='O veado dos campos abertos. Vive em grupos pequenos e depende de grandes áreas de campo nativo, que estão sumindo.',
   fatos=[('Comprimento', 'de 1,2 a 1,5 m'), ('Altura', 'de 70 a 75 cm'), ('Peso', 'de 30 a 40 kg; a fêmea é um pouco menor'), ('Come', 'capins, ervas e brotos'), ('Chifres', 'só os machos têm')],
   reconhecer=['Pelagem castanho-alaranjada, com a barriga clara.', 'Orelhas grandes e cauda curta, branca por baixo.', 'Fica em pé e parado no meio do campo, olhando, antes de fugir.'],
   importa='Onde ainda há bandos de veado-campeiro, ainda há campo nativo de verdade. O Parque Nacional das Emas é um dos melhores lugares para vê-lo. É vulnerável na lista nacional.',
   escala=(1.35, 0.72, '1,35 m de comprimento, 72 cm de altura')),
 'raposa-do-campo': dict(fontes=[38, 17], abre='O único canídeo que só existe no Cerrado: uma raposa pequena, de focinho curto, que vive de comer cupins.',
   fatos=[('Peso', 'de 2,5 a 4 kg'), ('Come', 'principalmente cupins, e também besouros, pequenos roedores e frutos'), ('Quando aparece', 'ao anoitecer e à noite, nos campos'), ('Situação', 'vulnerável na lista nacional')],
   reconhecer=['Pequena, menor que o cachorro-do-mato.', 'Pelagem cinza-amarelada, com uma faixa escura no alto da cauda e a ponta preta.', 'Focinho curto e dentes pequenos, de quem come insetos.'],
   importa='Por ser especializada em cupins e só existir no Cerrado, sofre muito com a troca dos campos por pasto e lavoura, e com os atropelamentos.',
   escala=None),
 'ema': dict(fontes=[37], abre='A maior ave do Brasil. Não voa, mas corre muito; vive em bandos nos campos abertos, muitas vezes perto de veados e de gado.',
   fatos=[('Altura', 'de 1,3 a 1,7 m'), ('Peso', 'de 25 a 45 kg (as fontes divergem)'), ('Come', 'folhas, sementes, frutos, insetos e pequenos bichos'), ('Ninho', 'o macho choca de 15 a 30 ovos, por cerca de 38 dias, e cuida dos filhotes')],
   reconhecer=['Pescoço longo e penas cinzentas, sem cauda.', 'Pernas compridas com três dedos.', 'Abre as asas para mudar de direção quando corre.'],
   importa='Come muitos insetos e espalha sementes pelos campos. É um dos símbolos dos chapadões do Cerrado.',
   escala=(0.9, 1.5, '1,3 a 1,7 m de altura')),
 'pato-mergulhao': dict(fontes=[18, 41], abre='Um dos patos mais raros do mundo. Vive só em rios de água limpa e com corredeiras do Cerrado, mergulhando atrás de peixes.',
   fatos=[('Tamanho', 'cerca de 56 cm'), ('Peso', 'de 600 a 700 g'), ('Quantos restam', 'menos de 250 adultos'), ('Onde vive', 'rios da Serra da Canastra, do Jalapão e da Chapada dos Veadeiros, entre outros')],
   reconhecer=['Pato escuro, de cabeça verde-escura com um topete para trás.', 'Bico fino, preto e serrilhado, feito para segurar peixes.', 'Nada baixo na água e mergulha muito.'],
   importa='Precisa de rios limpos, com mata nas margens e sem barragens: onde ele vive, o rio está bem. É criticamente em perigo de extinção.',
   escala=(0.56, 0.3, '56 cm')),
 'pequi': dict(fontes=[39, 19], abre='A árvore do fruto mais famoso do Cerrado, que tinge o arroz de amarelo e perfuma a cozinha de Goiás e de Minas.',
   fatos=[('Altura', 'em geral de 6 a 10 m, podendo passar de 12 m'), ('Frutos', 'de 500 a 2.000 por árvore em cada safra'), ('Safra', 'muda de região para região: de outubro a março'), ('Flores', 'grandes, claras, cheias de estames; abrem à noite')],
   reconhecer=['Folhas com três partes (trifoliadas), de bordas serrilhadas.', 'Tronco grosso e tortuoso, de casca rugosa.', 'Frutos verdes, redondos, do tamanho de uma laranja.'],
   importa='Na safra, a coleta do pequi é a renda de muitas famílias. Cuidado ao comer: o caroço tem espinhos finos escondidos, e não se morde.',
   escala=('arvore', 8, '8 m (em geral de 6 a 10)')),
 'baru': dict(fontes=[39, 19], abre='A árvore da castanha mais famosa do Cerrado. Os frutos caem na seca, quando falta comida, e alimentam muitos bichos.',
   fatos=[('Altura', 'pode passar de 15 m e chegar a 25 m'), ('Frutos', 'caem de setembro a outubro, segundo um estudo; a época muda de lugar para lugar'), ('Castanha', 'comida torrada, uma por fruto'), ('Quem come', 'o gado, morcegos, macacos e outros bichos comem a polpa')],
   reconhecer=['Frutos marrons, achatados e duros, que caem embaixo da árvore.', 'Folhas compostas, com vários folíolos.', 'Copa larga, que dá boa sombra no pasto.'],
   importa='A castanha virou fonte de renda para comunidades que colhem os frutos sem derrubar as árvores. Muitos baruzeiros ficam de pé nos pastos justamente por isso.',
   escala=('arvore', 20, '20 m (pode chegar a 25)')),
 'buriti': dict(fontes=[39, 19, 10], abre='A palmeira das veredas. Onde tem buriti, tem água: ele só cresce onde o solo fica encharcado.',
   fatos=[('Altura', 'pode passar de 20 m e chegar a 35 m'), ('Frutos', 'de dezembro a junho, com escamas avermelhadas'), ('Plantas', 'há buritis machos e fêmeas; só as fêmeas dão fruto'), ('Usos', 'doce, óleo, as folhas para artesanato e para cobrir casas')],
   reconhecer=['Folhas enormes em forma de leque, no alto de um tronco reto e liso.', 'Cachos pendurados de frutos cobertos de escamas cor de vinho.', 'Cresce em fileira, seguindo o fio de água da vereda.'],
   importa='Os frutos alimentam araras, antas e gente. E o buriti mostra onde está a água: proteger as veredas é proteger as nascentes.',
   escala=('palmeira', 25, '25 m (pode chegar a 35)')),
 'cachorro-vinagre': dict(fontes=[42, 15], abre='Um canídeo pequeno, de pernas curtas e corpo comprido, que vive e caça em bando. É tão raro de ver que cada registro em armadilha fotográfica vira notícia.',
   fatos=[('Comprimento', 'de 50 a 75 cm de cabeça e corpo, mais 12 a 15 cm de cauda'), ('Peso', 'de 5 a 7 kg'), ('Come', 'pacas, cutias, tatus e outros bichos, que caça em grupo (as fontes divergem sobre o tamanho dos bandos)'), ('Situação', 'vulnerável na lista nacional')],
   reconhecer=['Pelagem marrom-avermelhada, mais escura nas patas e na cauda.', 'Orelhas pequenas e redondas, focinho curto.', 'Pernas curtas, quase um bassê do mato; nada bem e entra na água.'],
   importa='Depende de matas de galeria e cerradões ligados entre si, e some quando a paisagem fica picada em pedaços. Já foi filmado no Parque Nacional das Emas.',
   escala=(0.88, 0.3, '88 cm do focinho à ponta da cauda')),
 'capivara': dict(fontes=[43], abre='O maior roedor do mundo. Vive em grupos perto da água, passa as horas quentes dentro dela e mergulha para fugir dos predadores.',
   fatos=[('Comprimento', 'cerca de 1,3 m (de 1 a 1,5 m)'), ('Altura', 'até uns 60 cm'), ('Peso', 'de 50 a 80 kg; algumas fontes falam em até 100 kg'), ('Come', 'capins e plantas da beira da água')],
   reconhecer=['Corpo grande e arredondado, sem cauda à vista.', 'Cabeça quadrada, com olhos, orelhas e narinas no alto, para ficar de fora quando nada.', 'Patas com uma membrana entre os dedos.'],
   importa='É uma das presas principais da onça-pintada e da sucuri. Nas veredas e nas matas ciliares, onde há capivara há água o ano todo.',
   escala=(1.3, 0.6, '1,3 m de comprimento, 60 cm de altura')),
 'macaco-prego': dict(fontes=[44], abre='O macaco que usa ferramentas. No Cerrado do Piauí, os macacos-prego quebram cocos duros batendo com pedras sobre uma rocha, como num pilão.',
   fatos=[('Ferramentas', 'pedras de até 2 kg, usadas como martelo, na Fazenda Boa Vista (PI)'), ('Come', 'frutos, insetos e cocos de piaçava, catulé e tucum'), ('Acerto', 'cerca de 90% com os frutos menos duros'), ('Há quanto tempo', 'cerca de 3.000 anos de marcas de uso de pedras na Serra da Capivara (PI)')],
   reconhecer=['Macaco de porte médio, de pelagem marrom-amarelada.', 'Um tufo de pelos escuros no alto da cabeça, como um topete.', 'Cauda forte, que ajuda a segurar nos galhos.'],
   importa='É um dos poucos animais que usam ferramentas na natureza, e os sítios onde quebra cocos são estudados como uma espécie de arqueologia dos macacos. Também espalha sementes dos frutos que come.',
   escala=None),
 'coruja-buraqueira': dict(fontes=[45], abre='A coruja que mora no chão. Fica de pé na entrada da toca, de dia, e vira a cabeça para vigiar o campo.',
   fatos=[('Tamanho', 'de 22 a 28 cm'), ('Peso', 'cerca de 150 g'), ('Casa', 'tocas no chão, muitas vezes as que os tatus abandonam; também cava a própria'), ('Quando aparece', 'de dia e à noite; evita o calor do meio-dia')],
   reconhecer=['Pequena, marrom com pintas claras, de pernas compridas para uma coruja.', 'Olhos amarelos e sobrancelhas brancas.', 'Balança o corpo e pia alto quando alguém chega perto da toca.'],
   importa='Come muitos insetos e pequenos roedores. É fácil de ver nos campos e nas beiras de estrada, e por isso é uma ótima porta de entrada para quem começa a observar aves.',
   escala=(0.15, 0.25, '25 cm de altura')),
 'cascavel': dict(fontes=[46], abre='A cobra do chocalho. Antes de se defender, ela avisa: levanta a cauda e faz o guizo chiar.',
   fatos=[('Comprimento', 'em geral até 1,5 m, podendo passar disso'), ('No Brasil', 'é a única espécie de cascavel'), ('Veneno', 'age sobre os nervos e os músculos: picada é caso de soro, no hospital'), ('Onde vive', 'campos e cerrados abertos, mais secos')],
   reconhecer=['Um chocalho (guizo) de anéis secos na ponta da cauda.', 'Corpo grosso, marrom ou cinza, com desenhos de losangos claros no dorso.', 'Cabeça triangular, mais larga que o pescoço.'],
   importa='Come roedores e ajuda a controlar as populações deles. Não ataca à toa: quase todas as picadas acontecem quando alguém pisa nela ou põe a mão onde não vê. Use botas e não tente pegar.',
   escala=(1.5, 0.08, '1,5 m de comprimento')),
 'vaga-lume-cupinzeiro': dict(fontes=[47], abre='Os cupinzeiros que brilham. Nas noites quentes e úmidas da primavera, as larvas deste vaga-lume acendem luzes verdes nos túneis dos cupinzeiros das Emas.',
   fatos=[('Quem brilha', 'as larvas, dentro de túneis na parede dos cupinzeiros'), ('Para quê', 'a luz atrai insetos, que as larvas comem'), ('Quando', 'nas noites quentes e úmidas da primavera, com as primeiras chuvas'), ('Onde', 'famoso no Parque Nacional das Emas (GO)')],
   reconhecer=['Pontinhos de luz verde fixos, espalhados num cupinzeiro de campo.', 'A luz fica parada, sem piscar como a dos vaga-lumes que voam.', 'Só se vê em noite escura, longe das luzes da cidade.'],
   importa='O espetáculo está ficando mais raro, e os pesquisadores ligam isso às lavouras que cercam o parque. Para ver, só com guia credenciado e sem lanterna apontada para os cupinzeiros.',
   escala=None),
 'lobeira': dict(fontes=[48], abre='A fruta-do-lobo. Um arbusto de folhas largas e frutos grandes e verdes, que o lobo-guará come tanto que ganhou o nome dele.',
   fatos=[('Para o lobo-guará', 'cerca de um terço da dieta, num estudo da USP'), ('A dieta do lobo', 'mais ou menos metade frutos e metade bichos'), ('Fruto', 'grande, redondo e verde, com muitas sementes'), ('Onde cresce', 'campos sujos, cerrados e beiras de estrada')],
   reconhecer=['Folhas grandes, acinzentadas e cobertas de pelos, com espinhos no caule.', 'Flores roxas, em forma de estrela, com o miolo amarelo.', 'Frutos verdes do tamanho de uma laranja grande, caídos no chão.'],
   importa='O lobo-guará come o fruto e espalha as sementes nas fezes, longe da planta-mãe: os dois dependem um do outro. A lobeira também é uma das primeiras plantas a voltar em áreas abertas.',
   escala=None),
 'cagaita': dict(fontes=[49, 19], abre='Uma árvore que floresce quase sem folhas, com a copa toda branca, e dá uma fruta amarela, ácida e suculenta no começo das chuvas.',
   fatos=[('Altura', 'até uns 10 m'), ('Flores', 'brancas, cobrindo a copa quase sem folhas, no fim da seca'), ('Frutos', 'amadurecem com as primeiras chuvas, em poucas semanas'), ('Usos', 'comida fresca, em suco, sorvete e geleia')],
   reconhecer=['Tronco tortuoso, de casca grossa e cheia de sulcos.', 'Frutos amarelo-claros, redondos e lisos, do tamanho de uma ameixa.', 'Na florada, a árvore inteira fica branca por poucos dias.'],
   importa='O nome científico avisa: comida em excesso, ou caída e fermentada, solta o intestino. Os frutos alimentam muitos bichos e são renda para quem coleta na safra.',
   escala=('arvore', 10, 'até uns 10 m')),
 'capim-dourado': dict(fontes=[50], abre='A haste que brilha como ouro. Colhido nos campos úmidos do Jalapão, no Tocantins, vira bolsas, chapéus e bijuterias costuradas com seda de buriti.',
   fatos=[('Colheita', 'de 20 de setembro a 30 de novembro, só com as hastes secas'), ('Quem colhe', 'só artesãos credenciados; cerca de 400 têm autorização do Naturatins'), ('Regras', 'portaria do Naturatins de 2007 e uma lei estadual de 2019 (as fontes divergem nos detalhes)'), ('Onde', 'campos úmidos e beiras de vereda')],
   reconhecer=['Hastes finas e douradas, de uns palmos de altura, com uma florzinha branca na ponta.', 'Folhas em roseta, rentes ao chão.', 'Cresce em campos úmidos, perto das veredas.'],
   importa='A colheita na época certa, depois de as sementes caírem, deixa o capim se renovar. É o artesanato que deu renda e fama às comunidades quilombolas do Jalapão, como a Mumbuca.',
   escala=None),
 'onca-parda': dict(fontes=[51, 15], abre='O segundo maior felino do Brasil, também chamado de suçuarana ou puma. Anda muito, ocupa quase todas as paisagens e aparece até perto de cidades.',
   fatos=[('Comprimento', 'de 1,5 a 2,75 m, com a cauda'), ('Peso', 'de 40 a 72 kg os machos e de 34 a 48 kg as fêmeas'), ('Come', 'veados, capivaras, tatus, pacas e outros bichos de porte médio'), ('Quando aparece', 'sozinha, mais ao anoitecer e à noite')],
   reconhecer=['Pelagem lisa, de marrom-claro a acinzentado, sem pintas (os filhotes nascem pintados).', 'Cabeça pequena para o corpo e cauda longa, de ponta escura.', 'Pegadas redondas, sem marca de unha.'],
   importa='Precisa de áreas enormes e se desloca pelas matas de galeria entre os fragmentos. Atropelamentos e conflitos com criadores são as maiores ameaças; na lista nacional, as populações ameaçadas estão como vulneráveis.',
   escala=(2.1, 0.7, '2,1 m do focinho à ponta da cauda')),
 'tamandua-mirim': dict(fontes=[52], abre='O primo menor do tamanduá-bandeira. Sobe em árvores, segura-se com a cauda e, quando se sente ameaçado, fica de pé e abre os braços com as garras à mostra.',
   fatos=[('Corpo', 'de 47 a 77 cm, mais 40 a 68 cm de cauda'), ('Peso', 'de uns 3,5 a 8,5 kg (as fontes divergem)'), ('Come', 'formigas e cupins, que pega com a língua comprida'), ('Quando aparece', 'mais à noite; de dia, também, nas árvores')],
   reconhecer=['Pelagem amarelada com uma mancha preta nas costas, como um colete.', 'Focinho comprido e fino, olhos pequenos.', 'Cauda pelada por baixo, que se enrola nos galhos.'],
   importa='Controla formigas e cupins nas árvores e no chão. Vive nas bordas de mata e no cerradão, e morre muito atropelado nas estradas.',
   escala=(1.1, 0.35, '1,1 m com a cauda')),
 'jaguatirica': dict(fontes=[53], abre='O maior dos gatos-do-mato. Pintada como uma onça em miniatura, caça à noite nas matas de galeria e no cerradão.',
   fatos=[('Corpo', 'de 70 a 100 cm, mais uma cauda de uns 40 cm'), ('Peso', 'de 8 a 15 kg, com média de 11 kg num estudo'), ('Come', 'roedores, gambás, aves, lagartos e outros bichos pequenos'), ('Quando aparece', 'à noite; de dia, descansa em galhos ou em moitas')],
   reconhecer=['Manchas em forma de correntes e rosetas compridas, que se juntam em faixas.', 'Cauda mais curta que a dos outros gatos-do-mato, mais ou menos do comprimento das patas de trás.', 'Do tamanho de um cachorro médio.'],
   importa='Precisa de mata contínua e sofre com o desmatamento e com a caça. Por ser carnívora de topo entre os bichos pequenos, controla roedores e outras presas.',
   escala=(1.25, 0.45, '1,25 m com a cauda')),
 'carcara': dict(fontes=[54], abre='A ave de rapina que anda no chão. Come de tudo, segue tratores e queimadas atrás de bichos que fogem, e não tem medo de gente.',
   fatos=[('Tamanho', 'de 50 a 65 cm'), ('Asas abertas', 'até cerca de 1,3 m'), ('Peso', 'de uns 800 g a 1,6 kg, conforme a região e o sexo'), ('Come', 'insetos, lagartos, cobras, filhotes, carniça e até frutos')],
   reconhecer=['Um boné preto no alto da cabeça e o rosto pelado, vermelho ou alaranjado.', 'Peito claro e listrado, corpo escuro.', 'Anda pelo chão com passos largos, como uma galinha grande.'],
   importa='É um dos faxineiros do Cerrado: limpa carniça e come muitos bichos que viram praga. É fácil de ver e muito comum nas beiras de estrada.',
   escala=(0.3, 0.56, '56 cm')),
 'teiu': dict(fontes=[55], abre='O maior lagarto do Cerrado. Ativo na primavera e no verão, passa o outono e o inverno enterrado numa toca, quase sem se mexer.',
   fatos=[('Comprimento', 'até 1,5 m, com a cauda'), ('Peso', 'pode passar de 4 kg; os machos são maiores'), ('Inverno', 'de três a cinco meses parado na toca, num estado parecido com a hibernação'), ('Come', 'de tudo: frutos, ovos, insetos, pequenos bichos e carniça')],
   reconhecer=['Corpo preto com faixas e pintas brancas ou amareladas.', 'Língua comprida e bifurcada, que ele põe para fora o tempo todo.', 'Cauda grossa e longa, com anéis claros e escuros.'],
   importa='Come muitos frutos e espalha as sementes. Se encontrar um teiú parado no frio, não acorde: ele está gastando o mínimo de energia para chegar à primavera.',
   escala=(1.5, 0.2, '1,5 m de comprimento')),
 'jiboia': dict(fontes=[56], abre='Uma cobra grande e sem veneno. Mata a presa apertando, com o corpo enrolado, e é muito mais tímida do que perigosa.',
   fatos=[('Comprimento', 'em geral de 2 a 3 m; algumas chegam a 4 m'), ('Veneno', 'não tem: mata por constrição'), ('Come', 'roedores, aves e lagartos'), ('Filhotes', 'nascem prontos, sem ovo')],
   reconhecer=['Desenhos grandes e escuros nas costas, como selas, sobre um fundo bege ou acinzentado.', 'Cauda com manchas avermelhadas.', 'Cabeça com uma listra escura que passa pelo olho.'],
   importa='Controla ratos e outros roedores, inclusive perto das casas. Muitas jiboias morrem por serem confundidas com cobras venenosas: na dúvida, não mate, chame os bombeiros.',
   escala=(2.5, 0.1, '2,5 m (o comum é 2 a 3 m)')),
 'mangaba': dict(fontes=[57, 19], abre='A árvore do leite branco. Corte uma folha e sai látex; os frutos, pintadinhos, só ficam bons de comer quando caem maduros.',
   fatos=[('Altura', 'muda muito: de arvoreta a árvore de até uns 15 m'), ('Safra', 'no Cerrado, em geral de outubro a dezembro'), ('Fruto', 'em média uns 32 g, de casca amarela com manchas avermelhadas'), ('Látex', 'a árvore dá menos leite quando está carregada de frutos')],
   reconhecer=['Folhas lisas e brilhantes, que soltam leite branco quando quebram.', 'Galhos tortuosos e pendentes.', 'Frutos redondos e pequenos, com pintas vermelhas quando maduros.'],
   importa='A mangaba vira suco, sorvete e doce, e a coleta é renda para muitas mulheres do Cerrado e do Nordeste. A fruta verde tem leite que amarga: espere cair.',
   escala=None),
 'jatoba': dict(fontes=[58], abre='Dentro da vagem dura, uma farinha amarela e doce, de cheiro forte. É comida antiga do sertão, que hoje vira bolo, pão e mingau.',
   fatos=[('Altura', 'até uns 10 m'), ('Fruto', 'uma vagem marrom, dura e grossa, cheia de polpa farinácea'), ('Usos', 'a farinha da polpa, que a Embrapa Cerrados estudou para pães e bolos'), ('Madeira', 'dura e pesada')],
   reconhecer=['Folhas com dois folíolos iguais, como asas de borboleta.', 'Vagens marrom-escuras penduradas ou caídas embaixo da árvore.', 'Tronco de casca grossa, que solta uma resina.'],
   importa='Os frutos alimentam pacas, cutias e outros bichos, que enterram as sementes e plantam novos jatobás. Para as comunidades, a farinha é uma das comidas da seca.',
   escala=('arvore', 10, 'até uns 10 m')),
 'macauba': dict(fontes=[59], abre='A palmeira do óleo. Tem espinhos no tronco e nas folhas e cachos de cocos amarelados, que dão óleo na polpa e na amêndoa.',
   fatos=[('Altura', 'pode chegar a 15 m, com o tronco de 20 a 30 cm de largura'), ('Óleo', 'da polpa e da amêndoa, que tem cerca de 50% de óleo'), ('Espinhos', 'escuros e pontudos; a quantidade muda de uma população para outra'), ('Usos', 'óleo, farinha da polpa, ração e o palmito')],
   reconhecer=['Tronco reto com espinhos pretos, às vezes coberto pela base das folhas velhas.', 'Folhas compridas e arqueadas, com folíolos em vários planos.', 'Cachos grandes de cocos redondos, verdes e depois amarelados.'],
   importa='É estudada pela Embrapa como fonte de óleo para alimento e combustível, plantada junto com pasto. Os cocos alimentam araras e outros bichos na seca.',
   escala=('palmeira', 15, 'até uns 15 m')),
 'cachorro-do-mato': dict(fontes=[60], abre='O canídeo mais comum do Cerrado. Anda em casal, sai ao anoitecer e come de tudo, de frutos a insetos, e por isso se vira até perto de fazendas e estradas.',
   fatos=[('Comprimento', 'uns 65 cm de corpo, mais uns 30 cm de cauda'), ('Peso', 'de 5 a 8 kg'), ('Come', 'frutos, insetos, caranguejos, sapos, lagartos, pequenos mamíferos, aves e ovos'), ('Quando aparece', 'ao anoitecer e à noite, quase sempre em dupla')],
   reconhecer=['Pelagem cinza-amarelada, com as patas e a ponta da cauda escuras.', 'Focinho curto e orelhas médias, de bordas escuras.', 'Menor e mais baixo que o lobo-guará, sem as pernas compridas dele.'],
   importa='Espalha as sementes dos frutos que come. É um dos bichos que mais morrem atropelados nas estradas do Cerrado, e às vezes pega doenças dos cachorros domésticos.',
   escala=(0.95, 0.4, '95 cm com a cauda')),
 'tatu-peba': dict(fontes=[61], abre='O tatu peludo dos campos. Tem pelos claros saindo do casco, cava muito rápido e anda de dia, coisa rara entre os tatus.',
   fatos=[('Comprimento', 'de 40 a 95 cm de corpo, mais 12 a 24 cm de cauda (as fontes divergem)'), ('Peso', 'de uns 3 a 7 kg'), ('Come', 'de tudo: raízes, frutos, insetos, pequenos bichos e carniça'), ('Quando aparece', 'de dia, mais de manhã e à tarde')],
   reconhecer=['Casco amarelado ou marrom-claro, com pelos claros e compridos entre as placas.', 'Seis ou sete cintas móveis no meio do casco.', 'Focinho largo e orelhas pequenas.'],
   importa='Revira o solo atrás de comida e abre tocas que outros bichos usam. É dos tatus mais caçados, mas ainda é comum em boa parte do Cerrado.',
   escala=None),
 'quati': dict(fontes=[62], abre='O bicho do focinho comprido e da cauda listrada em pé. As fêmeas e os filhotes andam em bandos, revirando o chão e os troncos atrás de comida.',
   fatos=[('Comprimento', 'de 85 cm a 1,1 m, com a cauda; a cauda é quase a metade'), ('Peso', 'de 2 a 7 kg (algumas fontes falam em até 10)'), ('Bandos', 'de fêmeas e jovens, que podem chegar a 30; os machos adultos andam mais sozinhos'), ('Come', 'insetos, frutos, ovos e pequenos bichos')],
   reconhecer=['Focinho longo e móvel, que fuça a terra e as folhas.', 'Cauda comprida, com anéis claros e escuros, que fica em pé quando anda.', 'Pelagem de marrom-avermelhada a acinzentada.'],
   importa='Come muitos frutos e espalha as sementes; revira o chão da mata atrás de insetos. Não dê comida: quatis acostumados com gente mordem e ficam doentes.',
   escala=(1.0, 0.35, '1 m com a cauda')),
 'sagui': dict(fontes=[63], abre='O macaquinho de tufos pretos nas orelhas, comum até nas praças das cidades do Cerrado. Faz furinhos nas árvores para comer a goma que escorre.',
   fatos=[('Peso', 'cerca de 250 g'), ('Come', 'principalmente goma de árvores; também frutos, insetos e ovos'), ('Dentes', 'os da frente são feitos para raspar a casca e fazer a goma escorrer'), ('Onde vive', 'só no Brasil, sobretudo no Cerrado')],
   reconhecer=['Tufos de pelos pretos e compridos na frente das orelhas.', 'Uma mancha branca na testa.', 'Cauda comprida, com anéis claros e escuros.'],
   importa='Fora do Cerrado, onde foi solto por gente, vira um problema: compete com outros saguis da Mata Atlântica e cruza com eles. No Cerrado, é bicho de casa. Não dê comida.',
   escala=None),
 'lontra': dict(fontes=[64], abre='A nadadora dos rios limpos. Caça peixes nos rios e córregos com mata na beira, e onde ela aparece o rio está bem.',
   fatos=[('Comprimento', 'de 53 a 80 cm de corpo, mais 36 a 50 cm de cauda'), ('Peso', 'de 5 a 14 kg; os machos são maiores'), ('Come', 'principalmente peixes, e também caranguejos e moluscos'), ('Situação', 'quase ameaçada no Brasil, segundo o ICMBio')],
   reconhecer=['Corpo comprido e baixo, marrom-escuro e brilhante quando molhado.', 'Garganta e peito mais claros.', 'Patas com membranas e cauda grossa e achatada na ponta.'],
   importa='Precisa de água limpa, de peixes e de mata nas margens. Barragens, esgoto e desmatamento das matas ciliares a fazem sumir.',
   escala=(1.1, 0.3, '1,1 m com a cauda')),
 'urubu-rei': dict(fontes=[65, 141], abre='O maior e mais colorido dos urubus. Branco e preto, com a cabeça pelada em laranja, roxo e vermelho, plana alto sobre as matas atrás de carcaças.',
   fatos=[('Asas abertas', 'de 1,7 a quase 2 m'), ('Peso', 'de 3 a 5 kg'), ('Comprimento', 'de uns 70 a 85 cm'), ('Come', 'carniça; costuma chegar depois dos urubus comuns, que acham a carcaça pelo cheiro'), ('Situação', 'menos preocupante no Brasil, segundo o ICMBio; vive em todos os biomas menos o Pampa')],
   reconhecer=['Corpo branco-creme e asas com as pontas pretas.', 'Cabeça e pescoço pelados, com cores fortes e uma carúncula laranja no bico.', 'Plana alto, quase sem bater as asas.'],
   importa='É um faxineiro: come carcaças grandes e evita que as doenças se espalhem. Precisa de mata alta para descansar e fazer o ninho, e por isso é raro de ver.',
   escala=None),
 'papagaio-verdadeiro': dict(fontes=[66], abre='O papagaio mais conhecido do Brasil, de testa azul e rosto amarelo. Também é o mais tirado da natureza para o comércio ilegal.',
   fatos=[('Tamanho', 'cerca de 36 cm'), ('Peso', 'cerca de 400 g'), ('Vida', 'na natureza, em média 60 anos, podendo chegar a 80'), ('Situação', 'quase ameaçado, segundo o ICMBio; dos mais apreendidos no tráfico')],
   reconhecer=['Verde, com a testa azul e o rosto amarelo (o desenho muda de uma ave para outra).', 'Mancha vermelha no ombro da asa.', 'Voa em casais ou em bandos, gritando alto, ao amanhecer e ao fim da tarde.'],
   importa='Os traficantes tiram ovos e filhotes dos ninhos, e cada ninho perdido é uma geração a menos. Papagaio não é bicho de casa: compre só de criadouro legalizado, ou não compre.',
   escala=(0.15, 0.36, '36 cm')),
 'papagaio-galego': dict(fontes=[67], abre='Um papagaio de cabeça amarela que vive quase só no Cerrado. Faz o ninho dentro de cupinzeiros.',
   fatos=[('Ninho', 'cavidades dentro de cupinzeiros'), ('Ovos', 'chocados de 19 a 22 dias; os filhotes ficam até 45 dias no ninho'), ('Come', 'sementes, frutos e flores de muitas plantas do Cerrado'), ('Situação', 'quase ameaçado no mundo; já foi dado como sumido em São Paulo')],
   reconhecer=['Cabeça e rosto amarelos, corpo verde.', 'Barriga com manchas alaranjadas e amarelas.', 'Menor que o papagaio-verdadeiro, sem a testa azul.'],
   importa='É uma das aves que só existem no Cerrado. Depende dos campos e cerrados abertos com cupinzeiros, que estão virando lavoura e pasto.',
   escala=None),
 'gralha-do-campo': dict(fontes=[147, 68], abre='Azul, branca e de topete, anda em grupos barulhentos pelo cerrado. É uma das aves mais típicas do bioma.',
   fatos=[('Tamanho', 'de 33 a 40 cm (as fontes divergem)'), ('Peso', 'cerca de 180 g'), ('Come', 'de tudo: insetos, frutos, ovos e pequenos bichos'), ('Machos e fêmeas', 'iguais, sem diferença de cor'), ('Ninhos alheios', 'em Águas Emendadas (DF), foi a principal predadora dos ninhos de outras aves')],
   reconhecer=['Um topete de penas na testa, enrolado para a frente.', 'Corpo azul-escuro, garganta preta, barriga e ponta da cauda brancas.', 'Grita alto e anda em grupo, pulando de árvore em árvore.'],
   importa='Como come muitos frutos, espalha sementes pelo cerrado. É fácil de ver e de ouvir, e boa para começar a observar aves.',
   escala=(0.15, 0.35, '33 a 40 cm')),
 'pica-pau-do-campo': dict(fontes=[69], abre='Um pica-pau que vive no chão. Em vez de bicar troncos, procura formigas e cupins nos campos, muitas vezes em grupo.',
   fatos=[('Tamanho', 'cerca de 32 cm'), ('Come', 'formigas, cupins e larvas de besouro; nas Emas, já foi visto comendo frutos'), ('Ninho', 'cavado em barrancos e às vezes em cupinzeiros'), ('Onde vive', 'campos, pastos e beiras de estrada')],
   reconhecer=['Cabeça e peito amarelos, com o alto da cabeça preto.', 'Costas listradas de preto e branco.', 'Pousa no chão e em mourões de cerca, não só em árvores.'],
   importa='Come muitos cupins e formigas. É uma ave dos campos abertos, que aproveita até os pastos, e é das mais fáceis de ver no Cerrado.',
   escala=(0.12, 0.32, '32 cm')),
 'beija-flor-tesoura': dict(fontes=[146, 70], abre='Um beija-flor grande, azul e verde, com a cauda aberta em tesoura. Briga pelas flores: expulsa os outros beija-flores do canteiro dele.',
   fatos=[('Tamanho', 'de 15 a 18 cm (as fontes divergem); quase a metade é a cauda'), ('Peso', 'até uns 9 g'), ('Come', 'néctar de flores e pequenos insetos'), ('Fêmeas', 'um pouco menores e mais opacas que os machos')],
   reconhecer=['Cabeça e peito azul-violeta brilhante, corpo verde.', 'Cauda comprida, escura e funda, aberta como uma tesoura.', 'Faz um "tic" seco quando se agita.'],
   importa='Poliniza muitas flores do Cerrado. Por ser grande, domina os bebedouros e as floradas; é comum nos jardins das cidades.',
   escala=(0.16, 0.06, '15 a 17 cm')),
 'curicaca': dict(fontes=[71], abre='Uma ave de bico longo e curvo, que enfia no chão atrás de larvas. O grito alto, em dupla, se ouve de longe pelos campos.',
   fatos=[('Tamanho', 'cerca de 70 cm de comprimento e 40 cm de altura'), ('Come', 'larvas, gafanhotos, aranhas, centopeias, lagartixas, sapos e até pequenas cobras'), ('Onde vive', 'campos abertos, pastos e beiras de áreas úmidas'), ('Quando aparece', 'de dia, em casais ou pequenos grupos')],
   reconhecer=['Bico preto, longo e curvado para baixo.', 'Pescoço e cabeça cor de creme, corpo cinzento.', 'Asas com uma mancha branca que aparece em voo.'],
   importa='Come muitos insetos do solo. Bastante comum, é um dos sons mais típicos dos campos do Cerrado ao amanhecer.',
   escala=(0.7, 0.4, '70 cm de comprimento, 40 cm de altura')),
 'coral': dict(fontes=[72], abre='A cobra dos anéis coloridos. É venenosa, mas tímida e de boca pequena; quase todos os acidentes acontecem quando alguém a pega na mão.',
   fatos=[('Veneno', 'age sobre os nervos; picada é caso de hospital, com soro'), ('O soro', 'feito com o veneno da Micrurus frontalis e da M. corallinus'), ('Falsas-corais', 'imitam as cores e não são perigosas, mas não dá para ter certeza só olhando'), ('Come', 'outras cobras e lagartos sem pernas')],
   reconhecer=['Anéis vermelhos, pretos e brancos ou amarelos, que dão a volta no corpo.', 'Cabeça pequena e arredondada, olhos pequenos.', 'Vive escondida no chão, embaixo de folhas e pedras.'],
   importa='O Instituto Butantan avisa: não dá para separar a coral verdadeira da falsa a olho nu. Se encontrar uma, afaste-se e chame os bombeiros. As corais controlam outras cobras.',
   escala=None),
 'jabuti-piranga': dict(fontes=[73, 142], abre='A tartaruga de terra do Cerrado. Tem manchas vermelhas nas patas e na cabeça, anda devagar pelo chão da mata e come frutos caídos.',
   fatos=[('Casco', 'fica adulto com 20 a 25 cm; os machos maiores passam de 50 cm'), ('Come', 'frutos caídos, flores, folhas e às vezes carniça'), ('Vida', 'muito longa, de décadas'), ('Onde vive', 'cerradões, matas secas e bordas de mata'), ('Situação', 'muito tirado da natureza para ser bicho de estimação')],
   reconhecer=['Casco alto e escuro, com o centro de cada placa amarelado.', 'Escamas vermelhas ou alaranjadas nas patas e na cabeça.', 'Os machos têm a parte de baixo do casco funda, côncava.'],
   importa='Espalha sementes dos frutos que come. Criar jabuti sem autorização é crime, e quem solta na natureza um bicho de cativeiro pode levar doenças para os outros.',
   escala=None),
 'sapo-cururu': dict(fontes=[74], abre='O sapo grande das noites de chuva. Atrás dos olhos, tem glândulas que soltam um veneno leitoso quando ele é apertado ou mordido.',
   fatos=[('Veneno', 'nas glândulas atrás dos olhos (paratoides), para se defender'), ('Come', 'insetos, aranhas, lesmas e às vezes pequenos vertebrados'), ('Quando aparece', 'à noite, principalmente depois da chuva; de dia fica escondido'), ('Ovos', 'em cordões, na água parada')],
   reconhecer=['Grande e atarracado, de pele grossa e cheia de verrugas.', 'Duas glândulas grandes e saltadas atrás dos olhos.', 'Cor parda a acinzentada.'],
   importa='Come muitos insetos, inclusive perto das casas. Não faz mal a quem não o aperta, mas cachorros que mordem um cururu podem passar mal: leve ao veterinário.',
   escala=None),
 'dourado': dict(fontes=[143, 75], abre='O peixe dourado e forte dos grandes rios que nascem no Cerrado. Na piracema, sobe centenas de quilômetros rio acima para desovar.',
   fatos=[('Tamanho', 'passa de 1 m de comprimento; vive em águas rápidas'), ('Piracema', 'pode subir até 400 km, nadando uns 15 km por dia'), ('Come', 'outros peixes; é predador'), ('Ameaças', 'barragens no caminho da migração, pesca demais e mudanças nas cheias')],
   reconhecer=['Corpo dourado, mais forte nos adultos.', 'Listras escuras finas ao longo das escamas.', 'Mancha escura na cauda e boca grande, cheia de dentes.'],
   importa='Precisa de rios livres para subir e desovar: cada barragem sem passagem para peixes corta o caminho. Na piracema, a pesca é proibida.',
   escala=(1.1, 0.25, 'mais de 1 m')),
 'jatai': dict(fontes=[76], abre='Uma das abelhas sem ferrão mais comuns do Brasil. Pequena e amarela, faz a entrada da colmeia num tubinho de cera e tem soldadas na porta.',
   fatos=[('Tamanho', 'operárias de 4 a 5 mm'), ('Mel', 'de meio a um litro e meio por ano numa colônia forte'), ('Guardas', 'operárias de 10% a 30% maiores, que defendem a entrada'), ('Potes', 'o mel e o pólen ficam em potes de cera com 1,5 cm')],
   reconhecer=['Abelha muito pequena, amarelo-dourada, de olhos escuros.', 'Na entrada do ninho, um tubinho de cera clara com guardas paradas no ar.', 'Não pica: no máximo, enrosca no cabelo.'],
   importa='Poliniza muitas plantas nativas e de horta. É criada até nas cidades, e o mel, pouco e muito procurado, é renda para meliponicultores. Veja mais no site Abelhas sem Ferrão.',
   escala=None),
 'ipe-amarelo': dict(fontes=[144, 77], abre='A árvore que anuncia o fim da seca. Perde todas as folhas e floresce inteira em amarelo, por poucos dias, entre o inverno e a primavera.',
   fatos=[('Altura', 'de 4 a 14 m, no cerrado'), ('Floração', 'de julho a setembro, sem folhas'), ('Por que sem folhas', 'perder as folhas ajuda a árvore a gastar menos água na seca'), ('Espécies', 'vários ipês amarelos; no Cerrado, o mais comum é o Handroanthus ochraceus')],
   reconhecer=['Na florada, a copa toda amarela, sem nenhuma folha.', 'Fora da florada, folhas com cinco folíolos, como os dedos de uma mão.', 'Frutos compridos como vagens, que soltam sementes com asas.'],
   importa='Floresce quando há pouca comida, e as flores alimentam abelhas e beija-flores. É a árvore-símbolo do Brasil e enche as cidades do Cerrado de amarelo na seca.',
   escala=('arvore', 14, 'até 14 m')),
 'ipe-roxo': dict(fontes=[78], abre='O primeiro ipê a florescer na seca. Perde as folhas e se cobre de flores rosa-arroxeadas, antes dos ipês amarelos.',
   fatos=[('Altura', 'até uns 15 m na cidade; na mata, pode passar de 30 m'), ('Floração', 'de junho a agosto, no Distrito Federal'), ('Ordem', 'em Brasília, os roxos florescem primeiro, depois os amarelos e os brancos'), ('Madeira', 'dura e muito procurada')],
   reconhecer=['Copa rosa-arroxeada, sem folhas, no meio da seca.', 'Flores em forma de trombeta, com o miolo amarelado.', 'Folhas com cinco folíolos, quando as tem.'],
   importa='As flores alimentam abelhas e beija-flores numa época de pouca comida. A madeira valiosa fez muitos ipês serem derrubados na mata.',
   escala=('arvore', 15, 'até uns 15 m')),
 'araticum': dict(fontes=[79], abre='O parente da fruta-do-conde que cresce no cerrado. O fruto é grande, perfumado e pode pesar alguns quilos.',
   fatos=[('Altura', 'de 4 a 8 m'), ('Fruto', 'de meio quilo a mais de 4 kg, conforme a planta (as fontes divergem)'), ('Safra', 'de fevereiro a abril'), ('Polpa', 'amarelada, doce e de cheiro forte, com muitas sementes')],
   reconhecer=['Árvore baixa, de tronco tortuoso e casca grossa.', 'Folhas grandes e grossas, arredondadas.', 'Fruto grande, arredondado, coberto de pequenas saliências.'],
   importa='O fruto alimenta bichos e gente, e vira doce, sorvete e licor. Quase todo araticum vendido vem de coleta em áreas nativas.',
   escala=('arvore', 8, 'até 8 m')),
 'babacu': dict(fontes=[80], abre='A palmeira das quebradeiras de coco. Forma palmeirais imensos no norte do Cerrado, e cada coco, quebrado a machado, dá algumas amêndoas cheias de óleo.',
   fatos=[('Altura', 'até uns 20 m, com o tronco de até 41 cm de largura'), ('Amêndoa', 'só uns 7% do coco, mas com mais de 60% de óleo'), ('Produção', 'o Maranhão colhe mais de 90% das amêndoas do Brasil'), ('Usos', 'óleo, sabão, farinha do mesocarpo, carvão da casca e as folhas')],
   reconhecer=['Palmeira alta, de tronco liso e reto.', 'Folhas enormes, em pé e arqueadas, como penas.', 'Cachos pesados de cocos marrons e duros.'],
   importa='A quebra do coco sustenta milhares de famílias do Maranhão, do Piauí e do Tocantins, que lutam pelo direito de entrar nos babaçuais. É o movimento das quebradeiras de coco.',
   escala=('palmeira', 20, 'até 20 m')),
 'barbatimao': dict(fontes=[81], abre='A árvore da casca que cicatriza. A casca, cheia de taninos, é usada há muito tempo para lavar feridas, e virou até remédio oficial.',
   fatos=[('Altura', 'de 2 a 6 m'), ('Casca', 'de 20% a 30% de taninos, que dão a ação adstringente'), ('Remédio', 'está na Farmacopeia Brasileira, como creme cicatrizante'), ('Parte usada', 'a casca do tronco e dos galhos')],
   reconhecer=['Árvore baixa, de tronco tortuoso e casca áspera e cheia de fendas.', 'Folhas compostas, com muitos folíolos pequenos e redondos.', 'Flores pequenas, em espigas creme.'],
   importa='A procura pela casca faz muitas árvores serem descascadas até morrer. Tirar só uma faixa e deixar o tronco se recuperar mantém a planta viva. Remédio, só com orientação.',
   escala=('arvore', 6, 'até 6 m')),
 'pau-terra': dict(fontes=[82], abre='Uma das árvores mais comuns do cerrado, de flores amarelas grandes. Gosta do alumínio que deixa os solos do Cerrado ácidos: sem ele, cresce mal.',
   fatos=[('Altura', 'de arvoreta a árvore: no cerrado, em geral de 3 a 10 m; as maiores chegam perto de 30 m'), ('Onde vive', 'em quase 90% do Cerrado'), ('Alumínio', 'acumula alumínio nas folhas e precisa dele para crescer bem'), ('Nome', 'vem do tronco, de cor vermelho-castanha, cor de terra'), ('Flores', 'amarelas e grandes, na época das chuvas')],
   reconhecer=['Folhas grandes, opostas, com as nervuras bem marcadas.', 'Flores amarelas com uma pétala só, grande, e um esporão.', 'Frutos secos e lenhosos que se abrem em três partes.'],
   importa='Mostra como as plantas do Cerrado se adaptaram a solos pobres e ácidos, que para a maioria das plantas são venenosos.',
   escala=None),
 'canela-de-ema': dict(fontes=[83], abre='A planta das pedras do campo rupestre. O "tronco" é feito dos restos das folhas velhas, que protegem as raízes e guardam a umidade da neblina.',
   fatos=[('Tronco', 'bainhas de folhas velhas, por dentro das quais correm raízes'), ('Fogo', 'em algumas espécies, o fogo é o sinal para florescer, poucas semanas depois'), ('Tamanho', 'quase todas baixas; a Vellozia gigantea, da Serra do Cipó, chega a 6 m'), ('Espécies', 'cerca de 265 no gênero')],
   reconhecer=['Um tufo de folhas finas no alto de galhos grossos e fibrosos.', 'Cresce no meio das pedras, em lugares onde quase nada cresce.', 'Flores grandes, roxas, brancas ou amarelas, depois das queimadas.'],
   importa='É um símbolo dos campos rupestres. Muitas espécies existem só numa serra, e os pesquisadores consideram o gênero vulnerável às mudanças do clima.',
   escala=None),
 'sempre-viva': dict(fontes=[84], abre='Flores que secam sem perder a forma. Nos campos da Serra do Espinhaço, são colhidas há gerações para arranjos e artesanato.',
   fatos=[('Onde', 'a Serra do Espinhaço tem cerca de 80% das espécies de sempre-vivas do Brasil'), ('Quem colhe', 'seis comunidades de Diamantina, Buenópolis e Presidente Kubitschek'), ('Reconhecimento', 'patrimônio agrícola mundial da FAO desde 2020'), ('Em Minas', 'patrimônio imaterial do estado desde 2023')],
   reconhecer=['Hastes finas e longas, com uma cabecinha de flores no alto.', 'Flores secas e firmes, brancas ou douradas, que não murcham.', 'Crescem em campos de altitude, no meio das pedras e da areia branca.'],
   importa='As comunidades decidem quando e quanto colher, seguindo o ciclo de cada planta. É um dos poucos casos em que a coleta das flores ajudou a manter o campo de pé.',
   escala=None),
 'copaiba': dict(fontes=[85], abre='A árvore do óleo. Dentro do tronco há canais cheios de um óleo-resina, que se tira com um furo e é usado há muito tempo na medicina popular.',
   fatos=[('Altura', 'de menos de 2 m a uns 10 m no cerrado; nas matas, passa de 20 m'), ('Óleo', 'fica em canais dentro do tronco'), ('Coleta', 'com um trado, que fura o tronco e faz menos estrago'), ('Porte', 'nos campos rupestres, vira arbusto de pouco mais de 1 m')],
   reconhecer=['Folhas compostas, com folíolos pequenos e brilhantes, cheios de pontinhos claros contra a luz.', 'Tronco curto e tortuoso no cerrado.', 'Frutos pequenos com uma semente preta envolta numa capa laranja.'],
   importa='As sementes alimentam aves, que as espalham. A coleta do óleo é renda para muitas comunidades; furar e tampar o buraco deixa a árvore viva para outras coletas.',
   escala=('arvore', 10, 'até uns 10 m')),
 'sucupira-branca': dict(fontes=[86], abre='Uma árvore de flores lilás e frutos com asa. O óleo do fruto é usado na medicina popular para dor de garganta e reumatismo.',
   fatos=[('Altura', 'até uns 15 m; no cerradão, às vezes só 4 m'), ('Fruto', 'seco, com uma asa, e uma semente cheia de óleo no meio'), ('Uso popular', 'o óleo do fruto, misturado à água, para inflamação da garganta'), ('Nome', 'há espécies de Pterodon muito parecidas, que alguns autores juntam numa só')],
   reconhecer=['Na florada, a copa fica coberta de flores lilás.', 'Casca clara e lisa.', 'Frutos achatados com uma asa, que voam com o vento.'],
   importa='É uma das plantas medicinais mais procuradas do Cerrado. Os usos são da tradição popular: remédio, só com orientação.',
   escala=('arvore', 15, 'até uns 15 m')),
 'murici': dict(fontes=[87], abre='As frutinhas amarelas de cheiro forte. O murici é comido fresco, em doce, sorvete e licor, e é rico em vitamina A.',
   fatos=[('Altura', 'arvoreta de uns 2 m, que pode chegar a 5 m'), ('Fruto', 'pequeno, amarelo, de polpa pastosa e cheiro muito marcante'), ('Safra', 'a primeira de fevereiro a junho, segundo a Embrapa'), ('Nutrição', 'muito betacaroteno, de onde vem a vitamina A')],
   reconhecer=['Folhas grandes, ásperas e com pelos por baixo.', 'Cachos de flores amarelas que ficam alaranjadas.', 'Frutinhas amarelas redondas que caem e cheiram de longe.'],
   importa='O cheiro forte atrai bichos que comem os frutos e espalham as sementes. Coletado no cerrado, é renda e comida típica do Centro-Oeste e do Norte.',
   escala=None),
 'cajuzinho': dict(fontes=[88], abre='Um cajueiro anão. Quase toda a planta fica embaixo da terra, num tronco subterrâneo que guarda água e a protege do fogo; por cima, só galhos e cajuzinhos.',
   fatos=[('Altura', 'de 30 cm a 1,5 m'), ('Embaixo da terra', 'um tronco (não uma raiz), muito fundo, que guarda água para a seca'), ('Flores', 'de julho a setembro'), ('Frutos', 'de agosto a outubro')],
   reconhecer=['Um arbustinho no meio do campo, com folhas grossas.', 'Cajuzinhos amarelos ou vermelhos, do tamanho de uma uva grande.', 'A castanha cinza, em forma de rim, embaixo do caju.'],
   importa='O que se come é o "caju", que não é o fruto: o fruto verdadeiro é a castanha. É um exemplo de como as plantas do Cerrado guardam a maior parte do corpo embaixo da terra.',
   escala=None),
 'gabiroba': dict(fontes=[89], abre='A prima da goiaba que cresce baixinha nos campos. As frutinhas verde-amareladas são doces, perfumadas e ricas em vitamina C.',
   fatos=[('Altura', 'um arbusto baixo, de uns 60 a 80 cm, num estudo em Minas'), ('Fruto', 'bago redondo e achatado, amarelado, com 5 a 6 sementes pequenas'), ('Sabor', 'doce, com cheiro de fruta cítrica'), ('Nutrição', 'rica em vitamina C')],
   reconhecer=['Arbusto pequeno, de folhas com pelinhos.', 'Flores brancas com muitos estames, como as da goiabeira.', 'Frutinhas verdes que ficam amarelas quando maduras.'],
   importa='É comida de muitos bichos e de quem anda pelo cerrado. Há várias espécies de gabiroba, quase todas pouco estudadas e com potencial para virar fruta de pomar.',
   escala=None),
 'jenipapo': dict(fontes=[90], abre='A fruta que serve para pintar. O sumo do fruto verde, misturado a carvão, vira a tinta preta-azulada com que muitos povos indígenas pintam o corpo.',
   fatos=[('Nome', 'do tupi: fruta que serve para pintar'), ('A tinta', 'a genipina do fruto verde reage com a pele e o ar e fica azul-escura'), ('Quanto dura', 'cerca de duas semanas na pele'), ('Fruto maduro', 'mole e de cheiro forte, vira doce e licor')],
   reconhecer=['Árvore de tronco reto, nas matas da beira dos rios.', 'Folhas grandes, opostas, juntas na ponta dos galhos.', 'Frutos redondos, marrons, de casca fina e polpa com muitas sementes.'],
   importa='É uma das plantas mais ligadas às culturas indígenas do Brasil. A genipina interessa à indústria como um corante azul natural.',
   escala=None),
 'guariroba': dict(fontes=[91], abre='A palmeira do palmito amargo. Em Goiás, a guariroba vai para o arroz, o empadão e a galinhada, e já é vendida em conserva.',
   fatos=[('Altura', 'pode chegar a 20 m'), ('Palmito', 'amargo por causa de compostos fenólicos, e com mais vitamina C que outros palmitos'), ('Onde', 'muito plantada e usada em Goiás'), ('Cultivo', 'a Embrapa testou plantá-la junto com arroz, milho e árvores')],
   reconhecer=['Palmeira de tronco único, reto e acinzentado.', 'Folhas compridas e arqueadas, com folíolos em grupos.', 'Cachos de coquinhos amarelados.'],
   importa='É uma das comidas que mais marcam a cozinha goiana. Plantar guariroba alivia a coleta nas palmeiras nativas, que morrem quando se tira o palmito.',
   escala=('palmeira', 20, 'até 20 m')),
 'faveiro': dict(fontes=[92], abre='A árvore das favas dos remédios. As vagens têm rutina, uma substância usada pela indústria de remédios e cosméticos, e toda ela vem da coleta no cerrado.',
   fatos=[('Altura', 'de 8 a 14 m, com o tronco de 30 a 50 cm'), ('Rutina', 'as favas do faveiro e da fava-d’anta, sua parente, dão perto de metade da rutina do mundo'), ('Coleta', 'só das favas maduras, pela cor e pelo tamanho'), ('Cultivo', 'não há plantio estabelecido: tudo vem do extrativismo')],
   reconhecer=['Árvore de copa aberta, com folhas compostas de muitos folíolos pequenos.', 'Flores amarelas, em espigas.', 'Vagens grossas, achatadas e marrons quando maduras.'],
   importa='É renda para muitas famílias do Cerrado. Colher as favas verdes ou quebrar os galhos prejudica as árvores; a coleta cuidadosa mantém a renda nos anos seguintes.',
   escala=('arvore', 14, 'até 14 m')),
 'chuveirinho': dict(fontes=[93], abre='Uma sempre-viva de flores brancas que se abrem no alto de várias hastes, como a ducha de um chuveiro. Faz parte de um grupo com muitas espécies que só existem numa serra.',
   fatos=[('Família', 'Eriocaulaceae, a família das sempre-vivas'), ('Gênero', 'Paepalanthus, com cerca de 256 espécies'), ('Endemismo', 'muitas espécies só existem no alto de uma única serra'), ('Na Canastra', '19 espécies de Paepalanthus registradas na Serra da Canastra')],
   reconhecer=['Muitas hastes finas saindo do mesmo ponto, como as varetas de um guarda-chuva.', 'Uma cabecinha branca de flores na ponta de cada haste.', 'Folhas em roseta, rentes ao chão.'],
   importa='Algumas espécies são colhidas para artesanato, como o botão-branco de Diamantina. Como muitas vivem numa área pequena, a coleta demais ou uma mineração pode acabar com uma espécie.',
   escala=None),
 'lixeira': dict(fontes=[94], abre='A árvore das folhas de lixa. As folhas são tão ásperas, por causa da sílica, que já foram usadas para polir madeira.',
   fatos=[('Altura', 'em geral de 6 a 10 m, mas há de 1 a 12 m'), ('Aspereza', 'vem de pelos e grãos de sílica nas folhas, que aumentam com a idade'), ('Uso antigo', 'as folhas como papel de lixa'), ('Onde vive', 'cerrados abertos, de solo pobre')],
   reconhecer=['Folhas grandes, duras e muito ásperas nos dois lados.', 'Tronco tortuoso, de casca que solta em placas.', 'Frutinhos que se abrem mostrando sementes com uma capa branca.'],
   importa='É uma das árvores mais típicas do cerrado aberto, e as sementes alimentam muitas aves.',
   escala=('arvore', 10, 'até uns 10 m')),
 'pau-santo': dict(fontes=[95], abre='A árvore de casca de cortiça. A casca grossa e macia protege o tronco do fogo, e as flores brancas, perfumadas, abrem no meio da seca.',
   fatos=[('Porte', 'de arbusto de 1,5 m a arvoreta de uns 3 m'), ('Casca', 'uma cortiça com cerca de 28% de suberina, a mesma substância da rolha'), ('Flores', 'brancas, com cinco pétalas e estames amarelos'), ('Gênero', 'Kielmeyera, com quase 50 espécies no Brasil')],
   reconhecer=['Tronco e galhos com casca grossa, macia e cheia de sulcos, como rolha.', 'Folhas grossas e duras, no fim dos galhos.', 'Frutos secos que se abrem soltando sementes com asas.'],
   importa='A cortiça do pau-santo é estudada como alternativa à cortiça de Portugal. É um bom exemplo de como as árvores do Cerrado se protegem do fogo.',
   escala=None),
 'cupim-de-montículo': dict(fontes=[96], abre='O arquiteto dos campos. Ergue os cupinzeiros duros que pontilham os campos do Cerrado, e cada um vira um prédio de muitos moradores.',
   fatos=[('Altura do cupinzeiro', 'em geral de 60 cm a 1,2 m; alguns passam de 1,5 m'), ('Largura', 'pode passar de 1 m na base'), ('Onde', 'é a espécie dominante dos campos do Brasil Central'), ('Come', 'capim seco e restos de plantas, que reciclam no solo')],
   reconhecer=['Montes de terra dura, arredondados, espalhados pelo campo.', 'Por dentro, galerias e câmaras cheias de cupins claros.', 'Soldados de cabeça escura e grande defendem os buracos quando o monte é aberto.'],
   importa='É uma espécie-chave: os cupinzeiros dão abrigo e comida a formigas, lagartos, cobras, corujas, papagaios-galegos e às larvas dos vaga-lumes que brilham nas Emas. Também devolvem nutrientes ao solo.',
   escala=(1.15, 1.5, '1,5 m de altura')),
 'queixada': dict(fontes=[97], abre='O porco-do-mato dos bandos enormes. Anda em grupos de dezenas a centenas, bate os dentes quando se assusta e precisa de grandes áreas de mata e água.',
   fatos=[('Comprimento', 'cerca de 1 m'), ('Peso', 'por volta de 30 kg'), ('Bandos', 'de 50 a 300 animais no Pantanal; os maiores de todos os ungulados'), ('Situação', 'vulnerável na lista nacional')],
   reconhecer=['Pelagem escura, quase preta, com o queixo e a boca brancos.', 'Anda em bando fechado, e o barulho dos dentes batendo se ouve de longe.', 'Cheiro forte, que fica no caminho por onde o bando passou.'],
   importa='Os bandos reviram o chão, comem e espalham sementes, e são comida da onça-pintada. Some primeiro onde há caça e desmatamento; o Parque Nacional das Emas é um dos refúgios no Cerrado.',
   escala=(1.0, 0.5, '1 m de comprimento')),
 'cateto': dict(fontes=[98], abre='O porco-do-mato menor, também chamado de caititu. Tem um colar claro em volta do pescoço e anda em grupos pequenos.',
   fatos=[('Peso', 'de uns 14 a 30 kg (as fontes divergem)'), ('Grupos', 'em média de 6 a 9 animais, podendo chegar a uns 30'), ('Come', 'frutos, raízes, sementes e pequenos bichos'), ('Diferença', 'menor que a queixada e em grupos muito menores')],
   reconhecer=['Pelagem cinzenta e salpicada, com uma faixa clara do pescoço até o peito, como um colar.', 'Focinho de porco e pernas finas.', 'Ouriça os pelos das costas quando está nervoso.'],
   importa='Espalha sementes e revira o solo. Aguenta melhor que a queixada as matas pequenas, e por isso ainda é comum em muitos lugares.',
   escala=None),
 'veado-catingueiro': dict(fontes=[99], abre='O veado mais comum do Cerrado, pequeno e acinzentado. Vive sozinho, na beira das matas e nos cerrados, e some num salto quando percebe gente.',
   fatos=[('Altura', 'cerca de 50 cm no ombro'), ('Peso', 'em geral de 17 a 23 kg'), ('Chifres', 'só nos machos: simples, sem galhos, de uns 6 a 12 cm'), ('Come', 'folhas, brotos, flores e frutos caídos')],
   reconhecer=['Pelagem cinza-amarronzada, sem pintas nos adultos.', 'Chifres retos e curtos, como dois espetos.', 'Levanta a cauda e mostra o branco de baixo quando foge.'],
   importa='É uma das presas da onça-parda e espalha sementes dos frutos que come. Os atropelamentos e os cachorros soltos matam muitos.',
   escala=(0.9, 0.5, '50 cm de altura no ombro')),
 'paca': dict(fontes=[100], abre='Um roedor grande e noturno, de fileiras de pintas brancas. Vive perto da água, nas matas de galeria, e foge mergulhando.',
   fatos=[('Comprimento', 'de uns 50 a 75 cm'), ('Peso', 'de 6 a 12 kg'), ('Quando aparece', 'à noite, sozinha, em trilhas na beira dos rios'), ('Come', 'frutos caídos, sementes, folhas e raízes')],
   reconhecer=['Pelagem marrom com quatro a sete fileiras de pintas brancas nos lados.', 'Corpo pesado, de cauda quase invisível.', 'Cabeça grande, com bochechas largas.'],
   importa='Come e espalha muitas sementes das matas ciliares. Caçar paca é proibido sem autorização, e a caça ainda é a maior ameaça a ela.',
   escala=(0.7, 0.35, '70 cm de comprimento')),
 'cutia': dict(fontes=[101], abre='A jardineira das matas. Enterra sementes para comer depois, esquece muitas, e assim planta árvores longe da planta-mãe.',
   fatos=[('Sementes', 'num estudo, levou 74% das sementes e enterrou 36%, a uns 8 m de distância'), ('Sementes pesadas', 'são levadas mais longe'), ('Quando aparece', 'de dia, principalmente de manhã e no fim da tarde'), ('Come', 'frutos, sementes e castanhas')],
   reconhecer=['Pelagem castanho-alaranjada, mais escura nas costas.', 'Pernas finas e compridas, corre aos saltos.', 'Senta nas patas de trás para comer segurando a semente.'],
   importa='Muitas árvores de sementes grandes dependem da cutia para se espalhar: sem ela, as sementes ficam embaixo da árvore-mãe e não vingam.',
   escala=None),
 'bugio': dict(fontes=[102], abre='O macaco do ronco. O grito grave dos machos, ao amanhecer, se ouve a quilômetros nas matas de galeria.',
   fatos=[('Peso', 'os machos chegam a uns 8 kg; as fêmeas, a uns 4,5 kg'), ('Cores', 'os machos são pretos; as fêmeas e os filhotes, de cor mais clara'), ('Come', 'principalmente folhas, e também frutos e flores'), ('Doença', 'muito sensível à febre amarela')],
   reconhecer=['Barba sob o queixo e garganta inchada, que funciona como caixa de som.', 'Cauda forte, que segura nos galhos.', 'Anda devagar e descansa a maior parte do dia.'],
   importa='Os bugios não transmitem a febre amarela: morrem dela e servem de alarme de que o vírus chegou. Quando aparece bugio morto, é hora de vacinar as pessoas. Não mate bugios.',
   escala=None),
 'mao-pelada': dict(fontes=[103], abre='O parente brasileiro do guaxinim. Tem máscara preta e mãos sem pelo, e anda à noite na beira dos rios procurando caranguejos e frutos.',
   fatos=[('Comprimento', 'de 40 a 100 cm de corpo, mais 20 a 38 cm de cauda'), ('Peso', 'de uns 3 a 10 kg'), ('Come', 'caranguejos, moluscos, peixes, insetos, sapos e frutos'), ('Hábito', 'mergulha a comida na água antes de comer')],
   reconhecer=['Máscara preta dos olhos até o queixo.', 'Cauda com anéis claros e escuros.', 'Pegadas que parecem mãos humanas pequenas, na lama dos rios.'],
   importa='É o maior procionídeo do Brasil e ajuda a controlar caranguejos e insetos nas margens. Depende de rios com mata ciliar.',
   escala=None),
 'irara': dict(fontes=[104], abre='Um carnívoro escuro, comprido, de cabeça clara, que sobe em árvores com facilidade. Adora mel: o nome, em tupi, quer dizer "tomador de mel".',
   fatos=[('Corpo', 'de 56 a 68 cm, mais 37 a 47 cm de cauda'), ('Peso', 'de 4 a 10 kg'), ('Come', 'mel, frutos, pequenos roedores, aves e ovos'), ('Quando aparece', 'de dia, sozinha ou em casal')],
   reconhecer=['Corpo marrom-escuro e cabeça mais clara, acinzentada.', 'Uma mancha amarelada na garganta, como um babador.', 'Cauda longa e peluda; sobe e desce das árvores de cabeça para baixo.'],
   importa='Come frutos e espalha sementes, e controla roedores. É difícil de ver e precisa de mata, mas aparece até em fragmentos.',
   escala=(1.05, 0.3, '1 m com a cauda')),
 'arara-azul-grande': dict(fontes=[105], abre='A maior arara do mundo, toda azul, com um anel amarelo em volta do olho. O bico é forte o bastante para quebrar cocos que nenhum outro bicho abre.',
   fatos=[('Tamanho', 'cerca de 1 m, do bico à ponta da cauda'), ('Peso', 'até 1,3 kg'), ('Come', 'castanhas de palmeiras, como o acuri e a bocaiuva, parente da macaúba'), ('Ninho', 'quase sempre em ocos de manduvi; um filhote por vez, em geral')],
   reconhecer=['Toda azul-cobalto, com a cauda longa e pontuda.', 'Pele amarela em volta do olho e na base do bico.', 'Voa em casais, com um grito rouco e alto.'],
   importa='Depende de palmeiras para comer e de árvores velhas para fazer ninho. Quase sumiu por causa do tráfico; no Pantanal, o trabalho de proteção levou a população a cerca de 6 mil aves.',
   escala=(0.3, 1.0, '1 m do bico à cauda')),
 'joao-de-barro': dict(fontes=[106], abre='O pedreiro dos campos. O casal constrói junto uma casa de barro em forma de forno, com um corredor por dentro que protege os ovos.',
   fatos=[('A casa', 'barro molhado misturado com capim, pelos e esterco'), ('Quanto tempo', 'de 18 a 30 dias de trabalho do casal'), ('Por dentro', 'uma parede separa a entrada da câmara dos ovos'), ('Onde', 'em galhos grossos, postes e mourões')],
   reconhecer=['Ave marrom-alaranjada, de garganta clara.', 'Anda pelo chão com passos firmes e canta em dueto com o par.', 'A casa de barro redonda no alto de um poste é a pista mais fácil.'],
   importa='As casas abandonadas viram ninho de outras aves, como andorinhas e periquitos. É uma das aves mais conhecidas do Brasil.',
   escala=None),
 'bem-te-vi': dict(fontes=[107], abre='A ave que diz o próprio nome. Barriga amarela, faixa branca na cabeça e um canto alto que começa ao amanhecer.',
   fatos=[('Tamanho', 'de uns 19 a 23 cm'), ('Come', 'de tudo: insetos, frutas, minhocas, girinos, peixinhos e ovos'), ('Canto', 'alto e repetido, que soa como "bem-te-vi"'), ('Onde', 'quase todo lugar com árvores, dos cerrados às cidades')],
   reconhecer=['Barriga amarelo-forte e costas marrons.', 'Cabeça preta com uma faixa branca por cima do olho.', 'Pousa em fios e galhos à vista e mergulha para pegar insetos.'],
   importa='Controla muitos insetos e é uma das aves mais fáceis de ver. Também é corajoso: enfrenta gaviões que chegam perto do ninho.',
   escala=(0.1, 0.21, '19 a 23 cm')),
 'periquito-rei': dict(fontes=[108], abre='Um periquito verde de testa laranja, comum nos cerrados. Faz o ninho cavando dentro de cupinzeiros que ficam no alto das árvores.',
   fatos=[('Tamanho', 'de 23 a 28 cm'), ('Peso', 'de uns 75 a 105 g'), ('Ninho', 'em cupinzeiros nas árvores; de 2 a 5 ovos'), ('Filhotes', 'ficam de 45 a 51 dias no ninho')],
   reconhecer=['Verde, com a testa e o anel em volta do olho cor de laranja.', 'Cauda comprida e pontuda.', 'Voa em bandos barulhentos, de manhã cedo e no fim da tarde.'],
   importa='Come frutos, sementes e flores do Cerrado. Mostra como os cupinzeiros são importantes: sem eles, faltam lugares para muitas aves fazerem ninho.',
   escala=(0.08, 0.26, '26 cm')),
 'anu-branco': dict(fontes=[109], abre='Uma ave clara e despenteada, de topete laranja, que vive em grupos. Várias fêmeas põem os ovos no mesmo ninho.',
   fatos=[('Tamanho', 'de 35 a 38 cm'), ('Ninho', 'coletivo: pode ter os filhotes de até sete mães'), ('Disputa', 'num estudo no Brasil Central, 97% dos ninhos perderam ovos jogados fora pelo próprio grupo'), ('Come', 'insetos, aranhas, pequenos lagartos e sapos')],
   reconhecer=['Plumagem creme, com estrias escuras e um topete laranja espetado.', 'Cauda comprida, escura com a ponta branca.', 'Pousa em grupo, todos encostados num galho, tomando sol.'],
   importa='É um dos casos mais estudados de criação em grupo entre as aves. Come muitos insetos de pasto e de campo.',
   escala=(0.12, 0.36, '35 a 38 cm')),
 'canario-da-terra': dict(fontes=[145, 110], abre='O canário nativo do Brasil. O macho é amarelo-ouro com a testa laranja; canta bonito e briga pelo território, e por isso é tão caçado.',
   fatos=[('Tamanho', 'cerca de 13,5 cm'), ('Peso', 'por volta de 20 g'), ('Come', 'sementes de capim e pequenos insetos'), ('Tráfico', 'a ave mais apreendida nos centros de triagem da Bahia (2009–2019) e de Goiás (2013–2017); também é usada em rinhas, que são crime')],
   reconhecer=['Macho amarelo-limão, com a testa e o rosto alaranjados.', 'Fêmeas e jovens pardos, com estrias.', 'Anda em bandos no chão dos campos e pastos, catando sementes.'],
   importa='Ainda é comum, mas a captura não para. Pegar, vender ou criar sem autorização é crime: denuncie ao Ibama ou à polícia ambiental.',
   escala=(0.06, 0.135, '13,5 cm')),
 'gaviao-carijo': dict(fontes=[111], abre='O gavião mais comum do Brasil. Pousa em postes, mourões e galhos à vista e grita alto, num tom agudo, quando voa.',
   fatos=[('Tamanho', 'de 31 a 41 cm'), ('Asas abertas', 'cerca de 45 cm de envergadura medida num banco de dados'), ('Peso', 'por volta de 300 g'), ('Come', 'insetos, lagartos, pequenas cobras, roedores e passarinhos')],
   reconhecer=['Cinza-amarronzado, com o peito listrado de marrom e branco.', 'Olhos e pernas amarelos.', 'Cauda com faixas claras e escuras.'],
   importa='Controla roedores, lagartos e insetos, inclusive nas cidades. Como todos os gaviões, é protegido por lei.',
   escala=(0.15, 0.36, '31 a 41 cm')),
 'urubu-de-cabeca-preta': dict(fontes=[112], abre='O urubu comum, todo preto, que vive em bandos. Limpa as carcaças dos campos e das estradas, e também acha comida pelo cheiro.',
   fatos=[('Asas abertas', 'de 1,3 a 1,6 m'), ('Peso', 'de 2 a 2,7 kg'), ('Olfato', 'um estudo da UFPA mostrou que acha pelo cheiro sacolas de comida escondidas'), ('Vida', 'em bandos, que dormem juntos nas mesmas árvores')],
   reconhecer=['Todo preto, de cabeça pelada e cinza-escura.', 'Em voo, uma mancha clara na ponta de cada asa.', 'Bate as asas várias vezes entre os planeios, ao contrário do urubu-rei.'],
   importa='É um faxineiro: come carcaças e reduz doenças. Muitos morrem envenenados por iscas colocadas para outros bichos.',
   escala=None),
 'morcego-beija-flor': dict(fontes=[113], abre='Um morcego pequeno que faz o trabalho dos beija-flores à noite. Voa parado diante das flores, enfia a língua comprida e leva o pólen de uma flor para outra.',
   fatos=[('Peso', 'cerca de 10 g'), ('Come', 'principalmente néctar, e também pólen, frutos moles e insetos'), ('Sementes', 'espalha as de árvores e arbustos pioneiros, que ajudam a mata a voltar'), ('Na cidade', 'visita até bebedouros de beija-flor')],
   reconhecer=['Morcego pequeno, marrom, de focinho comprido e fino.', 'Uma folhinha de pele em pé na ponta do nariz.', 'Paira diante das flores por um instante, à noite, e some.'],
   importa='Cerca de 528 espécies de plantas com flores são polinizadas por morcegos que tomam néctar. No Cerrado, muitas flores que abrem à noite, como as do pequi, recebem a visita deles.',
   escala=None),
 'jacare-de-papo-amarelo': dict(fontes=[114], abre='Um jacaré de focinho largo, que vive nos rios, lagoas e brejos do sul do Cerrado e da Mata Atlântica. Na época de reprodução, o papo fica amarelado.',
   fatos=[('Comprimento', 'cerca de 2 m, de porte médio entre os jacarés'), ('Ninho', 'um monte de folhas e terra; o calor do ninho decide se nascem machos ou fêmeas'), ('Temperatura', 'num estudo, a melhor eclosão foi a 31,8 °C'), ('Situação', 'pouco preocupante no Brasil (avaliação de 2013)')],
   reconhecer=['Focinho largo e curto, o mais largo entre os jacarés brasileiros.', 'Corpo verde-oliva escuro, com o papo mais claro.', 'Fica parado na água com só os olhos e as narinas de fora.'],
   importa='Controla peixes, caramujos e outros bichos das lagoas. Sofreu muito com a caça de couro e hoje sofre com a poluição e o aterro de brejos.',
   escala=(2.0, 0.35, '2 m de comprimento')),
 'sucuri': dict(fontes=[115, 148], abre='A maior cobra do Brasil, e a mais pesada do mundo. Não tem veneno: vive na água das veredas, rios e lagoas e mata a presa apertando.',
   fatos=[('Comprimento', 'o maior exemplar medido oficialmente tinha uns 7 m; o comum é bem menos'), ('Peso', 'as maiores passam de 100 kg (as fontes divergem)'), ('Veneno', 'não tem: mata por constrição'), ('Fêmeas e machos', 'as fêmeas são muito maiores; os machos raramente passam de 3 m')],
   reconhecer=['Corpo verde-oliva com manchas pretas arredondadas nas costas.', 'Olhos e narinas no alto da cabeça, para ficar quase toda submersa.', 'Rastro largo na lama da beira da água.'],
   importa='Come capivaras, aves aquáticas, peixes e jacarés pequenos, e ajuda a controlar essas populações. Ataque a gente é raríssimo: como toda cobra, prefere fugir.',
   escala=None),
 'caicaca': dict(fontes=[116], abre='A jararaca do Cerrado, também chamada de jararacão. Vive nas beiras de rio, nas matas de galeria e nas veredas, e é das cobras que mais causam acidentes na região.',
   fatos=[('Comprimento', 'em média 1,6 m; as maiores passam de 2 m'), ('Veneno', 'causa dor, inchaço e sangramento; picada é caso de hospital, com soro antibotrópico'), ('Acidentes', 'as jararacas (Bothrops) causaram 69% das picadas de cobra no Brasil em 2022'), ('Onde', 'Cerrado, perto da água, inclusive em lavouras e quintais')],
   reconhecer=['Corpo marrom ou acinzentado, com desenhos escuros em forma de V invertido nos lados.', 'Cabeça triangular, bem destacada do pescoço.', 'Uma fosseta entre o olho e a narina, que sente o calor.'],
   importa='Come roedores, e por isso aparece perto de casas e paióis. Use botas e luvas no mato, olhe antes de pôr a mão em buracos e, se for picado, vá direto ao hospital.',
   escala=(1.6, 0.08, '1,6 m em média')),
 'calango': dict(fontes=[117], abre='O lagarto das pedras, dos muros e dos troncos. Fica parado ao sol, esperando um inseto passar, e corre num estalo para pegá-lo.',
   fatos=[('Come', 'principalmente formigas, besouros, abelhas e cupins; também flores e frutos'), ('Caça', 'de tocaia: espera parado a presa passar'), ('Machos', 'maiores que as fêmeas'), ('Nomes', 'calango, calango-do-cerrado, lagartixa-preta e outros')],
   reconhecer=['Lagarto de uns palmos, cinza ou marrom, de escamas ásperas.', 'Faixa escura na nuca e no pescoço, como um colar, em algumas espécies.', 'Balança a cabeça para cima e para baixo quando outro chega perto.'],
   importa='Come muitos insetos e é comida de aves, cobras e mamíferos. Há várias espécies de Tropidurus no Cerrado, algumas só dos campos rupestres.',
   escala=None),
 'ra-pimenta': dict(fontes=[118], abre='Uma das maiores rãs do Brasil. O macho cava uma bacia na margem da água, onde o casal faz um ninho de espuma com milhares de ovos.',
   fatos=[('Tamanho', 'até uns 19,5 cm de corpo'), ('Ovos', 'em média 2.100 por desova, num ninho de espuma'), ('Girinos', 'ficam até 25 dias na espuma; na água, comem ovos de outras rãs'), ('Machos e fêmeas', 'do mesmo tamanho')],
   reconhecer=['Rã grande e pesada, marrom, com manchas escuras.', 'Coxas fortes, com listras escuras.', 'Canto grave, como um "fon-fon", nas noites de chuva.'],
   importa='Come insetos e pequenos bichos e é comida de cobras, aves e mamíferos. O nome vem da secreção da pele, que arde nos olhos e na boca: não esfregue o rosto depois de pegar uma.',
   escala=(0.19, 0.09, 'até 19,5 cm')),
 'pacu': dict(fontes=[119], abre='O peixe que come frutos. Na cheia, engole os frutos que caem na água e solta as sementes inteiras rio acima, plantando árvores nas margens.',
   fatos=[('Come', 'frutos e sementes; num estudo, os frutos de uma palmeira estavam em 73% dos pacus'), ('Tamanho', 'os maiores comem sementes de mais tamanhos que os pequenos'), ('Migração', 'sobe os rios na cheia, levando as sementes junto'), ('Pesca', 'proteger só os pequenos e pescar os grandes prejudica as sementes')],
   reconhecer=['Peixe alto e achatado, de corpo cinza a escuro.', 'Dentes parecidos com os nossos, de amassar frutos e sementes.', 'Primo da piranha, mas de boca menor e sem os dentes cortantes.'],
   importa='É um jardineiro dos rios: as árvores das matas ciliares dependem dele para levar as sementes contra a correnteza. Os pacus grandes são os melhores dispersores.',
   escala=None),
 'piranha': dict(fontes=[120], abre='Um peixe de dentes afiados e barriga vermelha, que vive em cardumes. A fama de devorar um boi em minutos é exagero.',
   fatos=[('Tamanho', 'em geral de 8 a 24 cm; os maiores já registrados chegaram a 50 cm'), ('Come', 'principalmente peixes, e também insetos, crustáceos, carniça, sementes e frutos'), ('Cardume', 'os jovens ficam por fora e os adultos no meio, protegidos'), ('Quando é perigosa', 'mais na seca e na reprodução, e quase sempre com presas já feridas')],
   reconhecer=['Corpo alto e prateado, com a barriga e a garganta vermelhas.', 'Mandíbula forte, com dentes triangulares e cortantes.', 'Anda em cardume, nas águas paradas e nos remansos.'],
   importa='Come peixes doentes e carniça, limpando os rios. Não entre na água com feridas abertas nem onde se limpa peixe.',
   escala=(0.24, 0.12, '8 a 24 cm')),
 'sauva': dict(fontes=[121], abre='A formiga agricultora. Corta folhas e carrega os pedaços para o formigueiro, não para comer, mas para cultivar um fungo que alimenta a colônia.',
   fatos=[('Tamanho', 'operárias de 12 a 15 mm; as quenquéns, parentes, de 8 a 10 mm'), ('O fungo', 'cresce sobre as folhas cortadas e é a comida das formigas'), ('Rainha', 'só ela põe ovos'), ('Formigueiro', 'muito fundo, com centenas de câmaras embaixo da terra')],
   reconhecer=['Filas de formigas avermelhadas carregando pedaços de folha.', 'Operárias de vários tamanhos, cada uma com uma tarefa.', 'Montes de terra solta com muitos olheiros.'],
   importa='Revira e aduba o solo, e é comida de tamanduás, tatus e aves. Nas lavouras, vira praga; no cerrado nativo, faz parte do equilíbrio.',
   escala=None),
 'mamangava': dict(fontes=[122], abre='Uma abelha grande e preta, que voa zumbindo alto. Faz o ninho cavando túneis em madeira morta e seca, e é a principal polinizadora do maracujá.',
   fatos=[('Ninho', 'em troncos de madeira morta, seca, começando a apodrecer'), ('Maracujá', 'a flor não se poliniza sozinha e depende das mamangavas'), ('Criação', 'caixas com tábuas de madeira seca atraem as abelhas para os pomares'), ('Ferrão', 'as fêmeas têm, mas só picam se forem apertadas')],
   reconhecer=['Abelha grande, preta e lustrosa, às vezes com pelos amarelos.', 'Zumbido forte e voo pesado.', 'Furos redondos, do tamanho de um dedo, em madeira seca.'],
   importa='Sem mamangava, o maracujá quase não dá fruto: em muitas roças, a polinização é feita à mão. Deixar troncos secos no lugar ajuda a manter as abelhas por perto.',
   escala=None),
 'rola-bosta': dict(fontes=[123], abre='Os besouros que fazem bolas de esterco. Algumas espécies rolam a bola para longe e a enterram; outras cavam túneis embaixo do monte.',
   fatos=[('O que fazem', 'enterram fezes, que viram comida para as larvas'), ('No solo', 'devolvem nutrientes, arejam a terra e ajudam a água a entrar'), ('Sementes', 'enterram de novo as sementes que estavam nas fezes'), ('Espécies', 'num estudo entre o Cerrado e o Pantanal, 29 espécies')],
   reconhecer=['Besouros redondos, de pernas da frente largas, de cavar.', 'Uma bola de esterco rolando, empurrada por um besouro de cabeça para baixo.', 'Alguns machos têm chifres na cabeça.'],
   importa='Limpam os pastos e os campos e diminuem as moscas. Também são bons indicadores: onde o rola-bosta some, a área está degradada.',
   escala=None),
 'cigarra': dict(fontes=[124], abre='O canto que anuncia o fim da seca. As ninfas passam anos embaixo da terra, sugando a seiva das raízes, e saem para virar adultas e cantar.',
   fatos=[('Embaixo da terra', 'em Brasília, cerca de quatro anos; o tempo muda de espécie para espécie'), ('Quem canta', 'só os machos, para atrair as fêmeas'), ('Quando', 'num estudo em Goiás, os adultos apareceram de setembro a dezembro'), ('As chuvas', 'o canto coincide com o começo delas, mas não há estudo que prove a ligação')],
   reconhecer=['Inseto de corpo grosso e asas transparentes, dobradas como um telhado.', 'Cascas vazias das ninfas presas nos troncos.', 'Um canto alto e contínuo, nas tardes quentes.'],
   importa='É comida de muitas aves e lagartos, e as ninfas arejam o solo. Não, a cigarra não canta até estourar: a casca que fica é a da ninfa, que ela deixa ao virar adulta.',
   escala=None),
 'caraiba': dict(fontes=[125], abre='Um ipê do cerrado aberto, de casca grossa como cortiça e folhas prateadas. Perde as folhas na seca e se cobre de flores amarelas em forma de sino.',
   fatos=[('Altura', 'em geral de 5 a 8 m, no cerrado'), ('Casca', 'cinza-amarronzada, com sulcos, que fica corticosa com a idade'), ('Floração', 'na seca, quando as folhas caem'), ('Onde', 'Cerrado e Pantanal; também chamada de cinco-folhas-do-campo')],
   reconhecer=['Folhas com cinco folíolos acinzentados, quase prateados.', 'Casca grossa, de cortiça, que aguenta o fogo.', 'Flores amarelas em cachos, na árvore sem folhas.'],
   importa='Floresce quando falta comida para abelhas e beija-flores. A casca grossa é um bom exemplo de como as árvores do cerrado aberto se protegem do fogo.',
   escala=('arvore', 8, 'até uns 8 m')),
 'angico': dict(fontes=[126], abre='A árvore dos curtumes. A casca é tão rica em taninos que foi, por séculos, a principal fonte para curtir couro no sertão.',
   fatos=[('Altura', 'de 3 a 15 m no Cerrado e na Caatinga; mais nas matas'), ('Taninos', 'cerca de 14% na casca, num estudo da UFCG'), ('Folhas', 'caem na seca'), ('Onde', 'matas secas, cerradões e florestas estacionais')],
   reconhecer=['Casca escura, com saliências e espinhos rombudos no tronco.', 'Folhas muito divididas, com folíolos miúdos.', 'Vagens finas e achatadas, marrons.'],
   importa='Os curtumes tradicionais do Nordeste ainda usam a casca. Tirar a casca de forma cuidadosa, sem anelar o tronco, deixa a árvore viva.',
   escala=('arvore', 15, 'até 15 m no cerrado')),
 'aroeira': dict(fontes=[127], abre='A árvore da madeira que não apodrece. Pesada, dura e resistente em contato com o chão, foi tão cortada para mourões e vigas que entrou na lista de espécies ameaçadas.',
   fatos=[('Madeira', 'muito pesada e resistente; considerada das mais duráveis do Brasil'), ('Usos', 'mourões, vigas, caibros e tacos'), ('Situação', 'já esteve na lista oficial de ameaçadas, como vulnerável (a conferir na lista atual)'), ('Onde', 'matas secas e cerradões, sobre solos mais férteis')],
   reconhecer=['Casca escura, que solta em placas, com cheiro de resina.', 'Folhas compostas, que caem na seca.', 'Na seca, sem folhas, fica coberta de cachinhos de flores miúdas.'],
   importa='A procura pela madeira acabou com muitas matas secas. Hoje é plantada para recuperar áreas, e o corte de árvores nativas depende de autorização.',
   escala=None),
 'sucupira-preta': dict(fontes=[128], abre='Uma das árvores mais típicas do cerrado, de flores roxas e madeira escura, densa e resistente, chamada de madeira de lei.',
   fatos=[('Madeira', 'densa e resistente, usada em construção e móveis'), ('Flores', 'roxas, em cachos'), ('Usos', 'também é usada na medicina popular'), ('Onde', 'cerrados do Planalto Central e outras savanas da América do Sul')],
   reconhecer=['Na florada, a copa fica roxa.', 'Folhas compostas, de folíolos com pelinhos.', 'Vagens achatadas e finas.'],
   importa='É uma das árvores que dão a cara do cerrado. A madeira valiosa fez muitas serem derrubadas.',
   escala=None),
 'pimenta-de-macaco': dict(fontes=[129], abre='Uma arvoreta do cerrado cujas sementes ardem como pimenta-do-reino. Povos tradicionais e indígenas as usam como tempero.',
   fatos=[('Altura', 'de 2,5 a 6 m'), ('Fruto', 'cachinhos de frutos escuros que se abrem mostrando uma polpa vermelha'), ('Sementes', 'de 3 a 6 por fruto, pretas e brilhantes; amassadas, viram tempero'), ('Quem espalha', 'as aves')],
   reconhecer=['Tronco reto e folhas alinhadas em dois lados do galho, que cheiram ao serem amassadas.', 'Frutos em feixes, como dedos, que se abrem em duas metades.', 'Sementes pretas sobre um arilo vermelho.'],
   importa='Está na Arca do Gosto do Slow Food, a lista de alimentos tradicionais que correm o risco de ser esquecidos. É pioneira: cresce em áreas abertas e ajuda o cerrado a voltar.',
   escala=('arvore', 6, 'até 6 m')),
 'caliandra': dict(fontes=[130], abre='Um arbusto de flores que parecem pincéis vermelhos: os estames longos e coloridos são o que mais aparece. É considerada uma das flores-símbolo do Cerrado.',
   fatos=[('Altura', 'em geral cerca de 1 m'), ('Flores', 'pompons de estames vermelhos'), ('Folhas', 'divididas em folíolos miúdos, com pelos'), ('Onde', 'cerrados do Brasil Central, inclusive em Brasília')],
   reconhecer=['Arbusto baixo, com flores como pincéis vermelhos.', 'Folhas finamente divididas.', 'Vagens achatadas com pelinhos.'],
   importa='As flores vermelhas atraem visitantes como beija-flores. É muito usada em jardins de Brasília e virou símbolo do bioma em materiais educativos.',
   escala=None),
 'arnica': dict(fontes=[131], abre='Um arbusto dos campos rupestres, de folhas finas e cheirosas. É usado na medicina popular contra dores e machucados, e por isso é muito arrancado.',
   fatos=[('Onde', 'campos rupestres de 800 a 2.000 m, de Goiás e do DF à Bahia e a São Paulo'), ('Uso popular', 'em infusões e pomadas, só por fora: não deve ser tomada'), ('Ameaças', 'a coleta e os incêndios frequentes, que podem acabar com populações locais'), ('Gênero', 'Lychnophora tem espécies vulneráveis e em perigo')],
   reconhecer=['Arbusto ramificado como um candelabro, com folhas finas, como agulhas.', 'Galhos com folhas só nas pontas.', 'Cabecinhas de flores roxas no alto dos galhos.'],
   importa='A "arnica" vendida em muitas feiras vem de plantas arrancadas na natureza. Comprar de cultivo, ou não comprar, ajuda a mantê-la nas serras.',
   escala=None),
 'algodaozinho': dict(fontes=[132], abre='Uma planta baixa, de flores amarelas grandes e brilhantes, que solta paina como algodão. Embaixo da terra, guarda um xilopódio grosso que rebrota depois do fogo.',
   fatos=[('Embaixo da terra', 'um xilopódio lenhoso e uma raiz grossa'), ('Flores', 'grandes, amarelo-vivas, no fim da seca'), ('Uso popular', 'a raiz e a casca, como depurativo e anti-inflamatório'), ('Cuidado', 'estudos em ratas indicam que o uso constante do extrato pode fazer mal')],
   reconhecer=['Flores amarelas grandes, de cinco pétalas, sobre hastes quase sem folhas.', 'Frutos que se abrem soltando sementes com paina branca.', 'Folhas divididas como uma mão.'],
   importa='Como a parte usada é a raiz, cada coleta pode matar a planta. A Embrapa estuda produzir mudas para aliviar a coleta. Remédio, só com orientação.',
   escala=None),
 'abacaxi-do-cerrado': dict(fontes=[133], abre='O abacaxizinho nativo do cerrado. É pequeno, bem azedo e cheio de fibras, e vira suco, doce e geleia.',
   fatos=[('Família', 'bromélias, como o abacaxi comum'), ('Fruto', 'bem menor e mais ácido que o abacaxi de feira'), ('Nutrição', 'rico em proteínas e fibras, segundo um estudo de 2025'), ('Ornamental', 'flores e frutos de haste longa duram até 40 dias em arranjos')],
   reconhecer=['Uma roseta de folhas duras e serrilhadas, no chão do cerrado.', 'Um abacaxi pequeno no alto de uma haste longa.', 'Brácteas rosadas em volta das flores.'],
   importa='É um parente selvagem do abacaxi, útil para os pesquisadores que melhoram a fruta. O consumo ainda é quase só local.',
   escala=None),
 'tingui': dict(fontes=[134], abre='Uma árvore de frutos lenhosos e redondos, que se abrem e soltam sementes achatadas com asas. A casca e os frutos já foram usados para fazer sabão.',
   fatos=[('Altura', 'em geral de 5 a 9 m; as maiores chegam perto de 16 m'), ('Sementes', 'achatadas e aladas, levadas pelo vento'), ('Usos', 'sabão caseiro e, na tradição, contra insetos'), ('Nome', 'para alguns, vem do tupi "que embriaga peixes"; não há consenso')],
   reconhecer=['Frutos grandes, redondos e lenhosos, que se abrem em três partes.', 'Folhas compostas, de folíolos arredondados.', 'Sementes finas como papel, com uma asa larga.'],
   importa='Aguenta solos pobres e é indicada para recuperar áreas degradadas. Estudos testam o extrato contra larvas do mosquito da dengue.',
   escala=('arvore', 9, 'até uns 9 m')),
 'bacupari': dict(fontes=[135], abre='Uma fruta amarela, doce, parecida com a lichia. O arbusto cresce no cerrado e dá frutos na época das chuvas.',
   fatos=[('Altura', 'arbusto de 1,5 a 3 m'), ('Fruto', 'amarelo, com três sementes e polpa doce'), ('Safra', 'no período chuvoso, de novembro a maio'), ('Usos', 'comida fresca, suco, sorvete e doce')],
   reconhecer=['Arbusto de casca cinza e áspera.', 'Folhas grossas e duras.', 'Frutos redondos e amarelos, de casca lisa.'],
   importa='Está na Arca do Gosto do Slow Food e é uma renda extra para quem coleta. As moscas-das-frutas atacam muito os frutos.',
   escala=None),
 'jacaranda-do-cerrado': dict(fontes=[136], abre='Uma das árvores mais típicas do cerrado, de flores roxas e tronco tortuoso. Também é chamada de caviúna-do-cerrado.',
   fatos=[('Altura', 'cerca de 8 m; algumas chegam a 12 ou 16 m'), ('Tronco', 'mais de 35 cm de diâmetro'), ('Flores', 'roxo-escuras, em cachos'), ('Onde', 'do Piauí a São Paulo e Minas Gerais, sobretudo no cerrado')],
   reconhecer=['Copa aberta, com folhas compostas de muitos folíolos.', 'Na florada, cachos de flores roxas pequenas.', 'Vagens achatadas e finas, com uma ou duas sementes.'],
   importa='É uma das árvores que dão a cara do cerrado sentido restrito. Como os outros jacarandás, tem madeira bonita e por isso sofreu com o corte.',
   escala=('arvore', 8, 'cerca de 8 m')),
 'orquidea-cyrtopodium': dict(fontes=[137], abre='Uma orquídea de chão, de flores amarelas pintadas de marrom. Em muitos cerrados, floresce em massa nos meses depois de uma queimada.',
   fatos=[('Hábito', 'terrestre, com pseudobulbos que guardam água'), ('Flores', 'amarelas, pintadas de marrom ou vinho, em hastes altas'), ('Fogo', 'registros de herbário anotam florada logo depois de queimadas'), ('No DF', '18 tipos do gênero, uma das áreas mais ricas')],
   reconhecer=['Uma haste alta e ramificada de flores amarelas saindo do chão do campo.', 'Pseudobulbos grossos, como charutos, na base.', 'Folhas longas e finas, que caem na seca.'],
   importa='Mostra que o fogo faz parte da vida de muitas plantas do Cerrado. Arrancar orquídeas da natureza é crime e quase sempre mata a planta.',
   escala=None),
 'capim-flecha': dict(fontes=[138], abre='Um capim alto dos campos das Emas. Rebrota rápido depois do fogo e forma manchas onde quase só ele cresce.',
   fatos=[('Fogo', 'rebrota rápido; a biomassa aumenta de 3 a 4 anos depois da queima'), ('Sementes', 'só floresce e dá semente na segunda estação de chuvas depois do fogo'), ('Queimas anuais', 'atrapalham a reprodução por semente'), ('Onde', 'campos do Brasil Central; dominante em partes do Parque Nacional das Emas')],
   reconhecer=['Touceiras altas de capim, com hastes finas e retas.', 'Espiguetas com aristas longas, como flechas.', 'Manchas grandes onde quase não há outras plantas.'],
   importa='O manejo do fogo nas Emas leva o capim-flecha em conta: queimar todo ano favorece a rebrota, mas impede as sementes.',
   escala=None),
 'pau-de-tucano': dict(fontes=[139], abre='Uma árvore que se enche de cachos de flores amarelas no começo das chuvas, quando o cerrado começa a ficar verde de novo.',
   fatos=[('Altura', 'de 3 a 8 m no cerrado; até perto de 20 m em matas'), ('Flores', 'amarelas, de 1,2 a 2,5 cm, em cachos'), ('Floração', 'principalmente de novembro a janeiro'), ('Família', 'Vochysiaceae, a mesma do pau-terra')],
   reconhecer=['Cachos em pé de flores amarelas, com um esporão curvo.', 'Folhas opostas ou em grupos de três ou quatro, no mesmo nó.', 'Frutos secos, que se abrem em três partes.'],
   importa='Floresce numa época em que o cerrado se renova, e é usada em jardins e na recuperação de áreas. É da mesma família do pau-terra, a das árvores que acumulam alumínio.',
   escala=('arvore', 8, 'até 8 m no cerrado')),
 'puca': dict(fontes=[140], abre='Uma frutinha escura e doce, chamada de jabuticaba-do-cerrado. É considerada a mais saborosa de todo o seu gênero.',
   fatos=[('Porte', 'arvoreta de uns 4 a 5 m'), ('Fruto', 'bago redondo, de polpa doce, com 1 a 4 sementes'), ('Variedades', 'amarela, marrom e preta, pela cor da casca'), ('Nutrição', 'vitamina C e compostos fenólicos')],
   reconhecer=['Arvoreta de folhas opostas, verdes e lisas.', 'Flores brancas pequenas.', 'Frutos que ficam cor de vinho ou pretos quando maduros.'],
   importa='Os frutos são renda para comunidades locais e quase não são conhecidos fora delas. É uma das frutas do Cerrado que ainda podem ganhar o país.',
   escala=('arvore', 4, 'cerca de 4 m')),
}
NOME_PAISAGEM = {p['id']: p['nome'] for p in P}
SITIO = AQUI.parents[2] / 'sitios' / 'fotografia-do-cerrado'
CRED_ESP = {c['arquivo']: c for c in json.loads((SITIO / 'img' / 'especies' / 'creditos.json').read_text())}
def foto_nova(id_):
    # uma foto salva em img/especies/<id>.webp e <id>-640.webp entra sozinha no catálogo (NO-COMPUTADOR.md, 9.1)
    return (SITIO / 'img' / 'especies' / f'{id_}-640.webp').exists()

ICONES = {
 'Mamíferos': '<path d="M12 21c-3 0-6-2-6-4.5S8.5 12 12 12s6 2 6 4.5-3 4.5-6 4.5Z"/><circle cx="6" cy="9" r="2"/><circle cx="10" cy="6" r="2"/><circle cx="14" cy="6" r="2"/><circle cx="18" cy="9" r="2"/>',
 'Aves': '<path d="M3 13c4 0 6-2 8-6 1 3 4 4 7 3l3-1-3 4c-2 3-6 5-10 5H6l-3-5Z"/>',
 'Répteis': '<path d="M4 18c4 0 4-5 8-5s4 5 8 5M6 10c3 0 3-4 6-4s3 4 6 4" fill="none" stroke-width="2.2" stroke-linecap="round"/>',
 'Insetos': '<ellipse cx="12" cy="14" rx="4" ry="6"/><path d="M12 8V5M8 11 4 9M16 11l4-2M8 15H4M16 15h4M8 18l-3 2M16 18l3 2" fill="none" stroke-width="1.8" stroke-linecap="round"/>',
 'Árvores': '<path d="M12 3c4 0 7 3 7 6.5S16 15 12 15 5 13 5 9.5 8 3 12 3Z"/><path d="M12 14v7" fill="none" stroke-width="2.5" stroke-linecap="round"/>',
 'Palmeiras': '<path d="M12 21V9M12 9c-2-3-6-3-8-1M12 9c2-3 6-3 8-1M12 9c-1-3-1-5 0-6M12 9c-3-1-5 1-6 3M12 9c3-1 5 1 6 3" fill="none" stroke-width="2" stroke-linecap="round"/>',
 'Arbustos': '<ellipse cx="8" cy="15" rx="5" ry="4"/><ellipse cx="16" cy="15" rx="5" ry="4"/><ellipse cx="12" cy="11" rx="5" ry="4"/>',
 'Ervas e arbustos': '<path d="M12 21V11M12 11l-4-6M12 11l4-6M12 14l-6-3M12 14l6-3" fill="none" stroke-width="2" stroke-linecap="round"/><circle cx="8" cy="5" r="1.8"/><circle cx="16" cy="5" r="1.8"/>',
 'Anfíbios': '<ellipse cx="12" cy="14" rx="7" ry="5"/><circle cx="8.5" cy="8.5" r="2.4"/><circle cx="15.5" cy="8.5" r="2.4"/>',
 'Peixes': '<path d="M3 12c3-4 8-5 12-3l5-3v12l-5-3c-4 2-9 1-12-3Z"/>',
}
SLUG_GRUPO = {g: re.sub(r'[^a-z]', '', unicodedata.normalize('NFD', g.lower()).encode('ascii', 'ignore').decode()) for g in ICONES}
def icones_defs():
    simbolos = ''.join(f'<symbol id="ic-{SLUG_GRUPO[g]}" viewBox="0 0 24 24">{d.replace('fill="none"', 'fill="none" stroke-width="2"')}</symbol>' for g, d in ICONES.items())
    return f'<svg class="icones-defs" width="0" height="0" aria-hidden="true" focusable="false">{simbolos}</svg>'
def cartao(e):
    id_, nome, cien, grupo, reino, am, pais, texto, foto, ficha, fs = e
    credito = ''
    if foto:
        img = f'<img src="{{{{raiz}}}}img/{foto}-640.webp" alt="" width="72" height="72" loading="lazy">'
    elif foto_nova(id_):
        img = f'<img src="{{{{raiz}}}}img/especies/{id_}-640.webp" alt="" width="72" height="72" loading="lazy">'
        c = CRED_ESP.get(f'{id_}.webp')
        if c: credito = f'<p class="esp-credito">Foto: {c["autor"]}, {c["licenca"]}</p>'
    else:
        # um <svg> só, que usa o desenho do grupo definido uma vez na página (menos elementos: orçamento de DOM)
        img = f'<svg class="esp-icone esp-{reino}" viewBox="-12 -12 48 48" width="72" height="72" aria-hidden="true" focusable="false"><use href="#ic-{SLUG_GRUPO[grupo]}" width="24" height="24"/></svg>'
    selo = f'<span class="selo">{AMEACA[am]}</span>' if am else ''
    link = f'<a href="especie-{id_}.html">{nome}</a>' if ficha or id_ in FICHAS else nome
    if id_ == 'jatai':
        texto = texto.replace('Veja o site Abelhas sem Ferrão.', 'Veja o site <a href="https://abelhas.linupedia.com.br/" rel="noopener">Abelhas sem Ferrão</a>.')
    # só o texto: os links para as paisagens ficam na ficha (e o filtro por paisagem continua na lista)
    onde = ', '.join(NOME_PAISAGEM[x].lower().replace("cerrado sentido restrito", "cerrado") for x in pais)
    return (f'<li class="esp" data-reino="{reino}" data-grupo="{grupo}" data-ameaca="{am or ""}" data-paisagens="{" ".join(pais)}" '
            f'data-busca="{(nome + " " + cien).lower()}">{img}<div class="esp-texto"><p class="esp-grupo">{grupo}</p><h2>{link}</h2>'
            f'<p class="cientifico">{cien}</p><p>{texto}{"".join(fonte(n) for n in fs)}</p><p class="esp-onde">Onde: {onde}</p>{selo}{credito}</div></li>')

grupos_fauna = ['Mamíferos', 'Aves', 'Répteis', 'Anfíbios', 'Peixes', 'Insetos']
grupos_flora = ['Árvores', 'Palmeiras', 'Arbustos', 'Ervas e arbustos']
chips = ''.join(f'<button type="button" class="chip" data-filtro-grupo="{g}" aria-pressed="false">{g}</button>' for g in grupos_fauna + grupos_flora)
opcoes_paisagem = ''.join(f'<option value="{p["id"]}">{p["nome"]}</option>' for p in P)
n_fauna = sum(1 for e in ESP if e[4] == 'fauna'); n_flora = len(ESP) - n_fauna

# o calendário das frutas (épocas do artigo do SciELO; variam muito de região para região)
FRUTAS = [('Pequi', [1, 2, 3]), ('Baru', [9, 10]), ('Cagaita', [9, 10]), ('Mangaba', [10, 11, 12]), ('Buriti', [12, 1, 2, 3, 4, 5, 6])]
MESES = ['jan', 'fev', 'mar', 'abr', 'mai', 'jun', 'jul', 'ago', 'set', 'out', 'nov', 'dez']
cab = ''.join(f'<th scope="col">{m}</th>' for m in MESES)
linhas = ''.join(f'<tr><th scope="row">{f}</th>' + ''.join(f'<td class="{"tem" if i + 1 in ms else ""}">{"<span class=\"so-leitor\">tem</span>" if i + 1 in ms else ""}</td>' for i in range(12)) + '</tr>' for f, ms in FRUTAS)

especies = f'''        <section class="titulo-pagina guia-topo">
            <div class="container">
                <p class="guia-chapeu">Guia do cerrado</p>
                <h1>Espécies do Cerrado</h1>
                <p>{n_fauna} bichos e {n_flora} plantas, para começar. Procure pelo nome, filtre pelo grupo ou pela paisagem, ou veja só as que estão ameaçadas de extinção.</p>
            </div>
        </section>
        <section class="secao especies-secao">
            <div class="container especies-layout">
                <div class="filtros-especies" role="search">
                    <label for="busca-especie">Procurar</label>
                    <input id="busca-especie" type="search" placeholder="Nome comum ou científico" autocomplete="off">
                    <fieldset><legend>Grupo</legend><div class="chips"><button type="button" class="chip" data-filtro-grupo="" aria-pressed="true">Todos</button>{chips}</div></fieldset>
                    <label for="paisagem-especie">Paisagem</label>
                    <select id="paisagem-especie"><option value="">Todas as paisagens</option>{opcoes_paisagem}</select>
                    <label class="so-ameacadas"><input type="checkbox" id="so-ameacadas"> Só as ameaçadas de extinção</label>
                    <p class="contagem" aria-live="polite"><strong id="contagem">{len(ESP)}</strong> espécies</p>
                    <p class="nota-calculo">A situação de ameaça é a da lista nacional (Portaria MMA nº 148/2022){fonte(15)}; confira cada espécie no SALVE, do ICMBio.{fonte(16)}</p>
                </div>
                <div>
                    {icones_defs()}<ul class="especies-lista">{"".join(cartao(e) for e in ESP)}</ul>
                    <p class="vazio" hidden>Nenhuma espécie com esses filtros. <button type="button" class="botao botao-linha" id="limpar-filtros">Limpar os filtros</button></p>
                    <p class="mais"><a href="galeria.html">Ver as fotos da galeria →</a></p>
                </div>
            </div>
        </section>
        <section class="secao creme" aria-labelledby="frutas-titulo">
            <div class="container">
                <h2 id="frutas-titulo">Quando tem fruta</h2>
                <p class="intro">A época em que cada fruta nativa amadurece, segundo um estudo sobre os frutos do Cerrado.{fonte(19)} Ela muda bastante de região para região e de um ano para o outro: no Distrito Federal e em Goiás, por exemplo, o pequi costuma aparecer bem antes, a partir de outubro.</p>
                <div class="calendario-rolagem" tabindex="0" role="group" aria-label="Calendário das frutas; role de lado no celular">
                    <table class="calendario"><caption class="so-leitor">Meses em que cada fruta amadurece</caption><thead><tr><th scope="col">Fruta</th>{cab}</tr></thead><tbody>{linhas}</tbody></table>
                </div>
            </div>
        </section>
'''
pagina('especies.html', 'Espécies do Cerrado: fauna e flora — Guia do Cerrado',
       f'{n_fauna} bichos e {n_flora} plantas do Cerrado, com busca, filtros por grupo e paisagem, as espécies ameaçadas e o calendário das frutas.',
       especies, scripts=['guia.js?v=1'])

# o menu passa a levar "Espécies" para o catálogo; a galeria e as fichas ficam dentro dele
MENU[3] = ('especies.html', 'Espécies')
ATUAL.update({'especie-': 'especies.html', 'galeria.html': 'especies.html'})
for f in COMPARTILHADAS:
    q = M / f; t = q.read_text()
    t = re.sub(r'\{\{\?pt-BR\}\}<ul class="menu" id="menu">.*?</ul>\{\{/pt-BR\}\}', lambda m: '{{?pt-BR}}' + menu_pt(f) + '{{/pt-BR}}', t)
    t = t.replace('<a class="porta" href="galeria.html"><span class="porta-chapeu">Espécies</span><strong>Bichos do Cerrado</strong><span>Fichas com medidas, hábitos e como fotografar.</span></a>',
                  f'<a class="porta" href="especies.html"><span class="porta-chapeu">Espécies</span><strong>Fauna e flora</strong><span>{len(ESP)} espécies com busca, filtros e o calendário das frutas.</span></a>')
    t = t.replace('<p class="mais"><a href="galeria.html">Ver todas as espécies →</a></p>', '<p class="mais"><a href="especies.html">Ver todas as espécies →</a></p>')
    q.write_text(t)
so_pt = json.loads((AQUI / 'so-pt.json').read_text())
if 'especies.html' not in so_pt: so_pt.append('especies.html')
(AQUI / 'so-pt.json').write_text(json.dumps(so_pt, ensure_ascii=False, indent=2) + '\n')
for f in so_pt:
    if f == '404.html': continue
    q = M / f; t = q.read_text()
    t = re.sub(r'<ul class="menu" id="menu">.*?</ul>', menu_pt(f), t, count=1)
    q.write_text(t)
# a página de fontes é refeita no fim, com as fontes novas
lista = ''.join(f'<li id="f{n}"><span class="fonte-numero">{n}</span> {t} <a href="{u}" rel="noopener">Abrir a fonte</a></li>' for n, t, u in FONTES)
q = M / 'fontes.html'; t = q.read_text()
t = re.sub(r'<ol class="fontes-lista">.*?</ol>', '<ol class="fontes-lista">' + lista + '</ol>', t, flags=re.S)
q.write_text(t)
print('espécies:', len(ESP))

# ================================================================ Parte 3: água, povos e ameaças
FONTES += [
 (21, 'Lima, J. E. F. W.; Silva, E. M. Contribuição hídrica do cerrado para as grandes bacias hidrográficas brasileiras. Embrapa Cerrados, 2002.', 'https://www.infoteca.cnptia.embrapa.br/infoteca/handle/doc/567621'),
 (22, 'Embrapa. Pantanal é dependente das águas do Cerrado (notícia): o Cerrado contribui com cerca de 94% da vazão do São Francisco e 71% da do Tocantins-Araguaia.', 'https://www.embrapa.br/en/busca-de-noticias/-/noticia/18023883/pantanal-e-dependente-das-aguas-do-cerrado-'),
 (23, 'Embrapa. Águas Emendadas, v. 3: Hidrografia. A vereda que manda água para duas bacias.', 'https://www.infoteca.cnptia.embrapa.br/infoteca/bitstream/doc/571673/1/V.3-Hidrografia.pdf'),
 (24, 'INPE. Brasil alcança menores taxas de desmatamento da série histórica na Amazônia e no Cerrado (PRODES): 5.516,69 km² no Cerrado de agosto de 2025 a julho de 2026, 23,8% a menos que os 7.235,27 km² do ano anterior; 74,3% nos estados do MATOPIBA.', 'https://www.gov.br/inpe/pt-br/assuntos/ultimas-noticias/brasil-alcanca-menores-taxas-de-desmatamento-da-serie-historica-na-amazonia-e-no-cerrado'),
 (25, 'Agência Gov. Desmatamento cai 30,6% na Amazônia e 25,8% no Cerrado em 2024: 8.174 km², o menor desde 2019 (6.319 km²), depois de cinco anos seguidos de alta.', 'https://agenciagov.ebc.com.br/noticias/202411/desmatamento-cai-30-6-na-amazonia-e-25-8-no-cerrado-em-2024'),
 (26, 'WWF-Brasil. Desmatamento cai 11% na Amazônia e no Cerrado em um ano: o pico de 11.011 km² no Cerrado em 2023.', 'https://www.wwf.org.br/?93220%2FDesmatamento-cai-11-na-Amazonia-e-no-Cerrado-em-um-ano='),
 (27, 'MapBiomas, 2025 (reportagem do Diario de Pernambuco): o Cerrado perdeu 28% da vegetação nativa em 40 anos, 40,5 milhões de hectares; somando o que mudou antes de 1985, 47,9% do bioma já foi transformado; as terras indígenas mantêm 97% de vegetação nativa.', 'https://www.diariodepernambuco.com.br/brasil/2025/10/11697115-cerrado-brasileiro-perdeu-28-da-vegetacao-nativa-em-40-anos.html'),
 (28, 'MMA. Consolidação do SNUC (apresentação, 2011): unidades de proteção integral em cerca de 3,1% do Cerrado e de uso sustentável em 5,1%.', 'https://antigo.mma.gov.br/estruturas/201/_arquivos/consolidao_do_snuc__ana_paula_prates_201.pdf'),
 (29, 'ISPN. Povos indígenas e comunidades tradicionais do Cerrado: geraizeiros, quebradeiras de coco babaçu (MIQCB, anos 1990) e outros.', 'https://ispn.org.br/en/biomas/cerrado/povos-indigenas-e-comunidades-tradicionais-do-cerrado/'),
 (30, 'Jornal Opção. Povos do Cerrado, os guardiões do bioma: o território Kalunga reconhecido pela ONU como TICCA em 2021, com 83% da área conservada.', 'https://www.jornalopcao.com.br/todo-ambiente/povos-do-cerrado-os-guardioes-do-bioma-mais-ameacado-do-brasil-744014/'),
 (31, 'Le Monde Diplomatique Brasil. Povos do Cerrado: os povos indígenas de troncos Macro-Jê (como os Xavante), Tupi-Guarani e Arawak, e as comunidades tradicionais.', 'https://diplomatique.org.br/sociobiodiversidade-e-defesa-da-soberania-alimentar/'),
 (32, 'Agência Brasil (2015). Berço das águas: os aquíferos Guarani, Bambuí e Urucuia, embaixo do Cerrado, alimentam rios importantes do continente.', 'https://ihu.unisinos.br/noticias/541069-berco-das-aguas-cerrado-precisa-de-protecao-para-garantir-abastecimento-no-pais'),
]
FONTES.sort()

# ---- Água
BACIAS = [('São Francisco', 94), ('Tocantins-Araguaia', 71), ('Paraná', 50)]
barras = ''.join(f'<li><span class="bacia-nome">{n}</span><span class="bacia-pct">{v}%</span><svg viewBox="0 0 100 14" preserveAspectRatio="none" aria-hidden="true"><rect class="estado-fundo" width="100" height="14"/><rect class="bacia-barra" width="{v}" height="14"/></svg></li>' for n, v in BACIAS)
agua = f'''        <section class="titulo-pagina guia-topo">
            <div class="container">
                <p class="guia-chapeu">Guia do cerrado</p>
                <h1>O berço das águas</h1>
                <p>Boa parte da água que corre pelos rios do Brasil nasce no Cerrado. As chapadas funcionam como esponjas: a chuva entra no chão e sai, devagar, nas nascentes e nas veredas, mesmo no meio da seca.</p>
            </div>
        </section>
        <div class="container guia-layout">
            {indice([('rios', 'Os rios'), ('esponja', 'A esponja'), ('aquiferos', 'Os aquíferos'), ('emendadas', 'Águas Emendadas'), ('cuidar', 'Por que importa')])}
            <div class="guia-texto">
                <section id="rios" aria-labelledby="rios-titulo">
                    <h2 id="rios-titulo">Quanto de cada rio vem do Cerrado</h2>
                    <p>O Cerrado manda água para oito das doze grandes regiões hidrográficas do país.{fonte(21)} Um estudo da Embrapa calculou quanto da vazão de cada grande bacia é gerada dentro do bioma:{fonte(21)}{fonte(22)}</p>
                    <ul class="bacias-lista">{barras}</ul>
                    <p class="nota-calculo">Parte da vazão de cada bacia que nasce no Cerrado (Embrapa, 2002). Em duas bacias a conta passa de 100%: no Parnaíba e no Paraguai, a água que sai do Cerrado é mais do que a vazão medida mais abaixo, porque parte dela evapora ou se espalha no caminho, como no Pantanal.{fonte(21)}{fonte(22)}</p>
                </section>
                <section id="esponja" aria-labelledby="esponja-titulo">
                    <h2 id="esponja-titulo">A esponja</h2>
                    <p>Os solos fundos do Cerrado e as raízes profundas da vegetação nativa deixam a chuva entrar no chão em vez de escorrer. Essa água desce devagar e reaparece nas nascentes, nas veredas e nas matas de galeria, e é por isso que muitos rios do Cerrado não secam mesmo depois de cinco meses quase sem chuva.</p>
                    <p>Quando a vegetação nativa sai, a chuva escorre mais e infiltra menos: chega mais terra aos rios na chuva e menos água às nascentes na seca.</p>
                    <p class="mais"><a href="paisagens.html#tipo-vereda">Veja como é uma vereda →</a></p>
                </section>
                <section id="aquiferos" aria-labelledby="aquiferos-titulo">
                    <h2 id="aquiferos-titulo">Os aquíferos</h2>
                    <p>Embaixo do Cerrado estão três grandes reservas de água subterrânea: os aquíferos Guarani, Bambuí e Urucuia. Elas alimentam rios importantes do continente.{fonte(32)} É a água guardada nesses aquíferos que sai devagar nas nascentes e mantém muitos rios correndo durante a seca.</p>
                </section>
                <section id="emendadas" aria-labelledby="emendadas-titulo">
                    <h2 id="emendadas-titulo">Águas Emendadas</h2>
                    <p>No Distrito Federal, a Estação Ecológica de Águas Emendadas guarda uma vereda que manda água para dois lados ao mesmo tempo: uma parte desce para a bacia do Tocantins, rumo ao Norte, e outra para a do Paraná, rumo ao Sul.{fonte(23)} É o retrato do Cerrado como divisor de águas do Brasil.</p>
                </section>
                <section id="cuidar" aria-labelledby="cuidar-titulo">
                    <h2 id="cuidar-titulo">Por que importa</h2>
                    <p>A água do Cerrado abastece cidades, irrigação e usinas hidrelétricas bem longe dele, e é a que enche o Pantanal.{fonte(22)} Proteger nascentes, veredas e matas de galeria é proteger a água de boa parte do país.</p>
                    <p class="mais"><a class="botao" href="ameacas.html">O que ameaça o Cerrado</a></p>
                </section>
            </div>
        </div>
'''
pagina('agua.html', 'O berço das águas — Guia do Cerrado',
       'Quanto da água do São Francisco, do Tocantins e do Paraná vem do Cerrado, os aquíferos e as veredas, com fontes.', agua, scripts=['guia.js?v=1'])

# ---- Povos
POVOS = [
 ('indigenas', 'Povos indígenas', 'Muitos povos vivem no Cerrado há milhares de anos. Os de tronco linguístico Macro-Jê, como os Xavante, estão entre os mais ligados ao bioma, ao lado de povos Tupi-Guarani e Arawak.{f31} Nas terras indígenas, 97% da vegetação nativa do Cerrado continua de pé.{f27}'),
 ('kalunga', 'Quilombolas Kalunga', 'Em Goiás, perto da Chapada dos Veadeiros, vivem os Kalunga, descendentes de pessoas escravizadas que fugiram e formaram comunidades nos vales. Em 2021, a ONU reconheceu o território como o primeiro do Brasil conservado por comunidades locais (TICCA): 83% da área continua conservada.{f30}'),
 ('geraizeiros', 'Geraizeiros', 'Vivem nos “gerais”, as chapadas do norte de Minas Gerais, criando gado solto, plantando nos vales e colhendo frutos nativos. Desde os anos 1970, o avanço das plantações de eucalipto sobre as chapadas é a maior ameaça ao seu modo de vida.{f29}'),
 ('quebradeiras', 'Quebradeiras de coco babaçu', 'Mulheres que vivem da coleta e da quebra do coco babaçu, no Maranhão, no Tocantins e no Piauí: tiram óleo, farinha e carvão. Nos anos 1990, formaram o Movimento Interestadual das Quebradeiras de Coco Babaçu, o MIQCB, para defender o acesso aos babaçuais.{f29}'),
 ('outros', 'Vazanteiros, ribeirinhos, raizeiros e outros', 'Vazanteiros, que plantam nas margens dos rios quando a água baixa; ribeirinhos; raizeiras e raizeiros, que conhecem as plantas que curam; apanhadores de sempre-viva; artesãs do capim-dourado. Cada um desses jeitos de viver depende do Cerrado de pé.{f31}'),
]
cartoes_povos = ''.join(f'''
                    <details class="povo" id="{i}">
                        <summary><span class="povo-nome">{n}</span></summary>
                        <p>{t.format(f27=fonte(27), f29=fonte(29), f30=fonte(30), f31=fonte(31))}</p>
                    </details>''' for i, n, t in POVOS)
povos = f'''        <section class="titulo-pagina guia-topo">
            <div class="container">
                <p class="guia-chapeu">Guia do cerrado</p>
                <h1>Os povos do Cerrado</h1>
                <p>O Cerrado não é só paisagem: é casa de povos indígenas, quilombolas e comunidades que vivem do que ele dá, sem derrubar. Onde eles estão, o Cerrado costuma estar mais inteiro.</p>
            </div>
        </section>
        <section class="secao">
            <div class="container povos-layout">
                <div class="povos-lista">{cartoes_povos}
                </div>
                <aside class="povos-numero">
                    <p class="povos-grande">97%</p>
                    <p>da vegetação nativa do Cerrado continua de pé dentro das terras indígenas.{fonte(27)}</p>
                    <p class="povos-grande">83%</p>
                    <p>do território Kalunga, em Goiás, está conservado.{fonte(30)}</p>
                </aside>
            </div>
        </section>
'''
pagina('povos.html', 'Os povos do Cerrado — Guia do Cerrado',
       'Povos indígenas, quilombolas Kalunga, geraizeiros, quebradeiras de coco babaçu e outras comunidades que vivem do Cerrado de pé.', povos)

# ---- Ameaças
PRODES = sorted(json.loads((AQUI / 'prodes.json').read_text())['anos'].items())
maior = max(v for _, v in PRODES)
barras_prodes = ''.join(f'<li><span class="ano">{a}</span><svg viewBox="0 0 100 18" preserveAspectRatio="none" aria-hidden="true"><rect class="desmate-barra" width="{100 * v / maior:.1f}" height="18"/></svg><span class="desmate-valor">{v:,} km²</span></li>'.replace(',', '.') for a, v in PRODES)
ameacas = f'''        <section class="titulo-pagina guia-topo">
            <div class="container">
                <p class="guia-chapeu">Guia do cerrado</p>
                <h1>O que ameaça o Cerrado</h1>
                <p>O Cerrado é um dos biomas brasileiros que mais perderam vegetação nativa nas últimas décadas, quase sempre para virar pasto e lavoura. A boa notícia: o desmatamento vem caindo desde 2023.</p>
            </div>
        </section>
        <div class="container guia-layout">
            {indice([('perda', 'Quanto já se perdeu'), ('ritmo', 'O ritmo do desmatamento'), ('onde', 'Onde se desmata'), ('protegido', 'Quanto está protegido'), ('fazer', 'O que dá para fazer')])}
            <div class="guia-texto">
                <section id="perda" aria-labelledby="perda-titulo">
                    <h2 id="perda-titulo">Quanto já se perdeu</h2>
                    <dl class="numeros-guia">
                        <div><dt>28%</dt><dd>da vegetação nativa perdida de 1985 a 2024, 40,5 milhões de hectares{fonte(27)}</dd></div>
                        <div><dt>47,9%</dt><dd>do Cerrado já transformado, somando o que mudou antes de 1985{fonte(27)}</dd></div>
                        <div><dt>97%</dt><dd>de vegetação nativa ainda de pé dentro das terras indígenas{fonte(27)}</dd></div>
                    </dl>
                </section>
                <section id="ritmo" aria-labelledby="ritmo-titulo">
                    <h2 id="ritmo-titulo">O ritmo do desmatamento</h2>
                    <p>O INPE mede todo ano, pelo sistema PRODES, quanto de vegetação nativa foi derrubada no Cerrado entre agosto de um ano e julho do seguinte. Depois de cinco anos seguidos de alta, o desmatamento chegou a 11.011 km² em 2023 e começou a cair; em 2026 foi o menor da série, que começa em 2001.{fonte(24)}{fonte(25)}{fonte(26)}</p>
                    <p class="so-leitor" id="desmate-legenda">Área desmatada no Cerrado por ano, em quilômetros quadrados:</p><ul class="desmate-lista" aria-describedby="desmate-legenda">{barras_prodes}</ul>
                    <p class="nota-calculo">{'Só os anos com o número conferido nas fontes; o PRODES publica a série completa. ' if len(PRODES) < 10 else ''} Cada ano vai de agosto do ano anterior a julho. Para comparar: 5.517 km² é mais de três vezes a área da cidade de São Paulo.{fonte(24)}{fonte(25)}{fonte(26)}</p>
                </section>
                <section id="onde" aria-labelledby="onde2-titulo">
                    <h2 id="onde2-titulo">Onde se desmata</h2>
                    <p>A maior parte do desmatamento recente está no norte do Cerrado, no MATOPIBA, a fronteira agrícola formada por Maranhão, Tocantins, Piauí e Bahia: 74,3% do que foi derrubado de 2025 a 2026. O Maranhão sozinho perdeu 1.718 km².{fonte(24)} É também ali que está a maior parte do Cerrado que ainda resta.{fonte(27)}</p>
                </section>
                <section id="protegido" aria-labelledby="protegido-titulo">
                    <h2 id="protegido-titulo">Quanto está protegido</h2>
                    <p>Pouco. Pelos dados do Ministério do Meio Ambiente de 2011, as unidades de proteção integral, como os parques nacionais, cobriam só cerca de 3% do Cerrado, e as de uso sustentável, outros 5%.{fonte(28)} Os números de hoje são um pouco maiores, mas o Cerrado continua sendo um dos biomas menos protegidos do país.</p>
                    <p>Fora das áreas protegidas, a lei permite desmatar a maior parte de uma propriedade no Cerrado, ao contrário do que acontece na Amazônia. Por isso, as terras indígenas e os territórios tradicionais fazem tanta diferença.</p>
                    <p class="mais"><a href="povos.html">Os povos que mantêm o Cerrado de pé →</a></p>
                </section>
                <section id="fazer" aria-labelledby="fazer-titulo">
                    <h2 id="fazer-titulo">O que dá para fazer</h2>
                    <p>Os canais para denunciar, socorrer um bicho e comprar do Cerrado estão em <a href="como-ajudar.html">Como ajudar</a>.</p>
                    <ul class="adaptacoes">
                        <li><strong>Conhecer.</strong> Pouca gente sabe nomear três plantas do Cerrado. Comece pelo <a href="especies.html">catálogo de espécies</a>.</li>
                        <li><strong>Comprar dos povos do Cerrado.</strong> Baru, pequi, óleo de babaçu, capim-dourado e mel de abelhas nativas vindos de comunidades e cooperativas mantêm o Cerrado de pé.</li>
                        <li><strong>Não soltar fogo na seca.</strong> Queimada de lixo e de pasto fora de hora vira incêndio.</li>
                        <li><strong>Plantar nativa.</strong> No quintal, na calçada ou numa nascente: ipê, pequi, baru, cagaita e buriti, cada um no seu lugar.</li>
                        <li><strong>Visitar as unidades de conservação.</strong> Parque visitado é parque defendido.</li>
                    </ul>
                </section>
            </div>
        </div>
'''
pagina('ameacas.html', 'O que ameaça o Cerrado — Guia do Cerrado',
       'Quanto o Cerrado já perdeu, o desmatamento medido pelo INPE ano a ano, onde ele acontece e quanto está protegido, com fontes.', ameacas, scripts=['guia.js?v=1'])

# ---- o menu do guia com as partes novas; Expedições e Sobre vão para o rodapé
MENU[:] = [('index.html', 'Início'), ('bioma.html', 'O bioma'), ('paisagens.html', 'Paisagens'), ('especies.html', 'Espécies'),
           ('agua.html', 'Água'), ('povos.html', 'Povos'), ('ameacas.html', 'Ameaças')]
RODAPE_PT = ' · <a href="expedicoes.html">Expedições</a> · <a href="diario.html">Diário de campo</a> · <a href="como-fotografamos.html">Como fotografamos</a> · <a href="sobre.html">Sobre</a> · <a href="contato.html">Contato</a> · <a href="fontes.html">Fontes</a>'
def com_rodape_novo(t):
    return re.sub(r'\{\{\?pt-BR\}\} · <a href="(?:expedicoes|diario|onde-ver|mes-a-mes)\.html">.*?\{\{/pt-BR\}\}', '{{?pt-BR}}' + RODAPE_PT + '{{/pt-BR}}', t)
for f in COMPARTILHADAS:
    q = M / f; t = q.read_text()
    t = re.sub(r'\{\{\?pt-BR\}\}<ul class="menu" id="menu">.*?</ul>\{\{/pt-BR\}\}', lambda m: '{{?pt-BR}}' + menu_pt(f) + '{{/pt-BR}}', t)
    t = com_rodape_novo(t)
    t = t.replace('<a class="porta" href="fontes.html"><span class="porta-chapeu">Fontes</span><strong>De onde vem cada número</strong><span>IBGE, Embrapa, ICMBio e artigos científicos.</span></a>',
                  '<a class="porta" href="agua.html"><span class="porta-chapeu">Água</span><strong>O berço das águas</strong><span>94% do São Francisco nasce aqui.</span></a>\n'
                  '                    <a class="porta" href="povos.html"><span class="porta-chapeu">Povos</span><strong>Quem vive no Cerrado</strong><span>Indígenas, Kalunga, geraizeiros, quebradeiras de coco.</span></a>\n'
                  '                    <a class="porta" href="ameacas.html"><span class="porta-chapeu">Ameaças</span><strong>O que ameaça o Cerrado</strong><span>O desmatamento ano a ano e o que dá para fazer.</span></a>')
    q.write_text(t)
so_pt = json.loads((AQUI / 'so-pt.json').read_text())
for f in ['agua.html', 'povos.html', 'ameacas.html']:
    if f not in so_pt: so_pt.append(f)
(AQUI / 'so-pt.json').write_text(json.dumps(so_pt, ensure_ascii=False, indent=2) + '\n')
for f in so_pt:
    if f == '404.html': continue
    q = M / f; t = q.read_text()
    t = re.sub(r'<ul class="menu" id="menu">.*?</ul>', menu_pt(f), t, count=1)
    t = com_rodape_novo(t)
    q.write_text(t)
lista = ''.join(f'<li id="f{n}"><span class="fonte-numero">{n}</span> {t} <a href="{u}" rel="noopener">Abrir a fonte</a></li>' for n, t, u in FONTES)
q = M / 'fontes.html'; t = q.read_text()
t = re.sub(r'<ol class="fontes-lista">.*?</ol>', '<ol class="fontes-lista">' + lista + '</ol>', t, flags=re.S)
q.write_text(t)
print('parte 3 pronta')

# ================================================================ Parte 4: aprender brincando (quiz, qual paisagem é esta? e glossário)
# o quiz só usa o que o guia já diz, com a página onde está a explicação
QUIZ = [
 ('bioma', 'Quanto do Brasil o Cerrado ocupa?', ['Cerca de 5%', 'Cerca de 23%', 'Cerca de 50%'], 1, 'São 1.983.017 km², cerca de 23,3% do país, segundo o IBGE (2019).', 'bioma.html#onde'),
 ('bioma', 'Em quantas regiões do Brasil o Cerrado aparece?', ['Só no Centro-Oeste', 'Em três', 'Em todas as cinco'], 2, 'É o único bioma presente em todas as regiões brasileiras.', 'bioma.html#onde'),
 ('bioma', 'Por que tantas árvores do Cerrado continuam verdes no meio da seca?', ['Porque não perdem água', 'Porque as raízes buscam água lá no fundo', 'Porque chove de madrugada'], 1, 'Muitas mandam raízes a vários metros de profundidade, até a água que fica guardada no solo.', 'bioma.html#solo'),
 ('bioma', 'O que protege muitas plantas do Cerrado do fogo?', ['Folhas molhadas', 'Casca grossa e partes que rebrotam embaixo da terra', 'Espinhos'], 1, 'A casca de cortiça isola o calor, e raízes grossas e xilopódios rebrotam depois da queimada.', 'bioma.html#fogo'),
 ('paisagens', 'Em que paisagem os buritis crescem alinhados num campo encharcado?', ['Vereda', 'Campo rupestre', 'Mata seca'], 0, 'A vereda tem dois andares: o capim úmido embaixo e os buritis em cima. Onde tem vereda, tem água.', 'paisagens.html#tipo-vereda'),
 ('paisagens', 'O que diferencia a mata de galeria da mata ciliar?', ['A galeria é mais baixa', 'Na galeria, as copas se fecham sobre o riacho', 'A galeria não tem árvores'], 1, 'A mata de galeria acompanha córregos pequenos e forma um túnel sobre a água; na ciliar, o rio é largo demais.', 'paisagens.html#tipo-mata-de-galeria'),
 ('paisagens', 'Quantas paisagens (fitofisionomias) o Cerrado tem, na classificação de Ribeiro e Walter?', ['3', '7', '11'], 2, 'São onze, em três grupos: campestres, savânicas e florestais.', 'paisagens.html'),
 ('especies', 'Qual destes é o único canídeo que só existe no Cerrado?', ['Lobo-guará', 'Raposa-do-campo', 'Cachorro-vinagre'], 1, 'A raposa-do-campo (Lycalopex vetulus) é endêmica do Cerrado e vulnerável na lista nacional.', 'especies.html'),
 ('especies', 'Quem choca os ovos da ema?', ['A fêmea', 'O macho', 'Os dois se revezam'], 1, 'É o macho que choca os ovos e cuida dos filhotes.', 'especies.html'),
 ('especies', 'Por que não se morde o caroço do pequi?', ['Porque é amargo', 'Porque tem espinhos finos por dentro', 'Porque é venenoso'], 1, 'Os espinhos ficam escondidos embaixo da polpa: rói-se com cuidado, sem morder.', 'especies.html'),
 ('agua', 'Quanto da vazão do Rio São Francisco nasce no Cerrado?', ['Cerca de 20%', 'Cerca de 50%', 'Cerca de 94%'], 2, 'Segundo a Embrapa, cerca de 94%.', 'agua.html#rios'),
 ('agua', 'O que tem de especial a Estação Ecológica de Águas Emendadas, no DF?', ['Um lago gigante', 'Uma vereda que manda água para duas bacias', 'A maior cachoeira do Brasil'], 1, 'Uma parte da água vai para a bacia do Tocantins e outra para a do Paraná.', 'agua.html#emendadas'),
 ('povos', 'Quem são as quebradeiras de coco babaçu?', ['Mulheres que vivem da coleta e da quebra do babaçu', 'Um time de futebol', 'Uma empresa de óleo'], 0, 'No Maranhão, no Tocantins e no Piauí; desde os anos 1990, organizadas no MIQCB.', 'povos.html#quebradeiras'),
 ('povos', 'Quanto da vegetação nativa continua de pé nas terras indígenas do Cerrado?', ['Cerca de 30%', 'Cerca de 60%', 'Cerca de 97%'], 2, 'Segundo o MapBiomas, 97%.', 'povos.html'),
 ('ameacas', 'Em que região está a maior parte do desmatamento recente do Cerrado?', ['No MATOPIBA', 'No Distrito Federal', 'Em São Paulo'], 0, 'Maranhão, Tocantins, Piauí e Bahia somaram 74,3% do desmatamento de 2025 a 2026.', 'ameacas.html#onde'),
 ('ameacas', 'O que aconteceu com o desmatamento do Cerrado desde 2023?', ['Dobrou', 'Ficou igual', 'Vem caindo'], 2, 'Do pico de 11.011 km² em 2023, caiu para 5.517 km² em 2026, o menor da série.', 'ameacas.html#ritmo'),
]
TEMAS = [('', 'Todos'), ('bioma', 'O bioma'), ('paisagens', 'Paisagens'), ('especies', 'Espécies'), ('agua', 'Água'), ('povos', 'Povos'), ('ameacas', 'Ameaças')]
quiz_json = json.dumps([{'t': t, 'p': p, 'o': o, 'c': c, 'e': e, 'l': l} for t, p, o, c, e, l in QUIZ], ensure_ascii=False).replace('</', '<\\/')
# "Qual paisagem é esta?": cada trecho do corte desenhado vira uma figura própria
trechos = {}
for i, p in enumerate(P):
    g = desenho(i, p)
    g = re.sub(r'<text [^>]*>[^<]*</text>', '', g)  # sem o nome embaixo: é isso que a pessoa tem de adivinhar
    trechos[p['id']] = f'<svg class="adivinha-desenho" viewBox="{i * W} 0 {W} 225" aria-hidden="true" focusable="false">{g}</svg>'
adivinha_json = json.dumps({'nomes': {p['id']: p['nome'] for p in P}, 'desenhos': trechos, 'dicas': {p['id']: p['reconhecer'] for p in P}}, ensure_ascii=False).replace('</', '<\\/')
GLOSSARIO = [
 ('Aquífero', 'Camada de rocha ou de solo que guarda água embaixo da terra. Sob o Cerrado estão o Guarani, o Bambuí e o Urucuia.', 'agua.html#aquiferos'),
 ('Bioma', 'Uma grande região com clima, vegetação e bichos parecidos. O Brasil tem seis: Amazônia, Cerrado, Mata Atlântica, Caatinga, Pampa e Pantanal.', 'bioma.html#onde'),
 ('Campo rupestre', 'Campo de capim e arbustos entre afloramentos de rocha, nas serras mais altas; cheio de plantas que só existem ali.', 'paisagens.html#tipo-campo-rupestre'),
 ('Cerradão', 'A floresta de árvores do cerrado, de copas quase fechadas, com 8 a 15 m de altura.', 'paisagens.html#tipo-cerradao'),
 ('Endêmica', 'Espécie que só existe num lugar. Cerca de 4.400 plantas são endêmicas do Cerrado.', 'bioma.html#vida'),
 ('Fitofisionomia', 'O “jeito” de uma vegetação: a altura, a densidade das árvores, o tipo de plantas. O Cerrado tem onze.', 'paisagens.html'),
 ('Geraizeiros', 'Comunidades tradicionais das chapadas (os “gerais”) do norte de Minas Gerais.', 'povos.html#geraizeiros'),
 ('Hotspot', 'Lugar com muitas espécies endêmicas e que já perdeu grande parte da vegetação original. O Cerrado é um dos hotspots do planeta.', 'bioma.html#vida'),
 ('Latossolo', 'Solo velho, fundo e bem drenado, mas pobre e ácido; o tipo mais comum no Cerrado.', 'bioma.html#solo'),
 ('MATOPIBA', 'A fronteira agrícola formada por Maranhão, Tocantins, Piauí e Bahia, onde está a maior parte do desmatamento recente.', 'ameacas.html#onde'),
 ('Murundu', 'Pequena elevação arredondada de terra, onde as árvores crescem no parque de cerrado; a origem (cupinzeiros antigos ou erosão) ainda é discutida.', 'paisagens.html#tipo-parque-de-cerrado'),
 ('PRODES', 'O sistema do INPE que mede, por satélite, quanto de vegetação nativa é derrubada a cada ano.', 'ameacas.html#ritmo'),
 ('Proteção integral', 'Tipo de unidade de conservação, como os parques nacionais, onde não se pode morar nem tirar recursos.', 'ameacas.html#protegido'),
 ('Quilombola', 'Pessoa de comunidade formada por descendentes de africanos escravizados, como os Kalunga, em Goiás.', 'povos.html#kalunga'),
 ('Reserva legal', 'A parte de cada propriedade rural que, pela lei, tem de ficar com vegetação nativa. No Cerrado, a maior parte da propriedade pode ser desmatada.', 'ameacas.html#protegido'),
 ('Savana', 'Vegetação de árvores espaçadas no meio de capim. O Cerrado é a savana mais rica do mundo.', 'bioma.html'),
 ('TICCA', 'Território e Área Conservada por Comunidades Indígenas e Locais, um reconhecimento da ONU. O território Kalunga foi o primeiro do Brasil.', 'povos.html#kalunga'),
 ('Vereda', 'Campo encharcado com buritis, onde a água do subsolo aflora; protege nascentes.', 'paisagens.html#tipo-vereda'),
 ('Xilopódio', 'Órgão grosso embaixo da terra que guarda reservas e gemas: a planta rebrota dele depois do fogo ou da seca.', 'bioma.html#fogo'),
]
gloss = ''.join(f'<div class="termo" data-termo="{t.lower()}"><dt id="g-{re.sub(r"[^a-z]", "", t.lower())}">{t}</dt><dd>{d} <a href="{l}">Ler mais</a></dd></div>' for t, d, l in GLOSSARIO)
botoes_temas = ''.join(f'<button type="button" class="chip" data-tema="{i}" aria-pressed="{"true" if i == "" else "false"}">{n}</button>' for i, n in TEMAS)
# "Qual é esta espécie?" (1/11/2026): as pistas saem das fichas; o nome da espécie vira "esta espécie"
def pistas_de(id_):
    if id_ in FICHAS:
        f = FICHAS[id_]
        return list(f['reconhecer']) + [f'{k}: {v}.' for k, v in f['fatos'][:2]]
    h = (M / f'especie-{id_}.html').read_text()
    m = re.search(r'id="reconhecer-titulo".*?<ul[^>]*>(.*?)</ul>', h, re.S)
    return [re.sub(r'<[^>]+>', '', x).strip() for x in re.findall(r'<li>(.*?)</li>', m.group(1), re.S)] if m else []
def sem_nome(texto, nome):
    for parte in sorted({nome, *[w for w in re.split(r'[\s-]+', nome) if len(w) > 3 and w.lower() not in ('campo', 'cerrado', 'mato')]}, key=len, reverse=True):
        texto = re.sub(r'(?i)(?<![\w-])' + re.escape(parte) + r's?(?![\w-])', 'esta espécie', texto)
    return texto
QUAL = []
for e in ESP:
    id_, nome, cien, grupo, reino = e[0], e[1], e[2], e[3], e[4]
    pistas = [sem_nome(x, nome) for x in pistas_de(id_)]
    pistas = [x for x in pistas if x][:4]
    if len(pistas) < 2: continue
    abre = FICHAS[id_]['abre'] if id_ in FICHAS else e[7]
    QUAL.append({'id': id_, 'n': nome, 'g': grupo, 'r': reino, 'p': pistas, 'e': abre})
qual_json = json.dumps(QUAL, ensure_ascii=False).replace('</', '<\\/')

aprender = f'''        <section class="titulo-pagina guia-topo">
            <div class="container">
                <p class="guia-chapeu">Guia do cerrado</p>
                <h1>Aprender brincando</h1>
                <p>Um quiz por tema, dois jogos (reconhecer as espécies pelas pistas e as paisagens pelo desenho) e um glossário. Tudo o que está aqui foi explicado no guia, com fonte.</p>
            </div>
        </section>
        <div class="container guia-layout">
            {indice([('quiz', 'Quiz'), ('qual-e', 'Qual é esta espécie?'), ('adivinha', 'Qual paisagem é esta?'), ('glossario', 'Glossário')])}
            <div class="guia-texto">
                <section id="quiz" aria-labelledby="quiz-titulo">
                    <h2 id="quiz-titulo">Quiz</h2>
                    <div class="chips" role="group" aria-label="Tema do quiz">{botoes_temas}</div>
                    <div class="quiz-caixa" aria-live="polite">
                        <p class="quiz-contador"></p>
                        <h3 class="quiz-pergunta" tabindex="-1">O quiz precisa de JavaScript ligado.</h3>
                        <div class="quiz-opcoes"></div>
                        <p class="quiz-retorno" hidden></p>
                        <div class="quiz-acoes"><button type="button" class="botao" id="quiz-proxima" hidden>Próxima</button></div>
                    </div>
                    <script type="application/json" id="quiz-dados">{quiz_json}</script>
                </section>
                <section id="qual-e" aria-labelledby="qual-titulo">
                    <h2 id="qual-titulo">Qual é esta espécie?</h2>
                    <p>Leia as pistas e escolha o nome. Se não souber, peça mais uma pista. As pistas saem das <a href="especies.html">fichas das {len(QUAL)} espécies</a>; cada partida tem dez.</p>
                    <div class="qual-caixa" aria-live="polite">
                        <p class="qual-placar"></p>
                        <ol class="qual-pistas"><li>O jogo precisa de JavaScript ligado.</li></ol>
                        <button type="button" class="botao botao-linha qual-mais" hidden>Mais uma pista</button>
                        <div class="quiz-opcoes qual-opcoes"></div>
                        <p class="quiz-retorno qual-retorno" hidden></p>
                        <div class="quiz-acoes"><button type="button" class="botao" id="qual-proxima" hidden>Próxima espécie</button></div>
                    </div>
                    <script type="application/json" id="qual-dados">{qual_json}</script>
                </section>
                <section id="adivinha" aria-labelledby="adivinha-titulo">
                    <h2 id="adivinha-titulo">Qual paisagem é esta?</h2>
                    <p>Olhe o desenho e escolha o nome. São as onze paisagens do <a href="paisagens.html">corte do Cerrado</a>, em ordem aleatória.</p>
                    <div class="adivinha-caixa" aria-live="polite">
                        <div class="adivinha-figura"></div>
                        <div class="quiz-opcoes adivinha-opcoes"></div>
                        <p class="quiz-retorno adivinha-retorno" hidden></p>
                        <div class="quiz-acoes"><p class="adivinha-placar"></p><button type="button" class="botao" id="adivinha-proxima" hidden>Próxima paisagem</button></div>
                    </div>
                    <script type="application/json" id="adivinha-dados">{adivinha_json}</script>
                </section>
                <section id="glossario" aria-labelledby="glossario-titulo">
                    <h2 id="glossario-titulo">Glossário</h2>
                    <label for="busca-termo" class="so-leitor">Procurar no glossário</label>
                    <input id="busca-termo" class="busca-termo" type="search" placeholder="Procurar uma palavra" autocomplete="off">
                    <dl class="glossario">{gloss}</dl>
                    <p class="vazio-glossario" hidden>Nenhuma palavra com esse nome. Experimente outra.</p>
                </section>
            </div>
        </div>
'''
pagina('aprender.html', 'Aprender brincando — Guia do Cerrado',
       'Quiz sobre o Cerrado por tema, os jogos “Qual é esta espécie?” e “Qual paisagem é esta?” e um glossário, tudo com base no guia.', aprender, scripts=['guia.js?v=1', 'aprender.js?v=3'])

MENU.append(('aprender.html', 'Aprender'))
for f in COMPARTILHADAS:
    q = M / f; t = q.read_text()
    t = re.sub(r'\{\{\?pt-BR\}\}<ul class="menu" id="menu">.*?</ul>\{\{/pt-BR\}\}', lambda m: '{{?pt-BR}}' + menu_pt(f) + '{{/pt-BR}}', t)
    t = t.replace('<a class="porta" href="ameacas.html"><span class="porta-chapeu">Ameaças</span><strong>O que ameaça o Cerrado</strong><span>O desmatamento ano a ano e o que dá para fazer.</span></a>',
                  '<a class="porta" href="ameacas.html"><span class="porta-chapeu">Ameaças</span><strong>O que ameaça o Cerrado</strong><span>O desmatamento ano a ano e o que dá para fazer.</span></a>\n'
                  '                    <a class="porta" href="aprender.html"><span class="porta-chapeu">Aprender</span><strong>Quiz e jogos</strong><span>Teste o que você sabe e reconheça as paisagens.</span></a>')
    q.write_text(t)
so_pt = json.loads((AQUI / 'so-pt.json').read_text())
if 'aprender.html' not in so_pt: so_pt.append('aprender.html')
(AQUI / 'so-pt.json').write_text(json.dumps(so_pt, ensure_ascii=False, indent=2) + '\n')
for f in so_pt:
    if f == '404.html': continue
    q = M / f; t = q.read_text()
    t = re.sub(r'<ul class="menu" id="menu">.*?</ul>', menu_pt(f), t, count=1)
    q.write_text(t)
print('parte 4 pronta')

# ================================================================ Onde ver o Cerrado: os parques num mapa (base, 31/10/2026)
# posições aproximadas (o centro de cada parque), na mesma projeção do biomas.py
import math as _m
def _xy(lon, lat):
    return ((lon + 74.5) * 9.0 * _m.cos(_m.radians(-14)), (5.6 - lat) * 9.0)
PARQUES = [
 ('Parque Nacional da Chapada dos Veadeiros', 'GO', -47.65, -14.05, 'Campos rupestres, cachoeiras e cânions; lobo-guará ao entardecer.'),
 ('Parque Nacional das Emas', 'GO e MS', -52.9, -18.15, 'Campos abertos, tamanduá-bandeira, veado-campeiro e os cupinzeiros que brilham no começo das chuvas.'),
 ('Parque Nacional de Brasília', 'DF', -48.0, -15.65, 'A saída mais fácil: trilhas planas, matas de galeria e aves perto da água.'),
 ('Parque Nacional da Serra da Canastra', 'MG', -46.6, -20.25, 'Onde nasce o São Francisco; campos de altitude e um dos últimos refúgios do pato-mergulhão.'),
 ('Parque Nacional Grande Sertão Veredas', 'MG e BA', -45.9, -15.3, 'Veredas e buritis sem fim, a paisagem do livro de Guimarães Rosa.'),
 ('Parque Nacional da Chapada dos Guimarães', 'MT', -55.85, -15.35, 'Paredões de arenito e cachoeiras, entre o Cerrado e o Pantanal.'),
 ('Parque Nacional da Serra do Cipó', 'MG', -43.55, -19.35, 'Campos rupestres da Serra do Espinhaço, com muitas plantas que só existem ali.'),
 ('Parque Estadual do Jalapão', 'TO', -47.4, -10.7, 'Dunas, fervedouros e o capim-dourado.'),
 ('Parque Nacional das Nascentes do Rio Parnaíba', 'PI, MA, TO e BA', -45.6, -9.9, 'Chapadas e nascentes no norte do Cerrado.'),
 ('Parque Nacional Cavernas do Peruaçu', 'MG', -44.25, -15.1, 'Cavernas gigantes, pinturas rupestres e mata seca sobre calcário.'),
 ('Parque Nacional das Sempre-Vivas', 'MG', -43.8, -17.9, 'Campos de sempre-vivas e as comunidades que vivem de colhê-las.'),
 ('Parque Nacional da Chapada das Mesas', 'MA', -47.3, -7.0, 'Morros de topo reto e cachoeiras no Cerrado do Maranhão.'),
 ('Parque Nacional do Araguaia', 'TO', -50.2, -10.6, 'Na Ilha do Bananal, onde o Cerrado encontra a Amazônia e as várzeas do Araguaia.'),
]
mapa_parques = (AQUI / 'biomas.svg').read_text()
pinos = ''.join(f'<a href="#parque-{n}" class="pino" data-parque="{n}"><circle class="pino-alvo" cx="{_xy(lon, lat)[0]:.1f}" cy="{_xy(lon, lat)[1]:.1f}" r="13"/><circle cx="{_xy(lon, lat)[0]:.1f}" cy="{_xy(lon, lat)[1]:.1f}" r="7"/><text x="{_xy(lon, lat)[0]:.1f}" y="{_xy(lon, lat)[1] + 3:.1f}" text-anchor="middle">{n}</text></a>'
                for n, (nome, uf, lon, lat, t) in enumerate(PARQUES, 1))
mapa_parques = mapa_parques.replace('class="mapa-biomas"', 'class="mapa-biomas mapa-parques" data-destaque="cerrado"').replace('</svg>', pinos + '</svg>')
mapa_parques = mapa_parques.replace('role="img" aria-labelledby="biomas-titulo"', 'role="group" aria-labelledby="parques-titulo"').replace('<title id="biomas-titulo">', '<title id="parques-titulo">').replace(
    'Mapa dos biomas do Brasil: o Cerrado ocupa o centro do país, entre a Amazônia, a Caatinga, a Mata Atlântica e o Pantanal', 'Mapa do Brasil com o Cerrado e 13 parques numerados')
lista_parques = ''.join(f'<li id="parque-{n}"><span class="parque-num">{n}</span><div><h2>{nome}</h2><p class="parque-uf">{uf}</p><p>{t}</p></div></li>' for n, (nome, uf, lon, lat, t) in enumerate(PARQUES, 1))
onde = f'''        <section class="titulo-pagina guia-topo">
            <div class="container">
                <p class="guia-chapeu">Guia do cerrado</p>
                <h1>Onde ver o Cerrado</h1>
                <p>Treze parques para conhecer o Cerrado de perto, do Maranhão a Minas Gerais. Toque num número do mapa para ler sobre o parque.</p>
            </div>
        </section>
        <section class="secao">
            <div class="container onde-ver">
                <figure class="onde-mapa">{mapa_parques}<figcaption>Posições aproximadas. Em cor, o Cerrado (IBGE, 2019).{fonte(1)}</figcaption></figure>
                <ol class="parques-lista">{lista_parques}</ol>
            </div>
            <div class="container"><p class="nota-calculo">Antes de ir, confira no site de cada parque (ICMBio ou o órgão do estado) se ele está aberto à visitação, o que precisa de guia e as regras de cada trilha. As expedições deste guia são de mentira; os parques, não.</p></div>
        </section>
'''
pagina('onde-ver.html', 'Onde ver o Cerrado — Guia do Cerrado', 'Treze parques para conhecer o Cerrado de perto, num mapa: Chapada dos Veadeiros, Emas, Canastra, Grande Sertão Veredas, Jalapão e outros.', onde)
RODAPE_PT = RODAPE_PT.replace(' · <a href="expedicoes.html">Expedições</a>', ' · <a href="onde-ver.html">Onde ver</a> · <a href="expedicoes.html">Expedições</a>')
for f in COMPARTILHADAS:
    q = M / f; t = q.read_text()
    t = com_rodape_novo(t)
    t = t.replace('<a class="porta" href="expedicoes.html"><span class="porta-chapeu">Expedições</span><strong>Ver de perto</strong><span>Quando ir e onde ficam os parques.</span></a>',
                  '<a class="porta" href="onde-ver.html"><span class="porta-chapeu">Onde ver</span><strong>13 parques do Cerrado</strong><span>Do Maranhão a Minas, num mapa.</span></a>')
    q.write_text(t)
so_pt = json.loads((AQUI / 'so-pt.json').read_text())
if 'onde-ver.html' not in so_pt: so_pt.append('onde-ver.html')
(AQUI / 'so-pt.json').write_text(json.dumps(so_pt, ensure_ascii=False, indent=2) + '\n')
for f in so_pt:
    if f == '404.html': continue
    q = M / f; t = q.read_text(); t = com_rodape_novo(t); q.write_text(t)
print('onde ver pronto')

# ================================================================ Uma página para cada paisagem (paisagem-<id>.html)
FONTES += [
 (33, 'Brasil. Lei nº 12.651, de 25 de maio de 2012 (Código Florestal), art. 4º, com a redação da Lei nº 12.727/2012: as Áreas de Preservação Permanente, como a faixa de pelo menos 50 m em volta da parte encharcada das veredas e as faixas nas margens dos rios.', 'https://www.planalto.gov.br/ccivil_03/_ato2011-2014/2012/lei/l12651.htm'),
]
FONTES.sort()
# o que cada página acrescenta à ficha: por que importa e onde ver (os números são os da lista de Onde ver)
MAIS = {
 'campo-limpo': ('É onde vivem as aves e os bichos de campo aberto, como a ema, o veado-campeiro e a coruja-buraqueira, e costuma cercar as nascentes e as veredas. Por ser fácil de transformar em pasto, é uma das paisagens que mais somem.', [2, 1]),
 'campo-sujo': ('É a paisagem de passagem entre o campo e o cerrado: um pouco de cada. Tem muita comida para quem come capim, frutos rasteiros e insetos, como o tamanduá-bandeira e a raposa-do-campo.', [2, 3]),
 'campo-rupestre': ('Junta muitas plantas que só existem numa serra, às vezes num único morro. As sempre-vivas e o capim-dourado são colhidos para artesanato, e a mineração é uma das maiores ameaças a esses campos.', [1, 7, 11]),
 'parque-de-cerrado': ('Na chuva, o campo entre os murundus encharca, e as árvores só conseguem viver em cima deles. É uma paisagem que guarda água e que some rápido quando o terreno é drenado para plantar.', [2, 3]),
 'cerrado-sentido-restrito': ('É a paisagem que cobre a maior parte do bioma e a que dá os frutos mais conhecidos: pequi, cagaita, mangaba, araticum. É também a mais derrubada para virar lavoura e pasto.', [1, 3, 5]),
 'palmeiral': ('Os babaçuais do norte do Cerrado sustentam o trabalho das quebradeiras de coco do Maranhão, do Tocantins e do Piauí. Os buritizais alimentam araras, antas e gente.', [12, 9]),
 'vereda': ('Onde tem vereda, tem água: ela guarda nascentes e solta água devagar para os rios durante a seca. Por isso a lei protege uma faixa de pelo menos 50 m em volta da parte encharcada de toda vereda.', [5, 8]),
 'cerradao': ('Guarda espécies do cerrado e da mata juntas, e por isso é cheio de vida. Foi muito cortado para tirar madeira e fazer carvão.', [3, 6]),
 'mata-seca': ('Cresce nos solos mais férteis, muitas vezes sobre calcário, perto de cavernas. Por isso mesmo foi muito procurada para a agricultura e pela madeira das árvores grandes.', [10, 13]),
 'mata-de-galeria': ('É o corredor por onde muitos bichos atravessam o Cerrado aberto, com sombra e água o ano inteiro, e protege os córregos de terra e de calor. A lei protege as faixas de mata nas margens dos rios.', [3, 1]),
 'mata-ciliar': ('Segura as margens dos rios grandes contra a erosão e dá comida e abrigo para peixes e bichos da beira d’água. A lei protege as faixas de mata nas margens, mais largas quanto mais largo é o rio.', [13, 6]),
}
LEI = {'vereda', 'mata-de-galeria', 'mata-ciliar'}
def desenho_grande(i, p):
    # a paisagem no meio e as vizinhas do corte, apagadas, dos lados: fica deitado e mostra o que vem antes e depois
    ini = min(max(i - 1, 0), len(P) - 3)
    partes = []
    for j in range(ini, ini + 3):
        g = re.sub(r'<text [^>]*>[^<]*</text>', '', desenho(j, P[j]))
        partes.append(g if j == i else g.replace('<g class="trecho"', '<g class="trecho vizinho"', 1))
    return f'<svg class="paisagem-desenho" viewBox="{ini * W} 20 {3 * W} 205" aria-hidden="true" focusable="false">{"".join(partes)}</svg>'
def especies_da(pid):
    lista = [e for e in ESP if pid in e[6]]
    return ''.join(cartao(e) for e in lista), len(lista)
for i, p in enumerate(P):
    ant, prox = P[i - 1], P[(i + 1) % len(P)]
    texto_mais, parques = MAIS[p['id']]
    cartoes_esp, n_esp = especies_da(p['id'])
    onde_li = ''.join(f'<li><a href="onde-ver.html#parque-{n}">{PARQUES[n - 1][0]}</a> <span class="parque-uf">({PARQUES[n - 1][1]})</span></li>' for n in parques)
    foto = foto_paisagem(p)
    corpo = f'''        <article class="pagina-paisagem">
            <section class="paisagem-topo">
                <div class="container">
                    <p class="trilha"><a href="paisagens.html">Paisagens</a> <span aria-hidden="true">›</span> {p['nome']}</p>
                    <div class="paisagem-topo-grade">
                        <div>
                            <p class="guia-chapeu">Formação {p['formacao'].lower()} · {i + 1} de {len(P)}</p>
                            <h1>{p['nome']}</h1>
                            <p class="paisagem-abre">{p['texto']}{''.join(fonte(n) for n in p['f'])}</p>
                            <dl class="paisagem-dados"><dt>Cobertura</dt><dd>{p['cobertura']}</dd><dt>Altura</dt><dd>{p['altura']}</dd></dl>
                        </div>
                        <figure class="paisagem-figura">{foto or desenho_grande(i, p)}<figcaption>{'' if foto else 'Desenho do trecho no corte do Cerrado, do campo à mata. '}<a href="paisagens.html#tipo-{p['id']}">Ver no corte inteiro</a></figcaption></figure>
                    </div>
                </div>
            </section>
            <div class="container paisagem-corpo">
                <section aria-labelledby="reconhecer-titulo">
                    <h2 id="reconhecer-titulo" class="sub">Como reconhecer</h2>
                    <p>{p['reconhecer']}</p>
                </section>
                <section aria-labelledby="importa-titulo">
                    <h2 id="importa-titulo" class="sub">Por que importa</h2>
                    <p>{texto_mais}{fonte(33) if p['id'] in LEI else ''}</p>
                </section>
                <section aria-labelledby="onde-titulo">
                    <h2 id="onde-titulo" class="sub">Onde ver</h2>
                    <ul class="lista">{onde_li}</ul>
                </section>
            </div>
            <section class="secao creme" aria-labelledby="esp-titulo">
                <div class="container">
                    <h2 id="esp-titulo">Espécies desta paisagem</h2>
                    <p class="intro">{n_esp} espécies do catálogo aparecem nesta paisagem. <a href="especies.html?paisagem={p['id']}">Ver com os filtros</a></p>
                    {icones_defs()}<ul class="especies-lista">{cartoes_esp}</ul>
                </div>
            </section>
            <div class="container">
                <nav class="ficha-navegar" aria-label="Outras paisagens">
                    <a href="paisagem-{ant['id']}.html" rel="prev"><span aria-hidden="true">←</span> {ant['nome']}</a>
                    <a href="paisagem-{prox['id']}.html" rel="next">{prox['nome']} <span aria-hidden="true">→</span></a>
                </nav>
            </div>
        </article>
'''
    pagina(f'paisagem-{p["id"]}.html', f'{p["nome"]}, uma paisagem do Cerrado — Guia do Cerrado',
           f'{p["nome"]}: como é, como reconhecer, por que importa, onde ver e as espécies dessa paisagem do Cerrado.', corpo)

# na página das paisagens, cada ficha leva à página completa; no catálogo, o "Onde" leva às paisagens
q = M / 'paisagens.html'; t = q.read_text()
t = re.sub(r'<p class="mais"><a href="especies\.html\?paisagem=([a-z-]+)">Espécies desta paisagem →</a></p>',
           r'<p class="mais paisagem-links"><a href="paisagem-\1.html">Página completa →</a> <a href="especies.html?paisagem=\1">Espécies desta paisagem →</a></p>', t)
q.write_text(t)
ATUAL['paisagem-'] = 'paisagens.html'
so_pt = json.loads((AQUI / 'so-pt.json').read_text())
for p in P:
    f = f'paisagem-{p["id"]}.html'
    if f not in so_pt: so_pt.append(f)
(AQUI / 'so-pt.json').write_text(json.dumps(so_pt, ensure_ascii=False, indent=2) + '\n')
for f in so_pt:
    if f == '404.html': continue
    q = M / f; t = q.read_text()
    t = re.sub(r'<ul class="menu" id="menu">.*?</ul>', menu_pt(f), t, count=1)
    t = com_rodape_novo(t)
    q.write_text(t)
lista = ''.join(f'<li id="f{n}"><span class="fonte-numero">{n}</span> {t} <a href="{u}" rel="noopener">Abrir a fonte</a></li>' for n, t, u in FONTES)
q = M / 'fontes.html'; t = q.read_text()
t = re.sub(r'<ol class="fontes-lista">.*?</ol>', '<ol class="fontes-lista">' + lista + '</ol>', t, flags=re.S)
q.write_text(t)
print('páginas das paisagens:', len(P))

# ================================================================ As fichas completas (especie-<id>.html) das espécies do dicionário FICHAS
FONTES += [
 (34, 'Tatu-canastra: estudo em Goiás (revista Multi-Science, IF Goiano), com o peso médio de 28 kg das fêmeas e 44 kg dos machos; e Estado de Minas (2026), as tocas usadas por mais de 100 espécies de vertebrados.', 'https://periodicos.ifgoiano.edu.br/multiscience/article/download/569/467/2140'),
 (35, 'National Geographic Brasil. Qual é o maior felino das Américas (2024); e o levantamento de medidas e pesos da onça-pintada, que variam com a região.', 'https://www.nationalgeographicbrasil.com/animais/2024/11/qual-e-o-maior-felino-das-americas-alguns-exemplares-medem-ate-1-metro-e-80-centimetros'),
 (36, 'UniCEUB (monografia, 2002): o veado-campeiro, com 1,2 a 1,5 m de comprimento, 70 a 75 cm de altura e 30 a 40 kg; só os machos têm chifres.', 'https://repositorio.uniceub.br/jspui/bitstream/123456789/2445/2/9810853.pdf'),
 (37, 'InfoEscola. Ema: a maior ave do Brasil, de 1,3 a 1,7 m e 25 a 45 kg; o macho choca os ovos por cerca de 38 dias.', 'https://www.infoescola.com/aves/ema/'),
 (38, 'Procarnívoros. Raposinha-do-campo: de 2,5 a 4 kg, com os cupins como base da alimentação.', 'https://procarnivoros.org.br/animais/raposinha-do-campo/'),
 (39, 'Embrapa e trabalhos acadêmicos: o pequizeiro (6 a 10 m, até mais de 12 m; 500 a 2.000 frutos por safra), o baru (até 25 m, Embrapa) e o buriti (até 35 m, folder da Embrapa).', 'https://www.infoteca.cnptia.embrapa.br/infoteca/bitstream/doc/859495/1/folderburiti.pdf'),
 (40, 'Prefeitura de Belo Horizonte. Dia Mundial da Anta: mais de 2 m de comprimento, mais de 1 m de altura e até 250 kg (outras fontes falam em 300 kg).', 'https://prefeitura.pbh.gov.br/noticias/dia-mundial-da-anta'),
 (41, 'Oiseaux.net. Brazilian Merganser: cerca de 56 cm e de 600 a 700 g; e o sumário do Plano de Ação Nacional do pato-mergulhão (ICMBio).', 'https://oiseaux.net/birds/brazilian.merganser.html'),
 (42, 'Procarnívoros. Cachorro-vinagre: de 50 a 75 cm de cabeça e corpo, cauda de 12 a 15 cm e de 5 a 7 kg; caça em grupo.', 'https://procarnivoros.org.br/animais/cachorro-vinagre/'),
 (43, 'National Geographic Brasil. As 6 curiosidades sobre a capivara (2023): cerca de 1,3 m, até 60 cm de altura e de 50 a 80 kg.', 'https://www.nationalgeographicbrasil.com/animais/2023/04/as-6-curiosidades-sobre-a-capivara-o-maior-roedor-do-mundo'),
 (44, 'Revista Pesquisa FAPESP. Como o macaco-prego quebra castanha, e as transformações milenares nas ferramentas de pedra da Serra da Capivara.', 'https://revistapesquisa.fapesp.br/como-o-macaco-prego-quebra-castanha/'),
 (45, 'InfoEscola. Coruja-buraqueira: de 22 a 28 cm e cerca de 150 g; mora em tocas, muitas vezes deixadas por tatus.', 'https://www.infoescola.com/aves/coruja-buraqueira/'),
 (46, 'National Geographic Brasil (2024), com o Instituto Butantan: a cascavel, a única espécie do gênero no Brasil, pode passar de 1,5 m.', 'https://www.nationalgeographicbrasil.com/animais/2024/01/conheca-5-caracteristicas-da-cascavel-uma-das-cobras-mais-perigosas-do-mundo'),
 (47, 'Agência FAPESP. Os cupinzeiros luminosos do Parque Nacional das Emas e o sumiço dos vaga-lumes perto das lavouras.', 'https://agencia.fapesp.br/luzes-de-alerta/12138'),
 (48, 'Revista Pesquisa FAPESP. A dieta equilibrada do lobo-guará: cerca de metade frutos, com a lobeira perto de um terço do total.', 'https://revistapesquisa.fapesp.br/a-dieta-equilibrada-do-lobo-guara/'),
 (49, 'Embrapa Cerrados, comunicado técnico 358 (2015), e Revista Brasileira de Fruticultura (v. 23, n. 2): a cagaiteira, sua florada e a safra.', 'https://scielo.br/pdf/rbf/v23n2/7976.pdf'),
 (50, 'Conexão Tocantins e Jornal Opção: a colheita do capim-dourado, de 20 de setembro a 30 de novembro, por artesãos credenciados pelo Naturatins.', 'https://jornalopcao.com.br/tocantins/festa-no-jalapao-celebra-colheita-do-capim-dourado-531164/'),
 (51, 'Prefeitura de Belo Horizonte. Dia Internacional do Puma: de 1,5 a 2,75 m com a cauda; os machos de 40 a 72 kg e as fêmeas de 34 a 48 kg.', 'https://prefeitura.pbh.gov.br/fundacao-de-parques-e-zoobotanica/dia-internacional-do-puma'),
 (52, 'ICMBio (CPB), ficha do tamanduá-mirim; e revisões acadêmicas com corpo de 47 a 77 cm, cauda de 40 a 68 cm e peso de 3,5 a 8,5 kg.', 'https://www.gov.br/icmbio/pt-br/assuntos/centros-de-pesquisa/cpb/arquivos/fichas_xenathra/pilosa/ficha_tamandua_tetradactyla.pdf'),
 (53, 'InfoEscola. Jaguatirica: de 70 a 100 cm e cauda de uns 40 cm; e Biotemas (UFSC), com 8 a 15 kg e média de 11 kg.', 'https://www.infoescola.com/mamiferos/jaguatirica/'),
 (54, 'Anais do SIIEPE (UFPel, 2015): medidas do carcará; e guias de aves, com 50 a 65 cm e asas abertas de até 1,3 m.', 'https://anais-siiepe.ufpel.edu.br/2015/CB_02854.pdf'),
 (55, 'Agência Estadual de Notícias do Paraná: o sono de inverno do teiú; e trabalhos do Butantan e da Unesp (de três a cinco meses na toca).', 'https://www.parana.pr.gov.br/aen/Noticia/Se-encontrar-nao-acorde-lagartos-teiu-entram-em-periodo-de-sono-profundo-no-inverno'),
 (56, 'National Geographic Brasil (2024), com o Instituto Butantan: quatro fatos sobre as jiboias, que em geral têm de 2 a 3 m.', 'https://www.nationalgeographicbrasil.com/animais/2024/07/dia-mundial-das-cobras-conheca-4-fatos-sobre-as-jiboias'),
 (57, 'Embrapa. Mangaba: o porte, as safras (no Cerrado, de outubro a dezembro) e o peso dos frutos.', 'https://www.infoteca.cnptia.embrapa.br/infoteca/bitstream/doc/1104669/1/Mangaba.pdf'),
 (58, 'Embrapa Cerrados, documento 280 (Cohen, 2010): o jatobá-do-cerrado, até 10 m, e a farinha da polpa.', 'https://www.infoteca.cnptia.embrapa.br/infoteca/bitstream/doc/953441/1/doc280.pdf'),
 (59, 'Embrapa. Espécies arbóreas brasileiras, vol. 3: a macaubeira, até 15 m, os espinhos e o óleo da polpa e da amêndoa.', 'https://www.alice.cnptia.embrapa.br/alice/bitstream/doc/1136643/1/Especies-Arboreas-Brasileiras-vol-3-Macaubeira.pdf'),
 (60, 'Monografia da UFU sobre o cachorro-do-mato: de 5 a 8 kg, uns 65 cm de corpo e 30 cm de cauda; a dieta onívora.', 'https://repositorio.ufu.br/bitstream/123456789/20856/3/MorfometriaCr%c3%a2nioCachorro.pdf'),
 (61, 'ICMBio, ficha do tatu-peba; e ((o))eco: de 3,2 a 6,5 kg, de 40 a 95 cm de corpo e 12 a 24 cm de cauda.', 'https://www.gov.br/icmbio/pt-br/assuntos/centros-de-pesquisa/primatas-brasileiros/arquivos/fichas_xenathra/cingulata/ficha_euphractus_sexcinctus.pdf'),
 (62, '((o))eco. O narigudo quati de cauda anelada: de 2 a 7,2 kg e de 85 a 113 cm; e anais da SEB, bandos de até 30.', 'https://www.oeco.org.br/wp-content/uploads/wp-post-to-pdf-enhanced-cache/1/27582-o-narigudo-quati-de-cauda-anelada.pdf'),
 (63, 'ICMBio, ficha do sagui-de-tufos-pretos; e anais da SEB, com o peso de cerca de 250 g e a goma na dieta.', 'https://www.gov.br/icmbio/pt-br/assuntos/centros-de-pesquisa/primatas-brasileiros/arquivos/fichas_primatas/CALLITRICHIDAE/ficha_callithrix_penicillata.pdf'),
 (64, 'UFU, relato sobre a lontra-neotropical: de 5 a 14 kg, corpo de 53 a 80 cm e cauda de 36 a 50 cm; quase ameaçada (ICMBio).', 'https://repositorio.ufu.br/bitstream/123456789/37356/1/Piot%c3%b3raxLontraLontra.pdf'),
 (65, 'Portal São Francisco e guias de aves: o urubu-rei, de 1,7 a quase 2 m de asa a asa e de 3 a 5 kg.', 'https://www.portalsaofrancisco.com.br/animais/urubu-rei'),
 (66, 'ICMBio. Sumário do Plano de Ação Nacional dos Papagaios: o papagaio-verdadeiro, 36 cm, 400 g, 60 anos em média, quase ameaçado.', 'https://www.gov.br/icmbio/pt-br/assuntos/biodiversidade/pan/pan-papagaios/2-ciclo/pan-papagaios-sumario.pdf'),
 (67, 'Bianchi (2009), Ornitologia Neotropical 20: o papagaio-galego faz ninho em cupinzeiros; incubação de 19 a 22 dias.', 'https://sora.unm.edu/sites/default/files/ON%2020%284%29%20479-489.pdf'),
 (68, 'Oiseaux-Birds e outros guias: a gralha-do-campo, de 33 a 40 cm (as fontes divergem), cerca de 180 g.', 'https://www.oiseaux-birds.com/card-curl-crested-jay.html'),
 (69, 'Prefeitura de São Paulo, espécies da cidade: o pica-pau-do-campo, que vive no chão e come formigas e cupins (cerca de 32 cm).', 'https://prefeitura.sp.gov.br/meio_ambiente/w/servicos/fauna/especies_da_cidade/11296'),
 (70, 'Wikipédia (em inglês), com base em guias de aves: o beija-flor-tesoura, de 15 a 17 cm e até 9 g.', 'https://en.wikipedia.org/wiki/Swallow-tailed_hummingbird'),
 (71, '((o))eco. Foto do dia: curicaca, com cerca de 70 cm de comprimento e 40 cm de altura, e o que ela come.', 'https://www.oeco.org.br/wp-content/uploads/wp-post-to-pdf-enhanced-cache/1/22874-foto-do-dia-curicaca.pdf'),
 (72, 'National Geographic Brasil (2024), com o Instituto Butantan: a diferença entre a coral verdadeira e a falsa.', 'https://www.nationalgeographicbrasil.com/animais/2024/02/qual-a-diferenca-entre-a-cobra-coral-verdadeira-e-a-cobra-coral-falsa'),
 (73, 'ICMBio, Sistema SALVE: a avaliação do jabuti-piranga, com a maturidade aos 20 a 25 cm de casco e machos de mais de 50 cm (Pritchard e Trebbau, 1984).', 'https://salve.icmbio.gov.br/salve/api/fichaHash/4f61496a79626d6831663232683859502f6e4d5176673d3d'),
 (74, 'EcoRegistros. Rhinella diptycha: as glândulas paratoides, a dieta e os hábitos noturnos.', 'https://ecoregistros.org/sheet/Rhinella-diptycha'),
 (75, 'InfoEscola. Dourado: a piracema de até 400 km; e estudos da UEM sobre barragens e a migração.', 'https://www.infoescola.com/peixes/dourado/'),
 (76, 'Conexão Tocantins (2017), com a Embrapa: as guardas da jataí; e artigos com o tamanho e a produção de mel.', 'https://conexaoto.com.br/2017/03/01/abelhas-sem-ferrao-passaram-por-processo-evolutivo-e-usam-guardas-especializadas-para-defender-as-colmeias-de-invasores'),
 (77, 'Museu de História Natural e Jardim Botânico da UFMG: o ipê-amarelo; e material educativo com 4 a 14 m e a florada de julho a setembro.', 'https://www.ufmg.br/mhnjb/ceplamt/plantadomes/abril-de-2019-ipe-amarelo/'),
 (78, 'Museu de História Natural e Jardim Botânico da UFMG: o ipê-roxo; e Correio Braziliense (2024), a florada em Brasília.', 'https://www.ufmg.br/mhnjb/ipe-roxo/'),
 (79, 'Embrapa Cerrados, boletim 270: o araticum, o peso dos frutos; e Plantas para o Futuro (4 a 8 m).', 'https://www.infoteca.cnptia.embrapa.br/infoteca/bitstream/doc/883941/1/bolpd270.pdf'),
 (80, 'Embrapa. Babaçu; e revisão da UFMA: até 20 m, a amêndoa com mais de 60% de óleo e o Maranhão com 93,8% da produção.', 'https://www.alice.cnptia.embrapa.br/alice/bitstream/doc/1050840/1/Babacu.pdf'),
 (81, 'Embrapa. Plantas para o Futuro, região Norte: o barbatimão, os taninos da casca e o uso cicatrizante.', 'https://www.infoteca.cnptia.embrapa.br/infoteca/bitstream/doc/1144711/1/Plantas-para-o-Futuro-Norte-1089-1095.pdf'),
 (82, 'Embrapa. Espécies arbóreas brasileiras, vol. 3: o pau-terra, até perto de 30 m, em 88% do Cerrado; e estudos da UnB sobre o acúmulo de alumínio.', 'https://www.alice.cnptia.embrapa.br/alice/bitstream/doc/1136652/1/Especies-Arboreas-Brasileiras-vol-3-Pau-terra-grande.pdf'),
 (83, 'Revista Pesquisa FAPESP. Ambiente único: as canelas-de-ema; e Agência FAPESP, o fogo e a florada.', 'https://revistapesquisa.fapesp.br/ambiente-unico/'),
 (84, 'ONU Brasil. Sistemas agrícolas apoiados pela FAO: os apanhadores de flores sempre-vivas da Serra do Espinhaço.', 'https://brasil.un.org/pt-br/201060-sistemas-agr%C3%ADcolas-apoiados-pela-fao-protegem-biodiversidade'),
 (85, 'Embrapa. Espécies arbóreas brasileiras, vol. 1: a copaíba, o porte e a coleta do óleo.', 'https://www.alice.cnptia.embrapa.br/alice/bitstream/doc/1139732/1/Especies-Arboreas-Brasileiras-vol-1-Copaiba.pdf'),
 (86, 'Embrapa. Plantas para o Futuro, Centro-Oeste: a sucupira-branca e o uso do óleo do fruto.', 'https://ainfo.cnptia.embrapa.br/digital/bitstream/doc/1073523/1/regio-centro-oeste-26-07-20171-862-875.pdf'),
 (87, 'Embrapa. Folder do murici: o fruto e o porte; e trabalhos da Embrapa sobre as safras.', 'https://www.infoteca.cnptia.embrapa.br/infoteca/bitstream/doc/859538/1/foldermurici.pdf'),
 (88, 'UFMG. Cajuzinho-do-cerrado: de 30 cm a 1,5 m, o tronco subterrâneo, a florada e a frutificação.', 'https://repositorio.ufmg.br/bitstream/1843/76920/2/Cajuzinho-do-cerrado.pdf'),
 (89, 'Embrapa: caracterização dos frutos da gabiroba; e estudo de fenologia em Bambuí (MG).', 'https://www.alice.cnptia.embrapa.br/alice/bitstream/doc/941017/1/CristianeHCBFrutCaracterizacao.pdf'),
 (90, 'Secretaria de Meio Ambiente de São Paulo: o jenipapo e a origem do nome; e trabalhos sobre a genipina e a pintura.', 'https://semil.sp.gov.br/?p=61480'),
 (91, 'Embrapa Cerrados, comunicado técnico 97: a guariroba e o palmito amargo de Goiás.', 'https://www.infoteca.cnptia.embrapa.br/infoteca/bitstream/doc/568687/1/comtec97.pdf'),
 (92, 'Movimento Econômico (2026): a UFPI e a fava-d’anta, que dá metade da rutina do mundo; e estudos da UFMG sobre o faveiro.', 'https://movimentoeconomico.com.br/ciencia/2026/09/25/ufpi-mapeia-genetica-da-fava-danta-do-cerrado-que-supre-50-da-rutina-mundial/'),
 (93, 'PhytoKeys (2024): uma espécie nova de Paepalanthus e as floras das serras de Minas; o gênero e o endemismo.', 'https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11188062/'),
 (94, 'UFU: anatomia foliar da lixeira e a sílica das folhas; e trabalhos com a altura das árvores.', 'https://repositorio.ufu.br/bitstream/123456789/25976/1/AnatomiaFoliarEspecies.pdf'),
 (95, 'Ciência da Madeira (UFPel): a cortiça do pau-santo, com cerca de 28% de suberina.', 'https://periodicos.ufpel.edu.br/index.php/cienciadamadeira/article/view/7686/7124'),
 (96, 'EPAMIG, circular técnica 201, e anais da Sociedade de Ecologia do Brasil: os cupinzeiros de Cornitermes cumulans, de 60 cm a mais de 1,5 m, e os animais que abrigam.', 'https://livrariaepamig.com.br/wp-content/uploads/2023/03/CT-201.pdf'),
 (97, 'ICMBio, Sistema SALVE: a queixada, vulnerável; e estudo do Pantanal (Imasul), com bandos de 50 a 300 animais.', 'https://www.imasul.ms.gov.br/wp-content/uploads/2018/08/A-resposta-de-Catetos-e-Queixadas-a-flutuações-Sazonais-no-pantanal.pdf'),
 (98, '((o))eco. Caititu, parece mas não é: o cateto, de 14 a 30 kg, em grupos de 5 a 25; e a revista MG.Biota.', 'https://www.oeco.org.br/wp-content/uploads/wp-post-to-pdf-enhanced-cache/1/27989-caititu-parece-mas-nao-e.pdf'),
 (99, '((o))eco. Veado-catingueiro em todos os lugares: de 17 a 23 kg, cerca de 50 cm de altura e os chifres simples dos machos.', 'https://oeco.org.br/wp-content/uploads/wp-post-to-pdf-enhanced-cache/1/28008-veado-catingueiro-em-todos-os-lugares.pdf'),
 (100, 'Revista Therya Ixmana: a paca, de 6 a 12 kg e de 50 a 75 cm; e o projeto de reintrodução da paca no Iberá.', 'https://theryaixmana.mastozoologiamexicana.com/index.php/theryaixmana/article/download/720/690/13542'),
 (101, 'UFMG (dissertação) e Rodriguésia: a cutia e a dispersão de sementes, com 74% das sementes levadas e 36% enterradas.', 'https://repositorio.ufmg.br/handle/1843/33136'),
 (102, 'ICMBio, ficha do bugio-preto; e Jornal da USP, o silêncio dos bugios e o alerta da febre amarela.', 'https://www.gov.br/icmbio/pt-br/assuntos/centros-de-pesquisa/primatas-brasileiros/arquivos/fichas_primatas/ATELIDAE/ficha_alouatta_caraya.pdf'),
 (103, 'Ciência Animal Brasileira (UFG): o mão-pelada, o maior procionídeo do Brasil, com as medidas e a dieta.', 'https://revistas.ufg.br/vet/article/download/9824/8374/50478'),
 (104, 'INIC/Univap (2024): a irara, de 4 a 10 kg, corpo de 56 a 68 cm e cauda de 37,5 a 47 cm; e Folha BV, a origem tupi do nome.', 'https://www.inicepg.univap.br/cd/INIC_2024/anais/arquivos/RE_0818_0424_01.pdf'),
 (105, 'Revista Pesquisa FAPESP: a arara-azul-grande, 1 m e até 1,3 kg; 95% dos ninhos em manduvis; cerca de 6 mil no Pantanal.', 'https://revistapesquisa.fapesp.br/wp-content/uploads/2022/10/047-049_arara-azul_321.pdf'),
 (106, '((o))eco. Um trabalhador incansável: o joão-de-barro e a construção da casa.', 'https://www.oeco.org.br/wp-content/uploads/wp-post-to-pdf-enhanced-cache/1/27952-um-trabalhador-incansavel.pdf'),
 (107, 'Ibram-DF. Aves de Águas Emendadas: o bem-te-vi; e Prefeitura de São Paulo, espécies da cidade.', 'https://prefeitura.sp.gov.br/meio_ambiente/w/servicos/fauna/especies_da_cidade/11315'),
 (108, 'Estudo de nidificação do periquito-rei em cupinzeiros (1995–1998); e Parrots.org, com o tamanho e o peso.', 'https://core.ac.uk/download/296714505.pdf'),
 (109, 'Revista Pesquisa FAPESP. Ninhos em conflito: o anu-branco e o ninho coletivo.', 'https://revistapesquisa.fapesp.br/ninhos-em-conflito/'),
 (110, 'Gazeta SP e outros: o canário-da-terra, cerca de 13,5 cm e 20 g, e o tráfico (fontes de divulgação; a conferir no Ibama).', 'https://www.gazetasp.com.br/gazeta-mais/curiosidades/canario-da-terra-trafico-fauna/'),
 (111, 'Prefeitura de São Paulo, espécies da cidade: o gavião-carijó; e guias de aves, de 31 a 41 cm.', 'https://prefeitura.sp.gov.br/meio_ambiente/w/servicos/fauna/especies_da_cidade/13233'),
 (112, 'UFPA (dissertação, 2021): o olfato do urubu-de-cabeça-preta; e Oiseaux.net, envergadura e peso.', 'https://ppgnc.propesp.ufpa.br/ARQUIVOS/dissertacoes/2021/LARISSA%20HASNAH%20QUEIROZ%20DOS%20SANTOS.pdf'),
 (113, 'Biota Neotropica (2022): o morcego que poliniza e dispersa sementes na cidade; e Annals of Botany (2009), as 528 plantas polinizadas por morcegos.', 'https://www.biotaneotropica.org.br/BN/article/view/1890'),
 (114, 'USP, tese de Miranda-Vilela: a temperatura de incubação e o sexo dos filhotes do jacaré-de-papo-amarelo; e ICMBio, a avaliação de 2013.', 'https://teses.usp.br/teses/disponiveis/11/11139/tde-20200111-154715/'),
 (115, 'National Geographic Brasil (2023): qual a maior cobra do Brasil; e o Instituto Butantan sobre a sucuri-verde.', 'https://www.nationalgeographicbrasil.com/animais/2023/08/qual-a-maior-cobra-do-brasil-o-tamanho-dela-vai-te-impressionar'),
 (116, 'Revista da Sociedade Brasileira de Medicina Tropical (2010) e Ministério da Saúde: a caiçaca e os acidentes com jararacas.', 'https://www.scielo.br/j/rsbmt/a/xmYQRDFjDn7bD4hgfh59kWh/?lang=en'),
 (117, 'Revista Brasileira de Biologia: a dieta do calango Tropidurus torquatus; e o Reptile Database, com os nomes populares.', 'https://reptile-database.reptarium.cz/Tropidurus/torquatus'),
 (118, 'UFU: história natural da rã-pimenta, o ninho de espuma, os 2.100 ovos e os girinos.', 'https://repositorio.ufu.br/bitstream/123456789/26826/1/HistoriaNaturalRa-Pimenta.pdf'),
 (119, 'Galetti e outros (2008) e Mongabay: o pacu, os frutos de palmeira e a dispersão de sementes no Pantanal.', 'https://news.mongabay.com/2008/02/overfishing-may-hurt-amazon-forest-trees/'),
 (120, 'Aquário de La Rochelle e Wikipédia (em inglês): a piranha-vermelha, o tamanho, o cardume e a fama exagerada.', 'https://www.aquarium-larochelle.com/en/species-encyclopedia/red-bellied-piranha/'),
 (121, 'Epagri e Portal Amazônia: as saúvas, o fungo cultivado, a rainha e os formigueiros fundos.', 'https://publicacoes.epagri.sc.gov.br/BD/article/download/2267/2018/18125'),
 (122, 'Ciência Rural (2003) e UFC (tese, 2018): as mamangavas, os ninhos em madeira e a polinização do maracujá.', 'https://repositorio.ufc.br/bitstream/riufc/59829/7/2018_tese_admbezerra.pdf'),
 (123, 'Pacheco e outros (PPBio, INPA): os rola-bostas e os serviços ao solo; e UEMS, 29 espécies entre o Cerrado e o Pantanal.', 'https://ppbio.inpa.gov.br/sites/default/files/Pacheco_T_L_et_al_2021_capitulo_livro.pdf'),
 (124, 'Jornal de Brasília (Agência Brasil): as cigarras na primavera de Brasília; e anais da UEG, as cigarras em Goiás.', 'https://jornaldebrasilia.com.br/brasilia/cigarras-voltam-e-anunciam-chegada-da-primavera-em-brasilia/'),
 (125, 'Virginia Tech, ficha de dendrologia: Tabebuia aurea, a casca corticosa e a floração na seca; e Universidade da Flórida.', 'https://dendro.cnre.vt.edu/dendrology/syllabus/factsheet.cfm?ID=904'),
 (126, 'Embrapa. Espécies arbóreas brasileiras, vol. 1: o angico-vermelho; e UFCG, os taninos da casca.', 'https://www.alice.cnptia.embrapa.br/alice/bitstream/doc/1137299/1/Especies-Arboreas-Brasileiras-vol-1-Angico-Vermelho.pdf'),
 (127, 'IPEF, Scientia Forestalis: a aroeira, a madeira e a situação de ameaça.', 'https://www.ipef.br/publicacoes/scientia/nr87/cap17.pdf'),
 (128, 'Revisão (MDPI, Life) e anais: a sucupira-preta, árvore do cerrado de madeira densa e resistente.', 'https://www.mdpi.com/2075-1729/16/2/358'),
 (129, 'Embrapa. Espécies arbóreas brasileiras, vol. 4: a pimenta-de-macaco; e a Arca do Gosto do Slow Food.', 'https://www.alice.cnptia.embrapa.br/alice/bitstream/doc/1140063/1/Especies-Arboreas-Brasileiras-vol-4-Pimenta-de-Macaco.pdf'),
 (130, 'Registros de herbário (IBGE, Jardim Botânico de Brasília) e Museu do Cerrado: a caliandra.', 'https://museucerrado.com.br/wp-content/uploads/2021/01/LETRA_C.pdf'),
 (131, 'Revista Pesquisa FAPESP. A essência da arnica; e Edinburgh Journal of Botany (2017), o fogo e a coleta.', 'https://revistapesquisa.fapesp.br/a-essencia-da-arnica/'),
 (132, 'Embrapa, Documentos 370 e Plantas para o Futuro: o algodãozinho-do-campo, o xilopódio e os cuidados com a raiz.', 'https://www.infoteca.cnptia.embrapa.br/infoteca/bitstream/doc/1124921/1/documentos-370-1.pdf'),
 (133, 'Embrapa. Plantas para o Futuro, Centro-Oeste: o abacaxi-do-cerrado; e o estudo de 2025 sobre frutas do Cerrado.', 'https://www.alice.cnptia.embrapa.br/alice/bitstream/doc/1073536/1/regio-centro-oeste-26-07-20171-913-920.pdf'),
 (134, 'Embrapa. Espécies arbóreas brasileiras, vol. 4: o tingui.', 'https://www.alice.cnptia.embrapa.br/alice/bitstream/doc/1140267/1/Especies-Arboreas-Brasileiras-vol-4-Tingui.pdf'),
 (135, 'Slow Food, Arca do Gosto: o bacupari-do-cerrado; e Ibram-DF, folder dos frutos.', 'https://www.fondazioneslowfood.com/en/ark-of-taste-slow-food/bacupari-do-cerrado/'),
 (136, 'Embrapa. Espécies arbóreas brasileiras, vol. 5: o jacarandá-do-cerrado; e UniCEUB, monografia.', 'https://www.alice.cnptia.embrapa.br/alice/bitstream/doc/1140511/1/Especies-Arboreas-Brasileiras-vol-5-Jacaranda-do-Cerrado.pdf'),
 (137, 'Embrapa: uma espécie nova de Cyrtopodium do Cerrado e os 18 táxons do DF; e registros de herbário do IBGE sobre a florada depois do fogo.', 'https://www.alice.cnptia.embrapa.br/alice/bitstream/doc/187926/1/ID276141.pdf'),
 (138, 'Ibama, plano operativo do Parque Nacional das Emas; e anais do XI Congresso de Ecologia do Brasil: o capim-flecha e o fogo.', 'https://seb-ecologia.org.br/revistas/indexar/anais/xiceb/pdf/574.pdf'),
 (139, 'Embrapa. Espécies arbóreas brasileiras, vol. 2: o pau-de-tucano; e IPE, a floração.', 'https://www.alice.cnptia.embrapa.br/alice/bitstream/doc/1140880/1/Especies-Arboreas-Brasileiras-vol-2-Pau-de-Tucano.pdf'),
 (140, 'UFMG e Acta Scientiarum (2023): o puçá, o fruto e as variedades; e Embrapa, o puçá-preto.', 'https://repositorio.ufmg.br/handle/1843/76872'),
 (141, 'ICMBio, Sistema SALVE: a avaliação do urubu-rei, menos preocupante, presente em todos os biomas menos o Pampa.', 'https://salve.icmbio.gov.br/salve/api/pdf/doi/382b574f73347872452b77383535307574712f6f31426e62467a3153333031735359474f30524a643531593d/PDF'),
 (142, 'Ciência Animal Brasileira (UFU): o dimorfismo do jabuti-piranga, com o plastrão côncavo dos machos adultos.', 'https://periodicos.pucpr.br/cienciaanimal/article/download/24686/pdf/48751'),
 (143, 'Acta Scientiarum (UEM, 2016): o crescimento e a migração do dourado no rio Cuiabá, um peixe que passa de 1 m.', 'https://www.redalyc.org/journal/1871/187146621008/movil'),
 (144, 'Embrapa Cerrados, Documentos 375 (2021): particularidades biológicas dos ipês do Cerrado, entre eles o Handroanthus ochraceus.', 'https://www.infoteca.cnptia.embrapa.br/infoteca/bitstream/doc/1139933/1/Doc-375.pdf'),
 (145, 'Revista Brasileira de Segurança Pública e estudos dos Cetas da Bahia (2009–2019) e de Goiás (2013–2017): o canário-da-terra, a ave mais apreendida.', 'https://pesquisa.bvsalud.org/bvs-vet/resource/pt/vtt-219682'),
 (146, 'Estudo num parque urbano de Taubaté (SP): o beija-flor-tesoura, de cerca de 18 cm, as plantas que visita e a defesa agressiva do território.', 'https://scielo.br/j/bjb/a/wNmKn67c8HCmZT9rFN5zbTb/?lang=en'),
 (147, 'Neotropical Biology and Conservation (2009): os predadores de ninhos em Águas Emendadas; e Journal of Field Ornithology (2003), a reprodução da gralha-do-campo.', 'https://dx.doi.org/10.1590/s1984-46702009000400028'),
 (148, 'National Geographic Brasil (2023), com o Instituto Butantan: as 4 curiosidades sobre a sucuri, com as fêmeas bem maiores que os machos.', 'https://www.nationalgeographicbrasil.com/animais/2023/11/as-4-curiosidades-sobre-a-sucuri-uma-das-cobras-mais-populares-do-brasil'),
]
FONTES.sort()

def escala_ficha(id_, nome, esc):
    """O bicho (ou a árvore) e uma pessoa de 1,70 m na mesma escala."""
    if not esc: return ''
    W2, chao = 420, 200
    px, ph = 40, 170
    if esc[0] in ('arvore', 'palmeira'):
        h_m = esc[1]; k = 180 / max(h_m, 1.7)  # px por metro, para caber
        hp = 1.7 * k; xa = 230; ha = h_m * k
        pessoa = f'<rect class="pessoa-barra" x="{px}" y="{chao - hp:.1f}" width="10" height="{hp:.1f}" rx="5"/>'
        if esc[0] == 'arvore':
            planta = f'<line class="tronco-escala" x1="{xa}" y1="{chao}" x2="{xa}" y2="{chao - ha * .55:.1f}"/><ellipse class="copa-escala" cx="{xa}" cy="{chao - ha * .72:.1f}" rx="{ha * .38:.1f}" ry="{ha * .28:.1f}"/>'
        else:
            planta = f'<line class="tronco-escala" x1="{xa}" y1="{chao}" x2="{xa}" y2="{chao - ha:.1f}"/>' + ''.join(f'<path class="folha-escala" d="M{xa} {chao - ha:.1f} q {dx * .5:.0f} -12 {dx} {dy}"/>' for dx, dy in [(-30, 10), (-20, -12), (0, -18), (20, -12), (30, 10)])
        rot = f'<text x="{px + 5}" y="222" text-anchor="start">1,70 m</text><text x="{xa}" y="222" text-anchor="middle">{esc[2]}</text>'
        return (f'<figure class="escala"><svg viewBox="0 0 {W2} 230" role="img" aria-labelledby="esc-{id_}"><title id="esc-{id_}">{nome}: {esc[2]}, ao lado de uma pessoa de 1,70 m</title>'
                f'<line class="chao" x1="0" y1="{chao}" x2="{W2}" y2="{chao}"/>{pessoa}{planta}{rot}</svg>'
                f'<figcaption>Na mesma escala: {nome.lower()}, {esc[2]}, e uma pessoa de 1,70 m (a barrinha à esquerda).</figcaption></figure>')
    comp, alt, txt = esc
    pessoa = (f'<g class="pessoa"><circle cx="{px + 15}" cy="{chao - 158}" r="12"/><rect x="{px}" y="{chao - 144}" width="30" height="74" rx="12"/>'
              f'<rect x="{px + 2}" y="{chao - 74}" width="11" height="74" rx="5"/><rect x="{px + 17}" y="{chao - 74}" width="11" height="74" rx="5"/></g>')
    c, a = comp * 100, alt * 100
    return (f'<figure class="escala"><svg viewBox="0 0 {W2} 230" role="img" aria-labelledby="esc-{id_}"><title id="esc-{id_}">{nome}: {txt}, ao lado de uma pessoa de 1,70 m</title>'
            f'<line class="chao" x1="0" y1="{chao}" x2="{W2}" y2="{chao}"/>{pessoa}<rect class="bicho" x="120" y="{chao - a}" width="{c}" height="{a}" rx="{min(a, 40) / 2}"/>'
            f'<text x="{px + 15}" y="222" text-anchor="middle">1,70 m</text><text x="{max(120 + c / 2, 150)}" y="222" text-anchor="middle">{re.split(r' (?:do|de) ', txt)[0]}</text></svg>'
            f'<figcaption>Na mesma escala: {txt}, ao lado de uma pessoa de 1,70 m.</figcaption></figure>')

POR_ID = {e[0]: e for e in ESP}

# "Não confunda com" (1/11/2026): pares de espécies parecidas, lado a lado, com a diferença numa frase
PARES = [
 ('onca-pintada', 'onca-parda', 'A pintada tem rosetas pelo corpo todo; a parda é lisa, de uma cor só (só os filhotes nascem pintados).'),
 ('onca-pintada', 'jaguatirica', 'A jaguatirica é do tamanho de um cachorro médio e tem manchas em correntes; a onça passa de 1,7 m e tem rosetas.'),
 ('lobo-guara', 'cachorro-do-mato', 'O lobo-guará é alto, de pernas pretas e compridas e pelagem ruiva; o cachorro-do-mato é baixo e cinza-amarelado.'),
 ('raposa-do-campo', 'cachorro-do-mato', 'A raposa-do-campo é menor, de focinho curto e dentes miúdos de comer cupim; o cachorro-do-mato é maior e come de tudo.'),
 ('cachorro-vinagre', 'cachorro-do-mato', 'O vinagre tem pernas curtas, corpo marrom-avermelhado e orelhas redondas, e anda em bando; o cachorro-do-mato anda em casal.'),
 ('tamandua-bandeira', 'tamandua-mirim', 'O bandeira é grande, de cauda peluda em forma de bandeira e vive no chão; o mirim é menor, tem um colete preto e sobe em árvores com a cauda pelada.'),
 ('tatu-canastra', 'tatu-peba', 'O canastra é enorme (1,5 m) e só sai à noite; o peba é bem menor, peludo, e anda de dia.'),
 ('anta', 'capivara', 'A anta tem uma tromba curta e pode passar de 250 kg; a capivara é um roedor de cabeça quadrada e uns 50 a 80 kg.'),
 ('ema', 'seriema', 'A ema não voa e passa de 1,3 m; a seriema é bem menor, tem um topete na base do bico e voa quando precisa.'),
 ('seriema', 'curicaca', 'A seriema tem pernas compridas e topete; a curicaca tem um bico longo e curvo. As duas gritam alto nos campos.'),
 ('papagaio-verdadeiro', 'papagaio-galego', 'O verdadeiro tem a testa azul e o rosto amarelo; o galego tem a cabeça toda amarela, sem azul.'),
 ('carcara', 'urubu-rei', 'O carcará anda pelo chão e tem um boné preto; o urubu-rei é branco e preto, de cabeça pelada colorida, e plana alto.'),
 ('jiboia', 'cascavel', 'A cascavel tem o chocalho na ponta da cauda e veneno; a jiboia não tem chocalho nem veneno e mata apertando.'),
 ('coral', 'jiboia', 'A coral tem anéis coloridos que dão a volta no corpo e é venenosa; a jiboia tem desenhos de sela nas costas e não tem veneno.'),
 ('ipe-amarelo', 'ipe-roxo', 'O roxo floresce primeiro, de junho a agosto; o amarelo vem depois, de julho a setembro. Os dois sem folhas.'),
 ('buriti', 'babacu', 'O buriti tem folhas em leque e cresce na água das veredas; o babaçu tem folhas em pena e forma palmeirais em terra firme.'),
 ('macauba', 'guariroba', 'A macaúba tem espinhos pretos no tronco e nas folhas; a guariroba não tem espinhos, e o palmito é amargo.'),
 ('capim-dourado', 'sempre-viva', 'O capim-dourado é a haste dourada do Jalapão; as sempre-vivas da Serra do Espinhaço têm cabecinhas de flores brancas ou douradas.'),
 ('sempre-viva', 'chuveirinho', 'A sempre-viva tem uma haste com uma cabecinha; o chuveirinho abre muitas hastes do mesmo ponto, como uma ducha.'),
 ('cagaita', 'gabiroba', 'A cagaita é uma árvore de até 10 m; a gabiroba é um arbusto baixo. As duas são primas da goiaba, de frutos amarelados.'),
 ('pau-terra', 'pau-santo', 'O pau-terra tem flores amarelas e tronco cor de terra; o pau-santo tem flores brancas e casca de cortiça.'),
 ('queixada', 'cateto', 'A queixada é escura, de queixo branco, e anda em bandos de dezenas a centenas; o cateto é cinzento, tem um colar claro e anda em grupos pequenos.'),
 ('veado-catingueiro', 'veado-campeiro', 'O catingueiro é pequeno, cinzento, de chifres simples, e vive na beira das matas; o campeiro é alaranjado, de chifres com galhos, e vive nos campos abertos.'),
 ('paca', 'cutia', 'A paca é mais pesada, tem fileiras de pintas brancas e sai à noite; a cutia é lisa, de pernas finas, e anda de dia.'),
 ('urubu-de-cabeca-preta', 'urubu-rei', 'O de cabeça preta é todo preto e anda em bando; o urubu-rei é branco e preto, de cabeça colorida, e bem maior.'),
 ('arara-azul-grande', 'arara-caninde', 'A arara-azul-grande é toda azul; a canindé é azul por cima e amarela por baixo.'),
 ('bugio', 'macaco-prego', 'O bugio é maior, ronca alto e come folhas; o macaco-prego é ágil, tem um topete e usa pedras para quebrar cocos.'),
 ('caicaca', 'jiboia', 'A caiçaca tem a cabeça triangular, a fosseta entre o olho e a narina e desenhos em V; a jiboia tem a cabeça menos destacada, desenhos de sela e não tem veneno.'),
 ('sucuri', 'jiboia', 'A sucuri vive na água, é bem maior e tem manchas pretas redondas; a jiboia vive em terra firme e tem desenhos de sela.'),
 ('pacu', 'piranha', 'O pacu tem dentes de amassar e come frutos; a piranha tem dentes cortantes e come principalmente peixes.'),
 ('jatai', 'mamangava', 'A jataí é minúscula, amarela e não pica; a mamangava é grande, preta e faz o ninho em madeira seca.'),
 ('caraiba', 'ipe-amarelo', 'A caraíba tem folhas prateadas e casca de cortiça e vive no cerrado aberto; o ipê-amarelo-do-cerrado tem folhas verdes e casca mais fina.'),
 ('jacaranda-do-cerrado', 'sucupira-preta', 'As duas têm flores roxas; o jacarandá tem folíolos lisos e vagem com uma ou duas sementes, e a sucupira-preta tem folíolos com pelinhos e a copa toda roxa na florada.'),
 ('pau-de-tucano', 'pau-terra', 'Os dois são da mesma família e têm flores amarelas com esporão; o pau-de-tucano tem cachos em pé de flores menores, e o pau-terra tem flores grandes de uma pétala só.'),
 ('puca', 'cagaita', 'O puçá dá frutinhas escuras, cor de vinho; a cagaita dá frutos amarelo-claros e ácidos.'),
 ('caliandra', 'chuveirinho', 'A caliandra é um arbusto de pincéis vermelhos; o chuveirinho é uma erva de cabecinhas brancas no alto de hastes finas.'),
]
def comparar(id_):
    pares = [(b if a == id_ else a, txt) for a, b, txt in PARES if id_ in (a, b)]
    if not pares: return ''
    este = POR_ID[id_]
    def lado(e, link):
        pist = pistas_de(e[0])
        nome = f'<a href="especie-{e[0]}.html">{e[1]}</a>' if link else e[1]
        return (f'<div class="lado{"" if link else " este"}"><p class="lado-nome">{nome}</p><p class="cientifico">{e[2]}</p>'
                f'<p>{pist[0] if pist else e[7]}</p></div>')
    blocos = ''.join(f'<div class="par"><div class="par-lados">{lado(este, False)}<span class="par-x" aria-hidden="true">×</span>{lado(POR_ID[o], True)}</div>'
                     f'<p class="par-diferenca"><strong>A diferença:</strong> {txt}</p></div>' for o, txt in pares)
    return (f'<section class="comparar" aria-labelledby="comparar-titulo"><h2 class="sub" id="comparar-titulo">Não confunda com</h2>{blocos}</section>')
ORDEM_F = list(FICHAS)
for n, id_ in enumerate(ORDEM_F):
    e = POR_ID[id_]; f = FICHAS[id_]
    _, nome, cien, grupo, reino, am, pais, _texto, _foto, _ficha, _fs = e
    ant, prox = POR_ID[ORDEM_F[n - 1]], POR_ID[ORDEM_F[(n + 1) % len(ORDEM_F)]]
    if foto_nova(id_):
        topo = f'<img src="{{{{raiz}}}}img/especies/{id_}.webp" srcset="{{{{raiz}}}}img/especies/{id_}-640.webp 640w, {{{{raiz}}}}img/especies/{id_}.webp 1000w" sizes="(max-width: 900px) 100vw, 55vw" alt="{nome}" width="1000" height="667" fetchpriority="high">'
    else:
        topo = f'<div class="ficha-sem-foto esp-{reino}" aria-hidden="true"><svg viewBox="0 0 24 24" width="120" height="120">{ICONES[grupo]}</svg><p>Foto em breve</p></div>'
    selo = f'<span class="selo">{AMEACA[am]} (lista nacional)</span>' if am else ''
    fatos = ''.join(f'<dt>{k}</dt><dd>{v}</dd>' for k, v in f['fatos'])
    rec = ''.join(f'<li>{r}</li>' for r in f['reconhecer'])
    pais_links = ', '.join(f'<a href="paisagem-{x}.html">{NOME_PAISAGEM[x].lower()}</a>' for x in pais)
    notas = ''.join(fonte(k) for k in f['fontes'])
    esc = escala_ficha(id_, nome, f['escala'])
    corpo = f'''        <article class="ficha-especie">
            <div class="container">
                <p class="trilha"><a href="especies.html">Espécies</a> <span aria-hidden="true">›</span> {nome}</p>
                <div class="ficha-topo">
                    {topo}
                    <div class="ficha-resumo">
                        <p class="ficha-grupo">{grupo}</p>
                        <h1>{nome}</h1>
                        <p class="cientifico">{cien}</p>
                        <p class="ficha-abre">{f['abre']}{notas}</p>
                        {selo}
                    </div>
                </div>
                <div class="ficha-corpo">
                    <section aria-labelledby="fatos-titulo">
                        <h2 class="sub" id="fatos-titulo">Em poucas palavras</h2>
                        <dl class="ficha-fatos">{fatos}</dl>
                    </section>
                    {f'<section aria-labelledby="tamanho-titulo"><h2 class="sub" id="tamanho-titulo">Do tamanho de quê?</h2>{esc}</section>' if esc else ''}
                    <section aria-labelledby="reconhecer-titulo">
                        <h2 class="sub" id="reconhecer-titulo">Como reconhecer</h2>
                        <ul class="lista">{rec}</ul>
                    </section>
                    <section aria-labelledby="importa-titulo">
                        <h2 class="sub" id="importa-titulo">Por que importa</h2>
                        <p>{f['importa']}</p>
                    </section>
                    {comparar(id_)}
                    <section class="ficha-onde" aria-labelledby="onde-titulo">
                        <h2 class="sub" id="onde-titulo">Em que paisagens</h2>
                        <p>Aparece em: {pais_links}.</p>
                    </section>
                </div>
                <nav class="ficha-navegar" aria-label="Outras fichas">
                    <a href="especie-{ant[0]}.html" rel="prev"><span aria-hidden="true">←</span> {ant[1]}</a>
                    <a href="especie-{prox[0]}.html" rel="next">{prox[1]} <span aria-hidden="true">→</span></a>
                </nav>
                <p class="ficha-nota">Medidas aproximadas, de adultos, e as fontes discordam em alguns números: veja cada uma em <a href="fontes.html">Fontes</a>. A situação de ameaça é a da lista nacional.</p>
            </div>
        </article>
'''
    titulo = f'{nome} ({cien}) — Guia do Cerrado'
    if len(titulo) > 70: titulo = f'{nome} — Guia do Cerrado'  # o limite do validador
    pagina(f'especie-{id_}.html', titulo, f'{nome}: como reconhecer, do que vive, o tamanho, por que importa e em que paisagens do Cerrado aparece.', corpo)


for id_ in [e[0] for e in ESP if e[0] not in FICHAS]:
    q = M / f'especie-{id_}.html'
    if not q.exists(): continue
    h = re.sub(r'\s*<section class="comparar".*?</section>', '', q.read_text(), flags=re.S)
    c = comparar(id_)
    if c: h = h.replace('<section class="ficha-onde"', c + '\n                    <section class="ficha-onde"', 1)
    q.write_text(h)

so_pt = json.loads((AQUI / 'so-pt.json').read_text())
for id_ in FICHAS:
    f = f'especie-{id_}.html'
    if f not in so_pt: so_pt.append(f)
(AQUI / 'so-pt.json').write_text(json.dumps(so_pt, ensure_ascii=False, indent=2) + '\n')
for f in so_pt:
    if f == '404.html': continue
    q = M / f; t = q.read_text()
    t = re.sub(r'<ul class="menu" id="menu">.*?</ul>', menu_pt(f), t, count=1)
    t = com_rodape_novo(t)
    q.write_text(t)
lista = ''.join(f'<li id="f{n}"><span class="fonte-numero">{n}</span> {t} <a href="{u}" rel="noopener">Abrir a fonte</a></li>' for n, t, u in FONTES)
q = M / 'fontes.html'; t = q.read_text()
t = re.sub(r'<ol class="fontes-lista">.*?</ol>', '<ol class="fontes-lista">' + lista + '</ol>', t, flags=re.S)
q.write_text(t)
print('fichas novas:', len(FICHAS))

# ================================================================ O Cerrado mês a mês (1/11/2026): o que floresce, o que amadurece, o que aparece
NOMES_MES = ['janeiro', 'fevereiro', 'março', 'abril', 'maio', 'junho', 'julho', 'agosto', 'setembro', 'outubro', 'novembro', 'dezembro']
def meses(a, b):
    """De a até b (1 a 12), passando de dezembro para janeiro se for preciso."""
    return [((a - 1 + i) % 12) + 1 for i in range(((b - a) % 12) + 1)]
def quando_txt(m):
    if len(m) == 1: return f'em {NOMES_MES[m[0] - 1]}'
    return f'de {NOMES_MES[m[0] - 1]} a {NOMES_MES[m[-1] - 1]}'
CATS = [('paisagem', 'Na paisagem'), ('flores', 'Florescendo'), ('frutas', 'Frutas maduras'), ('bichos', 'Bichos')]
EVENTOS = [
 ('paisagem', 'As chuvas', 'bioma.html', meses(10, 4), 'Chove muito, os rios enchem e o cerrado fica verde de novo.', [4]),
 ('paisagem', 'A seca', 'bioma.html', meses(5, 9), 'Quase não chove. O capim seca, muitas árvores perdem as folhas e os bichos se juntam perto da água.', [4]),
 ('paisagem', 'O auge da seca e do fogo', 'ameacas.html#fazer', meses(8, 9), 'O ar fica seco e o fogo se espalha fácil. Não solte fogo, nem para limpar terreno.', [4, 6]),
 ('paisagem', 'Colheita do capim-dourado', 'especie-capim-dourado.html', meses(9, 11), 'No Jalapão, só de 20 de setembro a 30 de novembro, e só com as hastes secas.', [50]),
 ('paisagem', 'A piracema', 'especie-dourado.html', meses(11, 1), 'Peixes como o dourado sobem os rios para desovar na cheia. Em muitas bacias, a pesca fica proibida nessa época: confira as datas da sua.', [75]),
 ('flores', 'Ipê-roxo', 'especie-ipe-roxo.html', meses(6, 8), 'O primeiro ipê a florir na seca, sem folhas.', [78]),
 ('flores', 'Ipê-amarelo', 'especie-ipe-amarelo.html', meses(7, 9), 'Floresce inteiro de amarelo, sem nenhuma folha, por poucos dias.', [77]),
 ('flores', 'Cagaita', 'especie-cagaita.html', meses(8, 9), 'A copa fica toda branca, quase sem folhas, no fim da seca.', [49]),
 ('flores', 'Cajuzinho-do-cerrado', 'especie-cajuzinho.html', meses(7, 9), 'O cajueiro anão floresce rente ao chão.', [88]),
 ('flores', 'Pau-de-tucano', 'especie-pau-de-tucano.html', meses(11, 1), 'Cachos de flores amarelas no começo das chuvas.', [139]),
 ('frutas', 'Baru', 'especie-baru.html', meses(9, 10), 'Os frutos caem na seca, quando falta comida para os bichos.', [39]),
 ('frutas', 'Cajuzinho-do-cerrado', 'especie-cajuzinho.html', meses(8, 10), 'Os cajuzinhos amarelos e vermelhos do campo.', [88]),
 ('frutas', 'Cagaita', 'especie-cagaita.html', meses(10, 10), 'Amadurece com as primeiras chuvas, em poucas semanas.', [49]),
 ('frutas', 'Pequi', 'especie-pequi.html', meses(10, 3), 'A safra muda de região para região. Não morda o caroço: tem espinhos.', [39]),
 ('frutas', 'Mangaba', 'especie-mangaba.html', meses(10, 12), 'No Cerrado, em geral de outubro a dezembro. Só presta madura, caída.', [57]),
 ('frutas', 'Bacupari-do-cerrado', 'especie-bacupari.html', meses(11, 5), 'A fruta amarela e doce da época das chuvas.', [135]),
 ('frutas', 'Buriti', 'especie-buriti.html', meses(12, 6), 'Os cachos de frutos cor de vinho, nas veredas.', [39]),
 ('frutas', 'Araticum', 'especie-araticum.html', meses(2, 4), 'O fruto grande e perfumado, que pode pesar alguns quilos.', [79]),
 ('frutas', 'Murici', 'especie-murici.html', meses(2, 6), 'As frutinhas amarelas que cheiram de longe.', [87]),
 ('bichos', 'Cigarras cantando', 'especie-cigarra.html', meses(9, 12), 'Os machos cantam depois de anos embaixo da terra.', [124]),
 ('bichos', 'Cupinzeiros que brilham', 'especie-vaga-lume-cupinzeiro.html', meses(9, 11), 'Nas noites quentes e úmidas, as larvas de vaga-lume acendem os cupinzeiros das Emas.', [47]),
 ('bichos', 'Rã-pimenta no ninho', 'especie-ra-pimenta.html', meses(10, 1), 'Nas noites de chuva, os machos cavam bacias na margem para o ninho de espuma.', [118]),
 ('bichos', 'Teiú na toca', 'especie-teiu.html', meses(5, 8), 'No frio, o maior lagarto do Cerrado passa meses parado embaixo da terra.', [55]),
]
def evento_li(e):
    cat, nome, link, ms, txt, fs = e
    return (f'<li class="evento" data-meses="{" ".join(map(str, ms))}"><p class="evento-nome"><a href="{link}">{nome}</a></p>'
            f'<p class="evento-quando">{quando_txt(ms)}</p><p>{txt}{"".join(fonte(n) for n in fs)}</p></li>')
grupos_ev = ''.join(f'<section class="mes-grupo" data-cat="{c}" aria-labelledby="mes-{c}"><h2 class="sub" id="mes-{c}">{n}</h2>'
                    f'<ul class="eventos">{"".join(evento_li(e) for e in EVENTOS if e[0] == c)}</ul></section>' for c, n in CATS)
mes = f'''        <section class="titulo-pagina guia-topo">
            <div class="container">
                <p class="guia-chapeu">Guia do cerrado</p>
                <h1>O Cerrado mês a mês</h1>
                <p>O que floresce, que fruta está madura, que bicho aparece e o que acontece na paisagem em cada mês do ano. Escolha um mês.</p>
            </div>
        </section>
        <section class="secao">
            <div class="container mes-a-mes">
                <div class="mes-escolha" hidden>
                    <div class="meses" role="group" aria-label="Mês"></div>
                    <p class="mes-titulo" aria-live="polite"></p>
                </div>
                <div class="mes-grupos">{grupos_ev}</div>
                <p class="vazio mes-vazio" hidden>Nada marcado neste mês por enquanto.</p>
                <p class="nota-calculo">As épocas mudam de uma região para outra e de um ano para o outro, com as chuvas. Cada uma vem da ficha da espécie, com a fonte.</p>
            </div>
        </section>
'''
pagina('mes-a-mes.html', 'O Cerrado mês a mês — Guia do Cerrado',
       'O que floresce, que fruta amadurece, que bicho aparece e o que acontece na paisagem do Cerrado em cada mês do ano.', mes, scripts=['mes-a-mes.js?v=1'])
RODAPE_PT = RODAPE_PT.replace(' · <a href="onde-ver.html">Onde ver</a>', ' · <a href="mes-a-mes.html">Mês a mês</a> · <a href="onde-ver.html">Onde ver</a>')
so_pt = json.loads((AQUI / 'so-pt.json').read_text())
if 'mes-a-mes.html' not in so_pt: so_pt.append('mes-a-mes.html')
(AQUI / 'so-pt.json').write_text(json.dumps(so_pt, ensure_ascii=False, indent=2) + '\n')
for f in COMPARTILHADAS:
    q = M / f; t = q.read_text(); t = com_rodape_novo(t)
    porta = '<a class="porta" href="mes-a-mes.html"><span class="porta-chapeu">Mês a mês</span><strong>O ano no Cerrado</strong><span>O que floresce, amadurece e aparece em cada mês.</span></a>'
    if porta not in t:
        t = re.sub(r'(<a class="porta" href="onde-ver\.html">.*?</a>)', lambda m: m.group(1) + '\n                    ' + porta, t, count=1, flags=re.S)
    q.write_text(t)
for f in so_pt:
    if f == '404.html': continue
    q = M / f; t = q.read_text(); t = com_rodape_novo(t); q.write_text(t)
print('mês a mês:', len(EVENTOS), 'acontecimentos')

# ================================================================ Como ajudar (1/11/2026): o que qualquer pessoa pode fazer, com os canais oficiais
FONTES += [
 (149, 'Tribuna de Minas (2026): o WikiAves como fonte de dados para a ciência, com mais de 3 mil citações em artigos; e UFSCar, inventário de aves com o WikiAves e o iNaturalist.', 'https://tribunademinas.com.br/colunas/bichoseacidade/31-05-2026/juiz-de-fora-como-potencia-na-observacao-de-aves.html'),
 (150, 'Governo federal (gov.br): apresentar denúncia ambiental ao Ibama, pela Central de Atendimento (0800 061 8080) ou pelo Fala.BR, com ou sem identificação.', 'https://www.gov.br/pt-br/servicos/apresentar-denuncia-ambiental'),
 (151, 'Governo federal (gov.br): entregar animal silvestre num Centro de Triagem (Cetas); e o folder dos Cetas do Ibama.', 'https://www.gov.br/pt-br/servicos/realizar-a-entrega-de-animal-silvestre-no-centro-de-triagem-de-animais-silvestres-cetas'),
 (152, 'Brasil de Fato (2020): a Central do Cerrado, cooperativa de associações de agricultores e extrativistas do DF e de nove estados, e a loja virtual.', 'https://www.brasildefato.com.br/2020/06/24/do-cerrado-para-a-mesa-a-loja-virtual-que-auxilia-nas-vendas-de-povos-tradicionais/'),
 (153, 'National Geographic Brasil (2023): os coletores de sementes e de capim que restauram o Cerrado; e relatórios do CEPF sobre a Rede de Sementes do Cerrado.', 'https://www.nationalgeographicbrasil.com/meio-ambiente/2023/04/dia-da-terra-quem-sao-os-coletores-de-sementes-e-grama-que-protegem-o-cerrado-brasileiro-de-desaparecer'),
 (154, 'Brasil de Fato (2025): o incêndio de Cavalcante (GO), controlado depois de atingir mais de 77 mil hectares, com Prevfogo, ICMBio e brigadas voluntárias.', 'https://www.brasildefato.com.br/2025/10/06/incendio-em-cavalcante-go-e-controlado-apos-atingir-mais-de-77-mil-hectares/'),
]
FONTES.sort()
ACOES = [
 ('registrar', 'Registrar o que você vê', 'Uma foto com data e lugar vira dado para a ciência. No WikiAves (aves) e no iNaturalist (qualquer bicho ou planta), outras pessoas ajudam a identificar, e os pesquisadores usam os registros: o WikiAves já foi citado em mais de 3 mil artigos científicos.', [149],
  ['Fotografe sem perturbar: não chegue perto de ninhos nem use som para atrair aves.', 'Anote o lugar e a data. Não divulgue a posição exata de espécies raras ou ameaçadas.', 'Comece pelas espécies deste guia: cada ficha diz como reconhecer.']),
 ('denunciar', 'Denunciar', 'Desmatamento, fogo posto, caça, venda de bichos silvestres em feira ou na internet: tudo isso é crime e pode ser denunciado ao Ibama, com ou sem identificação.', [150],
  ['Ibama: <a href="tel:08000618080">0800&nbsp;061&nbsp;8080</a>, ou pelo Fala.BR, na internet.', 'Fogo começando: Corpo de Bombeiros, <a href="tel:193">193</a>. Crime acontecendo: Polícia, <a href="tel:190">190</a>.', 'Anote o que puder: lugar, placa de carro, data, fotos tiradas sem se arriscar.']),
 ('bicho', 'Achou um bicho ferido ou um filhote?', 'O melhor quase sempre é não levar para casa. Tratar ou criar um animal silvestre em casa piora o estado dele, estressa e pode passar doenças, para ele e para você.', [151],
  ['Filhote de ave no chão, já com penas, em geral está aprendendo a voar, e os pais continuam dando comida: deixe onde está.', 'Bicho ferido: chame a Polícia Ambiental, a Guarda Municipal ou os Bombeiros (<a href="tel:193">193</a>), que levam ao Centro de Triagem (Cetas).', 'Se tem um animal silvestre em casa, dá para entregar ao Ibama de forma voluntária.']),
 ('comprar', 'Comprar do Cerrado em pé', 'Baru, pequi, óleo de babaçu, farinha de jatobá, capim-dourado e mel de abelhas nativas comprados de quem coleta sem derrubar mantêm as árvores e as comunidades no lugar.', [152],
  ['A Central do Cerrado reúne associações de agricultores e extrativistas do DF e de nove estados e vende pela internet.', 'Prefira produtos com a origem dita: a comunidade, a cooperativa, o município.', 'Desconfie de "arnica" e outras plantas medicinais arrancadas da natureza: muitas estão sumindo.']),
 ('plantar', 'Plantar nativa', 'Quintal, calçada, sítio ou beira de nascente: cada lugar tem as suas espécies. A restauração do Cerrado usa muitas sementes de capins e ervas nativas, colhidas por comunidades.', [153],
  ['Escolha a espécie pelo lugar: buriti só onde o solo fica encharcado; pequi, baru e cagaita no cerrado de terra firme.', 'Compre mudas e sementes de viveiros e redes que trabalham com nativas, como a Rede de Sementes do Cerrado.', 'Não plante capins africanos, como a braquiária, perto de áreas nativas: eles invadem os campos.']),
 ('fogo', 'Não soltar fogo, e ajudar a apagá-lo', 'Na seca, uma queima de lixo ou de pasto vira incêndio em minutos. Em 2025, um só incêndio em Cavalcante (GO) passou de 77 mil hectares e precisou de Prevfogo, ICMBio e brigadas voluntárias.', [154],
  ['Não queime lixo nem folhas; não jogue bituca de cigarro na beira da estrada.', 'Viu fumaça no mato? Ligue <a href="tel:193">193</a> e diga o lugar.', 'Muitas cidades do Cerrado têm brigadas voluntárias, que treinam gente para ajudar: procure a da sua região.']),
]
CURTO = {'registrar': 'Registrar', 'denunciar': 'Denunciar', 'bicho': 'Bicho ferido', 'comprar': 'Comprar', 'plantar': 'Plantar', 'fogo': 'Fogo'}
def acao_html(i, t, txt, fs, dicas):
    li = ''.join(f'<li>{d}</li>' for d in dicas)
    return (f'<section class="acao" id="{i}" aria-labelledby="acao-{i}"><h2 id="acao-{i}">{t}</h2><p>{txt}{"".join(fonte(n) for n in fs)}</p>'
            f'<ul class="lista">{li}</ul><label class="acao-marcar"><input type="checkbox" data-acao="{i}"> Vou fazer isto</label></section>')
ajudar = f'''        <section class="titulo-pagina guia-topo">
            <div class="container">
                <p class="guia-chapeu">Guia do cerrado</p>
                <h1>Como ajudar o Cerrado</h1>
                <p>Seis coisas que qualquer pessoa pode fazer, de onde estiver, com os canais oficiais. Marque as que você vai fazer: a lista fica guardada só no seu navegador.</p>
            </div>
        </section>
        <div class="container guia-layout">
            {indice([(i, CURTO[i]) for i, *_ in ACOES])}
            <div class="guia-texto">
                <p class="acoes-placar" aria-live="polite" hidden></p>
                {"".join(acao_html(*a) for a in ACOES)}
                <p class="nota-calculo">Mais sobre o que ameaça o Cerrado em <a href="ameacas.html">Ameaças</a>. Os telefones e serviços são os oficiais na data desta página: confira no site de cada órgão.</p>
            </div>
        </div>
'''
pagina('como-ajudar.html', 'Como ajudar o Cerrado — Guia do Cerrado',
       'Seis coisas que qualquer pessoa pode fazer pelo Cerrado: registrar, denunciar, socorrer um bicho, comprar, plantar e evitar o fogo.', ajudar, scripts=['guia.js?v=1', 'como-ajudar.js?v=1'])
RODAPE_PT = RODAPE_PT.replace(' · <a href="mes-a-mes.html">Mês a mês</a>', ' · <a href="mes-a-mes.html">Mês a mês</a> · <a href="como-ajudar.html">Como ajudar</a>')
so_pt = json.loads((AQUI / 'so-pt.json').read_text())
if 'como-ajudar.html' not in so_pt: so_pt.append('como-ajudar.html')
(AQUI / 'so-pt.json').write_text(json.dumps(so_pt, ensure_ascii=False, indent=2) + '\n')
for f in COMPARTILHADAS:
    q = M / f; t = q.read_text(); q.write_text(com_rodape_novo(t))
for f in so_pt:
    if f == '404.html': continue
    q = M / f; t = q.read_text(); t = com_rodape_novo(t)
    q.write_text(t)
lista = ''.join(f'<li id="f{n}"><span class="fonte-numero">{n}</span> {t} <a href="{u}" rel="noopener">Abrir a fonte</a></li>' for n, t, u in FONTES)
q = M / 'fontes.html'; t = q.read_text()
t = re.sub(r'<ol class="fontes-lista">.*?</ol>', '<ol class="fontes-lista">' + lista + '</ol>', t, flags=re.S)
q.write_text(t)
print('como ajudar:', len(ACOES), 'ações; fontes:', len(FONTES))

# ================================================================ Monte sua visita (1/11/2026): parque + mês = o que dá para ver
# As paisagens de cada parque são as principais, a partir do texto de "Onde ver" (aproximadas: ver NO-COMPUTADOR 9.12);
# os destaques são espécies que o próprio guia já liga ao parque, nas fichas ou em "Onde ver".
PARQUE_PAIS = {
 1: ['campo-rupestre', 'campo-limpo', 'cerrado-sentido-restrito', 'mata-de-galeria', 'vereda'],
 2: ['campo-limpo', 'campo-sujo', 'parque-de-cerrado', 'vereda'],
 3: ['cerrado-sentido-restrito', 'campo-sujo', 'mata-de-galeria', 'cerradao', 'parque-de-cerrado'],
 4: ['campo-rupestre', 'campo-limpo', 'mata-de-galeria'],
 5: ['vereda', 'cerrado-sentido-restrito', 'campo-limpo'],
 6: ['cerradao', 'mata-ciliar', 'cerrado-sentido-restrito'],
 7: ['campo-rupestre', 'cerrado-sentido-restrito', 'mata-de-galeria'],
 8: ['vereda', 'campo-limpo', 'cerrado-sentido-restrito'],
 9: ['palmeiral', 'vereda', 'cerrado-sentido-restrito'],
 10: ['mata-seca', 'cerrado-sentido-restrito'],
 11: ['campo-rupestre', 'campo-limpo'],
 12: ['palmeiral', 'cerrado-sentido-restrito', 'mata-ciliar'],
 13: ['mata-ciliar', 'mata-seca', 'vereda'],
}
DESTAQUES = {
 1: ['lobo-guara', 'pato-mergulhao', 'canela-de-ema'],
 2: ['vaga-lume-cupinzeiro', 'ema', 'veado-campeiro', 'tamandua-bandeira', 'queixada', 'cachorro-vinagre', 'capim-flecha'],
 4: ['pato-mergulhao'],
 5: ['buriti'],
 7: ['canela-de-ema'],
 8: ['capim-dourado', 'pato-mergulhao'],
 9: ['babacu'],
 11: ['sempre-viva', 'chuveirinho'],
 12: ['babacu'],
}
ROTEIRO = {
 'parques': [{'n': n, 'nome': p[0], 'uf': p[1], 'texto': p[4], 'pais': PARQUE_PAIS[n], 'dest': DESTAQUES.get(n, [])} for n, p in enumerate(PARQUES, 1)],
 'paisagens': {p['id']: p['nome'] for p in P},
 'especies': [{'id': e[0], 'n': e[1], 'g': e[3], 'p': e[6]} for e in ESP],
 'eventos': [{'c': c, 'n': nome, 'l': link, 'm': ms, 't': txt} for c, nome, link, ms, txt, fs in EVENTOS],
}
roteiro_json = json.dumps(ROTEIRO, ensure_ascii=False).replace('</', '<\\/')
op_parques = ''.join(f'<option value="{n}">{p[0]} ({p[1]})</option>' for n, p in enumerate(PARQUES, 1))
op_meses = ''.join(f'<option value="{i}">{m.capitalize()}</option>' for i, m in enumerate(NOMES_MES, 1))
roteiro = f'''        <section class="titulo-pagina guia-topo">
            <div class="container">
                <p class="guia-chapeu">Guia do cerrado</p>
                <h1>Monte sua visita</h1>
                <p>Escolha um parque e o mês da viagem: o guia junta as paisagens, as espécies para procurar e o que estará acontecendo por lá.</p>
            </div>
        </section>
        <section class="secao">
            <div class="container roteiro">
                <form class="roteiro-escolha" action="roteiro.html" method="get">
                    <div class="campo"><label for="roteiro-parque">Parque</label><select id="roteiro-parque" name="parque">{op_parques}</select></div>
                    <div class="campo"><label for="roteiro-mes">Mês</label><select id="roteiro-mes" name="mes">{op_meses}</select></div>
                    <noscript><button type="submit" class="botao">Ver</button></noscript>
                </form>
                <div class="roteiro-resultado" aria-live="polite">
                    <p class="sem-js">Esta página precisa de JavaScript para montar a visita. Sem ele, veja os parques em <a href="onde-ver.html">Onde ver</a> e as épocas em <a href="mes-a-mes.html">Mês a mês</a>.</p>
                </div>
                <script type="application/json" id="roteiro-dados">{roteiro_json}</script>
                <p class="nota-calculo">As paisagens de cada parque são as principais, de forma aproximada, e nem toda espécie aparece em todo parque que tem a paisagem dela: use a lista como um ponto de partida. Antes de ir, confira no site do parque se ele está aberto e o que precisa de guia.</p>
            </div>
        </section>
'''
pagina('roteiro.html', 'Monte sua visita — Guia do Cerrado',
       'Escolha um parque do Cerrado e o mês: o guia junta as paisagens, as espécies para procurar e o que estará acontecendo por lá.', roteiro, scripts=['roteiro.js?v=2'])
RODAPE_PT = RODAPE_PT.replace(' · <a href="onde-ver.html">Onde ver</a>', ' · <a href="onde-ver.html">Onde ver</a> · <a href="roteiro.html">Monte sua visita</a>')
so_pt = json.loads((AQUI / 'so-pt.json').read_text())
if 'roteiro.html' not in so_pt: so_pt.append('roteiro.html')
(AQUI / 'so-pt.json').write_text(json.dumps(so_pt, ensure_ascii=False, indent=2) + '\n')
for f in COMPARTILHADAS:
    q = M / f; q.write_text(com_rodape_novo(q.read_text()))
for f in so_pt:
    if f == '404.html': continue
    q = M / f; t = com_rodape_novo(q.read_text())
    if f == 'onde-ver.html':
        t = t.replace('Toque num número do mapa para ler sobre o parque.</p>', 'Toque num número do mapa para ler sobre o parque, ou <a href="roteiro.html">monte sua visita</a> escolhendo o parque e o mês.</p>', 1)
    q.write_text(t)
print('roteiro:', len(PARQUES), 'parques')
