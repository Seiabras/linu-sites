# Pica ou Não Pica? (1/11/2026): o site das Abelhas sem Ferrão vira, em português, o guia para reconhecer os bichos
# peçonhentos e venenosos do Brasil, com as abelhas dentro. Nas outras línguas, o site continua o das Abelhas até a
# tradução. Rode depois de mudar texto ou dado, e então o gerador das línguas:
#   python3 ferramentas/estudo/abelhas-sem-ferrao/guia-pt.py && node ferramentas/gerar-estudo.mjs abelhas-sem-ferrao
# Tudo o que diz se um bicho é perigoso vem de fonte (lista FONTES, números nas notas). Não é orientação médica: o site
# manda sempre procurar atendimento.
import json, pathlib, re, html

AQUI = pathlib.Path(__file__).resolve().parent
M = AQUI / 'modelo'
NOME = 'Pica ou Não Pica?'  # o nome do guia em português; trocar aqui troca em tudo
COMPARTILHADAS = ['index.html', 'descobrir.html', 'achei-um-ninho.html', 'criar.html', 'teste.html', 'creditos.html']
MENU = [('index.html', 'Início'), ('identificar.html', 'Que bicho é?'), ('bichos.html', 'Bichos'), ('socorro.html', 'Socorro'), ('aprender.html', 'Aprender')]
ATUAL = {'bicho-': 'bichos.html', 'emergencia': 'socorro.html', 'cartao': 'socorro.html', 'soro': 'socorro.html',
         'mitos': 'aprender.html', 'jogo': 'aprender.html', 'diferencas': 'aprender.html', 'prevenir': 'aprender.html',
         'numeros': 'aprender.html', 'escola': 'aprender.html'}
# o endereço no ar (para o WhatsApp e as imagens de compartilhar); vai mudar para picanaopica.linupedia.com.br (NO-COMPUTADOR, seção 10)
URL_SITE = 'https://abelhas.linupedia.com.br/'
REVISAO = '1/11/2026'
SITIO = AQUI.parents[2] / 'sitios' / 'abelhas-sem-ferrao'
JS = 'guia.js?v=2'

def fui_picado(arquivo):
    atual = ' aria-current="page"' if arquivo == 'emergencia.html' else ''
    return f'<a class="fui-picado" href="emergencia.html"{atual}>Fui picado</a>'
# o manifesto e o offline.js (o guia sem internet), em todas as páginas em português
CAB_OFF = '<link rel="manifest" href="{{raiz}}manifest.webmanifest"><script src="{{raiz}}js/offline.js?v=1" defer></script>'

def menu_pt(arquivo):
    atual = next((v for k, v in ATUAL.items() if arquivo.startswith(k)), arquivo)
    return '<ul class="menu">' + ''.join(f'<li><a href="{h}"{" aria-current=\"page\"" if h == atual else ""}>{t}</a></li>' for h, t in MENU) + '</ul>'

MARCA_PT = f'<span aria-hidden="true">🐍</span> {NOME}'

# ---------------------------------------------------------------- as fontes
FONTES = [
 (1, 'Instituto Butantan. Animais venenosos (cartilha): a diferença entre peçonhentos, que injetam a toxina, e venenosos, que não injetam.', 'https://publicacoeseducativas.butantan.gov.br/web/animais-venenosos/pages/pdf/animais_venenosos.pdf'),
 (2, 'Prefeitura de São Paulo, Hospital do Servidor Público Municipal: o que fazer em acidentes com serpentes, segundo o Ministério da Saúde (lavar com água e sabão, ir ao serviço de saúde; não fazer torniquete nem espremer).', 'https://prefeitura.sp.gov.br/web/hospital_do_servidor_publico_municipal/w/dia-19-de-setembro-%C3%A9-dedicado-%C3%A0-conscientiza%C3%A7%C3%A3o-de-acidentes-of%C3%ADdicos'),
 (3, 'Secretaria da Saúde do Paraná. Acidentes por animais peçonhentos: orientações e prevenção.', 'https://www.saude.pr.gov.br/Pagina/Acidentes-por-animais-peconhentos'),
 (4, 'Ministério da Saúde. Boletim Epidemiológico, vol. 55, nº 3 (2024): os acidentes com escorpiões (292.440 notificações em 2022) e o escorpião-amarelo.', 'https://www.gov.br/saude/pt-br/centrais-de-conteudo/publicacoes/boletins/epidemiologicos/edicoes/2024/boletim-epidemiologico-volume-55-no-03'),
 (5, 'CNN Brasil. Todos os escorpiões são perigosos? Em 2023, 195.645 acidentes notificados e 152 mortes (Ministério da Saúde).', 'https://www.cnnbrasil.com.br/tecnologia/todos-os-escorpioes-sao-perigosos/'),
 (6, 'Instituto Butantan (trabalho de conclusão): a aranha-marrom, a forma mais grave de acidente com aranha, mais no Sul; a armadeira, 42% dos acidentes com aranhas notificados.', 'https://repositorio.butantan.gov.br/bitstream/butantan/3793/1/TCC_Suzanne%20Toledo.pdf'),
 (7, 'Revista Pesquisa FAPESP. São Paulo na Amazônia: o veneno das caranguejeiras é fraco perto do da aranha-marrom (pesquisador do Butantan).', 'https://revistapesquisa.fapesp.br/s%c3%a3o-paulo-na-amaz%c3%b4nia/'),
 (8, 'Instituto Butantan. Cartaz: acidente com lagarta Lonomia (o que fazer).', 'https://publicacoeseducativas.butantan.gov.br/web/cartaz-acidente-lonomia-v3/pages/pdf/a5-Acidente-lonomia-v3-bx.pdf'),
 (9, 'Secretaria da Saúde do Paraná. Acidentes por lagartas e mariposas: lavar com água fria, compressa fria; não fazer torniquete, cortar, espremer nem sugar.', 'https://www.saude.pr.gov.br/Pagina/Acidentes-por-Lagartas-e-Mariposas'),
 (10, 'Conselho Federal de Medicina. Anvisa cria o Disque-Intoxicação, 0800 722 6001, gratuito, 24 horas, ligado aos centros de toxicologia (CIATox).', 'https://portal.cfm.org.br/noticias/anvisa-cria-disque-intoxicacao/'),
 (11, 'Gazeta SP, com texto do Instituto Butantan: as jararacas causaram 69,3% dos acidentes com serpentes em 2022.', 'https://www.gazetasp.com.br/gazeta-mais/curiosidades/descubra-a-cobra-que-mais-faz-vitimas-em-sp-com-mais-de-70-dos/1152663'),
 (12, 'Revista da Associação Médica Brasileira (SciELO). Ofidismo: os acidentes com surucucu e coral são raros.', 'https://www.scielo.br/j/ramb/a/PsGWFbY5RwdZdQSMJmHxpSN/?lang=pt'),
 (13, 'National Geographic Brasil (2024), com o Instituto Butantan: não dá para separar a coral verdadeira da falsa a olho nu.', 'https://www.nationalgeographicbrasil.com/animais/2024/02/qual-a-diferenca-entre-a-cobra-coral-verdadeira-e-a-cobra-coral-falsa'),
 (14, 'Secretaria da Saúde do Paraná. Acidentes por abelhas: tirar os ferrões raspando, sem pinçar o saco de veneno.', 'https://www.saude.pr.gov.br/Pagina/Acidentes-por-Abelhas'),
 (15, 'Revista Pesquisa FAPESP. Pesquisadores desenvolvem soro contra o veneno de abelhas africanizadas: o perigo das muitas picadas.', 'https://revistapesquisa.fapesp.br/pesquisadores-desenvolvem-soro-contra-o-veneno-de-abelhas-africanizadas/'),
 (16, 'Revista Brasileira de Medicina de Família e Comunidade: dermatite por potó (Paederus), relato de casos.', 'https://rbmfc.org.br/rbmfc/article/download/475/517/3205'),
 (17, 'Manual MSD. Queimaduras por água-viva (o vinagre não serve para a caravela-portuguesa).', 'https://www.msdmanuals.com/pt/casa/lesões-e-envenenamentos/mordidas-e-picadas/queimaduras-por-água-viva'),
 (18, 'Diário do Nordeste. Queimaduras por caravelas: lavar com água do mar, nunca água doce (Corpo de Bombeiros do Ceará).', 'https://diariodonordeste.verdesmares.com.br/ceara/casos-de-queimaduras-por-caravelas-alertam-para-a-importancia-dos-primeiros-socorros-veja-como-agir-1.3562906'),
 (19, 'Portal Amazônia. Biólogo do INPA explica o que fazer em caso de ferroada de arraia (água quente, sem torniquete, atendimento médico).', 'https://portalamazonia.com/saude/ferroada-de-arraia-o-que-fazer/'),
 (20, 'Revista Pesquisa FAPESP. Sapo amazônico espirra veneno: um comportamento de algumas espécies, não de todos os sapos.', 'https://revistapesquisa.fapesp.br/sapo-amazonico-espirra-veneno/'),
 (21, 'Olhar Digital (2026), com o Instituto Butantan: inseticida pode espalhar escorpiões; galinha e plantas não resolvem.', 'https://olhardigital.com.br/2026/01/18/ciencia-e-espaco/escorpiao-como-matar-certo-e-riscos/'),
 (22, 'National Geographic Brasil (2024), com o Instituto Butantan: quatro fatos sobre as jiboias, que não têm veneno.', 'https://www.nationalgeographicbrasil.com/animais/2024/07/dia-mundial-das-cobras-conheca-4-fatos-sobre-as-jiboias'),
 (23, 'National Geographic Brasil (2024), com o Instituto Butantan: cinco características da cascavel.', 'https://www.nationalgeographicbrasil.com/animais/2024/01/conheca-5-caracteristicas-da-cascavel-uma-das-cobras-mais-perigosas-do-mundo'),
 (24, 'National Geographic Brasil (2023): a sucuri, a maior cobra do Brasil, que não tem veneno.', 'https://www.nationalgeographicbrasil.com/animais/2023/11/as-4-curiosidades-sobre-a-sucuri-uma-das-cobras-mais-populares-do-brasil'),
 (25, 'Manual MSD. Picadas de abelhas, vespas, vespões e formigas (a pústula da lava-pés, a reação alérgica grave).', 'https://www.msdmanuals.com/pt/casa/lesões-e-envenenamentos/mordidas-e-picadas/picadas-de-abelhas-vespas-vespões-e-formigas'),
 (26, 'National Geographic Brasil (2023). Quais são as picadas mais perigosas do mundo: a tocandira, com dor que pode durar um dia.', 'https://www.nationalgeographicbrasil.com/animais/2023/09/quais-sao-as-picadas-mais-perigosas-do-mundo'),
 (27, 'Portal Amazônia. Como prevenir e o que fazer em caso de picada por lacraia (lavar, compressa fria, analgésico; sem mortes comprovadas no Brasil).', 'https://portalamazonia.com/saude/entenda-como-prevenir-e-o-que-fazer-em-caso-de-picada-por-lacraia/'),
 (28, 'Secretaria de Estado da Saúde de Goiás. Acidentes por animais peçonhentos: aranhas (armadeira, aranha-marrom e viúva-negra).', 'https://goias.gov.br/saude/acidente-por-animais-peconhentos-aranhas/'),
 (29, 'Correio Braziliense. O que significa encontrar lagartixas em casa: não são venenosas e comem insetos (especialistas).', 'https://www.correiobraziliense.com.br/cbradar/segundo-especialistas-o-que-significa-encontrar-largatixas-em-casa/'),
 (30, 'Catraca Livre, citando o Instituto Butantan: o opilião não tem glândulas de veneno e não consegue picar uma pessoa.', 'https://catracalivre.com.br/noticias/parece-uma-aranha-perigosa-mas-nao-e-o-opiliao-nao-possui-veneno-e-sequer-consegue-picar-uma-pessoa/'),
 (31, 'Secretaria de Estado da Saúde de Goiás. Peixes peçonhentos: arraias e bagres.', 'https://goias.gov.br/saude/peixes-peconhentos/'),
]
def fonte(n):
    return f'<sup class="nota"><a href="fontes.html#f{n}" aria-label="Fonte {n}">{n}</a></sup>'

# ---------------------------------------------------------------- os bichos
# perigo: alto (procure atendimento já), medio (atenção, procure atendimento), baixo (incomoda, raramente grave),
# nenhum (não pica ou não tem veneno). tipo: peconhento (injeta), venenoso (não injeta), urticante (pelos, contato) ou sem
PERIGO = {'alto': ('Perigoso', 'Procure atendimento já'), 'medio': ('Atenção', 'Pode precisar de atendimento'),
          'baixo': ('Incomoda', 'Raramente é grave'), 'nenhum': ('Sem perigo', 'Não pica ou não tem veneno')}
TIPO = {'peconhento': 'Peçonhento: injeta a toxina', 'venenoso': 'Venenoso: tem toxina, mas não injeta',
        'urticante': 'Urticante: queima no contato', 'sem': 'Sem veneno'}
GRUPOS = ['Cobras', 'Escorpiões', 'Aranhas e parecidos', 'Abelhas, vespas e formigas', 'Lagartas e besouros', 'Outros da terra', 'Da água']
SOCORRO_DE = {'Cobras': 'cobra', 'Escorpiões': 'escorpiao', 'Aranhas e parecidos': 'aranha', 'Abelhas, vespas e formigas': 'abelha',
              'Lagartas e besouros': 'lagarta', 'Outros da terra': 'geral', 'Da água': 'agua'}
