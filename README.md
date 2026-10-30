# Linu Sites

> **In English:** the site of Linu Sites, a studio for custom websites and web apps: 13 languages generated from one
> template, no dependencies and no server of its own, served by Caddy. Live: https://sites.linupedia.com.br

Site do **Linu Sites**, o estúdio de sites e aplicativos web da LinuPedia: **https://sites.linupedia.com.br**.

Uma página só (`public/index.html`), sem dependências e sem servidor próprio: o Caddy da VM da Oracle
(a mesma da LinuPedia, do v²tech, da Marginalia e do Los Vega) entrega os arquivos de `public/`.
O visual segue a LinuPedia: o azul do app, o gelo e o pergaminho da expedição e o Linu em pixel art.

- **No ar:** https://sites.linupedia.com.br
- **Repositório:** `Seiabras/linu-sites` (**público**: nada de senha, chave ou relatório interno aqui; isso vai
  para o `Seiabras/linuarquivos`, que é privado), branch `main`
- **Contato do estúdio:** contato@linupedia.com.br (Zoho Mail, caixa linu@linupedia.com.br) e WhatsApp
  (61) 99667-2610
- **Crédito nos projetos:** todo site feito pelo estúdio leva "Site feito por Linu Sites" no rodapé, com
  link para cá (V²Tech, Los Vega, Marginalia e, no Perfil, a LinuPedia).

## Como está organizado

| Pasta / arquivo | O que tem |
|---|---|
| `public/index.html` | A página inicial em pt-BR, **gerada** por `ferramentas/gerar-idiomas.mjs` (não edite à mão). |
| `public/<idioma>/index.html` | A mesma página em `pt-pt`, `es`, `ca`, `nl`, `en`, `fr`, `de` e `it`, também gerada. |
| `public/404.html` | Página de erro com o código E404, mostrada pelo Caddy em qualquer endereço que não existe (`handle_errors` no `deploy/Caddyfile-bloco`; liga no servidor pelo `endurecer.sh` do linuarquivos). |
| `public/projetos/*.html` | Página de cada projeto em português; nos outros idiomas, em `public/<pasta>/projetos/`. Geradas pelo `ferramentas/gerar-idiomas.mjs`. |
| `public/css/estilo.css` | Visual (cores da LinuPedia, modo claro e escuro). |
| `public/js/` | `tema-inicio.js` (aplica o tema antes de pintar), `tema.js` (o Linu e o lampião; com “menos movimento” ligado ele não anda, só aparece embaixo do lampião), `menu.js` (menu do celular), `movimento.js` (animações), `simulador.js` (o simulador do Café Aurora). |
| `public/img/` | Cena da estação, o Linu (`linu/`, `linu-pixel.png`), a logo (`linu-logo.png`), capturas dos projetos (`projetos/`), ícones e imagem de compartilhar. |
| `public/fontes/` | Nunito e as Noto de japonês, coreano e chinês (licença OFL), servidas pelo próprio site. |
| `sitios/` | Os sites dos subdomínios, fora de `public/`: `cafe-aurora/` (cafe.linupedia.com.br, também com `/bootstrap/` e `/tailwind/`), `fotografia-do-cerrado/` (cerrado.linupedia.com.br) e `abelhas-sem-ferrao/` (abelhas.linupedia.com.br). Cada um tem o seu repositório público no GitHub (`Seiabras/cafe-aurora`, `Seiabras/fotografia-do-cerrado`, `Seiabras/abelhas-sem-ferrao`); mudou aqui, leve a mudança para lá. |
| `ferramentas/cafe/` | O modelo do Café Aurora (`modelo.html`) e os textos dele em cada idioma (`textos/<código>.json`), para o `gerar-cafe.mjs`. |
| `ferramentas/pagina/` | O modelo da página inicial (`modelo.html`), os textos de cada idioma (`textos/<código>.json`) e os preços de cada moeda (`precos.json`). |
| `ferramentas/fontes/` | Os caracteres que estão em cada fonte Noto (`ja.txt`, `ko.txt`, `zh-hant.txt`), escritos pelo `gerar-fontes.mjs`. |
| `ferramentas/` | Geradores: a página em cada idioma (`gerar-idiomas.mjs`), as fontes Noto (`gerar-fontes.mjs`), páginas de projeto, imagem de compartilhar, cena noturna e o Linu trazido do app (`linu-do-app.py`). |
| `deploy/` | Instalação na VM (`instalar-uma-vez.sh`), recebimento (`receber.sh`), conferência antes de publicar (`conferir-pagina.py`), bloco do Caddy e o manual `ORACLE.md`. |
| `.github/workflows/oracle.yml` | Publicação automática (confere a página, entrega e testa se o site respondeu). |

