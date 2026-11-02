# Diretrizes de UI/UX e desempenho

Vale para **todos os sites e apps** dos projetos (V²Tech COMBUSTÍVEL, Marginalia, Linu Sites, Los Vega na Estrada,
LinuPedia/LinuLingo, NeuroSim, Trupe). Decidido em 21/10/2026; a regra do celular e do computador entrou em 30/10/2026
e virou a regra das três versões (celular, tablet e computador, cada uma com layout próprio) em 1/11/2026.
O mesmo texto está na raiz de cada repositório e no `modelos/linu-modelo/` do linuarquivos; mudou aqui, muda em todos.

Quatro regras resumem tudo:

1. **A melhor UI/UX possível:** bonito, claro e com resposta a cada toque.
2. **Nunca chato de mexer:** a pessoa não pode ter só a rolagem para baixo como opção.
3. **Três versões, uma para cada aparelho:** celular, tablet e computador têm cada um o seu layout, pensado para o
   jeito de usar aquele aparelho; nunca o celular esticado, o tablet improvisado nem o computador espremido.
4. **Sempre otimizado:** leve na rede, na memória e na bateria, mesmo num celular simples.

Toda entrega que mexe em tela passa pelo checklist do fim deste arquivo antes de ir para a `main`.

## 1. Movimento: animado, mas com propósito

- **Toda mudança de estado tem transição.** Hover, foco, abrir e fechar, trocar de aba, marcar e desmarcar. Duração de
  150 a 250 ms, curva `ease-out` na entrada e `ease-in` na saída. Nada aparece ou some "seco".
- **Seções entram ao rolar.** Um `fade` com subida de 12 a 16 px, uma vez só por elemento, com um único
  `IntersectionObserver` por página. Escalonar cartões de uma mesma lista em 40 a 60 ms.
- **Troca de página suave.** Nos sites de várias páginas, usar View Transitions entre documentos
  (`@view-transition { navigation: auto; }` no CSS), com o cabeçalho fixo (`view-transition-name`) para ele não piscar.
  Navegador sem suporte simplesmente troca de página: nada quebra.
- **Animar só `transform` e `opacity`.** Nunca `top`, `left`, `width`, `height` ou `box-shadow` em animação contínua:
  travam no celular.
- **`prefers-reduced-motion: reduce` sempre respeitado.** Quem pediu menos movimento recebe as mudanças sem animação
  (nunca sem a mudança).
- **O movimento nunca atrasa o conteúdo.** Texto e botões ficam utilizáveis desde o primeiro quadro; animação de entrada
  não esconde o que já está na tela no carregamento.
- **Proibido:** carrossel que gira sozinho, animação em loop infinito no meio do texto, efeito de digitação, paralaxe
  pesada, tela de carregamento decorativa (fora a exceção logo abaixo).
- **Exceção: a abertura de identidade (1/11/2026).** Um site cujo tema é a própria experiência (o Café Aurora é o
  primeiro) pode ter uma tela de abertura, se cumprir as cinco condições:
  1. aparece **uma vez por sessão** (`sessionStorage`), nunca a cada página;
  2. dura **no máximo 3 s** e some sozinha mesmo que algo trave (ver os dois limites logo abaixo);
  3. **pula com um toque** em qualquer lugar, com um botão visível “Pular abertura” (44 px) e com Esc, Enter ou espaço;
  4. com **“menos movimento”**, aparece sem animação (logo parado, barra sem deslizar);
  5. **não existe** sem JavaScript nem quando o site está embutido (no simulador do Linu Sites, por exemplo), a não ser
     na prévia que a pessoa pede ali com o botão “Ver a abertura”.

  **Dois limites de duração (2/11/2026):**
  - **Projeto de estudo ou de portfólio** (Café Aurora, Pica ou Não Pica?, Guia do Cerrado): até 3 s, porque a
    experiência é o assunto.
  - **Site de cliente:** 1,5 s por padrão. Chega a 3 s só se o cliente pedir depois de ver as duas lado a lado (no
    simulador do Linu Sites, módulo “Abertura de identidade”), e isso fica escrito na proposta.

  Para fazer, use a vinheta pronta do `linu-modelo` (`public/js/vinheta.js` e `public/css/vinheta.css`), que já
  cumpre as cinco condições; a duração é o `data-duracao` do `#vinheta`, contada desde o começo da página. Não vale
  a abertura que dura “até a página carregar”: no 4G lento ela passa dos 3 s.

  Fora isso, continua proibida: em site de informação, loja ou ferramenta, quem chega quer o conteúdo.