B = [
 dict(id='jararaca', n='Jararaca', c='Bothrops spp.', g='Cobras', p='alto', t='peconhento', pica='Pica, e é perigosa',
      r='A cobra que mais causa acidentes no Brasil: cerca de 70% das picadas de cobra.',
      rec=['Cabeça triangular, bem destacada do pescoço.', 'Uma fosseta entre o olho e a narina, que sente o calor.', 'Desenhos escuros em forma de V invertido nos lados do corpo.'],
      onde='Em quase todo o Brasil: matas, beiras de rio, plantações e quintais, onde há ratos.',
      faz='Dor, inchaço e manchas roxas no local; pode sangrar pela gengiva ou pela urina. Sem soro, pode causar necrose e problema nos rins.',
      soc='cobra', evitar='Botas e luvas no mato e na roça; olhe antes de pôr a mão em buracos, lenha e entulho.', f=[11, 2]),
 dict(id='cascavel', n='Cascavel', c='Crotalus durissus', g='Cobras', p='alto', t='peconhento', pica='Pica, e é perigosa',
      r='A cobra do chocalho. É a única cascavel do Brasil, e o veneno age sobre os nervos e os músculos.',
      rec=['Um chocalho (guizo) de anéis secos na ponta da cauda.', 'Desenhos de losangos claros nas costas.', 'Vive em campos e cerrados abertos, mais secos.'],
      onde='Campos, cerrados e áreas abertas de quase todo o país; rara na Amazônia densa.',
      faz='Pouca dor e pouco inchaço no local, o que engana; depois, pálpebras caídas, visão dupla, dor no corpo e urina escura.',
      soc='cobra', evitar='Use botas; o chocalho é um aviso: afaste-se devagar.', f=[23, 2]),
 dict(id='surucucu', n='Surucucu', c='Lachesis muta', g='Cobras', p='alto', t='peconhento', pica='Pica, e é perigosa',
      r='A maior cobra peçonhenta do Brasil. Os acidentes são raros, porque ela vive no fundo das matas.',
      rec=['Muito grande, de cor amarelada ou alaranjada com losangos escuros.', 'Escamas ásperas, eriçadas na cauda.', 'Só na Amazônia e em matas da Mata Atlântica.'],
      onde='Florestas úmidas da Amazônia e da Mata Atlântica.',
      faz='Parecido com a jararaca (dor, inchaço, sangramento), e também diarreia, cólica e pressão baixa.',
      soc='cobra', evitar='Botas e cuidado ao andar em trilhas de mata fechada.', f=[12, 2]),
 dict(id='coral', n='Coral-verdadeira', c='Micrurus spp.', g='Cobras', p='alto', t='peconhento', pica='Pica, e é perigosa',
      r='Tímida e de boca pequena, mas o veneno age sobre os nervos. Os acidentes são raros e graves.',
      rec=['Anéis vermelhos, pretos e brancos ou amarelos em volta do corpo.', 'Cabeça pequena, sem pescoço marcado.', 'As falsas-corais são quase iguais: não dá para ter certeza só olhando.'],
      onde='Em todo o Brasil, escondida embaixo de folhas, pedras e troncos.',
      faz='Pouca dor; depois pálpebras caídas, visão dupla, dificuldade para engolir e para respirar. É emergência.',
      soc='cobra', evitar='Nunca pegue cobras coloridas, nem as que parecem falsas-corais.', f=[13, 12]),
 dict(id='falsa-coral', n='Falsa-coral', c='várias espécies', g='Cobras', p='baixo', t='sem', pica='Pode morder; trate como coral',
      r='Cobras que imitam as cores da coral para se proteger. A maioria não tem veneno perigoso, mas não dá para diferenciar a olho nu.',
      rec=['Anéis ou faixas vermelhas, pretas e claras, como a coral.', 'Muitas vezes os anéis não dão a volta inteira no corpo.', 'Na dúvida, é coral: não chegue perto.'],
      onde='Em todo o Brasil.', faz='A maioria não causa nada grave; mas como não dá para ter certeza, toda picada de cobra colorida vai para o hospital.',
      soc='cobra', evitar='Não tente descobrir se é verdadeira ou falsa: afaste-se.', f=[13]),
 dict(id='jiboia', n='Jiboia', c='Boa constrictor', g='Cobras', p='nenhum', t='sem', pica='Morde se acuada, mas não tem veneno',
      r='Grande e sem veneno: mata as presas apertando. Ajuda a controlar ratos.',
      rec=['Grossa, com desenhos grandes nas costas, como selas.', 'Cauda com manchas avermelhadas.', 'Em geral de 2 a 3 m.'],
      onde='Matas, cerrados e até perto de casas, atrás de ratos.', faz='A mordida dói e pode infeccionar: lave e procure um posto. Não há veneno.',
      soc='geral', evitar='Não mate: chame os bombeiros (193) para levar para longe.', f=[22]),
 dict(id='sucuri', n='Sucuri', c='Eunectes murinus', g='Cobras', p='nenhum', t='sem', pica='Morde se acuada, mas não tem veneno',
      r='A maior cobra do Brasil. Vive na água e mata apertando; não tem veneno.',
      rec=['Verde-oliva com manchas pretas arredondadas.', 'Olhos e narinas no alto da cabeça.', 'Sempre perto de rios, lagoas e veredas.'],
      onde='Rios, lagoas e brejos da Amazônia, do Cerrado e do Pantanal.', faz='Ataque a gente é raríssimo. A mordida, se acontecer, pode infeccionar.',
      soc='geral', evitar='Não nade onde há sucuri à vista; não tente pegar.', f=[24]),
 dict(id='escorpiao-amarelo', n='Escorpião-amarelo', c='Tityus serrulatus', g='Escorpiões', p='alto', t='peconhento', pica='Pica, e é perigoso para crianças',
      r='O escorpião mais perigoso do Brasil e o que mais causa acidentes. Vive em casas, entulho e esgoto das cidades.',
      rec=['Corpo amarelo-claro, com o tronco mais escuro.', 'Uma serrinha nos últimos anéis da cauda.', 'Uns 7 cm; aparece à noite.'],
      onde='Cidades de quase todo o país, em ralos, caixas de esgoto, entulho e frestas.',
      faz='Dor forte na hora. Em crianças, pode causar vômito, suor, agitação e problemas no coração e nos pulmões: é emergência.',
      soc='escorpiao', evitar='Ralos com tela, lixo fechado, entulho longe de casa; sacuda roupas e sapatos antes de usar.', f=[4, 5]),
 dict(id='escorpiao-marrom', n='Escorpião-marrom', c='Tityus bahiensis', g='Escorpiões', p='medio', t='peconhento', pica='Pica; atenção com crianças',
      r='Escorpião escuro, comum no Sudeste e no Sul. A picada dói muito; em crianças pode ser grave.',
      rec=['Corpo marrom-escuro e pernas mais claras.', 'Sem a serrinha na cauda do amarelo.', 'Mesmo tamanho, uns 7 cm.'],
      onde='Sudeste, Centro-Oeste e Sul, em quintais, cupinzeiros e entulho.', faz='Dor forte no local; em crianças, os mesmos sinais de alarme do amarelo.',
      soc='escorpiao', evitar='Os mesmos cuidados do escorpião-amarelo.', f=[5, 4]),
 dict(id='armadeira', n='Armadeira', c='Phoneutria spp.', g='Aranhas e parecidos', p='medio', t='peconhento', pica='Pica, e dói muito',
      r='A aranha que mais causa acidentes (42% dos casos com aranhas). Levanta as patas da frente e “arma” para atacar.',
      rec=['Grande, marrom-acinzentada, com pernas grossas.', 'Levanta as patas da frente quando ameaçada.', 'Não faz teia: anda à noite atrás de presas.'],
      onde='Sul, Sudeste e Centro-Oeste; entra em sapatos, roupas, cachos de banana e entulho.',
      faz='Dor muito forte e imediata, suor e coração acelerado. Em crianças, pode ser grave.',
      soc='aranha', evitar='Sacuda sapatos e roupas; cuidado ao mexer em bananas e lenha.', f=[6, 28]),
 dict(id='aranha-marrom', n='Aranha-marrom', c='Loxosceles spp.', g='Aranhas e parecidos', p='alto', t='peconhento', pica='Pica, e pode ser grave',
      r='Pequena e tímida, mas a forma mais grave de acidente com aranha no Brasil, mais comum no Sul.',
      rec=['Pequena (uns 3 cm com as pernas), marrom, pernas finas.', 'Uma mancha escura em forma de violino no alto do corpo.', 'Vive atrás de móveis, quadros, rodapés e em roupas guardadas.'],
      onde='Dentro de casa, em cantos escuros e secos; mais no Sul e no Sudeste.',
      faz='A picada quase não dói; horas depois, o local fica vermelho, roxo e pode virar ferida (necrose). Às vezes, urina escura.',
      soc='aranha', evitar='Afaste móveis da parede, sacuda roupas e toalhas, limpe atrás de quadros.', f=[6, 28]),
 dict(id='viuva-negra', n='Viúva-negra', c='Latrodectus spp.', g='Aranhas e parecidos', p='medio', t='peconhento', pica='Pica; acidentes raros',
      r='Acidentes raros no Brasil, mais no litoral do Nordeste. O veneno causa dor e contrações nos músculos.',
      rec=['Pequena, preta ou marrom, de abdome redondo e brilhante.', 'Uma mancha vermelha ou alaranjada embaixo do abdome.', 'Faz teias irregulares em vegetação baixa e cantos.'],
      onde='Litoral e vegetação baixa, mais no Nordeste.', faz='Dor que se espalha, contrações nos músculos (barriga e costas), suor.',
      soc='aranha', evitar='Luvas ao mexer em vasos, entulho e plantas baixas.', f=[28]),
 dict(id='caranguejeira', n='Caranguejeira', c='várias espécies (Theraphosidae)', g='Aranhas e parecidos', p='baixo', t='urticante', pica='Pode picar, mas o veneno é fraco',
      r='Grande e peluda, assusta muito, mas o veneno é fraco perto do da aranha-marrom. Os pelos soltos coçam.',
      rec=['Muito grande e peluda.', 'Anda devagar, no chão.', 'Pode soltar pelos que irritam a pele e os olhos.'],
      onde='Em todo o Brasil, em tocas no chão e em troncos.', faz='Dor no local se picar; coceira e irritação pelos pelos.',
      soc='aranha', evitar='Não pegue com a mão; não esfregue os olhos depois de mexer.', f=[7]),
 dict(id='opiliao', n='Opilião', c='Opiliones', g='Aranhas e parecidos', p='nenhum', t='sem', pica='Não pica e não tem veneno',
      r='Parece aranha, mas não é: não tem glândulas de veneno e não consegue picar uma pessoa.',
      rec=['Corpo de uma peça só, redondo, sem “cintura”.', 'Pernas muito longas e finas.', 'Só um par de olhos (as aranhas têm seis ou oito) e não faz teia.'],
      onde='Lugares úmidos: troncos, pedras, paredes de casas perto de mata.', faz='Nada. Alguns soltam um cheiro forte para se defender.',
      soc='geral', evitar='Não precisa matar.', f=[30]),
 dict(id='abelha-africanizada', n='Abelha-africanizada', c='Apis mellifera', g='Abelhas, vespas e formigas', p='medio', t='peconhento', pica='Pica; muitas picadas são perigosas',
      r='A abelha do mel. Uma picada dói; muitas de uma vez, de um enxame, são perigosas. Quem tem alergia corre risco com uma só.',
      rec=['Abelha peluda, amarela e preta, de uns 1,5 cm.', 'O ferrão fica preso na pele, com a bolsa de veneno.', 'Defende a colmeia em grupo quando a mexem.'],
      onde='Em todo o Brasil, em ocos, telhados, caixas e árvores.', faz='Dor, vermelhidão e inchaço. Com muitas picadas: tontura, náusea, falta de ar. Alergia: inchaço no rosto e falta de ar.',
      soc='abelha', evitar='Não mexa em colmeias: chame os bombeiros (193) ou um apicultor.', f=[14, 15]),
 dict(id='abelha-sem-ferrao', n='Abelha sem ferrão', c='Meliponini (jataí, uruçu, mandaçaia…)', g='Abelhas, vespas e formigas', p='nenhum', t='sem', pica='Não pica',
      r='As abelhas nativas do Brasil: o ferrão é atrofiado e não pica. Algumas mordiscam ou enroscam no cabelo.',
      rec=['Pequenas, muitas vezes amarelas ou pretas.', 'Entrada do ninho em tubinho de cera ou de barro.', 'Fazem mel e polinizam plantas nativas.'],
      onde='Ocos de árvores, muros e postes, inclusive nas cidades.', faz='Nada de grave: no máximo uma mordidinha.',
      soc='geral', evitar='Achou um ninho? Não destrua: veja como pedir o resgate.', f=[]),
 dict(id='vespa', n='Vespa e marimbondo', c='várias espécies (Vespidae)', g='Abelhas, vespas e formigas', p='medio', t='peconhento', pica='Pica, e pode picar várias vezes',
      r='Diferente da abelha, a vespa não perde o ferrão e pode picar de novo. Os ninhos de papel ficam em beirais e galhos.',
      rec=['Corpo liso, de cintura bem fina.', 'Ninho de “papel” cinza ou marrom.', 'Amarelas, pretas ou marrons.'],
      onde='Em todo o Brasil, em beirais, árvores e arbustos.', faz='Dor forte, vermelhidão e inchaço; muitas picadas ou alergia podem ser graves.',
      soc='abelha', evitar='Não cutuque ninhos; chame os bombeiros para tirar.', f=[25]),
 dict(id='lava-pes', n='Formiga lava-pés', c='Solenopsis spp.', g='Abelhas, vespas e formigas', p='baixo', t='peconhento', pica='Pica, e arde',
      r='Formiguinha avermelhada de montes de terra solta. Pica muitas vezes; cada picada vira uma bolinha branca.',
      rec=['Pequena, avermelhada.', 'Montes de terra fofa em gramados e beiras de calçada.', 'Ataca em grupo quando o monte é pisado.'],
      onde='Gramados, jardins e beiras de estrada.', faz='Ardência e uma pústula branca no lugar de cada picada. Alergia grave é rara, mas existe.',
      soc='abelha', evitar='Calçado fechado em gramados; não pise nos montes.', f=[25]),
 dict(id='tocandira', n='Tocandira', c='Paraponera clavata', g='Abelhas, vespas e formigas', p='medio', t='peconhento', pica='Pica, e é a picada mais dolorosa',
      r='A formiga-cabo-verde, de 2 a 3 cm. A dor da picada vem em ondas e pode durar um dia inteiro.',
      rec=['Formiga grande, preta ou marrom-escura.', 'Anda sozinha em troncos e no chão da mata.', 'Vive na Amazônia e em outras florestas.'],
      onde='Florestas da Amazônia e do Centro-Oeste.', faz='Dor muito forte e longa, tremor e suor no local.',
      soc='abelha', evitar='Olhe antes de apoiar a mão em troncos na mata.', f=[26]),
 dict(id='taturana', n='Taturana (Lonomia)', c='Lonomia spp.', g='Lagartas e besouros', p='alto', t='urticante', pica='Queima no contato, e pode ser grave',
      r='Uma lagarta de espinhos que, no contato, pode causar sangramentos. O Butantan é o único produtor do soro no mundo.',
      rec=['Espinhos verdes ou marrons, ramificados como pinheirinhos.', 'Ficam em grupos, parados nos troncos das árvores.', 'Cor que se confunde com a casca.'],
      onde='Sul, Sudeste e Centro-Oeste, em troncos de árvores de pomar e de mata.',
      faz='Queimação na hora; horas depois, manchas roxas, sangramento na gengiva, no nariz ou na urina. É emergência.',
      soc='lagarta', evitar='Olhe o tronco antes de encostar; luvas ao podar árvores.', f=[8, 9]),
 dict(id='lagarta-urticante', n='Outras lagartas de fogo', c='várias espécies', g='Lagartas e besouros', p='baixo', t='urticante', pica='Queima no contato',
      r='Muitas lagartas peludas ou espinhudas queimam a pele no contato. Na dúvida, trate como se fosse Lonomia.',
      rec=['Pelos ou espinhos no corpo.', 'Folhas e troncos de árvores e arbustos.', 'Várias cores.'],
      onde='Em todo o Brasil.', faz='Queimação, vermelhidão e inchaço no local, que passam em horas.',
      soc='lagarta', evitar='Não toque em lagartas peludas ou espinhudas.', f=[9]),
 dict(id='poto', n='Potó', c='Paederus spp.', g='Lagartas e besouros', p='baixo', t='venenoso', pica='Não pica: queima se for esmagado na pele',
      r='Um besourinho fino, preto e alaranjado. Não pica nem morde: esmagado na pele, solta uma substância que queima.',
      rec=['Pequeno (cerca de 1 cm), fino, parecido com uma formiga.', 'Faixas alaranjadas e pretas.', 'Voa até lâmpadas acesas à noite.'],
      onde='Em todo o Brasil, mais na época das chuvas.', faz='Uma queimadura vermelha, com bolhas, que aparece horas depois e some em uma ou duas semanas.',
      soc='lagarta', evitar='Não esmague: sopre ou tire com um papel. Telas nas janelas.', f=[16]),
 dict(id='lacraia', n='Lacraia', c='Scolopendra e outras', g='Outros da terra', p='baixo', t='peconhento', pica='Pica (com as presas da frente), e dói',
      r='Bicho de muitas patas que pica com um par de presas na cabeça. Dói, mas não há morte comprovada no Brasil.',
      rec=['Corpo achatado e comprido, de muitos anéis.', 'Um par de patas em cada anel.', 'Rápida, foge da luz.'],
      onde='Ralos, entulho, madeira e terra úmida.', faz='Dor e inchaço no local; com as grandes, às vezes febre.',
      soc='geral', evitar='Ralos fechados e entulho longe de casa.', f=[27]),
 dict(id='sapo-cururu', n='Sapo-cururu', c='Rhinella spp.', g='Outros da terra', p='baixo', t='venenoso', pica='Não pica: é venenoso, não peçonhento',
      r='O exemplo de bicho venenoso: tem veneno nas glândulas atrás dos olhos, mas não injeta. O perigo é para quem morde ou põe na boca.',
      rec=['Sapo grande, de pele grossa e cheia de verrugas.', 'Duas glândulas saltadas atrás dos olhos.', 'Aparece à noite, depois da chuva.'],
      onde='Em todo o Brasil, perto de casas e luzes.', faz='Pegar na mão não faz mal; lave as mãos depois e não esfregue os olhos. Cachorro que morde um sapo pode passar mal.',
      soc='geral', evitar='Afaste os cães dos sapos à noite.', f=[1, 20]),
 dict(id='lagartixa', n='Lagartixa', c='Hemidactylus mabouia e outras', g='Outros da terra', p='nenhum', t='sem', pica='Não pica e não é venenosa',
      r='A lagartixa de parede não é venenosa: é um mito. Come mosquitos, baratas e outros insetos.',
      rec=['Pequena, clara, quase transparente.', 'Sobe em paredes e tetos.', 'Aparece perto das lâmpadas à noite.'],
      onde='Paredes e tetos das casas.', faz='Nada. Lave as mãos se pegar, como com qualquer bicho.',
      soc='geral', evitar='Não precisa matar: ela ajuda contra insetos.', f=[29]),
 dict(id='agua-viva', n='Água-viva e caravela', c='Cnidaria', g='Da água', p='medio', t='peconhento', pica='Queima no contato',
      r='Os tentáculos têm células que disparam veneno ao tocar a pele. A caravela é a mais perigosa do litoral.',
      rec=['Corpo gelatinoso e transparente, com tentáculos.', 'A caravela tem uma “bolsa” azul ou roxa que boia.', 'Aparecem mais com vento e mar agitado.'],
      onde='Praias de todo o litoral.', faz='Dor forte e marcas vermelhas em linhas. Raramente, falta de ar e mal-estar geral.',
      soc='agua', evitar='Respeite as bandeiras e os avisos dos guarda-vidas; não toque nas que estão na areia.', f=[18, 17]),
 dict(id='arraia', n='Arraia de água doce', c='Potamotrygon spp.', g='Da água', p='medio', t='peconhento', pica='Ferroa com a cauda, e dói muito',
      r='Fica enterrada na areia dos rios e ferroa quem pisa nela. A dor é muito forte e a ferida pode infeccionar.',
      rec=['Corpo achatado e redondo, com manchas.', 'Um ferrão serrilhado na cauda.', 'Rios da Amazônia, do Pantanal e do Centro-Oeste.'],
      onde='Praias de rio, mais na seca, quando a água baixa.', faz='Dor muito forte e longa; a ferida pode necrosar e infeccionar.',
      soc='agua', evitar='Arraste os pés na areia ao entrar no rio, em vez de dar passos: a arraia foge.', f=[19, 31]),
]
POR_ID = {b['id']: b for b in B}
# onde cada bicho aparece (os textos de "Onde vive" das fichas, resumidos para os filtros do catálogo)
LUGARES = [('casa', 'Dentro de casa'), ('quintal', 'Quintal e cidade'), ('mata', 'Mata e trilha'), ('campo', 'Campo e roça'), ('praia', 'Praia e mar'), ('rio', 'Rio e lagoa')]
REGIOES = {'N': 'Norte', 'NE': 'Nordeste', 'CO': 'Centro-Oeste', 'SE': 'Sudeste', 'S': 'Sul'}
TODAS = 'N NE CO SE S'
LUG_REG = {
 'jararaca': ('mata campo quintal', TODAS), 'cascavel': ('campo', TODAS), 'surucucu': ('mata', 'N NE SE'),
 'coral': ('mata quintal campo', TODAS), 'falsa-coral': ('mata quintal campo', TODAS), 'jiboia': ('mata campo quintal', TODAS),
 'sucuri': ('rio', 'N CO'), 'escorpiao-amarelo': ('casa quintal', TODAS), 'escorpiao-marrom': ('quintal casa', 'CO SE S'),
 'armadeira': ('casa quintal campo', 'CO SE S'), 'aranha-marrom': ('casa', 'SE S'), 'viuva-negra': ('quintal praia', 'NE'),
 'caranguejeira': ('mata quintal', TODAS), 'opiliao': ('mata quintal', TODAS), 'abelha-africanizada': ('quintal campo mata', TODAS),
 'abelha-sem-ferrao': ('quintal mata', TODAS), 'vespa': ('quintal campo', TODAS), 'lava-pes': ('quintal campo', TODAS),
 'tocandira': ('mata', 'N CO'), 'taturana': ('quintal mata', 'CO SE S'), 'lagarta-urticante': ('quintal mata', TODAS),
 'poto': ('casa quintal', TODAS), 'lacraia': ('casa quintal', TODAS), 'sapo-cururu': ('quintal', TODAS), 'lagartixa': ('casa', TODAS),
 'agua-viva': ('praia', 'N NE SE S'), 'arraia': ('rio', 'N CO'),
}
for b in B: b['lug'], b['reg'] = LUG_REG[b['id']]
assert set(LUG_REG) == set(POR_ID)

