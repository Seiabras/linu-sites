# Rodar: python3 ferramentas/estudo/fotografia-do-cerrado/paginas-pt.py e depois node ferramentas/gerar-estudo.mjs fotografia-do-cerrado
# Gera os modelos das páginas novas da Guia do Cerrado que, por enquanto, só existem em português (31/10/2026):
# as cinco fichas de espécie, o diário de campo e "Como fotografamos". O cabeçalho e o rodapé vêm do modelo da galeria.
import html, json, os, re

import pathlib
BASE = str(pathlib.Path(__file__).resolve().parent) + '/'
M = BASE + 'modelo/'
galeria = open(M + 'galeria.html').read()
cabeca, resto = galeria.split('    <main id="conteudo">', 1)
rodape = resto.split('    </main>', 1)[1]
# as páginas novas não usam o script da galeria
cabeca = re.sub(r'    <script src="\{\{raiz\}\}js/galeria\.js\?v=\d+" defer></script>\n', '', cabeca)
assert 'galeria.js' not in cabeca

def pagina(titulo, descricao, corpo, atual=None, script=None):
    s = cabeca
    # o título e a descrição da galeria (no <title>, na descrição e nas metatags de compartilhar) viram os desta página
    s = s.replace('{{galeria_090}}', html.escape(titulo)).replace('{{galeria_103}}', html.escape(descricao))
    s = s.replace('{{galeria_089}}', '{{contato_018}}')  # nenhuma página do menu fica marcada como atual
    if not script:
        s = s.replace('    <script src="{{raiz}}js/ficha.js?v=1" defer></script>\n', '')
    if atual == 'diario':
        s = s.replace('<li><a href="diario.html">Diário</a></li>', '<li><a href="diario.html" aria-current="page">Diário</a></li>')
    return s + '    <main id="conteudo">\n' + corpo + '    </main>' + rodape