- **Biblioteca de animação só quando o CSS não dá conta.** Nos sites, CSS e um pouco de JS bastam. No app (Expo), as
  animações rodam na thread de interface com o Reanimated.

## 2. Nunca chato de mexer

Uma página que no celular passa de **6 telas de altura** precisa de algo além da rolagem:

- **Navegação interna:** índice com âncoras (fixo no topo ou na lateral), que marca a seção atual enquanto a pessoa rola.
- **Conteúdo recolhível:** perguntas frequentes, detalhes e listas longas em `<details>` ou acordeão, com transição.
- **Listas de cartões em faixa horizontal** com `scroll-snap` no celular, em vez de empilhar 20 cartões.
- **Abas ou filtros** quando há grupos (destinos por continente, textos por categoria, combustíveis).
- **Botão "voltar ao topo"** e, em textos longos, **barra de progresso de leitura**.
- **Algo para fazer, não só ler:** simulador, comparador, busca, quiz, mapa. Cada site deve ter pelo menos uma interação
  que a pessoa usa com as próprias mãos.

E em toda tela:

- **Resposta em menos de 100 ms a cada toque:** estado pressionado, "carregando…", confirmação de sucesso.
- **Formulários:** validação na hora (não só ao enviar), mensagem de erro ao lado do campo, o que foi digitado nunca se
  perde.
- **Estados vazios e de carregamento desenhados:** esqueleto no lugar do conteúdo, nunca tela em branco.
- **Celular primeiro:** testar em 390 px de largura; área de toque de no mínimo 44 × 44 px; nada de rolagem lateral;
  margem lateral de 16 px.
- **Acessível:** contraste AA nos modos claro e escuro (o botão de tema é padrão em todos os projetos), foco visível,
  rótulos em botões só com ícone.

## 3. Três versões: celular, tablet e computador, cada uma com layout próprio

“A versão de celular e de computador tão iguais: todo projeto tem que ter sua versão dividida entre os aparelhos,
tablet, computador e celular, pra se adaptar à melhor forma de ver cada um, um layout específico” (1/11/2026).

Não basta a página “caber” em cada tela. Cada aparelho tem a **sua versão**, com o layout que fica melhor nele. O
conteúdo e as funções são os mesmos; o que muda é a arrumação, a navegação e o que fica sempre à vista. Uma página só
(o mesmo HTML), com `@media` no CSS e, se precisar, um pouco de JS; nada de dois sites.

**Celular (até 699 px; testar em 390 × 844).** Feito para o polegar e para uma mão:
- uma coluna, na ordem de leitura, com o mais importante no alto;
- a ação principal da tela presa embaixo, ao alcance do polegar (uma barra fixa), quando a tela tem uma ação;
- índices, filtros e escolhas numa faixa que rola de lado ou num painel que abre de baixo;
- listas longas compactas (miniatura pequena, uma linha de texto) ou em faixa horizontal com `scroll-snap`;
- menu no botão “Menu”; nada que dependa de passar o mouse.

**Tablet (700 a 1099 px; testar em 820 × 1180 em pé e 1180 × 820 deitado).** O meio-termo próprio, nunca o celular
esticado:
- duas colunas onde o computador tem três, e grades de cartões em 2 colunas;
- o que é de consulta (índice, filtros) num painel que abre ao lado ou numa faixa no alto, que não come a largura do
  conteúdo;
- áreas de toque grandes como no celular (é tela de dedo), mas aproveitando a largura;
- deitado, pode ganhar a coluna lateral do computador.

**Computador (1100 px ou mais; testar em 1280 × 800 e 1440 × 900).** Feito para ver muita coisa de uma vez:
- o que é de consulta (filtros, índice, mapa, foto, dados do grupo) parado numa coluna ao lado (`position: sticky`),
  com o conteúdo rolando junto;
- painéis que no celular abrem com um botão ficam abertos;
- listas de cartões em 3 ou mais colunas, tabelas inteiras, mapas e gráficos grandes;
- passar o mouse mostra detalhes (dica, prévia), sempre com um equivalente por toque e por teclado;
- linhas de texto com no máximo uns 75 caracteres; nada de uma coluna estreita no meio com metade da tela vazia.

**No notebook de tela baixa (800 px de altura):** a ação principal da tela aparece sem rolar, ou fica presa à vista.

**O teste das três capturas:** tire a captura da mesma página em 390, 820 e 1280 px e ponha lado a lado. Se as três
mostram a mesma arrumação, só mais larga ou mais estreita, a página **não passou**: pelo menos a navegação, a
posição dos filtros ou índices e o número de colunas têm de mudar de um aparelho para o outro.

