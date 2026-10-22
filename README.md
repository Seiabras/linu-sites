# Linu Sites

Site do **Linu Sites**, o estúdio de sites e aplicativos web da LinuPedia: **https://sites.linupedia.com.br**.

Uma página só (`public/index.html`), sem dependências e sem servidor próprio: o Caddy da VM da Oracle
(a mesma da LinuPedia, do v²tech, da Marginalia e do Los Vega) entrega os arquivos de `public/`.
O visual segue a LinuPedia: o azul do app, o gelo e o pergaminho da expedição e o Linu em pixel art.

- **No ar:** https://sites.linupedia.com.br
- **Repositório:** `Seiabras/linu-sites` (**público**: nada de senha, chave ou relatório interno aqui; isso vai
  para o `Seiabras/linuhub`, que é privado), branch `main`
- **Contato do estúdio:** contato@linupedia.com.br (Zoho Mail, caixa linu@linupedia.com.br) e WhatsApp
  (61) 99667-2610
- **Crédito nos projetos:** todo site feito pelo estúdio leva "Site feito por Linu Sites" no rodapé, com
  link para cá (V²Tech, Los Vega, Marginalia e, no Perfil, a LinuPedia).

## Como está organizado

| Pasta / arquivo | O que tem |
|---|---|
| `public/index.html` | A página inicial (uma página só). |
| `public/projetos/*.html` | Página de cada projeto, gerada por `ferramentas/gerar-projetos.py`. |
| `public/css/estilo.css` | Visual (cores da LinuPedia, modo claro e escuro). |
| `public/js/` | `tema-inicio.js` (aplica o tema antes de pintar), `tema.js` (o Linu e o lampião), `menu.js` (menu do celular), `movimento.js` (animações). |
| `public/img/` | Cena da estação, o Linu, capturas dos projetos (`projetos/`), ícones e imagem de compartilhar. |
| `public/fontes/` | Nunito (licença OFL), servida pelo próprio site. |
| `ferramentas/` | Geradores: páginas de projeto, imagens de compartilhar e ícones, cena noturna e o Linu de lado. |
| `deploy/` | Instalação na VM (`instalar-uma-vez.sh`), recebimento (`receber.sh`), conferência antes de publicar (`conferir-pagina.py`), bloco do Caddy e o manual `ORACLE.md`. |
| `.github/workflows/oracle.yml` | Publicação automática (confere a página, entrega e testa se o site respondeu). |

## Ver no computador

Abra `public/index.html` no navegador, ou, para ver como no servidor:

```bash
cd public && python3 -m http.server 8000
```

## O que tem na página

- **Abertura:** o que o estúdio faz e o botão de orçamento.
- **O que fazemos:** sites de apresentação, ferramentas e painéis, apps que instalam, hospedagem.
- **Página de cada projeto** (`/projetos/linupedia`, `/v2tech`, `/losvega`, `/marginalia`): o desafio, o
  que foi feito e como funciona por dentro, com os fatos dos READMEs de cada repositório. Geradas por
  `ferramentas/gerar-projetos.py`: mude o texto lá e rode o script. No computador, o `python3 -m
  http.server` não completa o `.html` como o Caddy; abra `projetos/<nome>.html`.
- **Projetos no ar:** LinuPedia, V²Tech COMBUSTÍVEL, Los Vega na Estrada e Marginalia, com capturas em
  `public/img/projetos/` (960×600, WebP). O NeuroSim fica de fora por enquanto, até sair do começo.
- **Como funciona** e **contato**: WhatsApp (61) 99667-2610 e `contato@linupedia.com.br`.
- **Preços de referência** nos cartões de “O que fazemos”: site de apresentação a partir de R$ 1.800,
  ferramentas e painéis a partir de R$ 6.000, apps que instalam a partir de R$ 9.000 e dois planos
  mensais: **No ar** (R$ 60: servidor, HTTPS, domínio e cópias) e **Cuidado** (R$ 120: tudo isso, mais
  atualizações e pequenos ajustes); pagando o ano, são 10 meses.
- **Dúvidas frequentes** (`#duvidas`, acordeão em `<details>`): prazo estimado por tipo, pagamento
  (50/50, ou 40/30/30 a partir de R$ 6.000), mensal obrigatório, painel para o cliente editar (extra de R$ 1.200 no site de apresentação,
  incluído em ferramentas e apps), domínio no nome do cliente, conteúdo e
  dados do cliente (código, layout e visual do Linu Sites) e saída (exportação e compra do código pelo
  valor do projeto). Decidido em 22/10/2026; os termos completos estão em rascunho no `Seiabras/linuhub`.
- **Depoimentos:** a seção está pronta no HTML, mas escondida (`hidden`) até chegarem frases de verdade.
- **Celular:** os links vão para um menu que abre no botão ☰ (`public/js/menu.js`).
- **Compartilhar:** `img/compartilhar.png` (1200 × 630) e os ícones em PNG, gerados por
  `ferramentas/gerar-imagens.mjs`; `sitemap.xml` e `robots.txt` apontando para ele.
- **Modo claro e escuro:** o botão da lâmpada, no topo. O Linu entra no quarto pela porta, vai até o
  lampião e apaga (modo escuro) ou acende (modo claro); a página troca de cor junto. A escolha fica
  guardada no navegador; sem escolha, vale a do sistema. Com “reduzir movimento” ligado, troca na hora.
  Se a cena do topo estiver fora da tela, a animação aparece num cartão no canto. Código em
  `public/js/tema.js`.

## Fonte e segurança

A Nunito fica em `public/fontes` (licença OFL), sem Google Fonts. A página leva uma CSP numa `<meta>` (só
carrega o que é do próprio site); o `deploy/Caddyfile-bloco` traz os cabeçalhos completos, para aplicar
na VM (ver `deploy/ORACLE.md`).

## Imagens da cena

As imagens da estação e do Linu vêm do app (LinuLingo, `assets/pixel/`), na mesma grade de 344 × 192.
O que é só do site fica em `ferramentas/`:

- `cena-apagada.py` gera `img/abrigo-estacao-apagada.png`, a noite com o lampião apagado (o modo escuro).
- `desenhar-linu-lado.py` desenha o Linu de lado andando (4 quadros, `img/linu/linu-lado.png`).
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