# fotos: entram sozinhas quando existem em img/bichos/<id>.webp e <id>-640.webp, com o crédito em img/bichos/creditos.json
# ({"<id>": {"autor": "...", "licenca": "CC BY-SA 4.0", "url": "https://commons.wikimedia.org/..."}})
try: CRED_FOTOS = json.loads((SITIO / 'img' / 'bichos' / 'creditos.json').read_text())
except FileNotFoundError: CRED_FOTOS = {}
def foto(b):
    if not (SITIO / 'img' / 'bichos' / f'{b["id"]}.webp').is_file(): return ''
    c = CRED_FOTOS.get(b['id'], {})
    cred = f' Foto: <a href="{c["url"]}" rel="noopener">{c.get("autor", "Wikimedia Commons")}</a>, {c.get("licenca", "")}.' if c.get('url') else ''
    return (f'<figure class="ficha-foto"><img src="{{{{raiz}}}}img/bichos/{b["id"]}-640.webp" srcset="{{{{raiz}}}}img/bichos/{b["id"]}-640.webp 640w, {{{{raiz}}}}img/bichos/{b["id"]}.webp 1000w" '
            f'sizes="(min-width: 700px) 50vw, 100vw" width="640" height="427" alt="{b["n"]}"><figcaption><strong>Repare:</strong> {b["rec"][0]}{cred}</figcaption></figure>')

def compartilhar(texto, endereco):
    from urllib.parse import quote
    t = f'{texto} {URL_SITE}{endereco}'
    return (f'<div class="compartilhar" data-texto="{html.escape(texto)}" data-url="{URL_SITE}{endereco}">'
            f'<a class="botao botao-claro" href="https://wa.me/?text={quote(t)}">Mandar no WhatsApp</a>'
            f'<button type="button" class="botao botao-claro partilhar" hidden>Compartilhar</button></div>')
PARES = [
 ('coral', 'falsa-coral', 'Não dá para separar a olho nu: o Butantan orienta tratar toda cobra colorida como coral-verdadeira.'),
 ('jararaca', 'jiboia', 'A jararaca tem a cabeça triangular, a fosseta e desenhos em V; a jiboia é mais grossa, de desenhos de sela, e não tem veneno.'),
 ('cascavel', 'jararaca', 'A cascavel tem o chocalho na cauda e losangos claros; a jararaca não tem chocalho.'),
 ('armadeira', 'caranguejeira', 'A armadeira é menos peluda e “arma” as patas da frente; a caranguejeira é bem maior, peluda, e o veneno é fraco.'),
 ('aranha-marrom', 'opiliao', 'A aranha-marrom tem cintura e a mancha de violino; o opilião tem o corpo de uma peça só e não tem veneno.'),
 ('abelha-africanizada', 'abelha-sem-ferrao', 'A africanizada é peluda, pica e deixa o ferrão; a sem ferrão é pequena e não pica.'),
 ('escorpiao-amarelo', 'escorpiao-marrom', 'O amarelo é claro e tem a serrinha na cauda; o marrom é escuro e sem serrinha. Os dois picam.'),
 ('vespa', 'abelha-africanizada', 'A vespa é lisa, de cintura fina, e pode picar várias vezes; a abelha é peluda e deixa o ferrão.'),
 ('taturana', 'lagarta-urticante', 'A Lonomia tem espinhos ramificados como pinheirinhos e fica em grupos nos troncos; na dúvida, trate qualquer lagarta de fogo como Lonomia.'),
]

# ---------------------------------------------------------------- o molde das páginas (a de Créditos, em português)
molde = (M / 'creditos.html').read_text()
cabeca, resto = molde.split('    <main id="conteudo">', 1)
rodape = resto.split('    </main>', 1)[1]
pt = json.loads((AQUI / 'textos' / 'pt-BR.json').read_text())['textos']
def resolver(s):
    return re.sub(r'\{\{([a-z_0-9]+)\}\}', lambda m: pt.get(m.group(1), m.group(0)) if m.group(1) not in ('lang', 'raiz', 'idiomas', 'alternativas', 'textos_js') else m.group(0), s)
cabeca = resolver(cabeca); rodape = resolver(rodape)
# o molde já traz, da rodada anterior, o botão "Fui picado" e o manifesto das páginas em português: tira para não repetir
cabeca = re.sub(r'\{\{\?pt-BR\}\}(?:<a class="fui-picado"|\s*<link rel="manifest"|\s*<script src="\{\{raiz\}\}js/guia).*?\{\{/pt-BR\}\}\n?', '', cabeca, flags=re.S)
cabeca = re.sub(r'<ul class="menu">.*?</ul>', '{{MENU}}', cabeca, flags=re.S)
cabeca = re.sub(r'<a class="marca" href="index.html">.*?</a>', f'<a class="marca" href="index.html">{MARCA_PT}</a>', cabeca, flags=re.S)
cabeca = re.sub(r"<link rel=\"icon\"[^>]*>", "<link rel=\"icon\" href=\"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'%3E%3Ctext y='.9em' font-size='90'%3E🐍%3C/text%3E%3C/svg%3E\">", cabeca)
rodape = rodape.replace('{{idiomas}}', '')
RODAPE_PT = f'<p>{NOME} é um guia de estudo: não substitui o atendimento médico. Em caso de acidente, ligue 192 ou vá ao serviço de saúde mais perto.</p><p><a href="fontes.html">Fontes</a> · <a href="descobrir.html">Abelhas sem ferrão</a> · <a href="creditos.html">Créditos das fotos</a> · Projeto de estudo de Luiz Matheus Moraes Vega</p>'
rodape = re.sub(r'<div class="container">.*?</div>', '<div class="container">' + RODAPE_PT + '</div>', rodape, count=1, flags=re.S)
so_pt = []
def pagina(arquivo, titulo, descricao, corpo, scripts=(), imagem='img/compartilhar/guia.jpg'):
    s = cabeca.replace('{{MENU}}', menu_pt(arquivo))
    s = s.replace('</nav>', '</nav>\n            ' + fui_picado(arquivo), 1)
    og = (f'    <meta property="og:type" content="website"><meta property="og:title" content="{html.escape(titulo)}">'
          f'<meta property="og:description" content="{html.escape(descricao)}"><meta property="og:image" content="{URL_SITE}{imagem}">'
          f'<meta property="og:url" content="{URL_SITE}{arquivo}"><meta name="twitter:card" content="summary_large_image">\n    {CAB_OFF}\n')
    s = re.sub(r'<title>.*?</title>', f'<title>{titulo}</title>', s)
    s = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{html.escape(descricao)}">', s)
    s = s.replace('<meta name="theme-color" content="#E9A23B">', '<meta name="theme-color" content="#2E2A1F">')
    extra = og + ''.join(f'    <script src="{{{{raiz}}}}js/{n}" defer></script>\n' for n in scripts)
    s = s.replace('{{alternativas}}', extra + '{{alternativas}}')
    (M / arquivo).write_text(s + '    <main id="conteudo">\n' + corpo + '    </main>' + rodape)
    if arquivo not in so_pt: so_pt.append(arquivo)

def selo(b):
    nome, sub = PERIGO[b['p']]
    return f'<span class="perigo perigo-{b["p"]}"><strong>{nome}</strong> {sub}</span>'

# ---------------------------------------------------------------- as fichas (bicho-<id>.html)
def ficha(b, n):
    ant, prox = B[n - 1], B[(n + 1) % len(B)]
    rec = ''.join(f'<li>{x}</li>' for x in b['rec'])
    notas = ''.join(fonte(k) for k in b['f'])
    pares = [(y if x == b['id'] else x, t) for x, y, t in PARES if b['id'] in (x, y)]
    comp = ''.join(f'<div class="par"><p class="par-nome"><a href="bicho-{o}.html">{POR_ID[o]["n"]}</a> {selo(POR_ID[o])}</p><p><strong>A diferença:</strong> {t}</p></div>' for o, t in pares)
    comp = f'<section aria-labelledby="conf-t"><h2 id="conf-t">Não confunda com</h2>{comp}</section>' if comp else ''
    abelha = '<p><a class="botao" href="descobrir.html">Conhecer as abelhas sem ferrão</a> <a class="botao botao-claro" href="achei-um-ninho.html">Achei um ninho!</a></p>' if b['id'] == 'abelha-sem-ferrao' else ''
    corpo = f'''        <article class="ficha-bicho">
            <div class="container">
                <p class="trilha"><a href="bichos.html">Bichos</a> <span aria-hidden="true">›</span> {b['n']}</p>
                <div class="ficha-topo">
                    {foto(b)}
                    <div class="ficha-titulo">
                        <p class="ficha-grupo">{b['g']}</p>
                        <h1>{b['n']}</h1>
                        <p class="cientifico">{b['c']}</p>
                        <p class="ficha-abre">{b['r']}{notas}</p>
                    </div>
                    <div class="ficha-resposta perigo-caixa-{b['p']}">
                        <p class="resposta-pergunta">Pica ou não pica?</p>
                        <p class="resposta">{b['pica']}</p>
                        {selo(b)}
                        <p class="resposta-tipo">{TIPO[b['t']]}</p>
                        <a class="botao botao-socorro" href="socorro.html#{b['soc']}">O que fazer se picar</a>
                    </div>
                </div>
                <div class="ficha-corpo">
                    <section aria-labelledby="rec-t"><h2 id="rec-t">Como reconhecer</h2><ul class="lista">{rec}</ul></section>
                    <section aria-labelledby="onde-t"><h2 id="onde-t">Onde vive</h2><p>{b['onde']}</p></section>
                    <section aria-labelledby="faz-t"><h2 id="faz-t">O que causa</h2><p>{b['faz']}</p></section>
                    <section aria-labelledby="evi-t"><h2 id="evi-t">Como evitar</h2><p>{b['evitar']}</p>{abelha}</section>
                    {comp}
                </div>
                <nav class="ficha-navegar" aria-label="Outros bichos"><a href="bicho-{ant['id']}.html" rel="prev"><span aria-hidden="true">←</span> {ant['n']}</a><a href="bicho-{prox['id']}.html" rel="next">{prox['n']} <span aria-hidden="true">→</span></a></nav>
                <div class="ficha-fim">
                    <div><h2 class="ficha-fim-t">Mande para quem precisa saber</h2>{compartilhar(f"{b['n']}: {b['pica'].lower()}. Veja como reconhecer e o que fazer:", f"bicho-{b['id']}.html")}</div>
                    <p class="ficha-nota">Este guia ajuda a reconhecer, mas não substitui o atendimento médico. Em qualquer picada de bicho peçonhento, procure o serviço de saúde: o soro só existe lá, e é de graça pelo SUS.</p>
                    <p class="revisao">Texto conferido nas fontes em {REVISAO}. Ainda não passou pela leitura de um profissional de saúde.</p>
                </div>
            </div>
        </article>
'''
    pagina(f'bicho-{b["id"]}.html', f'{b["n"]}: pica ou não pica? — {NOME}', f'{b["n"]}: é perigoso? Como reconhecer, o que causa, o que fazer e como evitar.', corpo, scripts=[JS], imagem=f'img/compartilhar/{b["id"]}.jpg')
for n, b in enumerate(B):
    ficha(b, n)

# ---------------------------------------------------------------- o catálogo (bichos.html)
def cartao(b):
    return (f'<li class="bicho-cartao" data-grupo="{b["g"]}" data-perigo="{b["p"]}" data-lugar="{b["lug"]}" data-regiao="{b["reg"]}" data-busca="{html.escape((b["n"] + " " + b["c"]).lower())}">'
            f'<a href="bicho-{b["id"]}.html"><span class="bicho-grupo">{b["g"]}</span><strong>{b["n"]}</strong><span class="bicho-pica">{b["pica"]}</span>{selo(b)}</a></li>')
