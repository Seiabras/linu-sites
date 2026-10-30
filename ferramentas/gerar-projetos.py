"""Gera as páginas de cada projeto (public/projetos/<id>.html): o problema, o que foi feito e como funciona
por dentro. Os fatos vêm dos READMEs dos repositórios de cada projeto; nada de número de resultado que
não esteja documentado. Para mudar um texto, edite PROJETOS e rode:

    python3 ferramentas/gerar-projetos.py
"""
from html import escape
from pathlib import Path
from urllib.parse import quote

SITE = 'https://sites.linupedia.com.br'
SAIDA = Path(__file__).resolve().parent.parent / 'public' / 'projetos'
WHATSAPP = 'https://wa.me/5561996672610?text='

PROJETOS = [
    {
        'id': 'linupedia',
        'nome': 'LinuPedia',
        'etiqueta': 'App que instala',
        'url': 'https://linupedia.com.br',
        'endereco': 'linupedia.com.br',
        'imagem': 'linupedia.webp',
        'alt': 'O linuhub da LinuPedia: o acampamento do Linu em pixel art, à noite, com a fogueira e os amigos dele',
        'resumo': 'Um app de idiomas que virou uma enciclopédia jogável: 197 idiomas e 39 áreas do conhecimento, no celular e no computador, funcionando até sem internet.',
        'desafio': 'Ensinar idiomas, e depois ciências, artes e lazer, para quem fala português: de graça para todos, sem anúncios, sem depender de internet e sem inventar nada. Cada fato e cada exemplo precisa vir com a fonte.',
        'feito': [
            'A trilha é uma aventura: um mapa que sai da Antártica e chega ao país do idioma, com travessias por rádio, decisões e conversa por voz.',
            'O linuhub, a casa do app: um acampamento em pixel art na Antártica, onde o Linu anda (tocando, no joystick ou no teclado) até as áreas, com o mapa da ilha e os pinguins de outras pessoas.',
            'O abrigo do Linu em pixel art, com a luz seguindo o relógio (dia, sol da meia-noite e noite com aurora), onde cada objeto é um atalho.',
            'Voz em todo idioma: gravações de falantes nativos, a voz do aparelho e uma voz neural que funciona offline.',
            'Muito para praticar: histórias com escolhas, diário com corretor, ditado, álbum de figurinhas e 77 jogos.',
            'Acessível: tema claro e escuro, “reduzir movimento” e leitores de tela.',
            'Conteúdo livre: as lições podem ser copiadas e adaptadas por professores e escolas (CC BY-NC-SA 4.0).',
        ],
        'dentro': [
            'Um código só para Android, iOS e web (React Native e Expo).',
            'Instala na tela do celular como app e abre sem internet; o progresso fica num banco no próprio aparelho.',
            'O servidor publica sozinho a versão nova, mas só se todos os testes passarem; quem tem o app instalado recebe o aviso “Versão nova” ao voltar para ele.',
        ],
    },
    {
        'id': 'v2tech',
        'nome': 'V²Tech COMBUSTÍVEL',
        'etiqueta': 'Ferramenta para empresas',
        'url': 'https://v2tech.app.br',
        'endereco': 'v2tech.app.br',
        'imagem': 'v2tech.webp',
        'alt': 'Página inicial do V²Tech COMBUSTÍVEL com o preço justo do diesel',
        'resumo': 'Para empresas de ônibus, transportadoras e frotas conferirem se o preço do diesel, da gasolina ou do etanol cobrado pela distribuidora faz sentido.',
        'desafio': 'Quando chega um preço novo de combustível, saber se ele é justo depende de uma conta longa: preço da Petrobras, impostos, biodiesel, frete, margem da distribuidora e juros do prazo. Essa conta vivia numa planilha.',
        'feito': [
            'O cliente informa onde recebe o combustível, o que diz o contrato e o preço proposto; o site responde se o preço faz sentido, qual seria o preço justo e quanto a diferença representa por mês.',
            'Contas por empresa, com equipe: todos veem os mesmos contratos e consultas.',
            'Contratos salvos são recalculados todo dia, com alerta por e-mail quando o preço pago sai da faixa ou há reajuste chegando.',
            'Relatório em PDF de uma página e, quando o preço vem alto, uma carta pronta para a distribuidora.',
            'Mapa público do preço justo por estado, simulador de cenários e calendário de reajustes.',
            'API para os sistemas de frota consultarem o preço justo sozinhos.',
        ],
        'dentro': [
            'O cálculo fica no servidor: o navegador do cliente recebe só o resultado.',
            'Os dados de mercado (Petrobras, Banco Central, ANP) são atualizados todo dia por um robô, que recusa valores fora do plausível.',
            'Cópia de segurança diária, criptografada.',
        ],
    },
    {
        'id': 'losvega',
        'nome': 'Los Vega na Estrada',
        'etiqueta': 'Site de vendas com painel',
        'url': 'https://losveganaestrada.com.br',
        'endereco': 'losveganaestrada.com.br',
        'imagem': 'losvega.webp',
        'alt': 'Página inicial do Los Vega na Estrada, roteiros de viagem personalizados',
        'resumo': 'Roteiros de viagem personalizados, num site feito para ser o link da bio do Instagram.',
        'desafio': 'Transformar quem chega pelo Instagram em pedido, mostrando o valor desde o começo, e organizar os pedidos sem planilha nem mensagem perdida.',
        'feito': [
            'Site com como funciona, o que está incluído, preços, para quem é, perguntas frequentes e guias de viagem.',
            'O formulário “Conte sobre a sua viagem” já mostra o valor do roteiro conforme o tipo e o número de destinos.',
            'Painel com os pedidos, a situação de cada um (novo, conversando, fechado, entregue), anotações e um botão para responder pelo WhatsApp com a mensagem pronta.',
            'Aba Instagram no painel: link para a bio que marca os pedidos vindos de lá, bio sugerida, legendas e hashtags para copiar.',
            'Instala no celular como app.',
        ],
        'dentro': [
            'Os preços ficam num arquivo e mudam sem reiniciar nada.',
            'Contagem de visitas sem cookie e sem guardar IP, mostrada no próprio painel.',
            'Cópia diária dos pedidos, guardando as últimas 30.',
        ],
    },
    {
        'id': 'marginalia',
        'nome': 'Marginalia',
        'etiqueta': 'Publicação digital',
        'url': 'https://marginalia.blog.br',
        'endereco': 'marginalia.blog.br',
        'imagem': 'marginalia.webp',
        'alt': 'Página inicial da Marginalia, publicação de História e humanidades',
        'resumo': 'Publicação digital independente de História e humanidades, de Íris Chermont.',
        'desafio': 'Publicar textos de pesquisa com notas, referências e cara de revista, sem depender de plataforma de blog e sem a autora precisar mexer em código.',
        'feito': [
            'Três abas: o projeto, o sumário (com busca e filtro por categoria) e a página sobre a autora.',
            'Cada texto tem categoria, tema, data, tempo de leitura, notas na margem, referências e a citação ABNT pronta para copiar.',
            'Assinatura por e-mail, com confirmação e saída com um clique.',
            'Painel da autora: o editor aceita texto colado do Word e do Google Docs mantendo as notas de rodapé, e tem botões de nota na margem e de nota de rodapé.',
            'No editor, uma imagem pronta para o Instagram com o título do texto.',
        ],
        'dentro': [
            'Servidor próprio, sem dependências externas.',
            'Contagem de leituras sem cookies e sem guardar IP.',
            'Cópia diária criptografada dos textos, páginas e imagens, guardada por 90 dias.',
        ],
    },
    {
        'id': 'iconvet',
        'nome': 'Iconvet',
        'etiqueta': 'Site institucional',
        'url': 'https://iconvet.com.br',
        'endereco': 'iconvet.com.br',
        'imagem': 'iconvet.webp',
        'alt': 'Página inicial da Iconvet, clínica veterinária em Salvador, com o destaque do setor de exames de imagem',
        'resumo': 'Site da Iconvet, clínica veterinária geral e especializada no Rio Vermelho, em Salvador.',
        'desafio': 'Uma clínica com muitos setores (clínico, cirúrgico, laboratório, exames de imagem, internamento) e dezenas de serviços e especialidades precisava de um site novo no próprio domínio, em que o tutor achasse rápido o que procura e chegasse ao WhatsApp em um toque.',
        'feito': [
            'Página inicial com destaques que passam (como o setor novo de exames de imagem), as áreas de atendimento, os serviços, os princípios da clínica e o internamento.',
            'Uma página para cada setor, exame, procedimento, serviço e área de atendimento: 74 páginas no mapa do site.',
            'Páginas da clínica: história, estrutura, equipe, valores, gestão de qualidade, setor jurídico, SCIH, programa de estágio, orientações para pacientes e visitantes e a galeria.',
            'Endereço, telefones, horário e WhatsApp sempre à mão: na barra do topo, no botão flutuante e no rodapé, com a rota pelo mapa.',
            'Botão “Área do Cliente”, que leva ao sistema da clínica (SimplesPet).',
        ],
        'dentro': [
            'Feito em Next.js e publicado na Vercel, com o domínio da clínica apontando para o site novo.',
            'Cada página com título e descrição próprios, mais o mapa do site e o robots.txt para os buscadores.',
        ],
    },
    {
        'id': 'ajoriente',
        'nome': 'Administração Judicial Oriente',
        'etiqueta': 'Site com consulta de processos',
        'url': 'https://ajoriente.com',
        'endereco': 'ajoriente.com',
        'imagem': 'ajoriente.webp',
        'alt': 'Página inicial da Administração Judicial Oriente: “Orientando empresas para novos começos”',
        'resumo': 'Site da Administração Judicial Oriente, do Rio de Janeiro: recuperação judicial e extrajudicial, falências, insolvência civil e liquidação judicial.',
        'desafio': 'Credores, empresas e o juízo precisam achar rápido as informações de cada processo e os modelos de documento. O site tinha de passar seriedade e deixar essa consulta a poucos cliques.',
        'feito': [
            'Apresentação da Oriente e das cinco áreas de atuação, com página própria para recuperação judicial e para falência.',
            'Consulta de processos por categoria (falências e recuperação judicial), com uma página por empresa: número do processo, documentos e comunicados.',
            'Os quatro modelos de documento (habilitação e impugnação de crédito, procuração para a assembleia de credores) para abrir ou baixar.',
            'Formulário de contato com o assunto escolhido numa lista, o consentimento para o tratamento dos dados e a política de privacidade.',
            'E-mail, telefone e WhatsApp em todas as páginas.',
        ],
        'dentro': [
            'Feito em Next.js e publicado na Vercel, no domínio próprio.',
            'O formulário tem um campo-armadilha contra robôs de spam.',
            'Link “Pular para o conteúdo” para quem navega pelo teclado ou com leitor de tela.',
        ],
    },
    {
        'id': 'dojo-legacy',
        'nome': 'Dojo Legacy',
        'etiqueta': 'Jogo no navegador e no celular',
        'url': 'https://www.bjj-link.com',
        'endereco': 'bjj-link.com',
        'imagem': 'dojo-legacy.webp',
        'alt': 'Página inicial do Dojo Legacy: “Da faixa branca à lenda do tatame”, com o jogo no computador e no celular',
        'resumo': 'Jogo de carreira de Jiu-Jitsu e MMA: começa na faixa branca e termina em lenda. Grátis no navegador, no iPhone e no Android.',
        'desafio': 'Um jogo de luta por turnos com uma carreira inteira, dentro e fora do tatame, que roda igual no navegador e no celular, guarda o progresso na nuvem e junta os jogadores em rankings, ligas e PVP.',
        'feito': [
            'Lutas lance a lance: posição, gás e momentum, com 165 técnicas de Jiu-Jitsu e 61 de striking no MMA.',
            'Carreira completa: graduação de faixa, academia própria com alunos, empresário, patrocínios e contratos, e um herdeiro que continua o legado.',
            'PVP online por turnos, torneios ao vivo e a Liga de Equipes, com cinco divisões, da Liga dos Novatos à Grande Liga.',
            'Rankings ao vivo e Hall da Fama, só com jogadores reais, atualizados a cada hora.',
            'Guia do jogo com uma página por técnica e por campeonato, em português e em inglês: 566 páginas no mapa do site.',
            'Dá para jogar sem conta; com a conta grátis, a carreira fica salva na nuvem e continua em outro aparelho.',
        ],
        'dentro': [
            'Site em Next.js na Vercel; o mesmo jogo no navegador e nos apps de iPhone e Android.',
            'As carreiras ficam salvas na nuvem, e as logos das equipes no Supabase.',
            'Português e inglês, com o idioma escolhido no topo.',
        ],
    },
    {
        'id': 'omega',
        'nome': 'Ômega Imóveis',
        'etiqueta': 'Site de apresentação',
        'url': 'https://omega-site-vert.vercel.app/',
        'endereco': 'omega-site-vert.vercel.app',
        'imagem': 'omega.webp',
        'alt': 'Página inicial da Ômega Imóveis: “O lugar certo muda tudo”, sobre a Zona Sul do Rio ao entardecer',
        'resumo': 'Site da Ômega Imóveis, imobiliária da Zona Sul do Rio de Janeiro, com atendimento próximo, elegante e estratégico.',
        'desafio': 'Apresentar uma imobiliária nova para um público exigente: menos vitrine de anúncios e mais a forma de trabalhar e os bairros onde ela atua, levando a conversa para o WhatsApp.',
        'feito': [
            'Página única que se lê como uma revista: a abertura, a essência (patrimônio, localização e escolhas), o manifesto, os bairros e a abordagem.',
            'Os bairros da Zona Sul com identidade própria: Ipanema, Leblon, Lagoa e Copacabana em destaque, e ainda Gávea, Jardim Botânico, São Conrado e Botafogo.',
            'O método em três passos: escuta antes de tudo, visão de mercado e relações que permanecem.',
            'Chamada para a conversa no topo e no fim da página, e o CRECI da empresa e do responsável técnico no rodapé.',
        ],
        'dentro': [
            'Publicado na Vercel, por enquanto sem domínio próprio.',
            'Página leve, com link “Pular para o conteúdo” para quem navega pelo teclado.',
        ],
    },
]