## Ver no computador

Abra `public/index.html` no navegador, ou, para ver como no servidor:

```bash
cd public && python3 -m http.server 8000
```

## Idiomas (30/10/2026)

A página inicial existe em 9 idiomas: pt-BR na raiz e `pt-pt/`, `es/`, `ca/`, `nl/`, `en/`, `fr/`, `de/` e `it/`. Tudo
sai de um modelo só, para as versões nunca ficarem diferentes entre si:

```bash
node ferramentas/gerar-idiomas.mjs
```

- **Mudar um texto:** no `ferramentas/pagina/textos/<código>.json` de cada idioma. O gerador recusa gravar se um
  idioma tiver chave a mais ou a menos que o pt-BR.
- **Mudar o HTML:** no `ferramentas/pagina/modelo.html` (`{{chave}}` é um texto, `{{p.x}}` um preço formatado e
  `{{n.x}}` o número).
- **Mudar um preço:** no `ferramentas/pagina/precos.json` (real para o Brasil, euro para a Europa, dólar para a Ásia e
  o resto do mundo). Os cartões, o simulador, o Monte o seu site e as dúvidas mudam juntos. Uma moeda com
  `"pendente"` gera as páginas, mas o `deploy/conferir-pagina.py` não deixa publicar se alguma página no ar usar essa
  moeda; com `"provisorio"`, publica e só avisa. As tabelas em euro e em dólar foram aprovadas em 30/10/2026, com o
  euro também no Reino Unido e o recebimento pela Wise.
- **Capturas do portfólio:** toda captura mostra a tela principal ou o menu do site, nunca uma cena de dentro (regra de
  30/10/2026; a LinuPedia entra pela Lista, o Minhocão pela tela inicial). Tamanho 960 × 600, em WebP, em
  `public/img/projetos/`.
- **Regiões (30/10/2026):** cada idioma diz a sua região no JSON (`"regiao"`: `brasil`, `europa` ou `asia`, e
  `"padrao": true` na página que representa a região; `"hreflang_extra"` para outros códigos que a página atende, como
  `en-IE` no inglês europeu e `zh-TW`/`zh-HK` no chinês). O seletor agrupa por região. A **Ásia-Pacífico e
  internacional** tem o inglês internacional (`/intl/`, em dólar, que também é o `x-default`), o japonês (`/ja/`), o
  coreano (`/ko/`) e o chinês tradicional (`/zh-hant/`), com fonte Noto própria para esses três (a Nunito não tem os
  caracteres) e a entrelinha e a quebra de linha de cada língua.
  Um idioma com `"rascunho": true` fica fora do site, do seletor e do sitemap.
- **Blocos só de algumas páginas (30/10/2026):** `{{?nome}}` … `{{/nome}}`, cada um na sua linha do modelo, entra só nas
  páginas daquela região (`europa`, `asia`, `brasil`), daquele idioma ou, com `cjk`, em japonês, coreano e chinês. As
  chaves do bloco ficam com `""` nos outros idiomas, e o gerador recusa um bloco que entra com chave vazia.