chips_g = '<button type="button" class="chip" data-filtro-grupo="" aria-pressed="true">Todos</button>' + ''.join(f'<button type="button" class="chip" data-filtro-grupo="{g}" aria-pressed="false">{g}</button>' for g in GRUPOS)
chips_p = '<button type="button" class="chip" data-filtro-perigo="" aria-pressed="true">Todos</button>' + ''.join(f'<button type="button" class="chip chip-{k}" data-filtro-perigo="{k}" aria-pressed="false">{v[0]}</button>' for k, v in PERIGO.items())
chips_l = '<button type="button" class="chip" data-filtro-lugar="" aria-pressed="true">Todos</button>' + ''.join(f'<button type="button" class="chip" data-filtro-lugar="{k}" aria-pressed="false">{v}</button>' for k, v in LUGARES)
chips_r = '<button type="button" class="chip" data-filtro-regiao="" aria-pressed="true">Brasil</button>' + ''.join(f'<button type="button" class="chip" data-filtro-regiao="{k}" aria-pressed="false">{v}</button>' for k, v in REGIOES.items())
# o mapa só mostra; quem filtra são os botões (o toque no mapa aperta o botão da região)
MAPA = (AQUI / 'regioes.svg').read_text().strip().replace('role="img" aria-label="Mapa das cinco regiões do Brasil"', 'aria-hidden="true"')
bichos = f'''        <section class="titulo-guia">
            <div class="container">
                <h1>Os bichos</h1>
                <p>{len(B)} bichos do Brasil que picam, queimam ou levam a fama sem merecer. Toque num para ver se é perigoso, como reconhecer e o que fazer.</p>
            </div>
        </section>
        <section class="secao">
            <div class="container catalogo">
                <div class="filtros-bichos">
                    <label for="busca-bicho">Procurar</label>
                    <input id="busca-bicho" type="search" placeholder="Ex.: escorpião, aranha, lagarta" autocomplete="off">
                    <fieldset><legend>Grupo</legend><div class="chips">{chips_g}</div></fieldset>
                    <fieldset><legend>Perigo</legend><div class="chips">{chips_p}</div></fieldset>
                    <fieldset><legend>Onde você está?</legend><div class="chips">{chips_l}</div></fieldset>
                    <fieldset><legend>Onde você mora?</legend><div class="chips">{chips_r}</div>{MAPA}</fieldset>
                    <p class="contagem" aria-live="polite"><strong id="contagem">{len(B)}</strong> bichos</p>
                </div>
                <ul class="bichos-lista">{''.join(cartao(b) for b in B)}</ul>
                <p class="vazio" hidden>Nenhum bicho com esses filtros.</p>
            </div>
        </section>
'''
pagina('bichos.html', f'Os bichos: quais picam e quais não — {NOME}', f'{len(B)} bichos do Brasil: cobras, escorpiões, aranhas, abelhas, vespas, formigas, lagartas e bichos da água. Quais são perigosos e quais não.', bichos, scripts=[JS])

# ---------------------------------------------------------------- "Que bicho é esse?" (identificar.html): perguntas que levam ao bicho
ARVORE = {
 'inicio': {'p': 'Como é o bicho?', 'o': [
   ('Comprido, sem patas (cobra)', 'cobra'), ('Oito patas: aranha ou parecido', 'aranha'), ('Pinças e uma cauda com ferrão', 'escorpiao'),
   ('Voa e pica: abelha ou vespa', 'voa'), ('Formiga', 'formiga'), ('Lagarta (com pelos ou espinhos)', 'lagarta'),
   ('Muitas patas, achatado e comprido', '=lacraia'), ('Besourinho fino, preto e laranja', '=poto'), ('Sapo ou lagartixa', 'sapo'), ('Na água: mar ou rio', 'agua')]},
 'cobra': {'p': 'Tem anéis coloridos (vermelho, preto e branco ou amarelo)?', 'o': [('Sim, anéis coloridos', '=coral'), ('Não', 'cobra2')]},
 'cobra2': {'p': 'Tem um chocalho na ponta da cauda?', 'o': [('Sim, um chocalho', '=cascavel'), ('Não', 'cobra3')]},
 'cobra3': {'p': 'Como é a cabeça?', 'o': [('Triangular, bem destacada do pescoço, com desenhos em V no corpo', 'cobra4'), ('Grossa, sem pescoço marcado, desenhos de sela nas costas', '=jiboia'), ('Enorme, na água, verde com manchas pretas', '=sucuri'), ('Não sei', '=jararaca')]},
 'cobra4': {'p': 'Onde estava?', 'o': [('Mata fechada da Amazônia ou da Mata Atlântica, e era muito grande', '=surucucu'), ('Em outro lugar', '=jararaca')]},
 'aranha': {'p': 'Como é o corpo?', 'o': [('Uma peça só, redonda, com pernas muito longas e finas', '=opiliao'), ('Grande e muito peluda', '=caranguejeira'), ('Pequena, marrom, em cantos escuros de casa', '=aranha-marrom'), ('Levanta as patas da frente para atacar', '=armadeira'), ('Preta, abdome redondo, mancha vermelha embaixo', '=viuva-negra')]},
 'escorpiao': {'p': 'Qual é a cor?', 'o': [('Amarelo-claro, com o tronco escuro', '=escorpiao-amarelo'), ('Marrom-escuro', '=escorpiao-marrom'), ('Não sei', '=escorpiao-amarelo')]},
 'voa': {'p': 'Como ela é?', 'o': [('Peluda, amarela e preta, deixou o ferrão', '=abelha-africanizada'), ('Lisa, de cintura fina', '=vespa'), ('Pequenina, não picou (só mordiscou)', '=abelha-sem-ferrao')]},
 'formiga': {'p': 'De que tamanho?', 'o': [('Grande (2 a 3 cm), escura, na mata', '=tocandira'), ('Pequena, avermelhada, de montes de terra', '=lava-pes')]},
 'lagarta': {'p': 'Como são os espinhos?', 'o': [('Ramificados como pinheirinhos, em grupo num tronco', '=taturana'), ('Outros pelos ou espinhos', '=lagarta-urticante'), ('Não sei', '=taturana')]},
 'sapo': {'p': 'Qual dos dois?', 'o': [('Sapo grande, de pele com verrugas', '=sapo-cururu'), ('Lagartixa de parede', '=lagartixa')]},
 'agua': {'p': 'Onde foi?', 'o': [('No mar: bicho gelatinoso com tentáculos', '=agua-viva'), ('No rio: ferroada no pé, na areia', '=arraia')]},
}
ID_DADOS = {b['id']: {'n': b['n'], 'pica': b['pica'], 'p': b['p'], 'pn': PERIGO[b['p']][0], 'ps': PERIGO[b['p']][1], 'r': b['r'], 'soc': b['soc']} for b in B}
ident_json = json.dumps({'arvore': {k: {'p': v['p'], 'o': v['o']} for k, v in ARVORE.items()}, 'bichos': ID_DADOS}, ensure_ascii=False).replace('</', '<\\/')
sem_js = ''.join(f'<li><a href="bichos.html">{t}</a></li>' for t, _ in ARVORE['inicio']['o'])
identificar = f'''        <section class="titulo-guia">
            <div class="container">
                <h1>Que bicho é esse?</h1>
                <p>Responda algumas perguntas sobre o bicho que você viu, ou que picou alguém, e veja se é perigoso e o que fazer.</p>
            </div>
        </section>
        <section class="secao">
            <div class="container identificar">
                <div class="id-caixa" aria-live="polite">
                    <noscript><p>As perguntas precisam de JavaScript. Sem ele, veja <a href="bichos.html">todos os bichos</a>.</p></noscript>
                    <ul class="id-sem-js">{sem_js}</ul>
                </div>
                <aside class="id-alerta">
                    <p class="id-alerta-titulo">Alguém foi picado?</p>
                    <p>Não espere descobrir o bicho: lave o local com água e sabão e procure o serviço de saúde. Se puder, tire uma foto do bicho, sem chegar perto.{fonte(2)}</p>
                    <p><a class="botao botao-socorro" href="socorro.html">O que fazer agora</a></p>
                    <p class="id-tel"><a href="tel:192">192</a> SAMU · <a href="tel:193">193</a> Bombeiros</p>
                </aside>
                <script type="application/json" id="id-dados">{ident_json}</script>
            </div>
        </section>
'''
pagina('identificar.html', f'Que bicho é esse? — {NOME}', 'Responda algumas perguntas e descubra que bicho é, se é perigoso e o que fazer: cobras, aranhas, escorpiões, abelhas, lagartas e mais.', identificar, scripts=[JS])

# ---------------------------------------------------------------- Socorro (socorro.html)
SOC = [
 ('cobra', 'Picada de cobra', ['Lave o local com água e sabão.', 'Deixe a pessoa deitada e calma, e evite que ela ande ou corra.', 'Tire anéis, relógios e calçados apertados: o local pode inchar.', 'Vá logo ao serviço de saúde: o soro só existe lá.', 'Se der, tire uma foto da cobra, de longe.'], [2, 3]),
 ('escorpiao', 'Picada de escorpião', ['Lave o local com água e sabão.', 'Uma compressa morna ajuda na dor.', 'Criança picada vai direto para o serviço de saúde, sem esperar sintomas.', 'Adulto com dor forte, vômito ou suor também vai.'], [3, 4]),
 ('aranha', 'Picada de aranha', ['Lave o local com água e sabão.', 'Compressa morna para a dor da armadeira.', 'Procure o serviço de saúde, mesmo que não doa: a da aranha-marrom quase não dói e pode piorar horas depois.'], [3, 28]),
 ('lagarta', 'Lagarta (taturana) e potó', ['Lave o local com água fria e sabão; compressa fria alivia.', 'Se a lagarta tinha espinhos, vá ao serviço de saúde: pode ser Lonomia, que causa sangramento.', 'Fotografe a lagarta, sem tocar.', 'Potó: lave com água e sabão e não esfregue; procure o médico se pegar nos olhos ou for extenso.'], [8, 9, 16]),
 ('abelha', 'Abelhas, vespas e formigas', ['Tire os ferrões da abelha logo, raspando com a unha ou um cartão, sem apertar o saquinho de veneno.', 'Lave e ponha gelo enrolado num pano.', 'Muitas picadas, picada na boca ou na garganta, inchaço no rosto ou falta de ar: serviço de saúde na hora (192).', 'Quem tem alergia conhecida deve ir ao hospital mesmo com uma picada.'], [14, 15, 25]),
 ('agua', 'Água-viva, caravela e arraia', ['Água-viva e caravela: saia da água, lave com água do mar e tire os tentáculos com cuidado, sem esfregar. Nunca use água doce.', 'O vinagre ajuda em água-viva, mas não serve para a caravela.', 'Arraia: lave e ponha o pé em água quente (sem queimar) para a dor, e vá ao serviço de saúde: a ferida infecciona.'], [18, 17, 19]),
 ('geral', 'Outros bichos (lacraia, mordida de cobra sem veneno, sapo)', ['Lave com água e sabão, compressa fria, e procure o serviço de saúde se a dor for forte ou piorar.', 'Sapo: lave a boca e os olhos com água corrente se houve contato; cachorro que mordeu sapo vai ao veterinário.'], [27, 1]),
]
NUNCA = ['Fazer torniquete ou amarrar o braço ou a perna.', 'Cortar, furar ou espremer o local.', 'Chupar o veneno.', 'Pôr folhas, pó de café, terra, álcool ou outras coisas no local.', 'Dar bebida alcoólica ou remédio por conta própria.', 'Esperar os sintomas aparecerem para ir ao médico.']
soc_html = ''.join(f'<details class="soc-bicho" id="{i}"><summary>{t}</summary><ol>{"".join(f"<li>{x}</li>" for x in passos)}</ol><p class="soc-fonte">Fontes:{"".join(fonte(k) for k in fs)}</p></details>' for i, t, passos, fs in SOC)
socorro = f'''        <section class="titulo-guia titulo-socorro">
            <div class="container">
                <h1>Picou? O que fazer</h1>
                <p>Calma, rapidez e o serviço de saúde. O soro contra o veneno só existe lá, e é de graça pelo SUS.</p>
            </div>
        </section>
        <section class="secao">
            <div class="container socorro">
                <aside class="telefones" aria-labelledby="tel-t">
                    <h2 id="tel-t">Telefones</h2>
                    <ul>
                        <li><a href="tel:192">192</a><span>SAMU</span></li>
                        <li><a href="tel:193">193</a><span>Bombeiros</span></li>
                        <li><a href="tel:08007226001">0800&nbsp;722&nbsp;6001</a><span>Disque-Intoxicação, 24 horas, grátis{fonte(10)}</span></li>
                    </ul>
                    <p class="tel-nota">O Disque-Intoxicação orienta enquanto você vai para o serviço de saúde. Tenha à mão: o bicho (ou a foto), a hora da picada e o que a pessoa está sentindo.</p>
                </aside>
                <div class="socorro-texto">
                    <section aria-labelledby="fazer-t">
                        <h2 id="fazer-t">Em qualquer picada</h2>
                        <ol class="passos"><li>Afaste a pessoa do bicho, sem tentar pegá-lo.</li><li>Lave o local com água e sabão.{fonte(2)}</li><li>Deixe a pessoa calma e quieta, com o membro picado parado.</li><li>Vá ao serviço de saúde mais perto, ou ligue 192.</li><li>Se der, leve uma foto do bicho: ajuda a escolher o soro.</li></ol>
                    </section>
                    <section aria-labelledby="nunca-t" class="nunca">
                        <h2 id="nunca-t">Nunca faça</h2>
                        <ul>{"".join(f"<li>{x}</li>" for x in NUNCA)}</ul>
                        <p class="soc-fonte">Fontes:{fonte(2)}{fonte(9)}{fonte(19)}</p>
                    </section>
                    <section aria-labelledby="bicho-t">
                        <h2 id="bicho-t">Bicho por bicho</h2>
                        {soc_html}
                    </section>
                    <section aria-labelledby="mais-t">
                        <h2 id="mais-t">Para estar pronto</h2>
                        <p class="socorro-mais"><a class="botao botao-socorro" href="emergencia.html">Fui picado: a tela da emergência</a> <a class="botao botao-claro" href="cartao.html">Cartão para o hospital</a> <a class="botao botao-claro" href="soro.html">Onde tem soro</a></p>
                    </section>
                    <p class="revisao">Texto conferido nas fontes em {REVISAO}. Ainda não passou pela leitura de um profissional de saúde.</p>
                </div>
                <a class="ligar-192" href="tel:192">Ligar&nbsp;192&nbsp;(SAMU)</a>
            </div>
        </section>
'''
pagina('socorro.html', f'Picou? O que fazer — {NOME}', 'Primeiros socorros em picadas de cobra, escorpião, aranha, lagarta, abelha, água-viva e arraia: o que fazer, o que nunca fazer e os telefones.', socorro, scripts=[JS])

