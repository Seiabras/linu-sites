# Linu Sites

> **In English:** the site of Linu Sites, a studio for custom websites and web apps: 13 languages generated from one
> template, no dependencies and no server of its own, served by Caddy. Live: https://sites.linupedia.com.br

Site do **Linu Sites**, o estúdio de sites e aplicativos web da LinuPedia: **https://sites.linupedia.com.br**.

Uma página só (`public/index.html`), sem dependências e sem servidor próprio: o Caddy da VM da Oracle
(a mesma da LinuPedia, do v²tech, da Marginalia e do Los Vega) entrega os arquivos de `public/`.
O visual é a planta (desde 07/11/2026, à noite): a página é a prancha do arquiteto, com papel quadriculado, traço azul,
cotas e carimbo, e de noite vira o cianotipo (ver “Identidade: a planta”).

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
| `public/css/estilo.css` | Visual: a planta (papel vegetal de dia, cianotipo de noite), com as três versões (celular, tablet e computador). |
| `public/js/` | `tema-inicio.js` (aplica o tema antes de pintar), `tema.js` (a luminária: troca o tema num círculo que sai dela), `planta.js` (a planta da abertura se desenha uma vez), `linu-vivo.js` (o Linu respira e pisca), `menu.js` (o painel do celular, que sobe de baixo, e o seletor de idioma), `movimento.js` (abas, entradas ao rolar, a seção atual no menu e na barra do celular, a hora de conversar e o Monte o seu site) e `simulador.js` (o simulador do Café Aurora). |
| `public/img/` | O Linu (`linu/`: o da planta, de capacete, com o quadro de piscar; o do contato; o de frente, na capa da LinuPedia), a logo (`linu-logo.png`), capturas dos projetos (`projetos/`), ícones e imagem de compartilhar. |
| `public/fontes/` | Space Grotesk (títulos, cotas e números), Instrument Sans (texto) e as Noto de japonês, coreano e chinês (licença OFL, `OFL-*.txt` ao lado), servidas pelo próprio site. |
| `sitios/` | Os sites dos subdomínios, fora de `public/`: `cafe-aurora/` (cafe.linupedia.com.br, também com `/bootstrap/`, `/tailwind/`, `/bulma/` e `/pico/`), `fotografia-do-cerrado/` (cerrado.linupedia.com.br), `pica-nao-pica/` (picanaopica.linupedia.com.br). O Digital Linu não entra aqui: é o serviço irmão, com repositório e publicação próprios (`Seiabras/digital-linu`). Cada um tem o seu repositório público no GitHub (`Seiabras/cafe-aurora`, `Seiabras/fotografia-do-cerrado`, `Seiabras/pica-nao-pica`); mudou aqui, leve a mudança para lá. |
| `ferramentas/cafe/` | O modelo do Café Aurora (`modelo.html`) e os textos dele em cada idioma (`textos/<código>.json`), para o `gerar-cafe.mjs`. Em `ferramentas/cafe/arte/`, os pedidos das fotos do Café e da Padaria à API de imagens do Google (4/11/2026), com `aprovadas.json`; o `ferramentas/cafe/arte.py` (cópia do kit de arte do linuarquivos, `modelos/ferramentas/arte/`) leva as aprovadas para `sitios/cafe-aurora/img/` conforme o `arte/saidas.json`: `python3 ferramentas/cafe/arte.py ferramentas/cafe/arte`. |
| `ferramentas/conferir-visual.mjs` | A conferência visual que o Actions roda antes de publicar (cópia do `linuarquivos/modelos/ferramentas/`, que o `sincronizar-familia.py` mantém igual): a inicial, `/ja/` e uma página de projeto em 390, 820 e 1280 px, claro e escuro; reprova com rolagem lateral, erro no console, arquivo faltando ou falha séria de acessibilidade, e guarda as capturas como artefato. |
| `ferramentas/pagina/` | O modelo da página inicial (`modelo.html`), os textos de cada idioma (`textos/<código>.json`) e os preços de cada moeda (`precos.json`). |
| `ferramentas/fontes/` | Os caracteres que estão em cada fonte Noto (`ja.txt`, `ko.txt`, `zh-hant.txt`), escritos pelo `gerar-fontes.mjs`. |
| `ferramentas/` | Geradores: a página em cada idioma (`gerar-idiomas.mjs`), as fontes Noto (`gerar-fontes.mjs`), páginas de projeto, imagem de compartilhar e capas do portfólio (`capas/`), cena noturna e o Linu trazido do app (`linu-do-app.py`). |
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
  euro também no Reino Unido e o recebimento pela Wise. Em 2/11/2026 baixei o euro: apresentação a partir de 700 €, ferramentas e
  painéis 2.000 €, aplicativos 3.500 €, plano Online 15 €/mês e Cuidado 35 €/mês (os extras ficaram como estavam).
  Ainda em 2/11, os extras em euro caíram na mesma proporção do site (700/1.500: painel 280 €,
  depoimentos 70 €…) e o dólar acompanhou: apresentação US$ 750, ferramentas 2.200, apps 3.750,
  Online 17 e Cuidado 41 por mês, extras × 750/1.600, arredondados de 10 em 10.
- **Capturas do portfólio:** toda captura mostra a tela principal ou o menu do site, nunca uma cena de dentro (regra de
  30/10/2026; a LinuPedia entra pela Lista, o Minhocão pela tela inicial). Tamanho 960 × 600, em WebP, em
  `public/img/projetos/`.