- **O aviso de outra versão** (`js/menu.js`) junta a região, que vem do fuso horário do aparelho (sem consultar IP), com
  o idioma do navegador: Tóquio com o navegador em inglês vai para o `/intl/`, Lisboa para o `/pt-pt/`, e fora da
  Europa as páginas em euro são o último recurso. Nunca troca de página sozinho.
- **Os textos dos scripts** (menu, luz, mensagem do WhatsApp e do e-mail) vão no `<script type="application/json"
  id="textos-js">` de cada página; a moeda e o formato do número vêm do `<html lang data-moeda>`. As páginas dos
  projetos também têm o bloco.
- **Seletor de idioma** no topo (o globo) e, uma vez por visitante, um aviso discreto quando o idioma do navegador é
  outro que o site tem (sem trocar de página sozinho). A escolha fica guardada no navegador (`js/menu.js`).
- **Para o Google:** cada página leva o `hreflang` de todas (o `x-default` é o inglês), os `og:locale`, os dados
  estruturados (`ProfessionalService`) e o `sitemap.xml` com as alternativas; o gerador refaz o sitemap.
- Na Europa: preço em euro, domínio do país (.pt, .es, .de…) e o WhatsApp com +55.
- **Pagamento em cada região (`faq_pagamento_r`, 30/10/2026):** o Brasil segue com Pix ou transferência. A Europa tem
  fatura em euro, transferência SEPA pela Wise e, entre empresas, IVA em autoliquidação quando se aplicar, com o nome de
  cada país (inversión del sujeto pasivo, btw verlegd, Reverse-Charge, reverse charge). A Ásia e o `/intl/` têm só a
  Wise, em dólar: o PayPal saiu desses textos. A divisão (50/50 ou 40/30/30) é a mesma em todas.
  As páginas “Como foi feito” e o Café Aurora do simulador também estão nesses idiomas.

## O que a Europa lê (30/10/2026)

As páginas com região `europa` levam, no fim do “Como funciona”, os cartões do bloco `{{?europa}}` do modelo. O bloco é
condicional: as chaves `europa_*` existem nos 13 idiomas (é a regra das chaves iguais), vazias fora da Europa. Uma chave
vazia dentro de um bloco que entra faz o gerador recusar a gravação.

- **Acessibilidade** (`europa_acess_titulo`, `europa_acess_texto`): cita o European Accessibility Act e a WCAG 2.2 e diz
  só o que esta página faz. Sem promessa de conformidade legal nem de certificação, e o texto diz isso. O que foi
  medido no Chrome em 30/10/2026, em 390 e 1280 px, claro e escuro, na inicial e na página de um projeto: contraste de
  texto AA (4,5:1, ou 3:1 no texto grande), anel de foco em toda parada do Tab, tudo alcançável por teclado sem ficar
  preso, alvos de pelo menos 24 × 24 px e nenhuma animação com “menos movimento”. Para isso, em 30/10 subiram os
  contrastes das abas e das áreas e do número dos passos, o anel de foco ficou azul-claro nas partes escuras e por
  dentro da captura dos projetos, e o topo preso não cobre mais o que recebe foco (`scroll-padding-top`).
- **O Café Aurora fica de fora** e o texto diz isso: é um site à parte, e ali o rodapé tem contraste de 3,7:1 e há alvos
  menores que 24 px. Se o Café for acertado, tire a frase. Mudou a página a ponto de um item deixar de valer, tire o
  item do texto nos 8 idiomas.

- **Privacidade** (`europa_priv_titulo`, `europa_priv_texto`): diz que o site não tem cookies, rastreador, CDN nem Google
  Fonts e que o tema e o idioma escolhidos ficam só no navegador. Conferido em 30/10/2026: nenhum `Set-Cookie` nem
  `document.cookie`, nem na página nem no Café; nenhum script, folha, fonte ou imagem de outro endereço nas páginas
  geradas (o único endereço de fora que carrega é o `cafe.linupedia.com.br`, no quadro do simulador, na mesma VM); o DNS
  aponta direto para a VM, sem CDN; e a CSP, na `<meta>` e no cabeçalho do Caddy, só libera o próprio site e o Café.
  O que fica no navegador é o `localStorage` (`tema`, `idioma`, `idioma-aviso` e, no Café, `aurora-modo`). Antes de pôr
  qualquer coisa de terceiro no site, mude esse texto nos 8 idiomas. Ele fala **deste site**, não dos sites dos clientes.

