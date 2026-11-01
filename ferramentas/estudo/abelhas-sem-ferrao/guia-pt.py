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
MENU = [('index.html', 'Início'), ('identificar.html', 'Que bicho é?'), ('bichos.html', 'Bichos'), ('socorro.html', 'Socorro'), ('mitos.html', 'Mitos')]
ATUAL = {'bicho-': 'bichos.html'}

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
cabeca = re.sub(r'<ul class="menu">.*?</ul>', '{{MENU}}', cabeca, flags=re.S)
cabeca = re.sub(r'<a class="marca" href="index.html">.*?</a>', f'<a class="marca" href="index.html">{MARCA_PT}</a>', cabeca, flags=re.S)
cabeca = re.sub(r"<link rel=\"icon\"[^>]*>", "<link rel=\"icon\" href=\"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'%3E%3Ctext y='.9em' font-size='90'%3E🐍%3C/text%3E%3C/svg%3E\">", cabeca)
rodape = rodape.replace('{{idiomas}}', '')
RODAPE_PT = f'<p>{NOME} é um guia de estudo: não substitui o atendimento médico. Em caso de acidente, ligue 192 ou vá ao serviço de saúde mais perto.</p><p><a href="fontes.html">Fontes</a> · <a href="descobrir.html">Abelhas sem ferrão</a> · <a href="creditos.html">Créditos das fotos</a> · Projeto de estudo de Luiz Matheus Moraes Vega</p>'
rodape = re.sub(r'<div class="container">.*?</div>', '<div class="container">' + RODAPE_PT + '</div>', rodape, count=1, flags=re.S)
so_pt = []
def pagina(arquivo, titulo, descricao, corpo, scripts=()):
    s = cabeca.replace('{{MENU}}', menu_pt(arquivo))
    s = re.sub(r'<title>.*?</title>', f'<title>{titulo}</title>', s)
    s = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{html.escape(descricao)}">', s)
    s = s.replace('<meta name="theme-color" content="#E9A23B">', '<meta name="theme-color" content="#2E2A1F">')
    extra = ''.join(f'    <script src="{{{{raiz}}}}js/{n}" defer></script>\n' for n in scripts)
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
                <p class="ficha-nota">Este guia ajuda a reconhecer, mas não substitui o atendimento médico. Em qualquer picada de bicho peçonhento, procure o serviço de saúde: o soro só existe lá, e é de graça pelo SUS.</p>
            </div>
        </article>
'''
    pagina(f'bicho-{b["id"]}.html', f'{b["n"]}: pica ou não pica? — {NOME}', f'{b["n"]}: é perigoso? Como reconhecer, o que causa, o que fazer e como evitar.', corpo)
for n, b in enumerate(B):
    ficha(b, n)

# ---------------------------------------------------------------- o catálogo (bichos.html)
def cartao(b):
    return (f'<li class="bicho-cartao" data-grupo="{b["g"]}" data-perigo="{b["p"]}" data-busca="{html.escape((b["n"] + " " + b["c"]).lower())}">'
            f'<a href="bicho-{b["id"]}.html"><span class="bicho-grupo">{b["g"]}</span><strong>{b["n"]}</strong><span class="bicho-pica">{b["pica"]}</span>{selo(b)}</a></li>')
chips_g = '<button type="button" class="chip" data-filtro-grupo="" aria-pressed="true">Todos</button>' + ''.join(f'<button type="button" class="chip" data-filtro-grupo="{g}" aria-pressed="false">{g}</button>' for g in GRUPOS)
chips_p = '<button type="button" class="chip" data-filtro-perigo="" aria-pressed="true">Todos</button>' + ''.join(f'<button type="button" class="chip chip-{k}" data-filtro-perigo="{k}" aria-pressed="false">{v[0]}</button>' for k, v in PERIGO.items())
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
                    <p class="contagem" aria-live="polite"><strong id="contagem">{len(B)}</strong> bichos</p>
                </div>
                <ul class="bichos-lista">{''.join(cartao(b) for b in B)}</ul>
                <p class="vazio" hidden>Nenhum bicho com esses filtros.</p>
            </div>
        </section>
'''
pagina('bichos.html', f'Os bichos: quais picam e quais não — {NOME}', f'{len(B)} bichos do Brasil: cobras, escorpiões, aranhas, abelhas, vespas, formigas, lagartas e bichos da água. Quais são perigosos e quais não.', bichos, scripts=['guia.js?v=1'])

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
pagina('identificar.html', f'Que bicho é esse? — {NOME}', 'Responda algumas perguntas e descubra que bicho é, se é perigoso e o que fazer: cobras, aranhas, escorpiões, abelhas, lagartas e mais.', identificar, scripts=['guia.js?v=1'])

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
                </div>
                <a class="ligar-192" href="tel:192">Ligar&nbsp;192&nbsp;(SAMU)</a>
            </div>
        </section>