- **Regiões (30/10/2026):** cada idioma diz a sua região no JSON (`"regiao"`: `brasil`, `europa` ou `asia`, e
  `"padrao": true` na página que representa a região; `"hreflang_extra"` para outros códigos que a página atende, como
  `en-IE` no inglês europeu e `zh-TW`/`zh-HK` no chinês). O seletor agrupa por região. A **Ásia-Pacífico e
  internacional** tem o inglês internacional (`/intl/`, em dólar, que também é o `x-default`), o japonês (`/ja/`), o
  coreano (`/ko/`) e o chinês tradicional (`/zh-hant/`), com fonte Noto própria para esses três (a Instrument Sans não tem os
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
  preso, alvos de pelo menos 24 × 24 px e, com “menos movimento”, nada se mexe (a troca de luz fica só na opacidade e na cor). Para isso, em 30/10 subiram os
  contrastes das abas e das áreas e do número dos passos, o anel de foco ficou azul-claro nas partes escuras e por
  dentro da captura dos projetos, e o topo preso não cobre mais o que recebe foco (`scroll-padding-top`).
- **O Café Aurora não fica mais de fora** (31/10/2026): o rodapé subiu para o `--muted` (antes 3,7:1), o link do rodapé
  ganhou sublinhado, os títulos do rodapé viraram `h3` e todo link e botão solto tem pelo menos 24 px (`estilo.css`, bloco
  “Alvos de toque”). Conferido com o axe 4.10, de dia e de noite, sem nenhuma falha, nas três versões; a frase que deixava o
  Café de fora saiu dos 8 idiomas. Mudou a página a ponto de um item deixar de valer, tire o item do texto nos 8 idiomas.

- **Privacidade** (`europa_priv_titulo`, `europa_priv_texto`): diz que o site não tem cookies, rastreador, CDN nem Google
  Fonts e que o tema e o idioma escolhidos ficam só no navegador. Conferido em 30/10/2026: nenhum `Set-Cookie` nem
  `document.cookie`, nem na página nem no Café; nenhum script, folha, fonte ou imagem de outro endereço nas páginas
  geradas (o único endereço de fora que carrega é o `cafe.linupedia.com.br`, no quadro do simulador, na mesma VM); o DNS
  aponta direto para a VM, sem CDN; e a CSP, na `<meta>` e no cabeçalho do Caddy, só libera o próprio site e o Café.
  O que fica no navegador é o `localStorage` (`tema`, `idioma`, `idioma-aviso` e, no Café do simulador, `aurora-modo`; o
  Café aberto no próprio endereço guarda também o pedido, as reservas e os carimbos, ver “O Café Aurora em cada idioma”). Antes de pôr
  qualquer coisa de terceiro no site, mude esse texto nos 8 idiomas. Ele fala **deste site**, não dos sites dos clientes.

## Fontes de japonês, coreano e chinês (30/10/2026)

As páginas `/ja/`, `/ko/` e `/zh-hant/` usam a Noto Sans CJK (licença OFL, `public/fontes/OFL-Noto.txt`) cortada só com os
caracteres que elas usam, servida de `public/fontes/`, sem CDN. São dois pesos por língua, 400 e 700, e as outras páginas
não baixam nada disso: as famílias só entram no `--texto` dessas línguas, no `css/estilo.css`.

| Língua | Caracteres | Regular + Bold |
|---|---:|---:|
| Japonês | 769 | 211 KB |
| Coreano | 598 | 81 KB |
| Chinês tradicional | 956 | 313 KB |

- **Refazer:** nada a fazer na hora. O `node ferramentas/gerar-idiomas.mjs` compara os caracteres das páginas com o
  `ferramentas/fontes/<pasta>.txt` e refaz a fonte que mudou; depois, suba o `?v=` dela no `css/estilo.css` e o do
  `estilo.css` nos modelos. Entram o HTML das páginas (com os textos dos scripts), o `content` do CSS e os dias da semana
  que o `Intl` escreve nos relógios do contato. `node ferramentas/gerar-fontes.mjs --tudo` refaz todas.
- **O que precisa:** a Noto Sans CJK em `/usr/share/fonts/noto-cjk` (pacote `noto-fonts-cjk` do Arch, ou `NOTO_CJK=<pasta>`)
  e o `pyftsubset`, com o brotli. O gerador procura em `PYFTSUBSET`, no `PATH` e no ambiente separado que uso aqui:
  `python3 -m venv ~/.local/share/linu-sites-fontes && ~/.local/share/linu-sites-fontes/bin/pip install fonttools brotli`.
  Sem eles, o gerador avisa e segue: a página sai normal, e o caractere novo aparece na fonte do aparelho.
  Sem o pacote do Arch (numa sessão na nuvem, por exemplo), os dois `.ttc` saem de
  `https://raw.githubusercontent.com/notofonts/noto-cjk/main/Sans/OTC/NotoSansCJK-{Regular,Bold}.ttc` para uma pasta
  qualquer, apontada pelo `NOTO_CJK` (foi assim em 31/10/2026).
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
- Desde 1/11/2026, as versões Bootstrap e Tailwind também saem em cada idioma (`/<pasta>/bootstrap/` e
  `/<pasta>/tailwind/`), dos modelos `ferramentas/cafe/modelo-bootstrap.html` e `modelo-tailwind.html`, com os mesmos
  textos; os scripts delas leem o mesmo `#textos-cafe`. A página `versoes.html` (só em português, para a disciplina)
  compara as três: o peso de cada uma, o mesmo cartão nos três jeitos e quando usar cada um.
- **Cinco versões e a troca entre elas (1/11/2026):** além do CSS puro, do Bootstrap e do Tailwind, o Café tem a
  versão Bulma 1.0 (`modelo-bulma.html`, a compilação com prefixo `bulma-` e sem os utilitários, em
  `sitios/cafe-aurora/bulma/vendor/`) e a Pico CSS 2 (`modelo-pico.html`, quase sem classes, em
  `sitios/cafe-aurora/pico/vendor/`). O `VERSOES` do `gerar-cafe.mjs` lista as quatro. Todo rodapé tem a mesma lista
  (`.versoes-troca`), que leva de qualquer versão para qualquer outra, no mesmo idioma, com a atual marcada. A
  `versoes.html` explica o que muda entre o puro e cada framework (tabela de ideia, layout, HTML, peso, tema, o que
  quebrou) e compara o peso comprimido: puro 40 KB, Bootstrap 83, Tailwind 30, Bulma 63, Pico 41. As chaves novas
  (`v_rotulo`, `css_puro`, `comparar`) estão nas 13 línguas; a `versoes.html` continua só em português.
- **A abertura do Café (1/11/2026):** a exceção “abertura de identidade” da `DIRETRIZES-UX.md` (seção 1): uma vez por
  sessão (`inicio.js` v3 põe `ja-abriu` no `<html>`), 3 s contados pelo script de cada versão, pular com toque, botão
  ou tecla (chave `pular_abertura`), parada com “menos movimento”.
- **O Café “de verdade” (1/11/2026):** pedido com quantidades e a mensagem pronta para o WhatsApp (o Café é fictício: o
  WhatsApp abre sem número), filtros e detalhes do cardápio (de noite e de dia), o teste “Que bebida combina com você?”,
  reserva de mesa com validação na hora (a hora respeita o horário do café e da padaria) e o cartão de carimbos (um por
  pedido mandado). Fica no `localStorage` do navegador (`aurora-pedido`, `aurora-carimbos`, `aurora-reservas`,
  `aurora-nome`). Tudo isso fica escondido quando o Café está embutido no simulador (classe `embutido`, bloco 15 do
  `script.js` e `.so-completo` no CSS): o simulador só mostra o que tem preço na tabela dele.
- **Sem internet:** o `gerar-cafe.mjs` também grava o `sitios/cafe-aurora/sw.js`, com a versão tirada dos arquivos (mudou
  o CSS ou o script, rode o gerador de novo); o `manifest.webmanifest` e os ícones ficam em `sitios/cafe-aurora/`. O
  bloco do Café no `deploy/Caddyfile-bloco` manda `no-cache` para o `sw.js` e o manifesto.
- **Café e padaria com as mesmas partes (regra 9, 1/11/2026):** de dia, o cardápio também tem quatro detalhes (forno,
  peso, kcal, alérgenos) e seis filtros (o novo é “vegano”), e o pedido fala da padaria. As versões Bootstrap e Tailwind
  ganharam a padaria (o botão de sol e lua, os textos de dia, o pão do “Monte o seu pão” e a farinha no ar) com dois
  arquivos que as duas usam, `sitios/cafe-aurora/padaria.css` e `padaria.js`; os textos de dia entraram nos modelos
  delas pelo mesmo `so-noite`/`so-dia` da versão principal.
- **Os módulos novos no simulador (1/11/2026):** pedido com carrinho (R$ 800), cardápio com filtros e detalhes (R$ 300),
  teste “o que combina com você” (R$ 300), reserva de mesa (R$ 600) e cartão fidelidade (R$ 400), com os valores em euro
  e dólar no `precos.json`. No Café, cada um vira uma classe `sem-...` (lista `MODULOS` do `script.js`); começam
  desligados e, com o pedido desligado, o “Pedir agora” volta a levar ao laboratório.
- **Nas 13 línguas (1/11/2026, a leva da regra 8):** depois do português aprovado, as linhas novas do simulador viraram
  chaves (`simulador_pedido`, `simulador_cardapio`, `simulador_teste`, `simulador_reservas`, `simulador_fidelidade`) e
  os textos novos do Café (`i_peso`, `d_f_vegano`, `d_p_vazio`, `d_p_nota`, `d_dim_hint`, `d_ficticia`, `v_rotulo`,
  `css_puro`, `comparar`, `pular_abertura` e o `d_titulo` dos `js`) entraram nos 12 `textos/*.json`. O Café sai nas 13
  línguas e nas cinco versões (65 páginas) com `node ferramentas/gerar-cafe.mjs`.
- **Abertura de identidade no simulador (2/11/2026, só em pt por enquanto, regra 8):** módulo de R$ 300 (€ 100,
  $ 110 no `precos.json`, já nas três moedas) num bloco `{{?pt-BR}}` do `ferramentas/pagina/modelo.html`. Ao ligar,
  aparece a duração (1,5 s, o padrão de site de cliente nas diretrizes, ou 3 s) e o Café mostra uma prévia
  (`{cafeAurora: {verAbertura: ms}}`, função `previaAbertura` do `script.js` e classe `previa-abertura`); o botão
  “Ver a abertura” repete. A vinheta para os sites de cliente fica pronta no `linu-modelo` (`vinheta.js`).
- **O simulador acompanha o modo do Café (1/11/2026):** o Café avisa a página por `postMessage` se está de noite ou de
  dia (no “pronto” e a cada troca); o `js/simulador.js` troca os textos marcados com `data-modo-texto` (a frase da
  seção, “Monte sua bebida” → “Monte seu pão”, os efeitos, a barra, o título do quadro e o crédito) pelo
  `data-dia` de cada um (chaves `simulador_dia_*`, nas 13 línguas; antes era um bloco `#simulador-dia` só em pt). O
  Café também troca o título da aba, o rodapé (“Padaria fictícia”) e a dica do painel de cores de dia (`d_titulo`,
  `d_ficticia`, `d_dim_hint`).
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
`picanaopica.linupedia.com.br/<idioma>/…`), com os idiomas no rodapé, e os cartões da página principal levam à versão no
mesmo idioma. Tudo sai de um modelo por página:

```bash
node ferramentas/gerar-estudo.mjs fotografia-do-cerrado
node ferramentas/gerar-estudo.mjs pica-nao-pica
```

- O texto muda no `ferramentas/estudo/<site>/textos/<código>.json`. O HTML em português foi transformado em modelo pelo
  `ferramentas/estudo/extrair.py` (cada bloco de texto vira uma chave inteira, com a marcação de dentro da frase); se
  mudar o HTML de uma página, mude no `ferramentas/estudo/<site>/modelo/`.
- As frases dos scripts (o formulário do Cerrado; o percurso e as 5 perguntas do teste das Abelhas) vão no
  `<script type="application/json" id="textos-estudo">` (desde 04/11/2026 sem cópia em português no código).
- **Modo claro e escuro**: botão no cabeçalho (`js/tema.js`, e `js/tema-inicio.js` no `<head>` para não piscar), com as
  cores por função no CSS. No escuro, os contrastes passam do AAA (medidos: texto do Cerrado 16,1:1, do teste das
  Abelhas acima de 7,5:1). Os CSS e scripts levam `?v=`: mudou um deles, suba o número no modelo (o CSS está em `?v=3`
  desde 31/10/2026).
- **O que entrou em 31/10/2026:** nas Abelhas, a página `criar.html` (“Posso criar?”: como começar, o mel e o que não
  fazer), aberta pelo cartão “Posso criar?” da inicial, e um `h1` no percurso; no Cerrado, as perguntas frequentes no fim
  das Expedições (`<details>`, sem JavaScript), o nome de cada foto da galeria como `h2` e a paleta do Sobre legível no
  modo escuro. Nos dois, os links do rodapé com 24 px de altura. O axe 4.10 não acha nenhuma falha em nenhuma página, nos
  dois modos.
- **O Cerrado como caderno de campo (31/10/2026):** títulos e nomes científicos na Newsreader (em `fontes/`), fotos sem
  caixa, os números em tipografia grande, o “Quando ir?” nas Expedições (`js/quando.js`; as frases em `js` do JSON, os
  meses pelo `Intl`), a foto ampliada com anterior e próxima e fotos em WebP com versão de 640 px. Detalhes no README de
  `Seiabras/fotografia-do-cerrado`.