## Fontes de japonês, coreano e chinês (30/10/2026)

As páginas `/ja/`, `/ko/` e `/zh-hant/` usam a Noto Sans CJK (licença OFL, `public/fontes/OFL-Noto.txt`) cortada só com os
caracteres que elas usam, servida de `public/fontes/`, sem CDN. São dois pesos por língua, 400 e 700, e as outras páginas
não baixam nada disso: as famílias só entram no `--texto` dessas línguas, no `css/estilo.css`.

| Língua | Caracteres | Regular + Bold |
|---|---:|---:|
| Japonês | 718 | 198 KB |
| Coreano | 550 | 75 KB |
| Chinês tradicional | 905 | 295 KB |

- **Refazer:** nada a fazer na hora. O `node ferramentas/gerar-idiomas.mjs` compara os caracteres das páginas com o
  `ferramentas/fontes/<pasta>.txt` e refaz a fonte que mudou; depois, suba o `?v=` dela no `css/estilo.css` e o do
  `estilo.css` nos modelos. Entram o HTML das páginas (com os textos dos scripts), o `content` do CSS e os dias da semana
  que o `Intl` escreve nos relógios do contato. `node ferramentas/gerar-fontes.mjs --tudo` refaz todas.
- **O que precisa:** a Noto Sans CJK em `/usr/share/fonts/noto-cjk` (pacote `noto-fonts-cjk` do Arch, ou `NOTO_CJK=<pasta>`)
  e o `pyftsubset`, com o brotli. O gerador procura em `PYFTSUBSET`, no `PATH` e no ambiente separado que uso aqui:
  `python3 -m venv ~/.local/share/linu-sites-fontes && ~/.local/share/linu-sites-fontes/bin/pip install fonttools brotli`.
  Sem eles, o gerador avisa e segue: a página sai normal, e o caractere novo aparece na fonte do aparelho.
- **Limite:** 400 KB somados por página. O `deploy/conferir-pagina.py` não deixa publicar acima disso. O chinês é o que
  tem menos folga; se apertar, o próximo passo é deixar no Bold só os caracteres que aparecem em negrito.
- **Entrelinha e quebra de linha** (`css/estilo.css`): 1,85 em japonês e chinês e 1,75 em coreano; `line-break: strict` nas
  três; `word-break: keep-all` em coreano, para quebrar entre palavras; `word-break: auto-phrase` e `palt` nos títulos em
  japonês. Nos navegadores sem `auto-phrase`, o título quebra do jeito normal.

## O Café Aurora em cada idioma (30/10/2026)

O Café do simulador fala a língua da página: `cafe.linupedia.com.br/` em pt-BR e `/pt-pt/`, `/es/`, `/ca/`, `/nl/`,
`/en/`, `/fr/`, `/de/`, `/it/`, `/intl/`, `/ja/`, `/ko/` e `/zh-hant/`, e o simulador, o “Abrir em tela cheia” e o cartão
de estudo de cada idioma apontam para o Café no mesmo idioma. Tudo sai de um modelo só:

```bash
node ferramentas/gerar-cafe.mjs
```

- O texto do Café muda no `ferramentas/cafe/textos/<código>.json` (o gerador recusa se faltar ou sobrar chave), e o HTML,
  no `ferramentas/cafe/modelo.html`. Os idiomas são os mesmos da página principal (um em rascunho fica de fora).