ESPECIES = [
 {'id': 'lobo-guara', 'nome': 'Lobo-guará', 'cientifico': 'Chrysocyon brachyurus', 'grupo': 'Mamífero', 'img': 'lobo-guara', 'w': 1000, 'h': 647,
  'alt': 'Lobo-guará de pelagem laranja e pernas pretas andando na grama',
  'abre': 'O maior canídeo da América do Sul, e o bicho que mais gente quer ver no cerrado. Parece uma raposa de pernas de pau, mas não é raposa nem lobo: é o único do seu gênero.',
  'situacao': 'Vulnerável', 'ameacado': True,
  'fatos': [('Comprimento', 'cerca de 1,5 m, com a cauda'), ('Altura', 'cerca de 90 cm no ombro'), ('Peso', '20 a 30 kg'),
            ('Come', 'frutos, como a lobeira, e também pequenos roedores, aves e insetos'), ('Quando aparece', 'no fim da tarde e à noite, quase sempre sozinho')],
  'reconhecer': ['Pernas longas e pretas, como se estivesse de meia.', 'Pelagem laranja, com uma crina preta no pescoço que se arrepia quando ele se assusta.', 'Orelhas grandes e a ponta da cauda branca.'],
  'fotografar': 'Ele costuma andar por trilhas e estradas de terra no fim da tarde. Fique parado num ponto com vista longa, use uma lente de 300 mm ou mais e nada de flash: a luz baixa do entardecer já basta.',
  'onde': ('expedicoes.html?mes=7', 'Chapada dos Veadeiros', 'o melhor horário é o entardecer, de junho a setembro'),
  'comp': 1.5, 'alt_m': 0.9, 'medida': '1,5 m do focinho à ponta da cauda, 90 cm de altura'},
 {'id': 'tamandua-bandeira', 'nome': 'Tamanduá-bandeira', 'cientifico': 'Myrmecophaga tridactyla', 'grupo': 'Mamífero', 'img': 'tamandua-bandeira', 'w': 1000, 'h': 667,
  'alt': 'Tamanduá-bandeira cinza, com a faixa preta no ombro, procurando alimento no capim',
  'abre': 'Não tem dentes e come quase só formigas e cupins, com uma língua que passa de meio metro. A cauda peluda, que ele carrega como uma bandeira, dá o nome.',
  'situacao': 'Vulnerável', 'ameacado': True,
  'fatos': [('Comprimento', 'até cerca de 2 m, com a cauda'), ('Altura', 'cerca de 60 cm no ombro'), ('Peso', '22 a 40 kg'),
            ('Come', 'formigas e cupins, às dezenas de milhares por dia'), ('Quando aparece', 'de dia quando faz frio e à noite quando faz calor')],
  'reconhecer': ['Focinho comprido e fino, como um tubo.', 'Uma faixa preta com borda branca do peito até as costas.', 'Cauda enorme e peluda, que serve de coberta para dormir.'],
  'fotografar': 'Enxerga mal, mas tem um faro ótimo: chegue contra o vento e em silêncio. Nos campos abertos das Emas ele aparece de longe, então dá para esperar ele vir na sua direção em vez de ir atrás.',
  'onde': ('expedicoes.html?mes=6', 'Parque Nacional das Emas', 'de maio a agosto, nos campos abertos'),
  'comp': 2.0, 'alt_m': 0.6, 'medida': '2 m do focinho à ponta da cauda, 60 cm de altura'},
 {'id': 'arara-caninde', 'nome': 'Arara-canindé', 'cientifico': 'Ara ararauna', 'grupo': 'Ave', 'img': 'arara-caninde', 'w': 1000, 'h': 772,
  'alt': 'Arara-canindé azul e amarela voando de asas abertas sobre a mata',
  'abre': 'Azul por cima e amarela por baixo, ela se anuncia antes de aparecer: os bandos voam gritando ao amanhecer, sempre aos pares dentro do grupo.',
  'situacao': 'Não ameaçada', 'ameacado': False,
  'fatos': [('Comprimento', '80 a 90 cm, com a cauda'), ('Peso', 'cerca de 1 kg'), ('Come', 'frutos, sementes e castanhas, até as duras de palmeiras'),
            ('Quando aparece', 'logo depois do amanhecer e no fim da tarde, voando entre os buritis'), ('Ninho', 'em ocos de palmeiras mortas, como o buriti')],
  'reconhecer': ['Costas e asas azuis, peito e barriga amarelos.', 'Rosto branco, sem penas, com listrinhas pretas.', 'Cauda longa e pontuda, que aparece bem em voo.'],
  'fotografar': 'Procure as veredas com buritis logo cedo. Em voo, use velocidade alta (1/2000 s ou mais) e acompanhe o bando com a câmera; pousadas, elas desconfiam de quem chega de frente.',
  'onde': ('expedicoes.html?mes=6', 'Parque Nacional das Emas', 'nas palmeiras mortas onde fazem ninho'),
  'comp': 0.85, 'alt_m': None, 'medida': '85 cm do bico à ponta da cauda'},
 {'id': 'seriema', 'nome': 'Seriema', 'cientifico': 'Cariama cristata', 'grupo': 'Ave', 'img': 'seriema', 'w': 1000, 'h': 729,
  'alt': 'Seriema de pernas vermelhas caminhando no chão de terra',
  'abre': 'Quem já passou uma manhã no cerrado ouviu a seriema antes de vê-la: o canto alto, que parece uma risada, vai longe. Ela prefere correr a voar.',
  'situacao': 'Não ameaçada', 'ameacado': False,
  'fatos': [('Comprimento', '75 a 90 cm'), ('Peso', '1,5 a 2,2 kg'), ('Come', 'insetos, lagartos, cobras pequenas e roedores'),
            ('Quando aparece', 'de manhã cedo, em casais ou grupos pequenos'), ('À noite', 'dorme no alto das árvores')],
  'reconhecer': ['Pernas e bico vermelhos.', 'Um topete de penas em pé na testa.', 'O canto, que parece uma gargalhada e se ouve de longe.'],
  'fotografar': 'Siga o canto de manhã cedo: ela costuma cantar em cima de cupinzeiros, e aí fica parada por alguns segundos. Fotografe na altura dela, agachado, para o fundo ficar no capim e não no céu.',
  'onde': ('expedicoes.html', 'qualquer uma das três expedições', 'nos campos abertos, o ano todo'),
  'comp': 0.85, 'alt_m': None, 'medida': '85 cm do bico à ponta da cauda'},
 {'id': 'tucano-toco', 'nome': 'Tucano-toco', 'cientifico': 'Ramphastos toco', 'grupo': 'Ave', 'img': 'tucano-toco', 'w': 1000, 'h': 589,
  'alt': 'Tucano-toco de bico laranja com a ponta preta, visto de perfil',
  'abre': 'O maior dos tucanos, com um bico que é quase um terço do corpo. Apesar do tamanho, o bico é oco e leve, e ajuda a ave a perder calor nos dias quentes.',
  'situacao': 'Não ameaçado', 'ameacado': False,
  'fatos': [('Comprimento', '55 a 65 cm, com o bico de uns 20 cm'), ('Peso', 'cerca de 500 a 800 g'), ('Come', 'frutos e, às vezes, ovos e filhotes de outras aves'),
            ('Quando aparece', 'em pares ou grupos pequenos, onde há árvores com fruta madura'), ('Voo', 'ondulado: algumas batidas e um planeio')],
  'reconhecer': ['Bico laranja com uma mancha preta na ponta.', 'Garganta branca e corpo preto.', 'Um anel azul em volta do olho.'],
  'fotografar': 'Ache uma árvore com fruta madura e espere: ele volta. Contra o céu o bico fica escuro, então prefira quando ele pousa com mata atrás.',
  'onde': ('expedicoes.html', 'Parque Nacional de Brasília', 'perto da mata, o ano todo'),
  'comp': 0.6, 'alt_m': None, 'medida': '60 cm do bico à ponta da cauda'},
]

