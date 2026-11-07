/* A planta da abertura se desenha uma vez, como no plotter (07/11/2026): primeiro o contorno das três vistas (o
   computador, o tablet e o celular, um depois do outro), depois o miolo de cada tela e, por fim, as cotas e as notas.
   Dura uns 2 s e não esconde nada que se lê: o texto e os botões já estão prontos desde o primeiro quadro.
   Sem JavaScript, com “menos movimento” ou com ?static=1, a planta já vem desenhada. Só usa a API de animação do
   navegador (a CSP do site bloqueia estilo embutido; a API não é estilo embutido). */
(function () {
  "use strict";
  var svg = document.querySelector(".planta");
  if (!svg || !("animate" in Element.prototype)) return;
  if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;
  if (/[?&]static=1\b/.test(location.search)) return;
  // só anima se a planta estiver na tela ao abrir (quem chega pelo meio da página não precisa ver)
  if (svg.getBoundingClientRect().top > window.innerHeight) return;

  var SAIDA = "cubic-bezier(.45, 0, .2, 1)";

  function tracar(forma, atraso, duracao) {
    var total = 0;
    try { total = forma.getTotalLength(); } catch (e) { return; }
    if (!total) return;
    var d = total + " " + total;
    forma.animate([{ strokeDasharray: d, strokeDashoffset: total }, { strokeDasharray: d, strokeDashoffset: 0 }],
      { duration: duracao, delay: atraso, easing: SAIDA, fill: "backwards" });
  }

  // o contorno: as três vistas em sequência
  var contorno = svg.querySelectorAll(".planta-traco > *");
  [].forEach.call(contorno, function (f, i) { tracar(f, i * 220, 800); });

  // o miolo: cada linha e cada caixa, em cascata curta
  var miolo = svg.querySelectorAll(".planta-miolo > *");
  [].forEach.call(miolo, function (f, i) {
    if (f.classList.contains("planta-barra")) {
      f.animate([{ opacity: 0 }, { opacity: 1 }], { duration: 300, delay: 900 + i * 30, fill: "backwards" });
      return;
    }
    tracar(f, 800 + i * 30, 520);
  });

  // as cotas e as notas aparecem por último
  [].forEach.call(svg.querySelectorAll(".planta-cotas"), function (g, i) {
    g.animate([{ opacity: 0 }], { duration: 450, delay: 1500 + i * 200, easing: "ease-out", fill: "backwards" });
  });
})();