- **Só em português por enquanto (31/10/2026):** o `gerar-estudo.mjs` gera só em pt-BR as páginas listadas em
  `ferramentas/estudo/<site>/so-pt.json` (sem alternativas nem lista de idiomas) e põe só na página em pt-BR o que estiver
  entre `{{?pt-BR}}` e `{{/pt-BR}}` num modelo. O Cerrado usa os dois (fichas, diário, mapa, testador de contraste); a
  lista está no README de `Seiabras/fotografia-do-cerrado`. Para traduzir, ver “Traduzir o guia novo” logo abaixo.
  **O Cerrado virou o Guia do Cerrado** (31/10/2026, pedido de “o site mais completo sobre o cerrado do mundo”; o nome novo vale
  em português, e as outras línguas ficam com “Fotografia do Cerrado” até a tradução, pela chave `cerrado_nome`): em português, a
  inicial e o menu são os do guia, com as páginas “O bioma” (mapa dos biomas do IBGE 2019, quanto de cada estado é Cerrado,
  clima, solo, fogo), “Paisagens” (as 11 fitofisionomias de Ribeiro e Walter num corte desenhado) e “Fontes”. Saem do
  `guia-pt.py` (rodar depois do `paginas-pt.py`); o mapa, do `biomas.py`. `{{!pt-BR}}…{{/!pt-BR}}` num modelo entra em todas
  as línguas menos o português: é o que mantém a inicial e o menu antigos nas outras 12 até a tradução.
  As fichas, o diário, “Como fotografamos” e a 404 do Cerrado saem do `ferramentas/estudo/fotografia-do-cerrado/paginas-pt.py`
  (mude o texto lá e rode antes do `gerar-estudo.mjs`); o mapa das Expedições, do `mapa.py` da mesma pasta.
  Fotos novas entram sozinhas: `img/especies/<id>.webp` e `<id>-640.webp` (com o crédito em `img/especies/creditos.json`) no
  catálogo, e `img/paisagens/<id>…` nas fichas das paisagens; a série do desmatamento fica no `prodes.json`.
  **Em 1/11/2026:** o catálogo passou a 114 espécies, todas com ficha (dicionário `FICHAS` do `guia-pt.py`, as fontes
  numeradas até 154); as fichas têm “Não confunda com” (lista `PARES`), o Aprender ganhou o jogo “Qual é esta espécie?”
  (pistas tiradas das fichas) e há duas páginas novas, “O Cerrado mês a mês” (lista `EVENTOS`) e “Como ajudar” (lista
  `ACOES`). Para caber no orçamento de DOM, os ícones do catálogo são um `<svg>` com `<use>` (os desenhos ficam uma vez
  só, em `icones_defs()`). No tablet, o menu de 8 itens do guia vira o botão “Menu” até 1099 px (regra por `:has()`).
- **Traduzir o guia novo (04/11/2026):** o texto em português escrito direto nos modelos (as páginas de `so-pt.json` e
  os trechos `{{?pt-BR}}`) se traduz por um catálogo por língua, guardado pelo próprio texto em português, sem chave
  inventada: mudar o pt-BR nos `.py` não exige mexer em nada. Os passos, para uma língua:
  1. Rode os `.py` do site e depois `node ferramentas/estudo/trechos.mjs <site>`. Ele junta os trechos (blocos de texto
     com a marcação de dentro da frase, o texto solto, `<title>`, `alt`, `title`, `aria-label`, `placeholder`, `label`,
     `data-texto`, `data-nome`, `data-busca`, o `content` da descrição e das metas de compartilhar, a mensagem do
     WhatsApp, os textos dos blocos JSON e do `data-parques`, e as frases dos scripts) e põe em dia
     `ferramentas/estudo/<site>/traducoes/<código>.json`: `{"pronto": false, "trechos": {"<português>": "<tradução>"}}`.
     O que é novo entra vazio, o que sumiu sai, e ele diz quanto falta em cada língua. Rodar de novo não muda nada.
  2. Preencha os trechos daquela língua. A ordem é a das páginas (a inicial, depois em ordem alfabética, as frases dos
     scripts no fim); onde cada trecho aparece está em `traducoes/onde.json` (gerado, não se edita). Mantenha a
     marcação (`<a href…>`, `<sup…>`) e os `{n}`, `{total}`… como estão; o mesmo texto em português tem uma tradução só
     no site inteiro (é assim que o filtro “Espécies” da busca continua batendo com o índice).
  3. Confira também os `textos/<código>.json` daquela língua: as `{{chave}}` de fora dos trechos entram com eles (por
     exemplo, `cerrado_nome` ainda diz “Fotografia do Cerrado” nas outras línguas).
  4. Ponha `"pronto": true` e rode `node ferramentas/gerar-estudo.mjs <site>`. A língua passa a sair no sabor pt-BR (os
     `{{?pt-BR}}` entram e os `{{!pt-BR}}` saem) e ganha as páginas de `so-pt.json`; essas páginas passam a ter
     `hreflang` e a lista de idiomas com o pt-BR e as línguas prontas (a lista entra no começo do rodapé quando o
     modelo não tem `{{idiomas}}`). O `og:url`, o `data-url` e o endereço da mensagem do WhatsApp vão para a pasta da
     língua. Como nas 6 páginas compartilhadas, o guia sem internet (manifesto e `offline.js`) fica só no pt-BR. A 404
     do Cerrado (sem `{{lang}}`) fica só em português. Língua marcada pronta com trecho vazio, ou com trecho que não
     está no catálogo, para o gerador com a lista; língua não pronta sai exatamente como antes, e as páginas só-pt
     dela que tiverem sobrado de uma rodada anterior são apagadas.
  - **Os scripts:** as frases do guia novo que os `js/*.js` montam saíram do código e ficam em
    `ferramentas/estudo/<site>/scripts-pt.json`, um grupo por script (`{"guia": {"chave": "texto"}}`, com `{n}` e afins
    no lugar dos números). O gerador põe cada grupo no `#textos-estudo` das páginas no sabor pt-BR que carregam
    `js/<grupo>.js`, traduzido pelo mesmo catálogo. Os meses e os números saem do `Intl`, no `lang` da página. Os
    scripts das páginas compartilhadas (`teste.js`, `percurso.js`, `galeria.js`, o “obrigado” do `contato.js`) usam só
    as chaves `js` dos `textos/<código>.json`, sem cópia em português no código.
  - **Os números (04/11/2026):** o Pica tem 1.466 trechos únicos para traduzir (13.800 palavras) e o Cerrado, 4.123
    (41.890 palavras), por língua. Nenhuma está traduzida ainda.
