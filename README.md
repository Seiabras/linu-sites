# Linu Sites

Site do **Linu Sites**, o estúdio de sites e aplicativos web da LinuPedia: **https://sites.linupedia.com.br**.

Uma página só (`public/index.html`), sem dependências e sem servidor próprio: o Caddy da VM da Oracle
(a mesma da LinuPedia, do v²tech, da Marginalia e do Los Vega) entrega os arquivos de `public/`.
O visual segue a LinuPedia: o azul do app, o gelo e o pergaminho da expedição e o Linu em pixel art.

## Ver no computador

Abra `public/index.html` no navegador, ou, para ver como no servidor:

```bash
cd public && python3 -m http.server 8000
```

## O que tem na página

- **Abertura:** o que o estúdio faz e o botão de orçamento.
- **O que fazemos:** sites de apresentação, ferramentas e painéis, apps que instalam, hospedagem.
- **Projetos no ar:** LinuPedia, V²Tech COMBUSTÍVEL, Los Vega na Estrada e Marginalia, com capturas em
  `public/img/projetos/` (960×600, WebP). O NeuroSim fica de fora por enquanto, até sair do começo.
- **Como funciona** e **contato** (`contato@linupedia.com.br`).

## Publicar

Ver [deploy/ORACLE.md](deploy/ORACLE.md).