# ---------------------------------------------------------------- Mitos (mitos.html): verdade ou mito, em cartões e em jogo
MITOS = [
 ('Chupar o veneno da picada ajuda.', 'mito', 'Não tira o veneno e ainda pode infeccionar o local e expor quem chupa.', [9]),
 ('Torniquete segura o veneno no braço ou na perna.', 'mito', 'Prende o veneno no lugar e piora a lesão. Não amarre nada.', [2]),
 ('Dá para saber se a coral é verdadeira pelos anéis.', 'mito', 'Nem especialista tem certeza a olho nu: trate toda cobra colorida como coral-verdadeira.', [13]),
 ('Toda cobra é venenosa.', 'mito', 'Jiboia e sucuri, por exemplo, não têm veneno: matam apertando.', [22, 24]),
 ('Galinha no quintal acaba com os escorpiões.', 'mito', 'A galinha anda de dia e o escorpião, de noite: os dois quase não se encontram.', [21]),
 ('Inseticida resolve o problema de escorpião em casa.', 'mito', 'Pode desalojar os escorpiões e espalhá-los pela casa. O que funciona é limpeza, ralos com tela e lixo fechado.', [21]),
 ('Tem planta que espanta escorpião.', 'mito', 'Não há prova científica de nenhuma planta que repila escorpiões.', [21]),
 ('A caranguejeira é a aranha mais perigosa.', 'mito', 'Ela assusta pelo tamanho, mas o veneno é fraco. As perigosas são a aranha-marrom e a armadeira.', [7, 6]),
 ('O opilião é uma aranha venenosa.', 'mito', 'Não é aranha e não tem glândulas de veneno.', [30]),
 ('A lagartixa de parede é venenosa.', 'mito', 'Não tem veneno nenhum e ainda come mosquitos e baratas.', [29]),
 ('Todo sapo espirra veneno nos olhos.', 'emparte', 'Alguns sapos da Amazônia lançam veneno quando ameaçados; o cururu comum só solta veneno quando é apertado ou mordido.', [20, 1]),
 ('Toda abelha pica.', 'mito', 'As abelhas sem ferrão, nativas do Brasil, não picam.', []),
 ('Água doce alivia a queimadura de água-viva.', 'mito', 'Faz as células dos tentáculos dispararem mais veneno. Use água do mar.', [18]),
 ('Picada de aranha-marrom dói muito na hora.', 'mito', 'Quase não dói: os sinais aparecem horas depois. Por isso, toda picada de aranha vai ao serviço de saúde.', [6]),
 ('A lagarta pode causar sangramento.', 'verdade', 'A Lonomia, uma taturana de espinhos em forma de pinheirinho, causa sangramentos. Há soro, do Butantan.', [8]),
 ('A criança picada por escorpião deve ir ao hospital mesmo sem sintomas.', 'verdade', 'Em crianças, o escorpião-amarelo pode ser grave e os sinais aparecem rápido.', [3, 4]),
 ('O soro contra veneno é pago.', 'mito', 'É de graça, pelo SUS, nos serviços de referência.', [8]),
]
ROT = {'mito': 'Mito', 'verdade': 'Verdade', 'emparte': 'Em parte'}
mitos_cartoes = ''.join(f'<li class="mito-cartao mito-{v}"><p class="mito-frase">“{f}”</p><p class="mito-veredito">{ROT[v]}</p><p>{e}{"".join(fonte(k) for k in fs)}</p></li>' for f, v, e, fs in MITOS)
mitos_json = json.dumps([{'f': f, 'v': v, 'e': e} for f, v, e, fs in MITOS], ensure_ascii=False).replace('</', '<\\/')
mitos = f'''        <section class="titulo-guia">
            <div class="container">
                <h1>Verdade ou mito?</h1>
                <p>O que todo mundo ouve falar sobre cobras, aranhas, escorpiões e companhia, conferido nas fontes. Jogue ou leia todos.</p>
            </div>
        </section>
        <section class="secao">
            <div class="container mitos">
                <section class="mito-jogo" aria-labelledby="jogo-t" hidden>
                    <h2 id="jogo-t">Jogo: verdade ou mito?</h2>
                    <p class="mito-placar"></p>
                    <p class="mito-pergunta" tabindex="-1"></p>
                    <div class="mito-botoes"><button type="button" class="botao" data-resp="verdade">Verdade</button><button type="button" class="botao" data-resp="mito">Mito</button></div>
                    <p class="mito-retorno" hidden></p>
                    <button type="button" class="botao botao-claro mito-proxima" hidden>Próxima</button>
                </section>
                <section aria-labelledby="todos-t">
                    <div class="mitos-partilha"><p>Viu um desses circulando? Mande a resposta:</p>{compartilhar("Chupar o veneno ajuda? Galinha acaba com escorpião? Veja o que é verdade e o que é mito:", "mitos.html")}</div>
                    <h2 id="todos-t">Todos os {len(MITOS)}</h2>
                    <ul class="mitos-lista">{mitos_cartoes}</ul>
                </section>
                <script type="application/json" id="mitos-dados">{mitos_json}</script>
            </div>
        </section>
'''
pagina('mitos.html', f'Verdade ou mito? — {NOME}', 'Chupar o veneno, torniquete, coral verdadeira, galinha contra escorpião, lagartixa venenosa: o que é verdade e o que é mito.', mitos, scripts=[JS])

# ================================================================ As ideias de 1/11/2026, à noite (todas pedidas)
FONTES += [
 (32, 'Ministério da Saúde. Hospitais de referência para atendimento: os Pontos Estratégicos de Soro Antiveneno (PESA), em cada estado.', 'https://www.gov.br/saude/pt-br/assuntos/saude-de-a-a-z/a/animais-peconhentos/hospitais-de-referencia/hospitais-de-referencia-para-atendimento'),
 (33, 'Ministério da Saúde. Boletim Epidemiológico, vol. 55, nº 15 (acidentes com serpentes): 342.713 acidentes com animais peçonhentos notificados em 2023 (escorpiões 58,79%, aranhas 12,85%, abelhas 9,85%, serpentes 9,51%, lagartas 2,07%, outros 5,35%) e 143 mortes por serpentes.', 'https://www.gov.br/saude/pt-br/assuntos/saude-de-a-a-z/a/animais-peconhentos/boletins-epidemiologicos/boletim-epidemiologico-volume-55-no-15'),
 (34, 'Ministério da Saúde. Boletim Epidemiológico, vol. 56, nº 5 (acidentes com escorpiões): 202.714 acidentes em 2023, 58,9% de todos os acidentes com animais peçonhentos.', 'https://www.gov.br/saude/pt-br/assuntos/saude-de-a-a-z/a/animais-peconhentos/boletins-epidemiologicos/boletim-epidemiologico-vol-56-no-5'),
 (35, 'Bahia Notícias, com dados do Instituto Butantan: os acidentes com animais peçonhentos aumentam cerca de 30% no calor e nas chuvas, sobretudo de dezembro a março.', 'https://www.bahianoticias.com.br/noticia/128364-ocorrencias-com-animais-venenosos-aumentam-30-em-periodos-de-chuva-e-calor'),
 (36, 'Tua Saúde (2026), citando o Instituto Butantan: no Sul, no Sudeste e no Centro-Oeste, os escorpiões aparecem mais de setembro a fevereiro.', 'https://www.tuasaude.com/news/2026/10/17/quais-animais-peconhentos-exigem-mais-atencao-em-cada-regiao-e-epoca-do-ano/'),
 (37, 'Petlove. Cachorro picado por cobra: os sinais (inchaço, dor, pele roxa) e o veterinário na hora.', 'https://www.petlove.com.br/dicas/cachorro-picado-por-cobra-o-que-fazer'),
 (38, 'Petscare. Sapos e cães: lavar a boca com água corrente, sem deixar engolir, e ir ao veterinário (salivação, vômito, convulsão).', 'https://www.petscare.com/pt/news/post/are-frogs-poisonous-to-dogs'),
 (39, 'Jornal de Brasília, com a Agência Brasil (2024): as aranhas são a segunda causa de acidentes, com 43.933 casos em 2023.', 'https://jornaldebrasilia.com.br/noticias/saude/picadas-de-aranhas-sao-segunda-causa-de-envenenamento-no-pais/'),
 (40, 'Petlove. Cachorro picado por escorpião: o que fazer (veterinário, sem remédio por conta própria).', 'https://www.petlove.com.br/dicas/cachorro-picado-por-escorpiao-o-que-fazer'),
 (41, 'CNN Brasil. Em 2023, 152 mortes por escorpião no Brasil (Ministério da Saúde).', 'https://www.cnnbrasil.com.br/tecnologia/todos-os-escorpioes-sao-perigosos/'),
]
SOC_DADOS = {i: {'t': t, 'passos': passos} for i, t, passos, fs in SOC}
NUNCA_CURTO = ['Torniquete ou amarrar', 'Cortar, furar ou espremer', 'Chupar o veneno', 'Pôr qualquer coisa no local', 'Bebida ou remédio por conta própria']
TEL = '<p class="emerg-tel"><a class="botao botao-socorro" href="tel:192">Ligar&nbsp;192&nbsp;(SAMU)</a><a class="botao botao-claro" href="tel:08007226001">0800&nbsp;722&nbsp;6001</a><span class="emerg-tel-nota">Disque-Intoxicação, 24 horas</span></p>'
QUAL = [('cobra', 'Cobra'), ('escorpiao', 'Escorpião'), ('aranha', 'Aranha'), ('abelha', 'Abelha, vespa ou formiga'), ('lagarta', 'Lagarta ou potó'), ('agua', 'Água-viva, caravela ou arraia'), ('geral', 'Outro bicho ou não sei')]
GUARDAR = ('<div class="guardar-guia" hidden><p class="guardar-titulo">Vai para sítio, trilha ou praia?</p>'
           '<p>Guarde o guia neste aparelho: o Socorro, o “Fui picado”, as fichas e o “Que bicho é?” funcionam sem internet.</p>'
           '<button type="button" class="botao guardar-botao">Guardar o guia</button><p class="guardar-estado" aria-live="polite"></p></div>')

# ---------------------------------------------------------------- Fui picado (emergencia.html): uma tela só, letras grandes, sem rolar à toa
emerg_json = json.dumps({'soc': SOC_DADOS}, ensure_ascii=False).replace('</', '<\\/')
qual_html = ''.join(f'<a class="emerg-qual" href="socorro.html#{i}" data-soc="{i}">{t}</a>' for i, t in QUAL)
pagina('emergencia.html', f'Fui picado: o que fazer agora — {NOME}', 'Picada de cobra, escorpião, aranha, abelha, lagarta ou água-viva: o que fazer agora, em poucos passos, e os telefones.', f'''        <section class="emergencia">
            <div class="container">
                <h1>Fui picado: o que fazer agora</h1>
                <ol class="emerg-ja">
                    <li><span><strong>Afaste-se do bicho.</strong> Não tente pegar nem matar.</span></li>
                    <li><span><strong>Lave com água e sabão.</strong> Tire anéis e relógio do braço ou da perna picada.</span></li>
                    <li><span><strong>Vá ao serviço de saúde</strong> ou ligue 192. O soro só existe lá, e é de graça.{fonte(2)}</span></li>
                </ol>
                {TEL}
                <div class="meu-hospital" hidden></div>
                <section class="emerg-bicho" aria-labelledby="qual-t">
                    <h2 id="qual-t">Que bicho foi?</h2>
                    <div class="emerg-quais">{qual_html}</div>
                    <div class="emerg-resposta" aria-live="polite" tabindex="-1"></div>
                </section>
                <section class="emerg-nunca" aria-labelledby="nun-t">
                    <h2 id="nun-t">Não faça</h2>
                    <ul>{"".join(f"<li>{x}</li>" for x in NUNCA_CURTO)}</ul>
                </section>
                <p class="emerg-mais"><a class="botao" href="cartao.html">Montar o cartão para o hospital</a> <a class="botao botao-claro" href="soro.html">Onde tem soro</a> <a class="botao botao-claro" href="identificar.html">Descobrir o bicho</a></p>
                {GUARDAR}
                <script type="application/json" id="emerg-dados">{emerg_json}</script>
            </div>
        </section>
        <a class="ligar-192" href="tel:192">Ligar&nbsp;192&nbsp;(SAMU)</a>
''', scripts=[JS])

# ---------------------------------------------------------------- Cartão para o hospital (cartao.html): o que a equipe vai perguntar, numa tela
opcoes_bicho = '<option value="">Escolha…</option>' + ''.join(f'<optgroup label="{g}">' + ''.join(f'<option>{b["n"]}</option>' for b in B if b['g'] == g) + '</optgroup>' for g in GRUPOS) + '<option>Não sei</option>'
SINTOMAS = ['Dor forte', 'Inchaço', 'Mancha roxa', 'Sangramento (gengiva, nariz, urina)', 'Vômito', 'Suor frio ou tremor', 'Falta de ar', 'Pálpebras caídas ou visão dupla', 'Tontura ou desmaio', 'Nada por enquanto']
sint_html = ''.join(f'<label class="marcar"><input type="checkbox" name="sintoma-{n}" data-sintoma value="{x}"> {x}</label>' for n, x in enumerate(SINTOMAS))
pagina('cartao.html', f'Cartão para o hospital — {NOME}', 'Anote o bicho, a hora da picada e o que a pessoa sente, e mostre a tela à equipe de saúde. Fica só neste aparelho.', f'''        <section class="titulo-guia titulo-socorro">
            <div class="container">
                <h1>Cartão para o hospital</h1>
                <p>A equipe de saúde vai perguntar o bicho, a hora e o que a pessoa sente. Anote aqui no caminho e mostre a tela. Fica só neste aparelho: nada vai para a internet.</p>
            </div>
        </section>
        <section class="secao">
            <div class="container cartao-pagina">
                <form class="cartao-form" novalidate>
                    <noscript><p>Sem JavaScript, anote num papel: o bicho (ou a foto), a hora da picada, a parte do corpo, o que a pessoa sente, a idade e se tem alergia.</p></noscript>
                    <div class="campo"><label for="c-bicho">Que bicho foi? <span class="obrig">(obrigatório)</span></label><select id="c-bicho" name="bicho" required aria-describedby="e-bicho">{opcoes_bicho}</select><p class="erro" id="e-bicho" hidden>Escolha o bicho, ou “Não sei”.</p></div>
                    <div class="campo"><label for="c-hora">Hora da picada <span class="obrig">(obrigatório)</span></label><div class="campo-linha"><input id="c-hora" name="hora" type="time" required aria-describedby="e-hora"><button type="button" class="botao botao-claro c-agora">Agora</button></div><p class="erro" id="e-hora" hidden>Diga a hora, mesmo aproximada.</p></div>
                    <div class="campo"><label for="c-parte">Parte do corpo</label><input id="c-parte" name="parte" type="text" placeholder="Ex.: pé direito" autocomplete="off"></div>
                    <div class="campo"><label for="c-onde">Onde aconteceu</label><input id="c-onde" name="onde" type="text" placeholder="Ex.: quintal de casa, Goiânia" autocomplete="off"></div>
                    <fieldset class="campo"><legend>O que a pessoa sente</legend><div class="marcas">{sint_html}</div></fieldset>
                    <div class="campo campo-dois"><div><label for="c-idade">Idade</label><input id="c-idade" name="idade" type="number" min="0" max="120" inputmode="numeric"></div><div><label for="c-peso">Peso (kg)</label><input id="c-peso" name="peso" type="number" min="1" max="300" inputmode="numeric"></div></div>
                    <div class="campo"><label for="c-alergia">Alergias e remédios que usa</label><input id="c-alergia" name="alergia" type="text" autocomplete="off"></div>
                    <div class="campo"><label class="marcar"><input type="checkbox" name="foto" value="sim"> Tenho foto do bicho no celular</label></div>
                    <p><button type="submit" class="botao botao-socorro">Mostrar o cartão</button></p>
                </form>
                <div class="cartao-hospital" hidden tabindex="-1" aria-live="polite"></div>
                <aside class="cartao-lado">
                    <p class="id-alerta-titulo">Enquanto isso</p>
                    <p>Pessoa deitada e calma, membro picado parado. Nada de torniquete, cortar ou chupar.</p>
                    <p class="id-tel"><a href="tel:192">192</a> SAMU · <a href="tel:08007226001">0800&nbsp;722&nbsp;6001</a> Disque-Intoxicação</p>
                    <div class="meu-hospital" hidden></div>
                </aside>
            </div>
        </section>
        <a class="ligar-192" href="tel:192">Ligar&nbsp;192&nbsp;(SAMU)</a>
''', scripts=[JS])

