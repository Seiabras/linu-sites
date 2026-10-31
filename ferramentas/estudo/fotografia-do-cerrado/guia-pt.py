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
import json, pathlib, re

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
]
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
        img = f'<div class="esp-icone esp-{reino}" aria-hidden="true"><svg viewBox="0 0 24 24" width="36" height="36">{ICONES[grupo]}</svg></div>'
    selo = f'<span class="selo">{AMEACA[am]}</span>' if am else ''
    link = f'<a href="especie-{id_}.html">{nome}</a>' if ficha else nome
    if id_ == 'jatai':
        texto = texto.replace('Veja o site Abelhas sem Ferrão.', 'Veja o site <a href="https://abelhas.linupedia.com.br/" rel="noopener">Abelhas sem Ferrão</a>.')
    onde = ', '.join(NOME_PAISAGEM[x].lower().replace('cerrado sentido restrito', 'cerrado') for x in pais)
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
                    <ul class="especies-lista">{"".join(cartao(e) for e in ESP)}</ul>
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
    return re.sub(r'\{\{\?pt-BR\}\} · <a href="(?:expedicoes|diario)\.html">.*?\{\{/pt-BR\}\}', '{{?pt-BR}}' + RODAPE_PT + '{{/pt-BR}}', t)
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
aprender = f'''        <section class="titulo-pagina guia-topo">
            <div class="container">
                <p class="guia-chapeu">Guia do cerrado</p>
                <h1>Aprender brincando</h1>
                <p>Um quiz por tema, um jogo de reconhecer as paisagens e um glossário. Tudo o que está aqui foi explicado no guia, com fonte.</p>
            </div>
        </section>
        <div class="container guia-layout">
            {indice([('quiz', 'Quiz'), ('adivinha', 'Qual paisagem é esta?'), ('glossario', 'Glossário')])}
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
       'Quiz sobre o Cerrado por tema, o jogo “Qual paisagem é esta?” e um glossário, tudo com base no guia.', aprender, scripts=['guia.js?v=1', 'aprender.js?v=1'])

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