- **As fotos do Guia do Cerrado (4/11/2026):** 111 das 114 espécies, 8 das 11 paisagens e os 3 parques das Expedições têm
  foto real do Wikimedia Commons (só CC0, CC BY, CC BY-SA e domínio público; bicho livre; espécie conferida olhando), em
  `img/especies/` (`<id>.webp` 1000 px, `-640` e `-144` quadrada) e `img/paisagens/`, com o crédito em `creditos.json` e
  na ficha. O que ficou sem foto e por quê, e as que vale conferir, está em
  `ferramentas/estudo/fotografia-do-cerrado/fotos-04-11.md`. Com elas, o guia sem internet passou a guardar uns 20 MB
  (`LIMITE` do service worker calculado pelo número de endereços). Para baixar mais: `modelos/ferramentas/commons.py`
  do linuarquivos, e depois `acervo/juntar.py` lá.
- **As Abelhas viraram o “Pica ou Não Pica?”** (1/11/2026, pedido de “o melhor site de reconhecer animais venenosos ou
  não”; nome provisório, as abelhas continuam dentro): em português, a inicial e o menu são os do guia, com “Que bicho
  é?” (perguntas em árvore até o bicho), “Bichos” (27 fichas com busca e filtros de grupo e perigo), “Socorro” (192, 193,
  0800 722 6001 e o que fazer em cada picada), “Mitos” (17 mitos e o jogo “Verdade ou mito?”) e “Fontes” (31). Tudo sai do
  `ferramentas/estudo/pica-nao-pica/guia-pt.py` (listas `B`, `ARVORE`, `MITOS`, `PARES`, `FONTES`; rodar antes do
  `gerar-estudo.mjs`), com o script `js/guia.js`. As outras 12 línguas seguem com o site das Abelhas até a tradução, pelo
  mesmo `{{!pt-BR}}` do Cerrado. O CSS das Abelhas está em `?v=7` e o script em `guia.js?v=2`.
  **Na noite de 1/11, as 17 ideias:** o botão “Fui picado” no topo de toda página (`emergencia.html`), o “Cartão para o
  hospital” (`cartao.html`, guardado só no navegador), “Onde tem soro” (`soro.html`, com o hospital da cidade guardado),
  “Qual é a diferença?” (`diferencas.html`: os pares desenhados em SVG e um jogo), “Prevenir” (`prevenir.html`: o teste
  da casa, crianças, cães e gatos, a época), “Os números” (`numeros.html`, 2023), o jogo “Pica ou não pica?”
  (`jogo.html`), “Para a escola” (`escola.html`, para imprimir), a porta “Aprender” no menu, filtros por lugar e região
  (com o mapa do `regioes.py`), o botão do WhatsApp e a imagem de compartilhar de cada ficha (`img/compartilhar/`), a
  data da revisão e o guia sem internet (`sw.js`, `manifest.webmanifest`, `js/offline.js`, copiados do modelo do Cerrado).
  As fotos dos bichos entram sozinhas quando existirem em `img/bichos/<id>.webp` (com `-640` e `creditos.json`). O
  Guia do Cerrado ganhou a sua página “Para a escola” (`escola.html`, CSS `?v=25`).
  **Terceira leva (1/11, noite):** 37 bichos (jararacuçu, caninana, cobra-cipó, cobra-de-duas-cabeças, escorpião-preto
  da Amazônia, aranha-de-grama, ouriço-do-mar e o grupo novo “Transmitem doença”: barbeiro, carrapato-estrela e
  caramujo-africano), 57 fontes, o “Que bicho é?” começando por “Onde você está?” (cada resposta sabe que bichos alcança),
  e no “Fui picado” os botões “Ouvir os passos” (a voz do aparelho), “Avisar alguém” (WhatsApp com o bicho, a hora, o
  hospital e, se a pessoa quiser, a localização; por isso o bloco das Abelhas no `Caddyfile-bloco` tem
  `geolocation=(self)`) e “O que dizer ao telefone”. No Prevenir, “Antes da trilha”; no jogo, o modo “Peçonhento ou
  venenoso?” e o modo turma. CSS em `?v=8` e `guia.js?v=3`.
- **O Pica ou Não Pica? com fotos e a interface nova (4/11/2026):** 36 dos 37 bichos têm foto real do Commons (o
  carrapato ficou sem: não há foto de campo com identificação segura), em `img/bichos/` (`<id>.webp`, `-640` e `-240`
  quadrada), crédito em `creditos.json`; a lista e as que vale conferir em
  `ferramentas/estudo/pica-nao-pica/fotos-04-11.md`. A interface: a abertura com quatro bichos e a resposta (fileira
  no celular e no tablet, 2 × 2 ao lado do título no computador), o catálogo com miniatura e selo curto, “Mais filtros”
  recolhido no celular e aberto no computador, a ficha com a foto ao lado do nome no computador; “Posso criar?” e o
  “Teste rápido”, que tinham ficado sem link em português, ligados na inicial. O `guia-pt.py` cai para a Noto quando
  não há a DejaVu e não refaz as imagens de compartilhar sem ela, e a inicial não ganha mais uma linha em branco a
  cada rodada.
- **A parte das abelhas, arrumada (4/11/2026):** em português, as abelhas deixam de ser um bloco à parte e entram no guia.
  “Achei um… e agora?” (`achei.html`, lista `ACHEI`): sete situações (ninho de jataí, enxame de africanizada, ninho de
  vespa, escorpião em casa, cobra no quintal, taturana, carrapato), cada uma com o que fazer agora, quem chamar, o que
  nunca fazer e a ficha; entra no Aprender, na inicial, no Socorro, no catálogo, no fim do “Que bicho é?” e no botão
  “Achou um? O que fazer” das fichas (dicionário `ACHOU`). Em português, `achei-um-ninho.html` abre com um aviso que leva
  para `achei.html#jatai`. No “Qual dos dois?” (`diferencas.html`), a rodada “Abelhas e vespas” (`ABELHAS_PARES`: quatro
  pares, com pistas a mais; também por `diferencas.html?rodada=abelhas`, recorde à parte). Na inicial, “Os injustiçados”
  (`INJUSTICADOS`, cada frase com fonte; a falsa-coral só com o aviso de se afastar) no lugar de “E as abelhas sem
  ferrão?”, com o link para `bichos.html?perigo=nenhum`. “De onde veio este guia” (`origem.html`) conta o projeto do CEUB
  e leva às páginas antigas (descobrir, criar, teste); o rodapé em português aponta para ela. Fontes novas 63 a 67
  (Bombeiros do CE, MS e MT, Saúde de Goiás, Embrapa). O CSS em português está em `?v=11` (`CSS_PT` no `guia-pt.py`)
  e as outras 12 línguas seguem com o `?v=10` do modelo, byte a byte iguais; o script em `guia.js?v=5`.