# ---------------------------------------------------------------- Onde tem soro (soro.html): como funciona e "o hospital da minha cidade"
pagina('soro.html', f'Onde tem soro contra veneno — {NOME}', 'O soro contra veneno de cobra, escorpião, aranha e lagarta fica nos hospitais de referência do SUS. Como achar o da sua cidade e guardar neste aparelho.', f'''        <section class="titulo-guia">
            <div class="container">
                <h1>Onde tem soro</h1>
                <p>O soro contra veneno não fica em farmácia nem em todo posto: fica nos hospitais de referência do SUS, os Pontos Estratégicos de Soro Antiveneno. É de graça.{fonte(32)}</p>
            </div>
        </section>
        <section class="secao">
            <div class="container soro">
                <div class="soro-texto">
                    <section aria-labelledby="ag-t"><h2 id="ag-t">Na hora do acidente</h2>
                        <p>Não perca tempo procurando a lista: vá ao pronto-socorro ou à UPA mais perto, ou ligue 192. A equipe sabe para onde levar e pede o soro se for preciso.</p></section>
                    <section aria-labelledby="an-t"><h2 id="an-t">Antes de precisar</h2>
                        <ol class="passos"><li>Abra a <a href="https://www.gov.br/saude/pt-br/assuntos/saude-de-a-a-z/a/animais-peconhentos/hospitais-de-referencia/hospitais-de-referencia-para-atendimento" rel="noopener">lista do Ministério da Saúde</a>, que tem os hospitais de cada estado.{fonte(32)}</li>
                        <li>Ache o mais perto de casa, ou do sítio, da trilha ou da praia para onde você vai.</li>
                        <li>Guarde aqui o nome, o telefone e o endereço. Eles aparecem no “Fui picado” e no cartão para o hospital, também sem internet.</li></ol></section>
                    <section aria-labelledby="dq-t"><h2 id="dq-t">Dúvida? Ligue</h2>
                        <p>O Disque-Intoxicação, <a href="tel:08007226001">0800&nbsp;722&nbsp;6001</a>, atende 24 horas, de graça, e liga você a um centro de toxicologia.{fonte(10)}</p></section>
                    {GUARDAR}
                </div>
                <form class="hospital-form" novalidate aria-labelledby="hf-t">
                    <h2 id="hf-t">O hospital da minha cidade</h2>
                    <div class="campo"><label for="h-nome">Nome do hospital <span class="obrig">(obrigatório)</span></label><input id="h-nome" name="nome" type="text" required autocomplete="off" aria-describedby="e-hnome"><p class="erro" id="e-hnome" hidden>Escreva o nome do hospital.</p></div>
                    <div class="campo"><label for="h-tel">Telefone</label><input id="h-tel" name="tel" type="tel" autocomplete="off" inputmode="tel"></div>
                    <div class="campo"><label for="h-end">Endereço</label><input id="h-end" name="end" type="text" autocomplete="off"></div>
                    <p class="hf-acoes"><button type="submit" class="botao">Guardar</button> <button type="button" class="botao botao-claro hf-apagar" hidden>Apagar</button></p>
                    <p class="hf-estado" aria-live="polite"></p>
                    <noscript><p>Para guardar, o navegador precisa de JavaScript. Anote num papel e deixe na carteira.</p></noscript>
                </form>
            </div>
        </section>
''', scripts=[JS])

# ---------------------------------------------------------------- Qual é a diferença? (diferencas.html): os pares lado a lado, com desenho, e o jogo
# os desenhos mostram só o detalhe que separa os dois; cada um tem texto ao lado, então a cor nunca é a única pista
def svg(corpo, rotulo):
    return f'<svg class="desenho" viewBox="0 0 200 120" width="200" height="120" role="img" aria-label="{rotulo}">{corpo}</svg>'
ANEIS = '<path class="d-cobra-base" d="M15 85 C55 30 95 110 135 60 S185 40 190 50"/><path class="d-anel-v" d="M15 85 C55 30 95 110 135 60 S185 40 190 50"/><path class="d-anel-p" d="M15 85 C55 30 95 110 135 60 S185 40 190 50"/>'
DESENHOS = {
 'coral': (svg(ANEIS, 'Cobra com anéis vermelhos, pretos e claros'), svg(ANEIS, 'A mesma cobra de anéis: igual a olho nu')),
 'cabeca': (svg('<path class="d-tinta" d="M0 52h70v16H0z"/><path class="d-tinta d-junta" d="M60 60 125 26 170 52 170 68 125 94Z"/><circle class="d-fundo" cx="128" cy="50" r="6"/><circle class="d-fundo" cx="152" cy="60" r="3.5"/><path class="d-seta" d="M152 56 166 14"/><text class="d-rotulo" x="134" y="12">fosseta</text>', 'Cabeça triangular bem destacada do pescoço, com a fosseta entre o olho e a narina'),
            svg('<path class="d-tinta" d="M0 42h120v36H0z"/><ellipse class="d-tinta" cx="135" cy="60" rx="45" ry="24"/><circle class="d-fundo" cx="155" cy="52" r="5"/><text class="d-rotulo" x="20" y="110">sem pescoço marcado</text>', 'Cabeça arredondada, quase da largura do corpo, sem pescoço marcado')),
 'cauda': (svg('<path class="d-traco" d="M0 60 C40 40 80 80 120 60"/><rect class="d-tinta" x="120" y="49" width="14" height="22" rx="5"/><rect class="d-tinta" x="137" y="51" width="13" height="18" rx="5"/><rect class="d-tinta" x="153" y="53" width="12" height="14" rx="5"/><rect class="d-tinta" x="168" y="55" width="10" height="10" rx="4"/><text class="d-rotulo" x="118" y="100">chocalho</text>', 'Cauda que termina num chocalho de anéis'),
           svg('<path class="d-traco-fino" d="M0 60 C40 40 80 80 120 60 S170 50 190 56"/><text class="d-rotulo" x="100" y="100">cauda fina</text>', 'Cauda fina, que termina em ponta')),
 'aranha': (svg('<g class="d-pernas"><path d="M80 55 50 25 20 40M80 60 40 45 10 65M80 65 40 75 15 100M85 70 60 100 40 115M120 55 150 25 180 40M120 60 160 45 190 65M120 65 160 75 185 100M115 70 140 100 160 115"/></g><ellipse class="d-tinta" cx="100" cy="60" rx="24" ry="18"/><ellipse class="d-tinta" cx="100" cy="98" rx="20" ry="17"/><path class="d-fundo" d="M100 48c-6 0-9 5-6 9 2 3 2 6 0 9h12c-2-3-2-6 0-9 3-4 0-9-6-9z"/><text class="d-rotulo" x="132" y="116">duas partes</text>', 'Aranha com o corpo em duas partes e a mancha de violino'),
            svg('<g class="d-pernas"><path d="M100 70 60 20 20 60M100 70 70 15 30 30M100 70 130 15 170 30M100 70 140 20 185 60M100 70 55 95 15 118M100 70 75 110 55 118M100 70 125 110 145 118M100 70 150 95 190 118"/></g><circle class="d-tinta" cx="100" cy="70" r="16"/><text class="d-rotulo" x="4" y="12">uma peça só</text>', 'Opilião: corpo redondo de uma peça só e pernas muito longas')),
 'escorpiao': (svg('<path class="d-amarelo" d="M30 70h70v18H30z"/><path class="d-amarelo-escuro" d="M45 72h40v14H45z"/><path class="d-amarelo-traco" d="M100 79 C130 79 150 70 150 50 C150 30 130 22 118 32"/><path class="d-dentes" d="M135 66l4-5 4 5 4-5 4 5"/><text class="d-rotulo" x="140" y="100">serrinha</text>', 'Escorpião amarelo-claro, com o tronco escuro e uma serrinha na cauda'),
               svg('<path class="d-marrom" d="M30 70h70v18H30z"/><path class="d-marrom-traco" d="M100 79 C130 79 150 70 150 50 C150 30 130 22 118 32"/><text class="d-rotulo" x="120" y="100">sem serrinha</text>', 'Escorpião marrom-escuro, sem serrinha na cauda')),
 'vespa': (svg('<circle class="d-tinta" cx="40" cy="60" r="13"/><ellipse class="d-tinta" cx="72" cy="60" rx="18" ry="13"/><path class="d-traco-fino" d="M90 60h22"/><ellipse class="d-tinta" cx="140" cy="60" rx="30" ry="15"/><text class="d-rotulo" x="78" y="100">cintura fina</text>', 'Vespa: corpo liso, com a cintura bem fina'),
           svg('<circle class="d-tinta" cx="45" cy="60" r="14"/><ellipse class="d-tinta" cx="80" cy="60" rx="22" ry="18"/><ellipse class="d-tinta" cx="125" cy="60" rx="28" ry="20"/><g class="d-pelos"><path d="M70 40l-3-6M80 39v-7M90 40l3-6M115 39l-2-6M125 38v-7M135 39l3-6M70 80l-3 6M80 81v7M90 80l3 6M115 81l-2 6M125 82v7M135 81l3 6"/></g><text class="d-rotulo" x="60" y="112">peluda, cintura grossa</text>', 'Abelha: peluda, sem cintura fina')),
 'lagarta': (svg('<rect class="d-tinta" x="20" y="60" width="160" height="26" rx="13"/><g class="d-pelos"><path d="M40 60v-20m0 8-8-8m8 8 8-8M70 60v-20m0 8-8-8m8 8 8-8M100 60v-20m0 8-8-8m8 8 8-8M130 60v-20m0 8-8-8m8 8 8-8M160 60v-20m0 8-8-8m8 8 8-8"/></g><text class="d-rotulo" x="20" y="110">espinhos como pinheirinhos</text>', 'Lonomia: espinhos ramificados como pinheirinhos'),
            svg('<rect class="d-tinta" x="20" y="60" width="160" height="26" rx="13"/><g class="d-pelos"><path d="M35 60l-4-16M50 60v-18M65 60l4-16M80 60l-4-16M95 60v-18M110 60l4-16M125 60l-4-16M140 60v-18M155 60l4-16M170 60l4-14"/></g><text class="d-rotulo" x="20" y="110">pelos simples</text>', 'Outra lagarta, de pelos simples')),
}
DIFS = [
 ('coral', 'falsa-coral', 'Anéis vermelhos, pretos e brancos ou amarelos', 'Os mesmos anéis; às vezes não dão a volta no corpo', 'coral', 'Não dá para separar a olho nu: trate as duas como coral-verdadeira e afaste-se.', [13]),
 ('jararaca', 'jiboia', 'Cabeça triangular, a fosseta entre o olho e a narina, desenhos em V', 'Corpo grosso, desenhos de sela, cabeça sem pescoço marcado', 'cabeca', 'A jararaca é peçonhenta; a jiboia não tem veneno.', [11, 22]),
 ('cascavel', 'jararaca', 'Chocalho na ponta da cauda e losangos claros', 'Cauda fina, sem chocalho', 'cauda', 'As duas são perigosas: o chocalho só ajuda a saber qual soro.', [23]),
 ('aranha-marrom', 'opiliao', 'Corpo em duas partes, com cintura, e a mancha de violino', 'Corpo de uma peça só, redondo, e pernas muito finas', 'aranha', 'A aranha-marrom pode ser grave; o opilião não tem veneno.', [6, 30]),
 ('escorpiao-amarelo', 'escorpiao-marrom', 'Amarelo-claro, com o tronco escuro e a serrinha na cauda', 'Marrom-escuro, sem serrinha', 'escorpiao', 'Os dois picam; o amarelo é o mais perigoso, sobretudo para crianças.', [4, 5]),
 ('vespa', 'abelha-africanizada', 'Lisa, de cintura bem fina; pica várias vezes', 'Peluda, de cintura grossa; deixa o ferrão', 'vespa', 'As duas picam; com muitas picadas ou alergia, é emergência.', [25, 14]),
 ('taturana', 'lagarta-urticante', 'Espinhos ramificados como pinheirinhos, em grupo no tronco', 'Pelos ou espinhos simples', 'lagarta', 'Na dúvida, trate qualquer lagarta de fogo como Lonomia.', [8, 9]),
 ('armadeira', 'caranguejeira', 'Média, pouco peluda; levanta as patas da frente', 'Muito grande e peluda; anda devagar', None, 'A armadeira dói muito e pode ser grave em crianças; o veneno da caranguejeira é fraco.', [6, 7]),
 ('abelha-africanizada', 'abelha-sem-ferrao', 'Peluda, de uns 1,5 cm; pica e deixa o ferrão', 'Pequena; não pica', None, 'A africanizada pica; a sem ferrão, nativa do Brasil, não.', [14]),
]
def lado(i, traco, d):
    b = POR_ID[i]
    return f'<div class="dif-lado">{d}<p class="dif-nome"><a href="bicho-{i}.html">{b["n"]}</a></p>{selo(b)}<p>{traco}</p></div>'
dif_html = ''.join(f'<li class="dif"><div class="dif-par">{lado(a, ta, DESENHOS[d][0] if d else "")}<span class="dif-x" aria-hidden="true">{"=" if d == "coral" else "×"}</span>{lado(b, tb, DESENHOS[d][1] if d else "")}</div><p class="dif-conclusao">{c}{"".join(fonte(k) for k in fs)}</p></li>' for a, b, ta, tb, d, c, fs in DIFS)
dif_json = json.dumps([{'a': POR_ID[a]['n'], 'b': POR_ID[b]['n'], 'ta': ta, 'tb': tb, 'c': c} for a, b, ta, tb, d, c, fs in DIFS if d != 'coral'], ensure_ascii=False).replace('</', '<\\/')
pagina('diferencas.html', f'Qual é a diferença? — {NOME}', 'Coral e falsa-coral, jararaca e jiboia, aranha-marrom e opilião, abelha e vespa: o detalhe que separa os bichos parecidos, desenhado, e um jogo.', f'''        <section class="titulo-guia">
            <div class="container">
                <h1>Qual é a diferença?</h1>
                <p>Bichos parecidos, lado a lado, com o detalhe que separa um do outro desenhado. Depois, teste no jogo.</p>
            </div>
        </section>
        <section class="secao">
            <div class="container diferencas">
                <section class="dif-jogo jogo-caixa" aria-labelledby="dj-t" hidden>
                    <h2 id="dj-t">Jogo: qual dos dois?</h2>
                    <p class="jogo-placar"></p>
                    <p class="jogo-pergunta" tabindex="-1"></p>
                    <div class="jogo-botoes"></div>
                    <p class="jogo-retorno" hidden></p>
                    <button type="button" class="botao botao-claro jogo-proxima" hidden>Próxima</button>
                </section>
                <ul class="dif-lista">{dif_html}</ul>
                <script type="application/json" id="dif-dados">{dif_json}</script>
            </div>
        </section>
''', scripts=[JS])

# ---------------------------------------------------------------- Prevenir (prevenir.html): a casa, as crianças, os bichos de estimação e a época
CASA = [
 ('Ralos com tela ou tampa, e tampados à noite', [3, 21]), ('Lixo bem fechado (atrai baratas, a comida do escorpião)', [3, 21]),
 ('Nada de entulho, tijolo, telha ou lenha encostados na casa', [3]), ('Quintal limpo e grama aparada', [3]),
 ('Frestas, rodapés e portas vedados (rolinho ou borracha embaixo da porta)', [3]), ('Roupas, toalhas e sapatos sacudidos antes de usar', [3]),
 ('Camas e berços afastados da parede, sem lençol arrastando no chão', [3]), ('Móveis afastados da parede e atrás dos quadros limpo de vez em quando', [6]),
 ('Telas nas janelas (potó e outros insetos que vêm à luz)', [16]), ('Luvas e botas para mexer em entulho, lenha ou jardim', [3]),
]
casa_html = ''.join(f'<li><label class="marcar"><input type="checkbox" data-casa="{n}"> {t}</label></li>' for n, (t, fs) in enumerate(CASA))
casa_fontes = ''.join(fonte(k) for k in sorted({k for t, fs in CASA for k in fs}))
MESES = ['jan', 'fev', 'mar', 'abr', 'mai', 'jun', 'jul', 'ago', 'set', 'out', 'nov', 'dez']
EPOCA = [('Todos os bichos peçonhentos', 'Cerca de 30% mais acidentes no calor e na chuva.', [12, 1, 2, 3], [35]),
         ('Escorpiões (Sul, Sudeste e Centro-Oeste)', 'Aparecem mais quando esquenta; a chuva os tira dos esconderijos.', [9, 10, 11, 12, 1, 2], [36])]
def linha_epoca(t, e, ms, fs):
    cel = ''.join(f'<span class="mes{" mes-sim" if i + 1 in ms else ""}" data-mes="{i + 1}"><span class="mes-nome">{m}</span><span class="vh">{": mais" if i + 1 in ms else ""}</span></span>' for i, m in enumerate(MESES))
    return f'<li class="epoca"><p class="epoca-t">{t}</p><div class="meses">{cel}</div><p class="epoca-e">{e}{"".join(fonte(k) for k in fs)}</p></li>'