- As frases que o script escreve (a abertura, os nomes das bebidas, a assinatura, o painel) vão no
  `<script type="application/json" id="textos-cafe">`; sem o bloco, o `script.js` usa o português. O preço da bebida
  segue o formato de número de cada língua.
- As versões `/bootstrap/` e `/tailwind/` continuam só em português. O repositório `Seiabras/cafe-aurora` ainda não tem
  os idiomas (o gerador e os textos moram aqui).
- `IDIOMAS=pt-BR node ferramentas/gerar-cafe.mjs` gera só os idiomas pedidos, para ver um texto novo antes de traduzir.

## De dia, a Padaria Aurora (30/10/2026)

Das 6h às 18h no relógio de quem visita, o Café vira a Padaria Aurora: o mesmo universo da fenda, só que de manhã
(croissant de 2087 camadas, pão de gravidade zero). Mudam as cores (creme, trigo, casca), o fundo (farinha no ar em
vez da grade de neon), o letreiro, o cardápio, os depoimentos, o horário, e o laboratório vira “Monte o seu pão”: a
farinha, o tempo de forno (a casca doura e o pão cresce) e o que vai por cima (gergelim, manteiga, queijo, açúcar de
cometa).

- O `inicio.js` escolhe o modo antes de pintar e põe `data-modo="dia"` ou `"noite"` no `<html>`: primeiro o
  `?modo=dia` / `?modo=noite` do endereço (só naquela visita), depois a escolha guardada pelo botão, depois o relógio.
  Sem JavaScript, fica o café.
- Cada texto que muda está duas vezes no modelo, `<span class="so-noite">` e `<span class="so-dia">`, e o CSS esconde
  o do outro modo. As chaves de dia começam com `d_` nos textos de cada idioma; o que não dá para trocar por CSS (o
  `aria-label` da marca e do laboratório) vai em `data-aria-dia` e o `script.js` troca.
- As cores de dia são as mesmas variáveis (`--cyan`, `--magenta`…) redefinidas no bloco 17 do `estilo.css`; o painel
  “Sintonizar dimensão” gira as duas paletas pelo `--desvio`.
- O botão de sol e lua, ao lado do menu, mostra para onde leva e faz a virada: o neon pisca, a tela se cobre, o sol
  nasce (ou a lua desce) e o modo troca por baixo. Com “menos movimento” ou sem os efeitos do simulador, troca direto.

## O Cerrado e as Abelhas em cada idioma, com modo claro e escuro (30/10/2026)

Os outros dois sites de estudo também falam os 13 idiomas (`cerrado.linupedia.com.br/<idioma>/…` e
`abelhas.linupedia.com.br/<idioma>/…`), com os idiomas no rodapé, e os cartões da página principal levam à versão no
mesmo idioma. Tudo sai de um modelo por página:

```bash
node ferramentas/gerar-estudo.mjs fotografia-do-cerrado
node ferramentas/gerar-estudo.mjs abelhas-sem-ferrao
```

- O texto muda no `ferramentas/estudo/<site>/textos/<código>.json`. O HTML em português foi transformado em modelo pelo
  `ferramentas/estudo/extrair.py` (cada bloco de texto vira uma chave inteira, com a marcação de dentro da frase); se
  mudar o HTML de uma página, mude no `ferramentas/estudo/<site>/modelo/`.
- As frases dos scripts (o formulário do Cerrado; o percurso e as 5 perguntas do teste das Abelhas) vão no
  `<script type="application/json" id="textos-estudo">`; sem o bloco, os scripts usam o português.
- **Modo claro e escuro**: botão no cabeçalho (`js/tema.js`, e `js/tema-inicio.js` no `<head>` para não piscar), com as
  cores por função no CSS. No escuro, os contrastes passam do AAA (medidos: texto do Cerrado 16,1:1, do teste das
  Abelhas acima de 7,5:1). Os CSS e scripts levam `?v=2`: mudou um deles, suba o número no modelo.