- **A 404 do Cerrado** (`sitios/fotografia-do-cerrado/404.html`) só aparece depois de o bloco novo do `deploy/Caddyfile-bloco`
  (`handle_errors` no `cerrado.linupedia.com.br`) ser posto na VM, como diz o `deploy/ORACLE.md`.
- **Links quebrados** (04/11/2026, `.github/workflows/links.yml`, com o lychee): a cada push que mexe nos sites, os links entre
  as páginas, sem internet, e o push falha se algum quebrar; toda segunda, as fontes e as fotos de fora, com o resultado no
  resumo da execução (não falha).
- Os repositórios `Seiabras/fotografia-do-cerrado` e `Seiabras/pica-nao-pica` recebem uma cópia de
  `sitios/<site>/` a cada mudança (o README e o CLAUDE.md de lá não vêm daqui).
- **O nome `pica-nao-pica`** (04/11/2026): a pasta, o repositório e o gerador se chamavam `abelhas-sem-ferrao`. Na VM 1, o
  `deploy/trocar-pasta-pica-nao-pica.sh` roda uma vez, antes do primeiro push com o nome novo: aponta o Caddy para a pasta
  nova e leva `/projetos/abelhas-sem-ferrao` (em qualquer língua) para `/projetos/pica-nao-pica`. O bicho
  `abelha-sem-ferrao` (a jataí, no singular) continua com esse nome: é um dos 37 bichos do guia.

## O que tem na página