'''
pagina('socorro.html', f'Picou? O que fazer — {NOME}', 'Primeiros socorros em picadas de cobra, escorpião, aranha, lagarta, abelha, água-viva e arraia: o que fazer, o que nunca fazer e os telefones.', socorro, scripts=['guia.js?v=1'])

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
                    <h2 id="todos-t">Todos os {len(MITOS)}</h2>
                    <ul class="mitos-lista">{mitos_cartoes}</ul>
                </section>
                <script type="application/json" id="mitos-dados">{mitos_json}</script>
            </div>
        </section>
'''
pagina('mitos.html', f'Verdade ou mito? — {NOME}', 'Chupar o veneno, torniquete, coral verdadeira, galinha contra escorpião, lagartixa venenosa: o que é verdade e o que é mito.', mitos, scripts=['guia.js?v=1'])

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
                    <a class="porta-guia" href="mitos.html"><strong>Verdade ou mito?</strong><span>Chupar o veneno, galinha contra escorpião…</span></a>
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
    if f == 'index.html':
        t = re.sub(r'(<title>.*?</title>)', lambda m: '{{!pt-BR}}' + m.group(1) + '{{/!pt-BR}}{{?pt-BR}}' + f'<title>{NOME} — o guia dos bichos que picam</title>' + '{{/pt-BR}}', t, count=1)
        t = re.sub(r'(<meta name="description" content="[^"]*">)', lambda m: '{{!pt-BR}}' + m.group(1) + '{{/!pt-BR}}{{?pt-BR}}<meta name="description" content="Reconheça os bichos do Brasil que picam e os que não picam: cobras, escorpiões, aranhas, abelhas, lagartas. E o que fazer se picar.">{{/pt-BR}}', t, count=1)
        t = re.sub(r'(    <main id="conteudo">\n)(.*?)(    </main>)', lambda m: m.group(1) + '{{!pt-BR}}' + m.group(2) + '{{/!pt-BR}}' + inicial + '\n' + m.group(3), t, count=1, flags=re.S)
        if 'guia.js' not in t: t = t.replace('{{alternativas}}', '{{?pt-BR}}    <script src="{{raiz}}js/guia.js?v=1" defer></script>\n{{/pt-BR}}{{alternativas}}', 1)
    # o rodapé em português ganha os links do guia
    t = re.sub(r'(\{\{idiomas\}\}\s*)(.*?)(\s*</div>\s*</footer>)', lambda m: m.group(1) + '{{?pt-BR}}' + RODAPE_PT + '{{/pt-BR}}{{!pt-BR}}' + m.group(2) + '{{/!pt-BR}}' + m.group(3), t, count=1, flags=re.S)
    q.write_text(t)

(AQUI / 'so-pt.json').write_text(json.dumps(so_pt, ensure_ascii=False, indent=2) + '\n')
print(f'{NOME}: {len(B)} bichos, {len(so_pt)} páginas só em português, {len(FONTES)} fontes')