epoca_html = ''.join(linha_epoca(*x) for x in EPOCA)
pagina('prevenir.html', f'Prevenir: a casa, as crianças, cães e gatos — {NOME}', 'Sua casa está segura contra escorpiões e aranhas? Um teste de 10 itens, os cuidados com crianças, cães e gatos, e a época de cada bicho.', f'''        <section class="titulo-guia">
            <div class="container">
                <h1>Prevenir</h1>
                <p>O bicho que mais pica no Brasil, o escorpião, vive dentro e perto das casas.{fonte(4)} Veja se a sua casa está segura, os cuidados com as crianças e com os bichos de estimação, e a época de cada bicho.</p>
            </div>
        </section>
        <section class="secao">
            <div class="container prevenir">
                <nav class="indice-pagina" aria-label="Nesta página"><a href="#casa-t">Minha casa está segura?</a><a href="#cri-t">Crianças</a><a href="#pet-t">Cães e gatos</a><a href="#epo-t">A época</a></nav>
                <div class="prevenir-texto">
                    <section class="casa" aria-labelledby="casa-t">
                        <h2 id="casa-t">Minha casa está segura?</h2>
                        <p>Marque o que já faz. Fica guardado neste aparelho.</p>
                        <ul class="casa-lista">{casa_html}</ul>
                        <p class="casa-nota" aria-live="polite"><strong class="casa-n">0</strong> de {len(CASA)}</p>
                        <div class="casa-barra" aria-hidden="true"><span></span></div>
                        <p class="soc-fonte">Fontes:{casa_fontes}</p>
                    </section>
                    <section aria-labelledby="cri-t">
                        <h2 id="cri-t">Crianças</h2>
                        <ul class="lista">
                            <li>Criança picada por escorpião vai direto ao serviço de saúde, sem esperar sintomas: nela, o veneno age mais rápido.{fonte(3)}{fonte(4)}</li>
                            <li>A picada da armadeira também pode ser grave em crianças.{fonte(6)}</li>
                            <li>Ensine a não pegar bicho nenhum, nem os bonitos: a coral é colorida, e a lagarta de fogo parece um brinquedo.{fonte(13)}{fonte(9)}</li>
                            <li>Berço longe da parede e sapatos sacudidos antes de calçar.{fonte(3)}</li>
                            <li>Na escola: veja a <a href="escola.html">versão para a escola</a>, com atividades e um cartaz.</li>
                        </ul>
                    </section>
                    <section aria-labelledby="pet-t">
                        <h2 id="pet-t">Cães e gatos</h2>
                        <ul class="lista">
                            <li><strong>Picado por cobra:</strong> muitas vezes ninguém vê a picada. Inchaço no focinho, no pescoço ou na pata, dor e pele roxa são sinais: veterinário na hora, sem remédio caseiro.{fonte(37)}</li>
                            <li><strong>Mordeu um sapo:</strong> lave a boca com água corrente, da frente para trás, sem deixar engolir, e vá ao veterinário. Baba, vômito e tremor são sinais.{fonte(38)}</li>
                            <li><strong>Picado por escorpião:</strong> veterinário, sem dar remédio por conta própria.{fonte(40)}</li>
                            <li>Com gatos vale o mesmo: veterinário, sem remédio caseiro. À noite, deixe cães e gatos longe dos sapos.</li>
                        </ul>
                    </section>
                    <section aria-labelledby="epo-t">
                        <h2 id="epo-t">A época de cada bicho</h2>
                        <p class="epoca-agora" aria-live="polite"></p>
                        <ul class="epocas">{epoca_html}</ul>
                        <ul class="lista">
                            <li><strong>Potó:</strong> mais na época das chuvas, quando voa até as lâmpadas.{fonte(16)}</li>
                            <li><strong>Arraia:</strong> mais na seca, quando a água do rio baixa e as praias aparecem.{fonte(19)}</li>
                        </ul>
                    </section>
                </div>
            </div>
        </section>
''', scripts=[JS])

# ---------------------------------------------------------------- Os números (numeros.html): 2023, Ministério da Saúde
NUM = [('Escorpiões', 58.79), ('Aranhas', 12.85), ('Abelhas', 9.85), ('Serpentes', 9.51), ('Outros', 5.35), ('Lagartas', 2.07)]
def br(x, c=1): return f'{x:.{c}f}'.replace('.', ',')
barras = ''.join(f'<tr><th scope="row">{t}</th><td><span class="barra"><span class="barra-v" data-v="{v}"></span></span></td><td class="num">{br(v)}%</td></tr>' for t, v in NUM)
pagina('numeros.html', f'Os números das picadas no Brasil — {NOME}', 'Em 2023, 342 mil acidentes com animais peçonhentos no Brasil: mais da metade com escorpiões. Os números do Ministério da Saúde.', f'''        <section class="titulo-guia">
            <div class="container">
                <h1>Os números do Brasil</h1>
                <p>Quantas picadas acontecem por ano, e de quais bichos. Dados de 2023 do Ministério da Saúde, os mais novos publicados.</p>
            </div>
        </section>
        <section class="secao">
            <div class="container numeros">
                <div class="numeros-destaques">
                    <p class="destaque-num"><strong>342 mil</strong><span>acidentes com animais peçonhentos notificados em 2023{fonte(33)}</span></p>
                    <p class="destaque-num"><strong>202 mil</strong><span>só com escorpiões: mais da metade{fonte(34)}</span></p>
                    <p class="destaque-num"><strong>152</strong><span>mortes por escorpião em 2023{fonte(41)}</span></p>
                    <p class="destaque-num"><strong>143</strong><span>mortes por cobra em 2023{fonte(33)}</span></p>
                </div>
                <figure class="grafico">
                    <figcaption><strong>De que bicho foram os acidentes</strong> (2023, em % dos notificados){fonte(33)}</figcaption>
                    <table class="tabela-barras"><thead><tr><th scope="col">Bicho</th><th scope="col"><span class="vh">Barra</span></th><th scope="col">%</th></tr></thead><tbody>{barras}</tbody></table>
                    <p class="nota-grafico">Os outros 1,6% não tinham o tipo de bicho anotado. Os totais mudam um pouco a cada atualização do banco do SUS (outro boletim do mesmo ano dá 344.138).</p>
                </figure>
                <div class="numeros-texto">
                    <h2>O que os números dizem</h2>
                    <ul class="lista">
                        <li><strong>O escorpião é o que mais pica</strong>, e em 2023 matou mais que as cobras.{fonte(34)}{fonte(41)} O escorpião-amarelo vive nas cidades, em ralos, esgoto e entulho: por isso vale o <a href="prevenir.html">teste da casa</a>.{fonte(4)}</li>
                        <li><strong>As aranhas vêm em segundo</strong>, com 43.933 casos.{fonte(39)}</li>
                        <li><strong>A cobra pica menos, mas pesa:</strong> sem soro, a picada de jararaca ou cascavel pode matar ou deixar sequela.{fonte(2)}</li>
                        <li>Os acidentes sobem no calor e na chuva, de dezembro a março.{fonte(35)} Veja <a href="prevenir.html#epo-t">a época de cada bicho</a>.</li>
                    </ul>
                </div>
            </div>
        </section>
''', scripts=[JS])

# ---------------------------------------------------------------- O jogo "Pica ou não pica?" (jogo.html)
jogo_json = json.dumps([{'id': b['id'], 'n': b['n'], 'g': b['g'], 'cuidado': b['p'] != 'nenhum', 'pica': b['pica'], 'r': b['r']} for b in B], ensure_ascii=False).replace('</', '<\\/')
pagina('jogo.html', f'Jogo: pica ou não pica? — {NOME}', 'Aparece o bicho; você tem seis segundos para dizer se é de ter cuidado ou se não tem perigo. Dez rodadas e o seu recorde.', f'''        <section class="titulo-guia">
            <div class="container">
                <h1>Pica ou não pica?</h1>
                <p>Aparece um bicho: é de ter cuidado ou não tem perigo? Dez rodadas, seis segundos cada.</p>
            </div>
        </section>
        <section class="secao">
            <div class="container jogo-pagina">
                <section class="pica-jogo jogo-caixa" aria-labelledby="pj-t" hidden>
                    <h2 id="pj-t" class="vh">O jogo</h2>
                    <p class="jogo-placar"></p>
                    <div class="tempo" aria-hidden="true"><span></span></div>
                    <p class="jogo-grupo"></p>
                    <p class="jogo-pergunta jogo-bicho" tabindex="-1"></p>
                    <div class="jogo-botoes"><button type="button" class="botao botao-socorro" data-resp="sim">Cuidado!</button><button type="button" class="botao" data-resp="nao">Sem perigo</button></div>
                    <p class="jogo-retorno" hidden></p>
                    <button type="button" class="botao botao-claro jogo-proxima" hidden>Próxima</button>
                    <label class="marcar sem-tempo"><input type="checkbox" class="sem-tempo-caixa"> Sem limite de tempo</label>
                </section>
                <noscript><p>O jogo precisa de JavaScript. Veja <a href="bichos.html">todos os bichos</a>.</p></noscript>
                <aside class="jogo-lado">
                    <h2>Como funciona</h2>
                    <p><strong>Cuidado!</strong> vale para quem pica, queima ou é venenoso, do perigoso ao que só incomoda. <strong>Sem perigo</strong> é para os que não picam ou não têm veneno.</p>
                    <p>Mais jogos: <a href="mitos.html">Verdade ou mito?</a> e <a href="diferencas.html">Qual é a diferença?</a></p>
                </aside>
                <script type="application/json" id="jogo-dados">{jogo_json}</script>
            </div>
        </section>
''', scripts=[JS])

# ---------------------------------------------------------------- Para a escola (escola.html): plano de aula, atividades e cartaz, para imprimir
ATIV = ['jararaca', 'lagartixa', 'escorpiao-amarelo', 'opiliao', 'abelha-sem-ferrao', 'aranha-marrom', 'jiboia', 'taturana', 'sapo-cururu', 'agua-viva']
ativ1 = ''.join(f'<tr><td>{POR_ID[i]["n"]}</td><td class="caixinha" aria-label="Cuidado"></td><td class="caixinha" aria-label="Sem perigo"></td></tr>' for i in ATIV)
gab1 = ', '.join(f'{POR_ID[i]["n"]}: {"cuidado" if POR_ID[i]["p"] != "nenhum" else "sem perigo"}' for i in ATIV)
ESC_MITOS = [m for m in MITOS if m[0] in ('Chupar o veneno da picada ajuda.', 'Toda cobra é venenosa.', 'Galinha no quintal acaba com os escorpiões.', 'A lagartixa de parede é venenosa.', 'A lagarta pode causar sangramento.', 'Toda abelha pica.')]
ativ2 = ''.join(f'<li>{f} <span class="vm">( ) Verdade &nbsp; ( ) Mito</span></li>' for f, v, e, fs in ESC_MITOS)
gab2 = ' '.join(f'{n + 1}. {ROT[v]}.' for n, (f, v, e, fs) in enumerate(ESC_MITOS))
pagina('escola.html', f'Para a escola — {NOME}', 'Plano de aula, atividades para imprimir e um cartaz de primeiros socorros sobre os bichos que picam, para o Ensino Fundamental.', f'''        <section class="titulo-guia nao-imprimir">
            <div class="container">
                <h1>Para a escola</h1>
                <p>Um plano de aula de 50 minutos, duas atividades e um cartaz de primeiros socorros, prontos para imprimir. Pensado para o Ensino Fundamental, a partir do 3º ano.</p>
                <p><button type="button" class="botao imprimir" hidden>Imprimir tudo</button></p>
            </div>
        </section>
        <section class="secao">
            <div class="container escola">
                <nav class="indice-pagina nao-imprimir" aria-label="Nesta página"><a href="#plano-t">Plano de aula</a><a href="#a1-t">Atividade 1</a><a href="#a2-t">Atividade 2</a><a href="#cartaz-t">Cartaz</a><a href="#gab-t">Respostas</a></nav>
                <div class="escola-folhas">
                    <section class="folha" aria-labelledby="plano-t">
                        <h2 id="plano-t">Plano de aula: pica ou não pica? (50 minutos)</h2>
                        <p><strong>Objetivos:</strong> diferenciar bicho peçonhento de venenoso; reconhecer os bichos perigosos da região; saber o que fazer, e o que não fazer, se alguém for picado.</p>
                        <ol class="passos">
                            <li><strong>Conversa (10 min):</strong> quem já viu um escorpião, uma cobra ou uma taturana? O que fizeram? Anote no quadro as ideias, sem corrigir ainda.</li>
                            <li><strong>Peçonhento × venenoso (10 min):</strong> o peçonhento injeta a toxina (ferrão, presas); o venenoso só faz mal se for mordido ou apertado (o sapo).{fonte(1)}</li>
                            <li><strong>Atividade 1 (10 min):</strong> pica ou não pica? Depois, conferir no <a href="jogo.html">jogo do site</a>, no projetor.</li>
                            <li><strong>Atividade 2 (10 min):</strong> verdade ou mito, voltando às ideias anotadas no começo.</li>
                            <li><strong>O que fazer (10 min):</strong> ler juntos o cartaz e combinar onde ele fica na escola. Telefone: 192.</li>
                        </ol>
                        <p><strong>Para ir além:</strong> “Qual é a diferença?” no site; uma volta pela escola procurando ralos sem tela e entulho (o <a href="prevenir.html">teste da casa</a> serve para a escola).</p>
                    </section>
                    <section class="folha" aria-labelledby="a1-t">
                        <h2 id="a1-t">Atividade 1: pica ou não pica?</h2>
                        <p>Nome: ______________________________ Turma: ______</p>
                        <p>Marque com um X: é de ter cuidado (pica, queima ou é venenoso) ou não tem perigo?</p>
                        <table class="tabela-ativ"><thead><tr><th scope="col">Bicho</th><th scope="col">Cuidado</th><th scope="col">Sem perigo</th></tr></thead><tbody>{ativ1}</tbody></table>
                    </section>
                    <section class="folha" aria-labelledby="a2-t">
                        <h2 id="a2-t">Atividade 2: verdade ou mito?</h2>
                        <p>Nome: ______________________________ Turma: ______</p>
                        <ol class="ativ-mitos">{ativ2}</ol>
                        <p>Desenhe um lugar da sua casa ou da escola onde um escorpião poderia se esconder:</p>
                        <div class="espaco-desenho" aria-hidden="true"></div>
                    </section>
                    <section class="folha cartaz" aria-labelledby="cartaz-t">
                        <h2 id="cartaz-t">Picou? O que fazer</h2>
                        <ol class="cartaz-passos"><li>Afaste-se do bicho.</li><li>Lave com água e sabão.</li><li>Fique calmo e parado.</li><li>Vá ao serviço de saúde ou ligue <strong>192</strong>.</li></ol>
                        <p class="cartaz-nunca"><strong>Nunca:</strong> amarrar, cortar, chupar ou pôr nada no local.</p>
                        <p class="cartaz-rodape">{NOME} · {URL_SITE.replace("https://", "").rstrip("/")}</p>
                    </section>
                    <section class="folha" aria-labelledby="gab-t">
                        <h2 id="gab-t">Respostas (para o professor)</h2>
                        <p><strong>Atividade 1:</strong> {gab1}.</p>
                        <p><strong>Atividade 2:</strong> {gab2} As explicações estão em <a href="mitos.html">Verdade ou mito?</a></p>
                    </section>
                </div>
            </div>
        </section>
''', scripts=[JS])

# ---------------------------------------------------------------- Aprender (aprender.html): a porta dos jogos, da prevenção, dos números e da escola
APR = [('jogo.html', 'Pica ou não pica?', 'O jogo: seis segundos para cada bicho.', 'apr-jogo'), ('mitos.html', 'Verdade ou mito?', f'{len(MITOS)} coisas que todo mundo ouve, conferidas.', ''),
       ('diferencas.html', 'Qual é a diferença?', 'Coral e falsa-coral, abelha e vespa: o detalhe, desenhado.', ''), ('prevenir.html', 'Prevenir', 'O teste da casa, as crianças, cães e gatos, a época.', 'apr-prevenir'),
       ('numeros.html', 'Os números do Brasil', '342 mil acidentes em 2023: de quais bichos.', ''), ('escola.html', 'Para a escola', 'Plano de aula, atividades e cartaz para imprimir.', '')]
