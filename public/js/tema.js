/* Modo claro e escuro com o Linu: ao tocar no botão da luz, o Linu entra no quarto pela porta, vai até o
   lampião, apaga (modo escuro) ou acende (modo claro) e sai. A página troca de cor no instante em que a
   luz da cena muda. A escolha fica guardada no navegador; sem escolha, vale a do sistema.
   Com "menos movimento" no aparelho, o Linu não anda: aparece embaixo do lampião e some.
   As coordenadas são as da imagem da cena (344 × 192), como no abrigo do app. */
(function () {
  "use strict";

  var raiz = document.documentElement;
  var botao = document.querySelector("[data-luz]");
  var cena = document.querySelector("[data-cena]");
  var sistemaEscuro = window.matchMedia("(prefers-color-scheme: dark)");
  var poucoMovimento = window.matchMedia("(prefers-reduced-motion: reduce)");
  if (!botao) return;

  var CENA_W = 344;
  var LINU_W = 52;
  var PORTA = 50;      // x dos pés na soleira da porta
  var LAMPIAO = 185;   // embaixo do lampião
  var MS_POR_PIXEL = 7;
  var ocupado = false;

  function temaAtual() {
    return raiz.dataset.theme || (sistemaEscuro.matches ? "dark" : "light");
  }

  function atualizarBotao() {
    var escuro = temaAtual() === "dark";
    var texto = escuro ? "Acender a luz (modo claro)" : "Apagar a luz (modo escuro)";
    botao.setAttribute("aria-label", texto);
    botao.title = escuro ? "Acender a luz" : "Apagar a luz";
  }

  function aplicarTema(tema, suave) {
    if (suave) {
      raiz.classList.add("trocando-tema");
      setTimeout(function () { raiz.classList.remove("trocando-tema"); }, 600);
    }
    raiz.dataset.theme = tema;
    try { localStorage.setItem("tema", tema); } catch (e) {}
    atualizarBotao();
  }

  function esperar(ms) {
    return new Promise(function (ok) { setTimeout(ok, ms); });
  }

  function posicao(x) {
    return ((x - LINU_W / 2) / CENA_W) * 100 + "%";
  }

  /* anda de um x a outro, de lado, com os quadros de caminhada; aparece ou some na porta */
  function andar(linu, de, ate, aparecer, sumir) {
    linu.dataset.pose = ate > de ? "direita" : "esquerda";
    linu.setAttribute("data-andando", "");
    var ms = Math.abs(ate - de) * MS_POR_PIXEL;
    var quadros = [{ left: posicao(de), opacity: aparecer ? 0 : 1 }];
    if (aparecer) quadros.push({ left: posicao(de + (ate - de) * 0.2), opacity: 1 });
    if (sumir) quadros.push({ left: posicao(ate - (ate - de) * 0.2), opacity: 1 });
    quadros.push({ left: posicao(ate), opacity: sumir ? 0 : 1 });
    return linu.animate(quadros, { duration: ms, fill: "forwards" }).finished.then(function () {
      linu.removeAttribute("data-andando");
    });
  }

  /* a luz da cena muda, e a página junto */
  function trocarLuz(alvo, tema) {
    var acesa = alvo.querySelector(".cena-acesa");
    var apagada = alvo.querySelector(".cena-apagada");
    aplicarTema(tema, true);
    if (tema === "dark") {
      // o lampião pisca e apaga
      return apagada.animate([{ opacity: 0 }, { opacity: 1, offset: 0.2 }, { opacity: 0.25, offset: 0.4 }, { opacity: 1 }], { duration: 380 }).finished;
    }
    // o lampião acende no escuro e o quarto clareia
    apagada.animate([{ opacity: 1 }, { opacity: 0, offset: 0.08 }, { opacity: 0 }], { duration: 1300 });
    return acesa.animate([{ opacity: 0 }, { opacity: 1, offset: 0.08 }, { opacity: 1, offset: 0.4 }, { opacity: 0 }], { duration: 1300, easing: "ease-in" }).finished;
  }

  function cenaVisivel() {
    if (!cena) return false;
    var r = cena.getBoundingClientRect();
    var visivel = Math.min(r.bottom, window.innerHeight) - Math.max(r.top, 0);
    return visivel >= r.height * 0.6;
  }

  async function animar(tema) {
    var alvo = cena;
    var cartao = null;
    if (!cenaVisivel()) {
      // a cena do topo está fora da tela: a troca aparece num cartão no canto
      cartao = document.createElement("div");
      cartao.className = "cena-flutuante";
      cartao.setAttribute("aria-hidden", "true");
      alvo = cena.cloneNode(true);
      alvo.removeAttribute("data-cena");
      cartao.appendChild(alvo);
      document.body.appendChild(cartao);
      await cartao.animate([{ opacity: 0, transform: "translateY(12px)" }, { opacity: 1, transform: "none" }], { duration: 220 }).finished;
    }
    var linu = alvo.querySelector(".cena-linu");
    await andar(linu, PORTA, LAMPIAO, true, false);
    linu.dataset.pose = "costas";
    await esperar(300);
    await trocarLuz(alvo, tema);
    await esperar(250);
    linu.dataset.pose = "frente";
    await esperar(450);
    await andar(linu, LAMPIAO, PORTA, false, true);
    linu.getAnimations().forEach(function (a) { a.cancel(); });
    linu.dataset.pose = "frente";
    if (cartao) {
      await cartao.animate([{ opacity: 1 }, { opacity: 0, transform: "translateY(12px)" }], { duration: 220, fill: "forwards" }).finished;
      cartao.remove();
    }
  }

  /* com "menos movimento" no aparelho (comum em computador de faculdade ou de trabalho), o Linu não anda:
     ele aparece embaixo do lampião, a luz troca e ele some, só com opacidade */
  async function animarParado(tema) {
    var linu = cena.querySelector(".cena-linu");
    linu.getAnimations().forEach(function (a) { a.cancel(); });
    linu.style.left = posicao(LAMPIAO);
    linu.dataset.pose = "costas";
    await linu.animate([{ opacity: 0 }, { opacity: 1 }], { duration: 200, fill: "forwards" }).finished;
    await esperar(250);
    aplicarTema(tema, true);
    await esperar(650);
    linu.dataset.pose = "frente";
    await esperar(300);
    await linu.animate([{ opacity: 1 }, { opacity: 0 }], { duration: 200, easing: "ease-in", fill: "forwards" }).finished;
    linu.getAnimations().forEach(function (a) { a.cancel(); });
    linu.style.left = "";
  }

  botao.addEventListener("click", function () {
    if (ocupado) return;
    var tema = temaAtual() === "dark" ? "light" : "dark";
    if (!cena || !Element.prototype.animate) {
      aplicarTema(tema, false);
      return;
    }
    ocupado = true;
    var feito = poucoMovimento.matches
      ? (cenaVisivel() ? animarParado(tema) : Promise.resolve(aplicarTema(tema, true)))
      : animar(tema);
    feito.catch(function () { aplicarTema(tema, false); }).then(function () { ocupado = false; });
  });

  // sem escolha guardada, o tema acompanha o sistema
  sistemaEscuro.addEventListener("change", atualizarBotao);
  atualizarBotao();
})();