- **A faixa da família (07/11/2026):** no alto, “Parte da família Linu, com …”, levando para a Família Linu
  (https://familia.linupedia.com.br). Todos os irmãos apontam para lá, e não mais um para o outro.
- **Identidade visual** (desde 07/11/2026): mora na Família Linu (https://familia.linupedia.com.br/identidade). O
  `/identidade` daqui leva para lá (um `redir` no `deploy/Caddyfile-bloco`), e o rodapé em pt-BR tem a nota “Da
  Família Linu · Identidade visual”. A fonte das decisões continua o `IDENTIDADE-LINU.md` do linuarquivos.
- **Abertura:** o que o estúdio faz, o botão de orçamento e a prancha com o site em três vistas, o Linu de capacete e
  o carimbo, que é o índice das seções (ver “Identidade: a planta”).
- **O que fazemos:** sites de apresentação, ferramentas e painéis, apps que instalam, hospedagem, em fichas de detalhe
  com marcas de corte nos cantos. Desde 07/11/2026, cada ficha tem um ícone em pixel art desenhado para o site (a janela, o painel, o celular e o lampião, numa
  grade de 16 × 16, em SVG no `ferramentas/pagina/modelo.html`), no lugar dos emojis; no tablet, os quatro ficam em 2 × 2.
  Também saíram as maiúsculas espaçadas (sobretítulo, etiquetas, regiões do menu de idiomas e rótulos do Monte o seu
  site e da conversa): os textos aparecem como estão escritos, seguindo o `IDENTIDADE-LINU.md` do linuarquivos.
- **Página de cada projeto** (`/projetos/linupedia`, `/v2tech`, `/losvega`, `/marginalia`, `/minhocao`, `/trupe`, `/iconvet`,
  `/ajoriente`, `/dojo-legacy`, `/omega`, `/barreto` e, desde 31/10/2026, os de estudo: `/cafe-aurora`,
  `/fotografia-do-cerrado` e `/pica-nao-pica`): o desafio, o que foi feito e como funciona por dentro, com os fatos
  dos READMEs de cada repositório (nos cinco de clientes, do que o próprio site mostra no ar). Em todos os idiomas da página
  (`/<pasta>/projetos/<nome>`), geradas pelo `ferramentas/gerar-idiomas.mjs` junto com a inicial: o modelo é o
  `ferramentas/projetos/modelo.html`, o nome, o endereço e a captura ficam no `ferramentas/projetos/projetos.json` e
  o texto de cada idioma no `ferramentas/projetos/textos/<código>.json`. Um projeto com `"codigo"` no `projetos.json`
  ganha o botão “Código no GitHub” ao lado do “Abrir”, e um `"url"` no texto do idioma troca o endereço do botão (os
  sites de estudo abrem no mesmo idioma; a etiqueta, o resumo e o alt são os do cartão). No computador, o `python3 -m
  http.server` não completa o `.html` como o Caddy; abra `projetos/<nome>.html`.
- **Projetos** (`#projetos`): duas abas lado a lado, “No ar” e “De estudo” (`js/movimento.js`, com setas, Home e
  End). O endereço com `#estudo` abre a segunda; sem JavaScript, as duas listas aparecem uma embaixo da outra.
  Por cima das abas, as **áreas** (30/10/2026): Educação e cultura, Saúde e serviços, Comércio e turismo, Indústria e
  Jogos. Elas filtram as duas listas, a conta de cada aba acompanha e, se a aba aberta ficar vazia, abre a outra. As
  áreas de cada projeto ficam no `data-areas` do `ferramentas/pagina/modelo.html` (pode ter mais de uma).
- **No ar:** LinuPedia, V²Tech COMBUSTÍVEL, Los Vega na Estrada e Marginalia; desde 29/10/2026 também
  Iconvet (iconvet.com.br), Administração Judicial Oriente (ajoriente.com), Dojo Legacy (bjj-link.com) e Ômega
  Imóveis (omega-site-vert.vercel.app, ainda sem domínio); desde 30/10/2026, o Minhocão (minhocao.linupedia.com.br) e a Trupe (em prévia, ainda sem domínio); e a Barreto Jiu-Jitsu (barreto-site-ashy.vercel.app, em prévia, ainda sem domínio), na área
  Saúde e serviços.
  Capturas em `public/img/projetos/` (960×600, WebP). A LinuPedia, o Minhocão e a Trupe não têm uma página de abertura que
  sirva de capa, então desde 31/10/2026 usam uma capa feita para o portfólio: o abrigo do Linu, a imagem de compartilhar
  do jogo e o cartaz com os bilhetes do mural (sem o crédito que a imagem da Trupe leva). As fontes dessas capas ficam em
  `ferramentas/capas/`, com a arte dos repositórios vizinhos: `node ferramentas/gerar-imagens.mjs capas` refaz. Trocou a
  imagem, suba o `?v=` dela no modelo da página e no `projetos.json` (imagem fica 7 dias em cache) e troque o texto
  alternativo nos 13 idiomas.
  O NeuroSim fica de fora por enquanto, até sair do começo.
- **De estudo** (`#estudo`, 29/10/2026): os sites que fiz na disciplina Desenvolvimento de Interfaces, com
  empresas fictícias: Café Aurora, Fotografia do Cerrado e Abelhas sem Ferrão. Cada cartão leva à página “Como foi
  feito” (desde 31/10/2026), ao subdomínio e ao código no GitHub; as capturas também ficam em `public/img/projetos/`.
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
- **Celular:** os links vão para um painel que sobe de baixo, aberto pelo botão ☰ do topo ou pela barra do polegar
  (presa embaixo, com a seção atual e o “Pedir orçamento”) (`public/js/menu.js`).
- **Compartilhar:** `img/compartilhar.png` (1200 × 630), gerada por `ferramentas/gerar-imagens.mjs`, e os ícones e a
  logo (`img/linu-logo.png`), que vêm do app pelo `ferramentas/linu-do-app.py`; `sitemap.xml` e `robots.txt` apontando para ele.
- **Modo claro e escuro:** a luminária da prancheta (pixel art), no topo. Apagar a luz mostra o cianotipo; acender
  volta ao papel. A troca abre num círculo que sai da luminária (View Transitions); sem suporte ou com “reduzir
  movimento”, as cores só passam devagar. A escolha fica guardada no navegador; sem escolha, vale a do sistema
  (`public/js/tema.js`).

## O registro dos pedidos (07/11/2026, só em português por enquanto)

No “Monte o seu site” da página em português há o bloco **Quem pede** (nome, negócio e cidade, e uma mensagem
opcional). Nome e negócio entram no começo da mensagem do WhatsApp e do e-mail e são pedidos antes de abrir os dois;
ao tocar, a página manda o pedido para `/api/pedido` por `sendBeacon`, sem atrasar nada. O Caddy encaminha para o
`linu-pedidos` (linuarquivos/servidor), que guarda por 12 meses e avisa por e-mail, como no Digital e no Seguro. O
aviso de privacidade fica embaixo dos botões e o campo escondido `site_extra` separa os robôs (`js/movimento.js`).
As outras 12 línguas ganham o bloco depois da aprovação (regra 8). **Falta no servidor:** trocar o bloco
`sites.linupedia.com.br` do `/etc/caddy/Caddyfile` pelo de `deploy/Caddyfile-bloco` (o `handle /api/pedido`) e
recarregar o Caddy; até lá a mensagem sai igual e só o registro não acontece.

## Identidade: a planta (07/11/2026)

A primeira identidade própria (a estação por dentro, de 07/11 de manhã: madeira, lona, cortiça, papel bege, verde e
laranja, máquina de escrever) ficou carregada e parecida com o caderno de expedição da LinuPedia; o dono não gostou.
No mesmo dia ela foi trocada pela **planta**: o estúdio desenha o site antes de construir, e a página inteira é a
prancha do arquiteto. Nenhum irmão usa esse visual (o Digital é a ilha de edição, o Seguro os blocos de gelo, o Farol
a torre, a Família a carta náutica), e o azul do traço é o azul da família.

- **Papel e cianotipo.** De dia (modo claro), o papel vegetal `#F3F7FC` quadriculado (grade de 24 px, linha forte a cada
  120) com tinta azul `#2563EB`; o texto é o azul-tinta `#0F2547` (14:1). De noite (modo escuro), o **cianotipo**: o azul
  da planta `#0C2A5B` com traço branco. O **marca-texto** amarelo (`#FDE047`) é a única cor de fora: sublinha a palavra
  importante do título no papel e vira a cor da palavra no cianotipo. O botão é o azul fundo `#1D4ED8` (6,7:1 com o
  branco); no escuro, branco com texto azul.
- **Abertura = a prancha.** O site desenhado em três vistas, em SVG no modelo (computador 1280, tablet 820 e celular
  390, com as cotas e as notas 1, 2 e 3), que se desenha uma vez ao abrir como num plotter (`js/planta.js`, uns 2 s; sem
  JavaScript, com “menos movimento” ou com `?static=1`, já vem pronta). Na frente, **o Linu de capacete** com o rolo da
  planta (`img/linu/linu-planta.png`, 120 × 194, sempre em 1×), que respira e pisca (`linu-vivo.js`).
- **A planta vira obra** (07/11/2026, à noite; nas 13 línguas desde a mesma noite, com os textos `vista_*`, `obra_*` e `lampiao_*`). Em cima da prancha,
  as abas “Planta” e “Obra pronta”: a obra é a cabana da identidade anterior (`abrigo-estacao-*.png`, de volta), sempre
  em 2× (688 × 384), inteira no tablet e recortada em volta da mesa no computador e no celular (`--centro`). Ela
  “imprime” de cima para baixo, em faixas, como saindo do plotter (só depois de as imagens carregarem, que baixam
  quando a pessoa passa o mouse, foca ou toca na aba), e o Linu entra pela porta e fica no quarto (tocar nele dá um
  pulinho). Com a obra na tela, trocar a luz (pelo botão do topo ou pelo “Apagar o lampião” embaixo da cena) volta a
  ser o lampião da estação: o Linu anda até ele, pula para puxar a cordinha, o lampião falha e apaga (ou acende) e a
  página troca de cor junto; de noite no relógio de quem visita, o quarto claro já é a noite com o lampião aceso
  (`data-hora`, do `tema-inicio.js`). Com a planta na tela, a troca é o círculo que sai da luminária. Tudo no
  `js/tema.js`; com “menos movimento”, nada anda e a troca é na hora.
- **O carimbo é o índice.** O quadro de legenda no canto da prancha lista as seis pranchas (01 O que fazemos a 06 Pedir
  orçamento) com os textos do menu. Computador: no canto da folha, 2 × 3. Tablet: uma faixa de seis casas embaixo da
  prancha. Celular: uma faixa que rola de lado.
- **Cada seção é uma prancha.** O número no círculo antes do título (contador do CSS, 01 a 06) e a **cota** da largura
  no alto de cada seção; o menu mostra os mesmos números. O que fazemos são fichas de detalhe com **marcas de corte**
  nos cantos; Projetos, o arquivo de pranchas (capturas com moldura fina); o Exemplo, a **lista de peças** ao lado do
  navegador desenhado; Como funciona, o **cronograma** com as etapas ligadas por uma cota tracejada; Dúvidas, as **notas
  gerais** N1 a N7; o contato, o **carimbo de aprovação** com o Linu e a hora de conversar, e o pedido montado; o
  rodapé, o carimbo da última prancha.
- **Três versões.** Celular: uma coluna, o Linu de pé em cima da prancha, as fichas e as partes do simulador em faixas
  que rolam de lado, os projetos numa lista compacta (miniatura quadrada e duas linhas), o menu num painel que sobe de
  baixo e a **barra do polegar** presa embaixo (a prancha atual, que abre o índice, e o orçamento). Tablet: os links do
  menu numa faixa embaixo do topo, o texto em duas colunas, fichas e projetos em 2 colunas, o simulador com a tela em
  cima e a lista e o total lado a lado, o cronograma em 2 × 2, o carimbo do contato deitado. Computador: o texto ao lado
  da prancha, o menu inteiro no topo, a coluna dos projetos (abas e áreas), o título das dúvidas e o carimbo do contato
  parados ao lado, fichas em 4 colunas.
- **Letras.** **Space Grotesk** nos títulos, nas cotas, nos números e nas etiquetas (técnica, de régua) e **Instrument
  Sans** no texto, as duas OFL, latim e latim estendido, baixadas com o `linuarquivos/modelos/ferramentas/fontes-locais.py`
  (80 KB as quatro). Em japonês, coreano e chinês, a Noto da língua entra para os caracteres que elas não têm.
- **Formas.** Canto reto (3 px), linha de 1,5 px, borda tracejada para o que é escolha, sombra curta. Nada de pílula,
  de madeira nem de papel bege. Ficou de fora o que os irmãos usam: a sombra dura deslocada (Família), as trilhas e o
  timecode (Digital), os blocos de gelo (Seguro) e as faixas vermelhas (Farol).
- **Ícones.** A luminária da prancheta (o botão do tema, com a luz amarela acesa no papel e apagada no cianotipo) e os
  quatro ícones das fichas, em pixel art de 16 × 16, com o detalhe em amarelo.
- **Imagem de compartilhar** refeita na mesma linha (`ferramentas/compartilhar.html`): o papel quadriculado, a prancha
  com as três vistas e o Linu de capacete em 2×.

## Digital Linu, o serviço irmão

O site de vídeo, redes sociais, anúncios, marca e automação, da mesma equipe: **https://digital.linupedia.com.br**.
Fica no seu próprio repositório, `Seiabras/digital-linu`, com publicação própria (separação de 06/11/2026): nada dele
mora aqui. Daqui saem só a faixa de ida e volta e a seção Identidade visual, que apontam para lá.

## Fonte e segurança

A Space Grotesk, a Instrument Sans e as Noto ficam em `public/fontes` (licença OFL), sem Google Fonts. A página leva uma CSP numa `<meta>` (só
carrega o que é do próprio site); o `deploy/Caddyfile-bloco` traz os cabeçalhos completos, para aplicar
na VM (ver `deploy/ORACLE.md`). Desde 29/10/2026 o bloco deixa o próprio site pôr uma página dele num quadro
(`frame-ancestors 'self'` e `X-Frame-Options SAMEORIGIN`), por causa do simulador; aplicado na VM em 29/10/2026 (a
cópia anterior ficou em `/etc/caddy/Caddyfile.antes-quadro`). A porta 22 é bloqueada em algumas redes: para mexer na
VM, use outra (a do celular serviu).

## Imagens do Linu

- **O Linu da planta** (`img/linu/linu-planta.png`, 120 × 194, e `linu-planta-piscando.png`): pedido à API de imagens
  em 07/11/2026 (`arte/linu-planta/linu-planta.md`, a escolhida em `aprovada.json`; as tentativas não vão para o git),
  levado para a grade e as cores do Linu pelo `linuarquivos/modelos/ferramentas/arte/pixelar.py` e com o quadro de olhos
  fechados do `arte/piscar.py` (olhos em 42,55 e 84.5,55). Fica na abertura, nas páginas de projeto e na de erro.
- **O Linu do contato** (`img/linu/linu-contato.png`, 4 poses de 138 × 190) acena quando aparece na tela e pula quando
  alguém toca nele (`js/movimento.js`). Vem do app, com a logo e os ícones, pelo `ferramentas/linu-do-app.py`, que tira
  a sobra do fundo antigo por fora do contorno (`sem_halo`; para limpar só o que já está no site:
  `python3 ferramentas/linu-do-app.py --so-limpar`).
- **O Linu de frente** (`img/linu/linu-frente.png`) fica só para a capa da LinuPedia (`ferramentas/capas/`).

- **A cabana da obra pronta** (`img/abrigo-estacao-dia.png`, `-noite.png` e `-apagada.png`, 344 × 192) e o Linu que
  anda nela (`linu/linu-frente.png`, `linu-costas.png` e os 4 passos de lado em `linu-lado.png`) voltaram em 07/11/2026,
  à noite, para a obra pronta. Os scripts que fizeram a cena da noite (`cena-apagada.py`, `corrigir-porta-estacao.py`)
  ficaram só no histórico do git (commit 46304cee), já que as imagens não mudam.

## Versão dos arquivos

O Caddy manda guardar `/img`, `/css` e `/js` por 7 dias. O Actions roda `ferramentas/versao-arquivos.py` (cópia do kit
do linuarquivos) antes de publicar e põe `?v=<8 letras do hash>` em todo `src` e `href` local das páginas: o endereço
muda quando o arquivo muda, e quem já visitou baixa só o que mudou. As fontes ficam de fora (o CSS as pede sem versão);
as Noto, que mudam com os textos, têm a `?v=` à mão no `css/estilo.css` (o `gerar-fontes.mjs` avisa quando subir).

## Publicar

Todo push na `main` publica sozinho: o GitHub Actions confere a página (`deploy/conferir-pagina.py`: HTML
válido e todo arquivo usado existe), manda `public/` para a VM pela chave do usuário `linusites` (segredo
`ORACLE_SSH_KEY`, refeito em 22/10/2026; a chave só pode rodar o `deploy/receber.sh`) e confere se o site
respondeu. A versão anterior fica em `/opt/linu-sites/app.anterior`. Detalhes em
[deploy/ORACLE.md](deploy/ORACLE.md).

## Documentos relacionados

- [`deploy/ORACLE.md`](deploy/ORACLE.md): DNS, Caddy, instalação e publicação.
- [`DIRETRIZES-UX.md`](DIRETRIZES-UX.md): regras de interface e desempenho (iguais em todos os projetos).
