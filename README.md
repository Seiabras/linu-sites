# Linu Sites

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
| `public/projetos/*.html` | Página de cada projeto, gerada por `ferramentas/gerar-projetos.py`. |
| `public/css/estilo.css` | Visual (cores da LinuPedia, modo claro e escuro). |
| `public/js/` | `tema-inicio.js` (aplica o tema antes de pintar), `tema.js` (o Linu e o lampião; com “menos movimento” ligado ele não anda, só aparece embaixo do lampião), `menu.js` (menu do celular), `movimento.js` (animações), `simulador.js` (o simulador do Café Aurora). |
| `public/img/` | Cena da estação, o Linu (`linu/`, `linu-pixel.png`), a logo (`linu-logo.png`), capturas dos projetos (`projetos/`), ícones e imagem de compartilhar. |
| `public/fontes/` | Nunito (licença OFL), servida pelo próprio site. |
| `sitios/` | Os sites dos subdomínios, fora de `public/`: `cafe-aurora/` (cafe.linupedia.com.br, também com `/bootstrap/` e `/tailwind/`), `fotografia-do-cerrado/` (cerrado.linupedia.com.br) e `abelhas-sem-ferrao/` (abelhas.linupedia.com.br). Cada um tem o seu repositório público no GitHub (`Seiabras/cafe-aurora`, `Seiabras/fotografia-do-cerrado`, `Seiabras/abelhas-sem-ferrao`); mudou aqui, leve a mudança para lá. |
| `ferramentas/pagina/` | O modelo da página inicial (`modelo.html`), os textos de cada idioma (`textos/<código>.json`) e os preços de cada moeda (`precos.json`). |
| `ferramentas/` | Geradores: a página em cada idioma (`gerar-idiomas.mjs`), páginas de projeto, imagem de compartilhar, cena noturna e o Linu trazido do app (`linu-do-app.py`). |
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
  moeda; com `"provisorio"`, publica e só avisa. **O euro foi ao ar em 30/10/2026 com os valores provisórios**, para
  eu ver; falta aprovar a tabela.
- **Regiões (30/10/2026):** cada idioma diz a sua região no JSON (`"regiao"`: `brasil`, `europa` ou `asia`, e
  `"padrao": true` na página que representa a região). O seletor agrupa por região. A **Ásia-Pacífico e
  internacional** está em preparação: o inglês internacional (`/intl/`, em dólar) e o japonês têm textos, mas com
  `"rascunho": true` (ficam fora do site, do seletor e do sitemap); faltam o coreano, o chinês tradicional, a sugestão
  da região pelo fuso horário e as fontes do sistema para japonês, coreano e chinês. O dólar está pendente.
- **Os textos dos scripts** (menu, luz, mensagem do WhatsApp e do e-mail) vão no `<script type="application/json"
  id="textos-js">` de cada página; a moeda e o formato do número vêm do `<html lang data-moeda>`. As páginas dos
  projetos não têm o bloco e ficam em português.
- **Seletor de idioma** no topo (o globo) e, uma vez por visitante, um aviso discreto quando o idioma do navegador é
  outro que o site tem (sem trocar de página sozinho). A escolha fica guardada no navegador (`js/menu.js`).
- **Para o Google:** cada página leva o `hreflang` de todas (o `x-default` é o inglês), os `og:locale`, os dados
  estruturados (`ProfessionalService`) e o `sitemap.xml` com as alternativas; o gerador refaz o sitemap.
- Na Europa: preço em euro, pagamento por transferência SEPA, domínio do país (.pt, .es, .de…) e o WhatsApp com +55.
  As páginas “Como foi feito” e o Café Aurora do simulador ainda estão em português, e os links avisam isso.

## O que tem na página

- **Abertura:** o que o estúdio faz e o botão de orçamento.
- **O que fazemos:** sites de apresentação, ferramentas e painéis, apps que instalam, hospedagem.
- **Página de cada projeto** (`/projetos/linupedia`, `/v2tech`, `/losvega`, `/marginalia`, `/iconvet`,
  `/ajoriente`, `/dojo-legacy`, `/omega`): o desafio, o que foi feito e como funciona por dentro, com os fatos
  dos READMEs de cada repositório (nos quatro de clientes, do que o próprio site mostra no ar). Geradas por
  `ferramentas/gerar-projetos.py`: mude o texto lá e rode o script. No computador, o `python3 -m
  http.server` não completa o `.html` como o Caddy; abra `projetos/<nome>.html`.
- **Projetos** (`#projetos`): duas abas lado a lado, “No ar” e “De estudo” (`js/movimento.js`, com setas, Home e
  End). O endereço com `#estudo` abre a segunda; sem JavaScript, as duas listas aparecem uma embaixo da outra.
  Por cima das abas, as **áreas** (30/10/2026): Educação e cultura, Saúde e serviços, Comércio e turismo, Indústria e
  Jogos. Elas filtram as duas listas, a conta de cada aba acompanha e, se a aba aberta ficar vazia, abre a outra. As
  áreas de cada projeto ficam no `data-areas` do `ferramentas/pagina/modelo.html` (pode ter mais de uma).
- **No ar:** LinuPedia, V²Tech COMBUSTÍVEL, Los Vega na Estrada e Marginalia; desde 29/10/2026 também
  Iconvet (iconvet.com.br), Administração Judicial Oriente (ajoriente.com), Dojo Legacy (bjj-link.com) e Ômega
  Imóveis (omega-site-vert.vercel.app, ainda sem domínio). Capturas em `public/img/projetos/` (960×600, WebP).
  O NeuroSim fica de fora por enquanto, até sair do começo.
- **De estudo** (`#estudo`, 29/10/2026): os sites que fiz na disciplina Desenvolvimento de Interfaces, com
  empresas fictícias: Café Aurora, Fotografia do Cerrado e Abelhas sem Ferrão. Cada cartão leva ao subdomínio e ao
  código no GitHub; as capturas também ficam em `public/img/projetos/`.
- **Como funciona** e **contato**: WhatsApp (61) 99667-2610 e `contato@linupedia.com.br`.
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

A Nunito fica em `public/fontes` (licença OFL), sem Google Fonts. A página leva uma CSP numa `<meta>` (só
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
