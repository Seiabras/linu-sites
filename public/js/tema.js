/* Modo claro e escuro (identidade “a planta”, 07/11/2026): o botão é a luminária da prancheta. Apagar a luz mostra o
   cianotipo (a planta azul de traço branco); acender volta ao papel vegetal. A troca abre num círculo que sai da
   luminária (View Transitions, onde o navegador tem); sem isso, ou com “menos movimento”, as cores só passam devagar.
   A escolha fica guardada no navegador; sem escolha, vale a do sistema. */
(function () {
  "use strict";

  var raiz = document.documentElement;
  var bloco = document.getElementById("textos-js");
  var T = bloco ? JSON.parse(bloco.textContent) : {};
  var botao = document.querySelector("[data-luz]");
  var sistemaEscuro = window.matchMedia("(prefers-color-scheme: dark)");
  var poucoMovimento = window.matchMedia("(prefers-reduced-motion: reduce)");
  if (!botao) return;

  function temaAtual() {
    return raiz.dataset.theme || (sistemaEscuro.matches ? "dark" : "light");
  }

  function atualizarBotao() {
    var escuro = temaAtual() === "dark";
    botao.setAttribute("aria-label", escuro ? T.luz_acender_aria || "Acender a luz (modo claro)" : T.luz_apagar_aria || "Apagar a luz (modo escuro)");
    botao.title = escuro ? T.luz_acender || "Acender a luz" : T.luz_apagar || "Apagar a luz";
  }

  function aplicar(tema) {
    raiz.dataset.theme = tema;
    try { localStorage.setItem("tema", tema); } catch (e) {}
    atualizarBotao();
  }

  botao.addEventListener("click", function () {
    var tema = temaAtual() === "dark" ? "light" : "dark";
    if (poucoMovimento.matches || !document.startViewTransition) {
      raiz.classList.add("trocando-tema");
      aplicar(tema);
      setTimeout(function () { raiz.classList.remove("trocando-tema"); }, 450);
      return;
    }
    var r = botao.getBoundingClientRect();
    var x = r.left + r.width / 2;
    var y = r.top + r.height / 2;
    var raio = Math.hypot(Math.max(x, innerWidth - x), Math.max(y, innerHeight - y));
    var troca = document.startViewTransition(function () { aplicar(tema); });
    troca.ready.then(function () {
      raiz.animate({ clipPath: ["circle(0px at " + x + "px " + y + "px)", "circle(" + raio + "px at " + x + "px " + y + "px)"] },
        { duration: 520, easing: "cubic-bezier(.4, 0, .2, 1)", pseudoElement: "::view-transition-new(root)" });
    }).catch(function () {});
  });

  // sem escolha guardada, o tema acompanha o sistema
  sistemaEscuro.addEventListener("change", atualizarBotao);
  atualizarBotao();
})();