- Os repositórios `Seiabras/fotografia-do-cerrado` e `Seiabras/abelhas-sem-ferrao` ainda não têm nada disso.

## O que tem na página

- **Abertura:** o que o estúdio faz e o botão de orçamento.
- **O que fazemos:** sites de apresentação, ferramentas e painéis, apps que instalam, hospedagem.
- **Página de cada projeto** (`/projetos/linupedia`, `/v2tech`, `/losvega`, `/marginalia`, `/minhocao`, `/trupe`, `/iconvet`,
  `/ajoriente`, `/dojo-legacy`, `/omega`): o desafio, o que foi feito e como funciona por dentro, com os fatos
  dos READMEs de cada repositório (nos quatro de clientes, do que o próprio site mostra no ar). Em todos os idiomas da página
  (`/<pasta>/projetos/<nome>`), geradas pelo `ferramentas/gerar-idiomas.mjs` junto com a inicial: o modelo é o
  `ferramentas/projetos/modelo.html`, o nome, o endereço e a captura ficam no `ferramentas/projetos/projetos.json` e
  o texto de cada idioma no `ferramentas/projetos/textos/<código>.json`. No computador, o `python3 -m
  http.server` não completa o `.html` como o Caddy; abra `projetos/<nome>.html`.
- **Projetos** (`#projetos`): duas abas lado a lado, “No ar” e “De estudo” (`js/movimento.js`, com setas, Home e
  End). O endereço com `#estudo` abre a segunda; sem JavaScript, as duas listas aparecem uma embaixo da outra.
  Por cima das abas, as **áreas** (30/10/2026): Educação e cultura, Saúde e serviços, Comércio e turismo, Indústria e
  Jogos. Elas filtram as duas listas, a conta de cada aba acompanha e, se a aba aberta ficar vazia, abre a outra. As
  áreas de cada projeto ficam no `data-areas` do `ferramentas/pagina/modelo.html` (pode ter mais de uma).
- **No ar:** LinuPedia, V²Tech COMBUSTÍVEL, Los Vega na Estrada e Marginalia; desde 29/10/2026 também
  Iconvet (iconvet.com.br), Administração Judicial Oriente (ajoriente.com), Dojo Legacy (bjj-link.com) e Ômega
  Imóveis (omega-site-vert.vercel.app, ainda sem domínio); desde 30/10/2026, o Minhocão (minhocao.linupedia.com.br) e a Trupe (em prévia, ainda sem domínio).
  Capturas em `public/img/projetos/` (960×600, WebP).
  O NeuroSim fica de fora por enquanto, até sair do começo.
- **De estudo** (`#estudo`, 29/10/2026): os sites que fiz na disciplina Desenvolvimento de Interfaces, com
  empresas fictícias: Café Aurora, Fotografia do Cerrado e Abelhas sem Ferrão. Cada cartão leva ao subdomínio e ao
  código no GitHub; as capturas também ficam em `public/img/projetos/`.
- **Como funciona** e **contato**: WhatsApp (61) 99667-2610 e `contato@linupedia.com.br`.
- **Como funciona mais detalhado, só em japonês, coreano e chinês** (bloco `{{?cjk}}` do modelo, 30/10/2026): as quatro
  etapas, os prazos e o orçamento em PDF. As chaves `detalhe_*` ficam vazias nos outros 10 idiomas. Os prazos vêm das
  chaves `prazo_*`, as mesmas do Monte o seu site, e o pagamento repete a dúvida frequente; o “1 dia útil” para responder
  já estava no contato dessas páginas. Número novo aqui, só combinado antes.
- **Quando a gente conversa** (no contato, 30/10/2026): a hora de quem visita ao lado da de Brasília, se dá para falar
  agora e, se não der, quando abre a próxima janela, na hora de quem visita e com o dia da semana. A janela é de segunda
  a sexta, das 9h às 21h em Brasília (UTC−3): para mudar, são as constantes `ABRE` e `FECHA` no `js/movimento.js` e a
  chave `conversa_janela` de cada idioma. Sai tudo do relógio do aparelho, com `Intl`, sem pedir permissão e sem guardar
  nada; o relógio só corre com o bloco na tela e a aba aberta. Sem JavaScript, fica só a janela em horário de Brasília.
