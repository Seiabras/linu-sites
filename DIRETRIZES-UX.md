# Diretrizes de UI/UX e desempenho

Vale para **todos os sites e apps** dos projetos (V²Tech COMBUSTÍVEL, Marginalia, Linu Sites, Los Vega na Estrada,
LinuPedia/LinuLingo, NeuroSim). Decidido em 21/10/2026. O mesmo texto está na raiz de cada repositório; mudou aqui, muda
em todos.

Três regras resumem tudo:

1. **A melhor UI/UX possível:** bonito, claro e com resposta a cada toque.
2. **Nunca chato de mexer:** a pessoa não pode ter só a rolagem para baixo como opção.
3. **Sempre otimizado:** leve na rede, na memória e na bateria, mesmo num celular simples.

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
  pesada, tela de carregamento decorativa.
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

## 3. Sempre otimizado

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

## 4. Como conferir

- **Rápido:** no Chrome, DevTools → Lighthouse, modo celular. Desempenho, acessibilidade e boas práticas acima de 90.
- **Memória:** DevTools → Memory → tirar um retrato antes e depois de usar a página por um minuto. Se cresceu e não volta,
  tem vazamento.
- **Movimento:** DevTools → Rendering → "Emulate CSS prefers-reduced-motion" e conferir que tudo continua funcionando.
- **Celular de verdade:** abrir no celular, no 4G, ao menos uma vez por entrega grande.

## 5. Checklist antes de publicar

- [ ] Toda mudança de estado nova tem transição de 150 a 250 ms e respeita `prefers-reduced-motion`.
- [ ] Nenhuma página nova passa de 6 telas no celular sem índice, abas, acordeão ou faixa horizontal.
- [ ] A página tem ao menos uma interação além de ler e rolar.
- [ ] Testado em 390 px, nos modos claro e escuro.
- [ ] Dentro do orçamento da seção 3 (peso, requisições, memória, DOM).
- [ ] Imagens novas com `width`, `height`, `lazy` e formato leve.
- [ ] Nenhum intervalo, observer ou listener fica vivo depois de a tela sair.
