/* O Linu vivo (07/11/2026), o mesmo nos sites da família. Toda imagem com data-linu-vivo ganha:
   - a respiração: desce e sobe 1 pixel da grade (2 px na tela se ele está em 2×), devagar;
   - o piscar: troca pelo quadro de olhos fechados (data-piscar="img/…-piscando.png") por um instante, a cada 2,5 a 6 s,
     às vezes duas vezes seguidas;
   - o pulinho ao passar o mouse ou tocar.
   Só anima enquanto ele está na tela e a aba está aberta; com “menos movimento”, fica parado (regra da identidade:
   o Linu pode viver; o texto não anima sozinho). Usa a API de animação do navegador e a propriedade `translate`, para
   somar com as animações próprias de cada site (que usam `transform`) sem brigar. Sem CSS: a CSP dos sites bloqueia
   estilo embutido. Se alguém trocar a imagem (o Linu andando no Linu Sites), o piscar espera ela voltar.
   O original mora em linuarquivos/modelos/ferramentas/familia/; cada site tem uma cópia em js/. */
(function () {
  "use strict";
  var menos = window.matchMedia("(prefers-reduced-motion: reduce)");
  var linus = Array.prototype.slice.call(document.querySelectorAll("img[data-linu-vivo]"));
  if (!linus.length || !("animate" in Element.prototype)) return;

  function escala(img) {
    var k = img.naturalWidth ? Math.round(img.getBoundingClientRect().width / img.naturalWidth) : 1;
    return Math.max(1, k || 1);
  }

  linus.forEach(function (img) {
    var base = img.getAttribute("src");
    var fechado = img.dataset.piscar;
    var visivel = false;
    var respira = null;
    var relogio = null;
    if (fechado) { var pre = new Image(); pre.src = fechado; }

    function livre() { return img.getAttribute("src") === base && !img.closest("[data-andando]") && !img.hasAttribute("data-andando"); }

    function respirar() {
      if (respira) respira.cancel();
      var k = escala(img);
      respira = img.animate([{ translate: "0 0" }, { translate: "0 " + k + "px" }],
        { duration: 1700, iterations: Infinity, direction: "alternate", easing: "steps(1, end)" });
      if (!visivel) respira.pause();
    }

    function piscarUmaVez(depois) {
      if (!fechado || !livre()) return depois && depois();
      img.setAttribute("src", fechado);
      setTimeout(function () {
        if (img.getAttribute("src") === fechado) img.setAttribute("src", base);
        if (depois) setTimeout(depois, 170);
      }, 130);
    }

    function agendar() {
      clearTimeout(relogio);
      relogio = setTimeout(function () {
        if (visivel && !document.hidden && !menos.matches) {
          piscarUmaVez(Math.random() < 0.25 ? function () { piscarUmaVez(); } : null);
        }
        agendar();
      }, 2500 + Math.random() * 3500);
    }

    function pular() {
      if (menos.matches) return;
      var k = escala(img);
      img.animate([{ translate: "0 0" }, { translate: "0 " + (-6 * k) + "px", offset: 0.4 }, { translate: "0 0" }],
        { duration: 420, easing: "steps(6, end)", composite: "add" });
      piscarUmaVez();
    }

    function ligar() {
      if (menos.matches) { if (respira) respira.cancel(); respira = null; clearTimeout(relogio); return; }
      respirar();
      agendar();
    }

    if ("IntersectionObserver" in window) {
      new IntersectionObserver(function (itens) {
        visivel = itens[0].isIntersecting;
        if (respira) { if (visivel && !document.hidden) respira.play(); else respira.pause(); }
      }).observe(img);
    } else {
      visivel = true;
    }
    document.addEventListener("visibilitychange", function () {
      if (respira) { if (document.hidden || !visivel) respira.pause(); else respira.play(); }
    });
    img.addEventListener("pointerenter", function (e) { if (e.pointerType === "mouse") pular(); });
    img.addEventListener("pointerdown", pular);
    if (menos.addEventListener) menos.addEventListener("change", ligar);
    if (img.complete) ligar(); else img.addEventListener("load", ligar, { once: true });
  });
})();
