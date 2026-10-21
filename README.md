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
- **Como funciona** e **contato**: WhatsApp (61) 99667-2610 e `contato@linupedia.com.br`.
- **Preços de referência** nos cartões de “O que fazemos”: site de apresentação a partir de R$ 1.800,
  ferramentas e painéis a partir de R$ 6.000, apps que instalam a partir de R$ 9.000 e hospedagem e
  cuidado por R$ 120 por mês.
- **Depoimentos:** a seção está pronta no HTML, mas escondida (`hidden`) até chegarem frases de verdade.
- **Celular:** os links vão para um menu que abre no botão ☰ (`public/js/menu.js`).
- **Compartilhar:** `img/compartilhar.png` (1200 × 630) e os ícones em PNG, gerados por
  `ferramentas/gerar-imagens.mjs`; `sitemap.xml` e `robots.txt` apontando para ele.
- **Modo claro e escuro:** o botão da lâmpada, no topo. O Linu entra no quarto pela porta, vai até o
  lampião e apaga (modo escuro) ou acende (modo claro); a página troca de cor junto. A escolha fica
  guardada no navegador; sem escolha, vale a do sistema. Com “reduzir movimento” ligado, troca na hora.
  Se a cena do topo estiver fora da tela, a animação aparece num cartão no canto. Código em
  `public/js/tema.js`.

## Imagens da cena

As imagens da estação e do Linu vêm do app (LinuLingo, `assets/pixel/`), na mesma grade de 344 × 192.
O que é só do site fica em `ferramentas/`:

- `cena-apagada.py` gera `img/abrigo-estacao-apagada.png`, a noite com o lampião apagado (o modo escuro).
- `desenhar-linu-lado.py` desenha o Linu de lado andando (4 quadros, `img/linu/linu-lado.png`).
- `corrigir-porta-estacao.py` tirou o retângulo da porta e da escotilha nas imagens de noite.

## Publicar

Ver [deploy/ORACLE.md](deploy/ORACLE.md).