def escala(e):
    # "Do tamanho de quê?": a pessoa de 1,70 m e o bicho na mesma escala (1 m = 100 unidades)
    W, chao = 420, 200
    pessoa_x, pessoa_h = 40, 170
    bicho_x = 120
    comp = e['comp'] * 100
    alt = (e['alt_m'] or 0.25) * 100
    y = chao - alt
    pessoa = (f'<g class="pessoa"><circle cx="{pessoa_x + 15}" cy="{chao - 158}" r="12"/>'
              f'<rect x="{pessoa_x}" y="{chao - 144}" width="30" height="74" rx="12"/>'
              f'<rect x="{pessoa_x + 2}" y="{chao - 74}" width="11" height="74" rx="5"/><rect x="{pessoa_x + 17}" y="{chao - 74}" width="11" height="74" rx="5"/></g>')
    return f'''<figure class="escala">
                    <svg viewBox="0 0 {W} 230" role="img" aria-labelledby="escala-{e['id']}">
                        <title id="escala-{e['id']}">{e['nome']}: {e['medida']}, ao lado de uma pessoa de 1,70 m</title>
                        <line class="chao" x1="0" y1="{chao}" x2="{W}" y2="{chao}"/>
                        {pessoa}
                        <rect class="bicho" x="{bicho_x}" y="{y}" width="{comp}" height="{alt}" rx="{min(alt, 40) / 2}"/>
                        <text x="{pessoa_x + 15}" y="222" text-anchor="middle">1,70 m</text>
                        <text x="{bicho_x + comp / 2}" y="222" text-anchor="middle">{e['medida'].split(' do ')[0]}</text>
                    </svg>
                    <figcaption>Na mesma escala: {e['medida']}, ao lado de uma pessoa de 1,70 m.</figcaption>
                </figure>'''