- **Monte o seu site** (no contato, 22/10/2026): a pessoa escolhe o tipo, o que o site precisa ter e o plano
  mensal, e vê na hora a estimativa (a partir de), o prazo e o mensal; a mensagem do WhatsApp e do e-mail já sai
  com tudo. Os preços são os mesmos dos cartões e das dúvidas (o painel é extra de R$ 1.200 só no site de
  apresentação); o que não tem preço fixo aparece como “na proposta”. Os preços saem do
  `ferramentas/pagina/precos.json`.
- **Simulador** (`#exemplo`, 29/10/2026): o Café Aurora, uma cafeteria que não existe, embutido num `<iframe>`
  (`https://cafe.linupedia.com.br/`, que mora em `sitios/cafe-aurora/`). A pessoa liga e desliga as partes do site (depoimentos, efeitos, troca de cores, monte sua
  bebida, assinatura por e-mail, painel) e vê o site e o preço mudarem na hora: base de R$ 1.800 e cada parte com o
  seu valor no `ferramentas/pagina/precos.json`. A página manda as partes ligadas por `postMessage`
  (só para o endereço do Café, que só aceita mensagens de `https://sites.linupedia.com.br`) e avisa quando o quadro sai da tela, para as animações dele pararem. No celular, as partes
  viram uma faixa que desliza para o lado. O Café foi aliviado em 30/10/2026 (o navegador ficava ocupado o tempo
  todo, com só 4% de folga; agora sobra 69%): o fundo desenha na resolução da página e a 30 quadros, as
  partículas saem de um brilho pré-desenhado, o cursor e o halo param de regravar o estilo quando estão parados, o
  chuvisco e as linhas ficam sem mistura de camadas e sem movimento, o brilho do topo gira como camada pronta e os
  cartões desfocam menos. As versões `/bootstrap/` e `/tailwind/` ficaram como estavam.
- **Preços de referência** nos cartões de “O que fazemos”: site de apresentação a partir de R$ 1.800,
  ferramentas e painéis a partir de R$ 6.000, apps que instalam a partir de R$ 9.000 e dois planos
  mensais: **No ar** (R$ 60: servidor, HTTPS, domínio e cópias) e **Cuidado** (R$ 120: tudo isso, mais
  atualizações e pequenos ajustes); pagando o ano, são 10 meses. Clicar num dos três primeiros cartões (o cartão
  inteiro é o link do título) ou num dos planos leva ao “Conte sobre o seu site” com a opção já marcada (atributo
  `data-escolher="tipo=…"` ou `"plano=…"`, tratado no `js/movimento.js`).
- **Dúvidas frequentes** (`#duvidas`, acordeão em `<details>`): prazo estimado por tipo, pagamento
  (50/50, ou 40/30/30 a partir de R$ 6.000), mensal obrigatório, painel para o cliente editar (extra de R$ 1.200 no site de apresentação,
  incluído em ferramentas e apps), domínio no nome do cliente, conteúdo e
  dados do cliente (código, layout e visual do Linu Sites) e saída (exportação e compra do código pelo
  valor do projeto). Decidido em 22/10/2026; os termos completos estão em rascunho no `Seiabras/linuarquivos`.
- **Depoimentos:** a seção está pronta no HTML, mas escondida (`hidden`) até chegarem frases de verdade.
- **Celular:** os links vão para um menu que abre no botão ☰ (`public/js/menu.js`).
- **Compartilhar:** `img/compartilhar.png` (1200 × 630), gerada por `ferramentas/gerar-imagens.mjs`, e os ícones e a
  logo (`img/linu-logo.png`), que vêm do app pelo `ferramentas/linu-do-app.py`; `sitemap.xml` e `robots.txt` apontando para ele.