PAGINA = '''<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{nome} — Linu Sites</title>
  <meta name="description" content="{resumo}">
  <meta name="theme-color" content="#1F2A44">
  <meta http-equiv="Content-Security-Policy" content="default-src 'self'; img-src 'self' data:; font-src 'self'; style-src 'self'; script-src 'self'; connect-src 'self'; object-src 'none'; base-uri 'self'; form-action 'self'">
  <link rel="icon" href="../img/linu-logo.png" type="image/png" sizes="128x128">
  <link rel="icon" href="../img/icone-32.png" type="image/png" sizes="32x32">
  <link rel="apple-touch-icon" href="../img/icone-180.png">
  <link rel="canonical" href="{site}/projetos/{id}">
  <meta property="og:title" content="{nome}, por Linu Sites">
  <meta property="og:description" content="{resumo}">
  <meta property="og:type" content="article">
  <meta property="og:url" content="{site}/projetos/{id}">
  <meta property="og:locale" content="pt_BR">
  <meta property="og:image" content="{site}/img/projetos/{imagem}">
  <meta name="twitter:card" content="summary_large_image">
  <link rel="preload" href="../fontes/nunito-latin.woff2" as="font" type="font/woff2" crossorigin>
  <script src="../js/tema-inicio.js?v=5"></script>
  <link rel="stylesheet" href="../css/estilo.css?v=14">
  <script src="../js/tema.js?v=7" defer></script>
  <script src="../js/menu.js?v=6" defer></script>
</head>
<body>
  <header class="topo">
    <div class="dentro topo-dentro">
      <a class="marca" href="../" aria-label="Linu Sites, início">
        <img src="../img/linu-logo.png" alt="" width="40" height="40">
        <span>Linu <b>Sites</b></span>
      </a>
      <nav class="menu" aria-label="Seções">
        <div class="menu-links" id="menu-links">
          <a href="../#servicos">O que fazemos</a>
          <a href="../#projetos">Projetos</a>
          <a href="../#como">Como funciona</a>
          <a class="botao menu-links-orcamento" href="#contato">Pedir orçamento</a>
        </div>
        <button class="luz" type="button" data-luz aria-label="Apagar a luz (modo escuro)" title="Apagar a luz">
          <svg viewBox="0 0 24 24" width="22" height="22" aria-hidden="true">
            <path class="luz-raios" d="M12 1.5v2M4.6 4.6l1.4 1.4M1.5 12h2M20.5 12h2M19.4 4.6 18 6" />
            <path class="luz-bulbo" d="M12 6a5.5 5.5 0 0 0-3.2 10c.5.4.8.9.8 1.5v.5h4.8v-.5c0-.6.3-1.1.8-1.5A5.5 5.5 0 0 0 12 6Z" />
            <path class="luz-base" d="M9.8 20.5h4.4M10.5 22.5h3" />
          </svg>
        </button>
        <a class="botao botao-pequeno menu-orcamento" href="#contato">Pedir orçamento</a>
        <button class="menu-abrir" type="button" aria-expanded="false" aria-controls="menu-links" aria-label="Abrir o menu">
          <svg viewBox="0 0 24 24" width="22" height="22" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16" /></svg>
        </button>
      </nav>
    </div>
  </header>

  <main>
    <section class="abertura caso-abertura">
      <div class="dentro">
        <a class="caso-voltar" href="../#projetos">← Todos os projetos</a>
        <p class="etiqueta">{etiqueta}</p>
        <h1>{nome}</h1>
        <p class="abertura-sub">{resumo}</p>
        <div class="botoes">
          <a class="botao" href="{url}" target="_blank" rel="noopener">Abrir {endereco}</a>
        </div>
        <img class="caso-imagem" src="../img/projetos/{imagem}" alt="{alt}" width="960" height="600">
      </div>
    </section>

    <section class="secao">
      <div class="dentro caso-texto">
        <h2>O desafio</h2>
        <p class="caso-desafio">{desafio}</p>

        <h2>O que foi feito</h2>
        <ul class="caso-lista">
{feito}
        </ul>

        <h2>Por dentro</h2>
        <ul class="caso-lista caso-lista-dentro">
{dentro}
        </ul>
      </div>
    </section>

    <section class="secao contato" id="contato">
      <div class="dentro contato-dentro">
        <img class="pixel contato-linu" src="../img/linu-pixel.png" alt="" width="138" height="190">
        <div>
          <h2>Quer algo assim para o seu negócio?</h2>
          <p>Conte o que você faz e o que imagina. Pode ser só uma ideia: a resposta vem com perguntas e próximos passos.</p>
          <div class="botoes contato-botoes">
            <a class="botao botao-grande botao-whatsapp" href="{whatsapp}" target="_blank" rel="noopener">
              <svg viewBox="0 0 24 24" width="22" height="22" aria-hidden="true"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2Zm0 18.2a8.2 8.2 0 0 1-4.2-1.2l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2Zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8-.2-.1-.4-.1-.6.1l-.8 1c-.1.2-.3.2-.5.1a6.7 6.7 0 0 1-3.3-2.9c-.3-.4.2-.4.7-1.4.1-.2 0-.3 0-.4l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.3 3 3 0 0 0-.9 2.2 5.2 5.2 0 0 0 1.1 2.7 11.8 11.8 0 0 0 4.5 4c1.7.7 2.3.8 3.2.6.5-.1 1.5-.6 1.7-1.2.2-.6.2-1.1.2-1.2-.1-.1-.3-.2-.5-.3Z" /></svg>
              <span>WhatsApp <span class="sem-quebra">(61) 99667-2610</span></span>
            </a>
            <a class="botao botao-grande botao-contorno-claro" href="mailto:contato@linupedia.com.br?subject=Quero%20um%20site">contato@linupedia.com.br</a>
          </div>
        </div>
      </div>
    </section>
  </main>

  <footer class="rodape">
    <div class="dentro rodape-dentro">
      <p><b>Linu Sites</b> · sites e aplicativos web sob medida</p>
      <p>Um estúdio da <a href="https://linupedia.com.br">LinuPedia</a></p>
    </div>
  </footer>
</body>
</html>
'''


def itens(lista):
    return '\n'.join(f'          <li>{escape(t, quote=False)}</li>' for t in lista)


SAIDA.mkdir(parents=True, exist_ok=True)
for p in PROJETOS:
    texto = {k: escape(v) for k, v in p.items() if isinstance(v, str)}
    mensagem = f'Olá! Vi o projeto {p["nome"]} e quero conversar sobre um site.'
    html = PAGINA.format(
        site=SITE,
        feito=itens(p['feito']),
        dentro=itens(p['dentro']),
        whatsapp=WHATSAPP + quote(mensagem),
        **texto,
    )
    (SAIDA / f'{p["id"]}.html').write_text(html, encoding='utf-8')
    print(SAIDA / f'{p["id"]}.html')