paginas = []
for n, e in enumerate(ESPECIES):
    ant, prox = ESPECIES[n - 1], ESPECIES[(n + 1) % len(ESPECIES)]
    fatos = ''.join(f'<dt>{k}</dt><dd>{v}</dd>' for k, v in e['fatos'])
    reconhecer = ''.join(f'<li>{r}</li>' for r in e['reconhecer'])
    selo = f'<span class="selo">{e["situacao"]} (ICMBio)</span>' if e['ameacado'] else f'<span class="selo selo-calmo">{e["situacao"]}</span>'
    corpo = f'''        <article class="ficha-especie">
            <div class="container">
                <p class="trilha"><a href="galeria.html">Galeria</a> <span aria-hidden="true">›</span> {e['nome']}</p>
                <div class="ficha-topo">
                    <img src="{{{{raiz}}}}img/{e['img']}.webp" srcset="{{{{raiz}}}}img/{e['img']}-640.webp 640w, {{{{raiz}}}}img/{e['img']}.webp 1000w" sizes="(max-width: 900px) 100vw, 55vw" alt="{e['alt']}" width="{e['w']}" height="{e['h']}" fetchpriority="high">
                    <div class="ficha-resumo">
                        <p class="ficha-grupo">{e['grupo']}</p>
                        <h1>{e['nome']}</h1>
                        <p class="cientifico">{e['cientifico']}</p>
                        <p class="ficha-abre">{e['abre']}</p>
                        {selo}
                    </div>
                </div>
                <div class="ficha-corpo">
                    <section aria-labelledby="fatos-titulo">
                        <h2 class="sub" id="fatos-titulo">Em poucas palavras</h2>
                        <dl class="ficha-fatos">{fatos}</dl>
                    </section>
                    <section aria-labelledby="tamanho-titulo">
                        <h2 class="sub" id="tamanho-titulo">Do tamanho de quê?</h2>
                        {escala(e)}
                    </section>
                    <section aria-labelledby="reconhecer-titulo">
                        <h2 class="sub" id="reconhecer-titulo">Como reconhecer</h2>
                        <ul class="lista">{reconhecer}</ul>
                    </section>
                    <section aria-labelledby="fotografar-titulo">
                        <h2 class="sub" id="fotografar-titulo">Como fotografar</h2>
                        <p>{e['fotografar']}</p>
                    </section>
                    <section class="ficha-onde" aria-labelledby="onde-titulo">
                        <h2 class="sub" id="onde-titulo">Onde a gente vê</h2>
                        <p><a href="{e['onde'][0]}">{e['onde'][1]}</a>: {e['onde'][2]}.</p>
                    </section>
                </div>
                <nav class="ficha-navegar" aria-label="Outras espécies">
                    <a href="especie-{ant['id']}.html" rel="prev"><span aria-hidden="true">←</span> {ant['nome']}</a>
                    <a href="especie-{prox['id']}.html" rel="next">{prox['nome']} <span aria-hidden="true">→</span></a>
                </nav>
                <p class="ficha-nota">Medidas aproximadas, de animais adultos. A situação de ameaça é a da lista nacional do ICMBio.</p>
            </div>
        </article>
'''
    f = f'especie-{e["id"]}.html'
    open(M + f, 'w').write(pagina(f'{e["nome"]} ({e["cientifico"]}) — Guia do Cerrado',
                                  f'{e["nome"]}: como reconhecer, do que se alimenta, como fotografar e onde ver no cerrado.', corpo, script=False))
    paginas.append(f)

# Diário de campo: três relatos curtos da empresa fictícia
RELATOS = [
 ('emas-julho', 'Emas, julho: o tamanduá que não ligou para a gente', '14 de julho', 'tamandua-bandeira', 1000, 667,
  'Tamanduá-bandeira procurando cupins no capim seco',
  ['Saímos às seis, com cinco graus e o capim branco de geada. Às oito, o sol já esquentava as costas quando o Pedro, nosso guia, apontou uma mancha cinza andando no meio do campo.',
   'Era um tamanduá-bandeira, de focinho enfiado num cupinzeiro. A regra é não ir atrás: ficamos agachados, contra o vento, e esperamos. Ele comeu por uns vinte minutos, veio na nossa direção sem pressa e passou a uns trinta metros, sem levantar a cabeça uma vez.',
   'Foi a primeira expedição de três dos seis participantes. Nenhum usou flash, ninguém falou alto, e todos voltaram com a foto.'],
  ('especie-tamandua-bandeira.html', 'a ficha do tamanduá-bandeira'), ('contato.html?expedicao=emas&mes=7', 'a expedição das Emas')),
 ('veadeiros-agosto', 'Veadeiros, agosto: lobo-guará às 17h40', '23 de agosto', 'lobo-guara', 1000, 647,
  'Lobo-guará andando na grama, de perfil',
  ['No terceiro dia, na estrada de terra que leva ao mirante, paramos o carro com o sol baixo e desligamos o motor. Ninguém falava. O combinado era esperar até escurecer.',
   'Às 17h40 ele apareceu na curva, trotando pela beira da estrada, com aquelas pernas pretas que parecem de outro bicho. Parou, olhou para o carro por uns segundos e seguiu para o capim.',
   'Deu tempo para umas vinte fotos. A melhor saiu com ISO alto e um pouco de granulação, e a gente gosta dela assim: é a luz que tinha.'],
  ('especie-lobo-guara.html', 'a ficha do lobo-guará'), ('contato.html?expedicao=veadeiros&mes=8', 'a expedição da Chapada dos Veadeiros')),
 ('brasilia-janeiro', 'Brasília, janeiro: tucanos na chuva', '18 de janeiro', 'tucano-toco', 1000, 589,
  'Tucano-toco de perfil, com o bico laranja',
  ['Época de chuva é época de saída curta. Choveu a manhã inteira no Parque Nacional de Brasília, e quase desistimos.',
   'Quando a chuva afinou, três tucanos-tocos pousaram numa árvore carregada de frutos perto da trilha da mata. Molhados, de penas arrepiadas, ficaram ali comendo sem se importar com o grupo.',
   'Para quem acha que só a seca rende foto: o verde do cerrado em janeiro é outro, e os bichos estão ocupados demais comendo para fugir.'],
  ('especie-tucano-toco.html', 'a ficha do tucano-toco'), ('contato.html?expedicao=brasilia&mes=1', 'a saída no Parque Nacional de Brasília')),
]
itens = []
for n_rel, (id_, tit, data, img, w, h, alt, pars, ficha, exp) in enumerate(RELATOS):
    texto = ''.join(f'<p>{p}</p>' for p in pars)
    itens.append(f'''                <article class="relato" id="{id_}">
                    <img src="{{{{raiz}}}}img/{img}.webp" srcset="{{{{raiz}}}}img/{img}-640.webp 640w, {{{{raiz}}}}img/{img}.webp 1000w" sizes="(max-width: 900px) 100vw, 40vw" alt="{alt}" width="{w}" height="{h}" loading="{'eager' if n_rel == 0 else 'lazy'}">
                    <div>
                        <p class="relato-data">{data} de 2026</p>
                        <h2>{tit}</h2>
                        {texto}
                        <p class="relato-links">Veja <a href="{ficha[0]}">{ficha[1]}</a> ou <a href="{exp[0]}">fale com a gente sobre {exp[1]}</a>.</p>
                    </div>
                </article>''')