- **Modo claro e escuro:** o botão da lâmpada, no topo. O Linu entra no quarto pela porta, vai até o
  lampião e apaga (modo escuro) ou acende (modo claro); a página troca de cor junto. A escolha fica
  guardada no navegador; sem escolha, vale a do sistema. Com “reduzir movimento” ligado, troca na hora.
  Se a cena do topo estiver fora da tela, a animação aparece num cartão no canto. Código em
  `public/js/tema.js`.

## Fonte e segurança

A Nunito e as Noto ficam em `public/fontes` (licença OFL), sem Google Fonts. A página leva uma CSP numa `<meta>` (só
carrega o que é do próprio site); o `deploy/Caddyfile-bloco` traz os cabeçalhos completos, para aplicar
na VM (ver `deploy/ORACLE.md`). Desde 29/10/2026 o bloco deixa o próprio site pôr uma página dele num quadro
(`frame-ancestors 'self'` e `X-Frame-Options SAMEORIGIN`), por causa do simulador; aplicado na VM em 29/10/2026 (a
cópia anterior ficou em `/etc/caddy/Caddyfile.antes-quadro`). A porta 22 é bloqueada em algumas redes: para mexer na
VM, use outra (a do celular serviu).

## Imagens da cena

As imagens da estação e do Linu vêm do app (linupedia, `assets/pixel/`), na mesma grade de 344 × 192.
Desde 29/10/2026 o Linu é o novo do app em todo o site (o app trocou em 24/10): a logo e os ícones, o Linu que anda
na cena (frente, costas e os 4 passos de lado do mapa do linuhub, 172 × 190, com 61 de altura na cena) e o Linu
acenando da página de erro. O Linu do contato acena quando aparece na tela e pula quando alguém toca nele
(`js/movimento.js`, uma folha com 4 poses em `img/linu/linu-contato.png`). Os quadros do app vêm sem a sombra do
chão, e desde 30/10/2026 o Linu anda pelo quarto sem sombra nenhuma. Também desde 30/10, os quadros saem sem a sobra
do fundo antigo que ficava por fora do contorno preto (`sem_halo` no `linu-do-app.py`; para limpar só o que já está no
site: `python3 ferramentas/linu-do-app.py --so-limpar`). Ao apagar a luz, ele dá um pulinho para puxar a cordinha, o
quarto vira noite com o lampião aceso, o lampião falha e apaga, e só então a página escurece; ao acender, o lampião
falha e acende no escuro, a página clareia e o dia volta devagar (`js/tema.js`). `ferramentas/linu-do-app.py` copia
tudo do app de novo; depois, o
`ferramentas/gerar-imagens.mjs` refaz a imagem de compartilhar. O que é só do site fica em `ferramentas/`:

- `cena-apagada.py` gera `img/abrigo-estacao-apagada.png`, a noite com o lampião apagado (o modo escuro).
- `corrigir-porta-estacao.py` tirou o retângulo da porta e da escotilha nas imagens de noite.

## Publicar

Todo push na `main` publica sozinho: o GitHub Actions confere a página (`deploy/conferir-pagina.py`: HTML
válido e todo arquivo usado existe), manda `public/` para a VM pela chave do usuário `linusites` (segredo
`ORACLE_SSH_KEY`, refeito em 22/10/2026; a chave só pode rodar o `deploy/receber.sh`) e confere se o site
respondeu. A versão anterior fica em `/opt/linu-sites/app.anterior`. Detalhes em
[deploy/ORACLE.md](deploy/ORACLE.md).

## Documentos relacionados

- [`deploy/ORACLE.md`](deploy/ORACLE.md): DNS, Caddy, instalação e publicação.
- [`DIRETRIZES-UX.md`](DIRETRIZES-UX.md): regras de interface e desempenho (iguais em todos os projetos).
