/* Menu do celular: o botão abre e fecha o painel com os links; fecha ao escolher um link, ao tocar fora e com Esc. */
(function () {
  "use strict";

  var menu = document.querySelector(".menu");
  var botao = document.querySelector(".menu-abrir");
  if (!menu || !botao) return;
  // os textos no idioma da página; as páginas dos projetos não têm o bloco e ficam em português
  var bloco = document.getElementById("textos-js");
  var T = bloco ? JSON.parse(bloco.textContent) : {};

  function abrir(sim) {
    menu.classList.toggle("aberto", sim);
    botao.setAttribute("aria-expanded", sim ? "true" : "false");
    botao.setAttribute("aria-label", sim ? T.menu_fechar || "Fechar o menu" : T.menu_abrir || "Abrir o menu");
  }

  botao.addEventListener("click", function () {
    abrir(!menu.classList.contains("aberto"));
  });
  menu.addEventListener("click", function (e) {
    if (e.target.closest(".menu-links a")) abrir(false);
  });
  document.addEventListener("click", function (e) {
    if (menu.classList.contains("aberto") && !menu.contains(e.target)) abrir(false);
  });
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape" && menu.classList.contains("aberto")) {
      abrir(false);
      botao.focus();
    }
  });
})();

/* Seletor de idioma: a lista fecha ao tocar fora e com Esc, e a escolha fica guardada. Quem chega por um navegador
   em outro idioma que o site tem vê, uma vez, um aviso discreto com o link (sem trocar de página sozinho). */
(function () {
  "use strict";

  var seletor = document.querySelector(".idiomas");
  if (!seletor) return;
  var links = [].slice.call(seletor.querySelectorAll("a[hreflang]"));
  var aqui = document.documentElement.lang;
  function guardado(chave, valor) {
    try { if (valor === undefined) return localStorage.getItem(chave); localStorage.setItem(chave, valor); } catch (e) {}
    return null;
  }

  document.addEventListener("click", function (e) {
    if (seletor.open && !seletor.contains(e.target)) seletor.open = false;
  });
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape" && seletor.open) {
      seletor.open = false;
      seletor.querySelector("summary").focus();
    }
  });
  links.forEach(function (a) {
    a.addEventListener("click", function () { guardado("idioma", a.hreflang); });
  });

  // o aviso: só quando a pessoa ainda não escolheu nem fechou, e o primeiro idioma do navegador é outro que o site tem
  if (guardado("idioma") || guardado("idioma-aviso")) return;
  var pedido = (navigator.languages && navigator.languages[0]) || navigator.language || "";
  var primeiro = function (l) { return l.toLowerCase().split("-")[0]; };
  if (!pedido || pedido.toLowerCase() === aqui.toLowerCase()) return;
  var alvo = links.filter(function (a) { return a.hreflang.toLowerCase() === pedido.toLowerCase(); })[0];
  // sem o idioma exato (en-US, pt, de-AT), serve o da mesma língua, mas não se a página já está nela
  if (!alvo && primeiro(pedido) !== primeiro(aqui)) {
    alvo = links.filter(function (a) { return primeiro(a.hreflang) === primeiro(pedido); })[0];
  }
  if (!alvo) return;

  var aviso = document.createElement("div");
  aviso.className = "idioma-aviso";
  aviso.lang = alvo.hreflang;
  var link = document.createElement("a");
  link.href = alvo.getAttribute("href");
  link.hreflang = alvo.hreflang;
  link.textContent = alvo.dataset.sugestao + " →";
  link.addEventListener("click", function () { guardado("idioma", alvo.hreflang); });
  var fechar = document.createElement("button");
  fechar.type = "button";
  fechar.setAttribute("aria-label", alvo.dataset.fechar);
  fechar.textContent = "×";
  fechar.addEventListener("click", function () {
    guardado("idioma-aviso", "fechado");
    aviso.remove();
  });
  aviso.appendChild(link);
  aviso.appendChild(fechar);
  document.querySelector(".topo").appendChild(aviso);
})();