corpo = f'''        <section class="titulo-pagina">
            <div class="container">
                <h1>Diário de campo</h1>
                <p>O que aconteceu nas últimas saídas, contado por quem estava lá. A empresa e as saídas são de mentira; os bichos e o jeito de fotografar, não.</p>
            </div>
        </section>
        <section class="secao">
            <div class="container diario">
{chr(10).join(itens)}
            </div>
        </section>
'''
open(M + 'diario.html', 'w').write(pagina('Diário de campo — Guia do Cerrado', 'Relatos das últimas expedições de fotografia de fauna no cerrado: Emas, Chapada dos Veadeiros e Parque Nacional de Brasília.', corpo, atual='diario'))
paginas.append('diario.html')

corpo = '''        <section class="titulo-pagina">
            <div class="container">
                <h1>Como fotografamos</h1>
                <p>O jeito de trabalhar da Guia do Cerrado: a foto nunca vale mais do que o bicho.</p>
            </div>
        </section>
        <section class="secao">
            <div class="container texto-longo">
                <h2 class="sub">A regra que vem antes de todas</h2>
                <p>Se o animal mudou o que estava fazendo por causa da gente, chegamos perto demais. Nessa hora a câmera abaixa e o grupo se afasta, mesmo que a foto ainda não tenha saído.</p>
                <h2 class="sub espaco">Distância e silêncio</h2>
                <ul class="lista">
                    <li>Nada de chamar, cercar, alimentar ou imitar o som de um bicho para ele aparecer.</li>
                    <li>Com mamíferos grandes, a gente espera onde está e deixa ele decidir se chega perto.</li>
                    <li>Ninhos e tocas ficam de fora: sem flash, sem drone e sem mexer em galho para abrir a vista.</li>
                </ul>
                <h2 class="sub espaco">A luz</h2>
                <p>As melhores horas são a primeira depois do nascer do sol e a última antes de escurecer. É quando a luz fica baixa e quente e quando a maioria dos bichos do cerrado está ativa. No meio do dia, a gente descansa e anda de trilha.</p>
                <h2 class="sub espaco">O equipamento</h2>
                <p>Não precisa de câmera profissional. Um celular com zoom resolve aves perto da água e paisagens; para mamíferos de longe, uma lente de 300 mm ou mais faz diferença. Leve também pilhas ou bateria extra, porque o frio da madrugada na seca descarrega tudo mais rápido.</p>
                <h2 class="sub espaco">Depois da saída</h2>
                <p>Na edição, só ajuste de luz, cor e corte. Nada de juntar duas fotos, tirar elementos ou mudar o lugar de um bicho: a foto mostra o que aconteceu.</p>
                <h2 class="sub espaco">As fotos deste site</h2>
                <p>O Guia do Cerrado é um projeto de estudo, e as expedições e o diário de campo são de mentira. As fotos são de fotógrafos de verdade, publicadas com licença livre no Wikimedia Commons; o nome de cada um está nos <a href="creditos.html">créditos</a>.</p>
                <p class="mais"><a class="botao" href="expedicoes.html">Ver as expedições</a></p>
            </div>
        </section>
'''
open(M + 'como-fotografamos.html', 'w').write(pagina('Como fotografamos — Guia do Cerrado', 'O jeito de trabalhar da Guia do Cerrado: distância, silêncio, a luz certa e nenhuma montagem.', corpo))
paginas.append('como-fotografamos.html')