- **No app (Expo):** o mesmo vale para telefone e tablet (`useWindowDimensions`), e para a versão web aberta no
  computador.
- **Exemplo:** a Trupe (30/10/2026). No computador, o Explorar tem os filtros sempre abertos numa coluna e o cartão
  deitado; o perfil deixa a foto parada à esquerda; o formulário longo tem o índice em pé ao lado. No celular, tudo em
  uma coluna, com os botões presos acima das abas.

## 4. Sempre otimizado

Orçamento por página, medido no celular (390 × 844) com o cache vazio:

| Medida | Limite | Situação em 21/10/2026 |
|---|---|---|
| Dados transferidos na abertura | até 300 KB | 100 a 310 KB |
| Requisições | até 25 | 7 a 18 |
| Memória de JavaScript (heap) | até 5 MB | 1,1 a 1,5 MB |
| Elementos na página (DOM) | até 1.500 | 61 a 540 |
| Maior conteúdo visível (LCP), em 4G | até 2,5 s | a medir |
| Deslocamento do layout (CLS) | até 0,1 | a medir |
| Cada imagem | até 200 KB, WebP ou AVIF | ok |

Regras que mantêm isso:

- **Imagens:** sempre com `width` e `height` (sem pulo de layout), `loading="lazy"` abaixo da primeira tela, tamanho
  certo para a tela (`srcset`), WebP ou AVIF.
- **Fontes:** no máximo duas famílias, `display=swap`, `preconnect`; carregar só os pesos usados.
- **JavaScript:** sem framework nem biblioteca para o que o navegador já faz. Scripts com `defer`. Nada de código de
  terceiros (rastreadores, widgets) sem motivo forte.
- **Nada de abrir páginas e janelas à toa:** `target="_blank"` só para link de outro site, nunca pop-up, nunca abrir
  aba sozinho. Uma página aberta não carrega as outras escondidas (pré-carregar só o próximo passo provável).
- **Memória que não cresce:** todo `setInterval`, `requestAnimationFrame`, `observer` e `addEventListener` em elemento
  que sai da tela é desligado; listas grandes são paginadas ou virtualizadas; nada de guardar resultados para sempre em
  variáveis globais.
- **Service worker** com cache versionado e limitado, apagando as versões antigas.
- **No app (Expo):** listas longas sempre virtualizadas, imagens com cache, telas que não estão visíveis não ficam
  animando nem buscando dados.

## 5. Como conferir

- **Rápido:** no Chrome, DevTools → Lighthouse, modo celular. Desempenho, acessibilidade e boas práticas acima de 90.
- **Com tela de abertura, o Lighthouse engana (medido em 2/11/2026):** ele toma o logo da abertura como o “maior
  conteúdo” e dá a mesma nota com ou sem ela (Café Aurora: 95 com 3 s, 94 sem). Meça o **tempo até o conteúdo à vista**
  (quando a abertura começa a sumir) no celular, em 4G lento e em 4G bom. No Café: sem abertura 1,6 s e 0,6 s; com
  1,5 s, 2,3 s e 1,7 s; com 3 s, 3,2 s e 3,1 s.
- **Memória:** DevTools → Memory → tirar um retrato antes e depois de usar a página por um minuto. Se cresceu e não volta,
  tem vazamento.
- **Movimento:** DevTools → Rendering → "Emulate CSS prefers-reduced-motion" e conferir que tudo continua funcionando.
- **Celular e computador de verdade:** abrir no celular, no 4G, e num notebook, ao menos uma vez por entrega grande.
- **Larguras:** DevTools → modo dispositivo em 390, 820 e 1280 px (e 1280 × 800 para o notebook de tela baixa).

## 6. Checklist antes de publicar

- [ ] Toda mudança de estado nova tem transição de 150 a 250 ms e respeita `prefers-reduced-motion`.
- [ ] Tela de abertura só com as cinco condições da exceção (seção 1): até 1,5 s em site de cliente, 3 s só se ele pediu.
- [ ] Nenhuma página nova passa de 6 telas no celular sem índice, abas, acordeão ou faixa horizontal.
- [ ] A página tem ao menos uma interação além de ler e rolar.
- [ ] Três versões (seção 3): celular, tablet e computador com layout próprio, e o teste das três capturas (390, 820
      e 1280 px, nos modos claro e escuro) mostrando arrumações diferentes.
- [ ] Dentro do orçamento da seção 4 (peso, requisições, memória, DOM).
- [ ] Imagens novas com `width`, `height`, `lazy` e formato leve.
- [ ] Nenhum intervalo, observer ou listener fica vivo depois de a tela sair.