pagina('aprender.html', f'Aprender — {NOME}', 'Jogos, mitos, as diferenças entre bichos parecidos, como prevenir, os números do Brasil e material para a escola.', f'''        <section class="titulo-guia">
            <div class="container">
                <h1>Aprender</h1>
                <p>Para saber antes de precisar: jogos, mitos, os bichos parecidos, a prevenção em casa, os números e material para a escola.</p>
            </div>
        </section>
        <section class="secao">
            <div class="container">
                <ul class="aprender-lista">{"".join(f'<li><a class="porta-guia {c}" href="{h}"><strong>{t}</strong><span>{d}</span></a></li>' for h, t, d, c in APR)}</ul>
            </div>
        </section>
''')

# ---------------------------------------------------------------- Fontes
lista = ''.join(f'<li id="f{n}"><span class="fonte-numero">{n}</span> {t} <a href="{u}" rel="noopener">Abrir a fonte</a></li>' for n, t, u in FONTES)
pagina('fontes.html', f'Fontes — {NOME}', 'As fontes do guia: Ministério da Saúde, Instituto Butantan, secretarias de saúde e revistas científicas.',
       f'''        <section class="titulo-guia"><div class="container"><h1>Fontes</h1><p>De onde vem cada informação deste guia. Os números aparecem nos textos, ao lado de cada afirmação.</p></div></section>
        <section class="secao"><div class="container"><ol class="fontes-lista">{lista}</ol></div></section>
''')

# ---------------------------------------------------------------- A inicial e o menu em português (nas outras línguas, o site das Abelhas, como estava)
perigosos = [b for b in B if b['p'] == 'alto']
cartoes_perigo = ''.join(cartao(b) for b in perigosos)
inicial = f'''{{{{?pt-BR}}}}        <section class="abertura-guia">
            <div class="container">
                <h1>Pica ou não pica?</h1>
                <p>O guia para reconhecer os bichos do Brasil que picam, queimam ou só levam a fama: cobras, escorpiões, aranhas, abelhas, lagartas e bichos da água. E o que fazer se picar.</p>
                <div class="portas-guia">
                    <a class="porta-guia porta-identificar" href="identificar.html"><strong>Que bicho é esse?</strong><span>Responda algumas perguntas e descubra.</span></a>
                    <a class="porta-guia porta-socorro" href="socorro.html"><strong>Picou? O que fazer</strong><span>Os primeiros passos e os telefones.</span></a>
                    <a class="porta-guia" href="bichos.html"><strong>Todos os bichos</strong><span>{len(B)} bichos, do perigoso ao inofensivo.</span></a>
                    <a class="porta-guia" href="aprender.html"><strong>Aprender</strong><span>Jogos, mitos, prevenção e material para a escola.</span></a>
                </div>
            </div>
        </section>
        <section class="secao">
            <div class="container">
                <h2>Venenoso ou peçonhento?</h2>
                <div class="dois">
                    <div class="conceito"><p class="conceito-nome">Peçonhento</p><p>Produz a toxina e tem como injetar: ferrão, presas, quelíceras. Cobras, escorpiões, aranhas, abelhas.{fonte(1)}</p></div>
                    <div class="conceito"><p class="conceito-nome">Venenoso</p><p>Tem a toxina, mas não injeta: o perigo é para quem morde, aperta ou põe na boca. O sapo é o exemplo clássico.{fonte(1)}</p></div>
                </div>
            </div>
        </section>
        <section class="secao secao-clara">
            <div class="container">
                <h2>Os mais perigosos</h2>
                <p>Se picar, é serviço de saúde na hora.</p>
                <ul class="bichos-lista bichos-faixa">{cartoes_perigo}</ul>
                <p><a href="bichos.html">Ver todos os {len(B)} bichos</a></p>
            </div>
        </section>
        <section class="secao">
            <div class="container">
                <h2>Onde você está?</h2>
                <p>Os bichos que aparecem em cada lugar.</p>
                <ul class="atalhos-lugar">{"".join(f'<li><a class="chip" href="bichos.html?lugar={k}">{v}</a></li>' for k, v in LUGARES)}</ul>
                {GUARDAR}
            </div>
        </section>
        <section class="secao secao-clara">
            <div class="container">
                <h2>Para saber antes de precisar</h2>
                <ul class="aprender-lista">{"".join(f'<li><a class="porta-guia {c}" href="{h}"><strong>{t}</strong><span>{d}</span></a></li>' for h, t, d, c in APR)}</ul>
            </div>
        </section>
        <section class="secao">
            <div class="container abelhas-chamada">
                <div>
                    <h2>E as abelhas sem ferrão?</h2>
                    <p>Nem toda abelha pica. As abelhas nativas do Brasil, como a jataí, não têm ferrão que funcione, polinizam as plantas e fazem um mel especial. Este guia nasceu delas.</p>
                    <p><a class="botao" href="descobrir.html">Descobrir em 3 minutos</a> <a class="botao botao-claro" href="achei-um-ninho.html">Achei um ninho!</a></p>
                </div>
                <img src="{{{{raiz}}}}img/jatai.jpg" alt="Abelha jataí sobre uma flor branca" width="1000" height="667" loading="lazy">
            </div>
        </section>
{{{{/pt-BR}}}}'''
for f in COMPARTILHADAS:
    q = M / f; t = q.read_text()
    # tira o que uma rodada anterior pôs, para poder rodar de novo
    t = re.sub(r'\{\{\?pt-BR\}\}.*?\{\{/pt-BR\}\}', '', t, flags=re.S)
    t = re.sub(r'\{\{!pt-BR\}\}(.*?)\{\{/!pt-BR\}\}', r'\1', t, flags=re.S)
    t = re.sub(r'(<a class="marca" href="index.html">.*?</a>)', lambda m: '{{!pt-BR}}' + m.group(1) + '{{/!pt-BR}}{{?pt-BR}}' + f'<a class="marca" href="index.html">{MARCA_PT}</a>' + '{{/pt-BR}}', t, count=1, flags=re.S)
    t = re.sub(r'(<ul class="menu">.*?</ul>)', lambda m: '{{!pt-BR}}' + m.group(1) + '{{/!pt-BR}}{{?pt-BR}}' + menu_pt(f) + '{{/pt-BR}}', t, count=1, flags=re.S)
    t = t.replace('</nav>', '</nav>{{?pt-BR}}' + fui_picado(f) + '{{/pt-BR}}', 1)
    t = t.replace('{{alternativas}}', '{{?pt-BR}}    ' + CAB_OFF + '\n{{/pt-BR}}{{alternativas}}', 1)
    if f == 'index.html':
        t = re.sub(r'(<title>.*?</title>)', lambda m: '{{!pt-BR}}' + m.group(1) + '{{/!pt-BR}}{{?pt-BR}}' + f'<title>{NOME} — o guia dos bichos que picam</title>' + '{{/pt-BR}}', t, count=1)
        t = re.sub(r'(<meta name="description" content="[^"]*">)', lambda m: '{{!pt-BR}}' + m.group(1) + '{{/!pt-BR}}{{?pt-BR}}<meta name="description" content="Reconheça os bichos do Brasil que picam e os que não picam: cobras, escorpiões, aranhas, abelhas, lagartas. E o que fazer se picar.">{{/pt-BR}}', t, count=1)
        t = re.sub(r'(    <main id="conteudo">\n)(.*?)(    </main>)', lambda m: m.group(1) + '{{!pt-BR}}' + m.group(2) + '{{/!pt-BR}}' + inicial + '\n' + m.group(3), t, count=1, flags=re.S)
        t = t.replace('{{alternativas}}', '{{?pt-BR}}    <script src="{{raiz}}js/' + JS + '" defer></script>\n{{/pt-BR}}{{alternativas}}', 1)
    # o rodapé em português ganha os links do guia
    t = re.sub(r'(\{\{idiomas\}\}\s*)(.*?)(\s*</div>\s*</footer>)', lambda m: m.group(1) + '{{?pt-BR}}' + RODAPE_PT + '{{/pt-BR}}{{!pt-BR}}' + m.group(2) + '{{/!pt-BR}}' + m.group(3), t, count=1, flags=re.S)
    q.write_text(t)

(AQUI / 'so-pt.json').write_text(json.dumps(so_pt, ensure_ascii=False, indent=2) + '\n')
print(f'{NOME}: {len(B)} bichos, {len(so_pt)} páginas só em português, {len(FONTES)} fontes')

# ================================================================ As imagens de compartilhar (1200 × 630) e os ícones do app
from PIL import Image, ImageDraw, ImageFont
F_TIT = '/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf'
F_TXT = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
F_NEG = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
COR = {'alto': ('#9B2C1F', '#FFFFFF'), 'medio': ('#E9A23B', '#2E2A1F'), 'baixo': ('#FBE3B8', '#2E2A1F'), 'nenhum': ('#3F6B3A', '#FFFFFF')}
def quebrar(d, texto, fonte, largura):
    linhas, atual = [], ''
    for p in texto.split():
        t = (atual + ' ' + p).strip()
        if d.textlength(t, font=fonte) <= largura: atual = t
        else: linhas.append(atual); atual = p
    return linhas + [atual]
def imagem(destino, titulo, linha, perigo=None, sub=None):
    im = Image.new('RGB', (1200, 630), '#FFF8EC'); d = ImageDraw.Draw(im)
    d.rectangle([0, 0, 1200, 14], fill='#9B2C1F')
    d.text((70, 60), 'Pica ou Não Pica?', font=ImageFont.truetype(F_NEG, 34), fill='#5C5648')
    ft = ImageFont.truetype(F_TIT, 92 if len(titulo) < 18 else 70)
    y = 130
    for l in quebrar(d, titulo, ft, 1060)[:2]:
        d.text((70, y), l, font=ft, fill='#2E2A1F'); y += ft.size + 12
    fl = ImageFont.truetype(F_TXT, 44)
    for l in quebrar(d, linha, fl, 1060)[:3]:
        d.text((70, y + 10), l, font=fl, fill='#2E2A1F'); y += 58
    if perigo:
        fundo, tinta = COR[perigo]; nome, s = PERIGO[perigo]
        fp = ImageFont.truetype(F_NEG, 40); txt = f'{nome} · {s}'
        w = d.textlength(txt, font=fp)
        d.rounded_rectangle([70, 500, 70 + w + 56, 572], radius=36, fill=fundo, outline='#2E2A1F' if perigo == 'baixo' else None, width=2)
        d.text((98, 512), txt, font=fp, fill=tinta)
    elif sub:
        d.text((70, 520), sub, font=ImageFont.truetype(F_NEG, 36), fill='#9B2C1F')
    destino.parent.mkdir(parents=True, exist_ok=True)
    im.save(destino, 'JPEG', quality=82, optimize=True, progressive=True)
for b in B:
    imagem(SITIO / 'img' / 'compartilhar' / f'{b["id"]}.jpg', b['n'], b['pica'] + '.', b['p'])
imagem(SITIO / 'img' / 'compartilhar' / 'guia.jpg', 'Pica ou não pica?', 'Reconheça os bichos do Brasil que picam e os que não picam, e saiba o que fazer se picar.', sub='Em caso de acidente: 192')
def icone(lado, destino):
    im = Image.new('RGB', (lado, lado), '#2E2A1F'); d = ImageDraw.Draw(im)
    r = lado * 0.36; c = lado / 2
    d.ellipse([c - r, c - r, c + r, c + r], fill='#E9A23B')
    f = ImageFont.truetype(F_TIT, int(lado * 0.42))
    d.text((c, c + lado * 0.02), '?', font=f, fill='#2E2A1F', anchor='mm')
    im.save(destino, 'PNG', optimize=True)
for lado in (180, 192, 512): icone(lado, SITIO / 'img' / f'icone-{lado}.png')
(SITIO / 'img' / 'icone.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><rect width="100" height="100" fill="#2E2A1F"/><circle cx="50" cy="50" r="36" fill="#E9A23B"/><text x="50" y="66" font-family="Georgia,serif" font-weight="700" font-size="44" text-anchor="middle" fill="#2E2A1F">?</text></svg>\n')

# ================================================================ O guia sem internet: manifesto e service worker (o mesmo modelo do Guia do Cerrado)
import hashlib
paginas_pt = so_pt + COMPARTILHADAS
arquivos = set()
for f in paginas_pt:
    t = re.sub(r'\{\{!pt-BR\}\}.*?\{\{/!pt-BR\}\}', '', (M / f).read_text(), flags=re.S)
    for u in re.findall(r'(?:src|href)="\{\{raiz\}\}([^"#]+)"', t):
        if not u.endswith(('.html', '.webmanifest')): arquivos.add(u)
    for s_ in re.findall(r'srcset="([^"]+)"', t):
        for parte in s_.split(','):
            u = parte.strip().split(' ')[0].replace('{{raiz}}', '')
            if u: arquivos.add(u)
arquivos |= {'img/icone-192.png', 'img/icone-512.png', 'img/icone.svg'}
arquivos = sorted(a for a in arquivos if (SITIO / a.split('?')[0]).is_file())
BASE_OFF = ['./', 'index.html', 'emergencia.html', 'socorro.html', 'cartao.html', 'soro.html', 'identificar.html', 'bichos.html', 'manifest.webmanifest']
BASE_OFF += [a for a in arquivos if a.startswith(('css/', 'js/')) or 'icone' in a]
TUDO_OFF = sorted(set(BASE_OFF + paginas_pt + arquivos))
h = hashlib.sha256()
for f in sorted(M.glob('*.html')): h.update(f.read_bytes())
for a in arquivos: h.update((SITIO / a.split('?')[0]).read_bytes())
VERSAO_OFF = 'pica-' + h.hexdigest()[:10]
sw = (AQUI.parent / 'fotografia-do-cerrado').joinpath('..', '..', '..', 'sitios', 'fotografia-do-cerrado', 'sw.js').resolve().read_text()
sw = re.sub(r"const VERSAO = '[^']*';", f"const VERSAO = '{VERSAO_OFF}';", sw)
sw = re.sub(r'const BASE = \[.*?\];', 'const BASE = ' + json.dumps(BASE_OFF) + ';', sw)
sw = re.sub(r'const TUDO = \[.*?\];', 'const TUDO = ' + json.dumps(TUDO_OFF) + ';', sw)
sw = re.sub(r'// o guia inteiro tem \d+ endereços', f'// o guia inteiro tem {len(TUDO_OFF)} endereços', sw)
sw = sw.replace("!nome.startsWith('cerrado-')", "!nome.startsWith('pica-')").replace('Gerado pelo guia-pt.py', 'Gerado pelo guia-pt.py do Pica ou Não Pica? (copiado do Guia do Cerrado)')
(SITIO / 'sw.js').write_text(sw)
(SITIO / 'js' / 'offline.js').write_text((SITIO.parent / 'fotografia-do-cerrado' / 'js' / 'offline.js').read_text().replace('o guia funciona sem internet neste aparelho', 'o guia funciona sem internet neste aparelho'))
(SITIO / 'manifest.webmanifest').write_text(json.dumps({
 'name': NOME, 'short_name': 'Pica ou Não', 'lang': 'pt-BR', 'start_url': './index.html', 'scope': './', 'display': 'standalone',
 'background_color': '#FFF8EC', 'theme_color': '#2E2A1F',
 'description': 'Reconheça os bichos que picam e saiba o que fazer, também sem internet.',
 'icons': [{'src': 'img/icone-192.png', 'sizes': '192x192', 'type': 'image/png', 'purpose': 'any maskable'},
           {'src': 'img/icone-512.png', 'sizes': '512x512', 'type': 'image/png', 'purpose': 'any maskable'},
           {'src': 'img/icone.svg', 'sizes': 'any', 'type': 'image/svg+xml'}],
}, ensure_ascii=False, indent=2) + '\n')
print(f'sem internet: {len(TUDO_OFF)} endereços, versão {VERSAO_OFF}')