json.dump(paginas, open(BASE + 'so-pt.json', 'w'), ensure_ascii=False, indent=2)
open(BASE + 'so-pt.json', 'a').write('\n')
print(paginas)

# A página de erro (404): aparece em qualquer endereço que não existe, então tudo nela é absoluto (começa com /)
pagina404 = '''<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Página não encontrada — Guia do Cerrado</title>
    <meta name="robots" content="noindex">
    <meta name="theme-color" content="#814F12">
    <link rel="icon" href="/img/icone.svg" type="image/svg+xml">
    <script src="/js/tema-inicio.js?v=2"></script>
    <link rel="preload" href="/fontes/newsreader-600.woff2" as="font" type="font/woff2" crossorigin>
    <link rel="stylesheet" href="/css/estilo.css?v=20">
    <script src="/js/tema.js?v=2" defer></script>
    <script src="/js/menu.js?v=2" defer></script>
</head>
<body>
    <a class="pular" href="#conteudo">Pular para o conteúdo</a>
    <header class="topo">
        <div class="container">
            <a class="marca" href="/"><svg viewBox="0 0 32 32" aria-hidden="true"><circle cx="16" cy="16" r="15" fill="#C8985A"/><circle cx="16" cy="16" r="8" fill="#5E3A0D"/><circle cx="16" cy="16" r="4" fill="#FBF7F1"/></svg> Guia do Cerrado</a>
            <button class="botao-tema" type="button" data-escuro="Mudar para o modo escuro" data-claro="Mudar para o modo claro" aria-label="Mudar para o modo escuro"><svg class="lua" viewBox="0 0 24 24" width="20" height="20" aria-hidden="true"><path d="M20 14.5A8.5 8.5 0 0 1 9.5 4a8.5 8.5 0 1 0 10.5 10.5Z"/></svg><svg class="sol" viewBox="0 0 24 24" width="20" height="20" aria-hidden="true"><circle cx="12" cy="12" r="4.5"/><path d="M12 1.5v3M12 19.5v3M1.5 12h3M19.5 12h3M4.6 4.6l2.1 2.1M17.3 17.3l2.1 2.1M4.6 19.4l2.1-2.1M17.3 6.7l2.1-2.1"/></svg></button>
            <button class="botao-menu" type="button" aria-expanded="false" aria-controls="menu">Menu</button>
            <nav aria-label="Navegação principal">
                <ul class="menu" id="menu"><li><a href="/">Início</a></li><li><a href="/galeria">Galeria</a></li><li><a href="/expedicoes">Expedições</a></li><li><a href="/diario">Diário</a></li><li><a href="/sobre">Sobre</a></li><li><a href="/contato">Contato</a></li></ul>
            </nav>
        </div>
    </header>
    <main id="conteudo">
        <section class="secao pagina-erro">
            <div class="container">
                <p class="erro-codigo">Erro 404</p>
                <h1>Essa trilha não leva a lugar nenhum</h1>
                <p class="intro">A página que você procurou não existe ou mudou de endereço. Acontece até com guia: a gente volta e pega outro caminho.</p>
                <p><a class="botao" href="/">Voltar ao início</a> <a class="botao botao-linha" href="/galeria">Ver a galeria</a></p>
            </div>
        </section>
    </main>
    <footer class="rodape">
        <div class="container">
            <p>© 2026 Guia do Cerrado · projeto de estudo de Luiz Matheus Moraes Vega</p>
            <p><a href="/creditos">Créditos das fotos</a> · <a href="/como-fotografamos">Como fotografamos</a></p>
        </div>
    </footer>
</body>
</html>
'''
open(M + '404.html', 'w').write(pagina404)
paginas.append('404.html')
json.dump(paginas, open(BASE + 'so-pt.json', 'w'), ensure_ascii=False, indent=2)
open(BASE + 'so-pt.json', 'a').write('\n')
print('404 pronta')
