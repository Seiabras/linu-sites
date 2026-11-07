/* Modo claro e escuro e a obra pronta (identidade “a planta”, 07/11/2026).

   O botão do topo é a luminária da prancheta. Com a planta na tela, apagar a luz mostra o cianotipo num círculo que
   sai da luminária (View Transitions, onde o navegador tem).

   A planta vira obra: na abertura (só em português por enquanto), as abas “Planta” e “Obra pronta” trocam o desenho
   pela cabana em pixel art. Ao abrir a obra, o Linu entra pela porta e fica no quarto. Com a obra na tela, trocar a luz
   (pelo botão do topo ou pelo “Apagar o lampião” embaixo da cena) é como era na estação: o Linu anda até o lampião,
   pula para puxar a cordinha, o lampião falha e apaga (ou acende), e a página troca de cor junto; depois ele volta.

   Com “menos movimento”, nada anda: a troca é na hora e a obra aparece sem a entrada do Linu. A escolha do tema fica
   guardada no navegador; sem escolha, vale a do sistema. As coordenadas são as da imagem da cena (344 × 192), e a cena
   está sempre em 2× (o CSS recorta onde não cabe); o Linu fica em 1× (172 × 190 px). */
(function () {
  "use strict";

  var raiz = document.documentElement;
  var bloco = document.getElementById("textos-js");
  var T = bloco ? JSON.parse(bloco.textContent) : {};
  var botoes = [].slice.call(document.querySelectorAll("[data-luz]"));
  var sistemaEscuro = window.matchMedia("(prefers-color-scheme: dark)");
  var poucoMovimento = window.matchMedia("(prefers-reduced-motion: reduce)");
  if (!botoes.length) return;

  var folha = document.querySelector(".prancha-folha");
  var obra = document.querySelector(".vista-obra");
  var cena = document.querySelector("[data-cena]");
  var linu = cena && cena.querySelector(".cena-linu");

  var K = 2;            // a escala da cena
  var LINU_PX = 172;    // o quadro do Linu, sempre em 1×
  var PORTA = 50;       // x dos pés na soleira da porta
  var REPOUSO = 118;    // onde ele fica parado, entre a porta e a mesa
  var LAMPIAO = 185;    // embaixo do lampião
  var MS_POR_PIXEL = 7;
  var ocupado = false;

  function temaAtual() {
    return raiz.dataset.theme || (sistemaEscuro.matches ? "dark" : "light");
  }

  function atualizarBotoes() {
    var escuro = temaAtual() === "dark";
    botoes.forEach(function (b) {
      // o botão embaixo da obra tem o texto à vista, que já é o nome dele; o do topo, só o ícone
      var texto = b.querySelector("[data-luz-texto]");
      if (texto) { texto.textContent = escuro ? "Acender o lampião" : "Apagar o lampião"; return; }
      b.setAttribute("aria-label", escuro ? T.luz_acender_aria || "Acender a luz (modo claro)" : T.luz_apagar_aria || "Apagar a luz (modo escuro)");
      b.title = escuro ? T.luz_acender || "Acender a luz" : T.luz_apagar || "Apagar a luz";
    });
  }

  function aplicar(tema, suave) {
    if (suave) {
      raiz.classList.add("trocando-tema");
      setTimeout(function () { raiz.classList.remove("trocando-tema"); }, 450);
    }
    raiz.dataset.theme = tema;
    try { localStorage.setItem("tema", tema); } catch (e) {}
    atualizarBotoes();
  }

  function esperar(ms) {
    return new Promise(function (ok) { setTimeout(ok, ms); });
  }

  /* ---- O Linu da obra ---- */

  // x é a coordenada da imagem; a resposta, em px de tela, é onde fica o canto esquerdo do Linu com os pés em x
  function px(x) { return Math.round(x * K - LINU_PX / 2) + "px"; }

  function parar(x, pose) {
    linu.getAnimations().forEach(function (a) { a.cancel(); });
    linu.style.left = px(x);
    linu.dataset.pose = pose || "frente";
    linu.setAttribute("data-parado", "");
    linu.dataset.x = x;
  }

  /* anda de um x a outro, de lado, com os quadros de caminhada; pode aparecer na porta */
  function andar(de, ate, aparecer) {
    linu.dataset.pose = ate > de ? "direita" : "esquerda";
    linu.setAttribute("data-andando", "");
    var quadros = [{ left: px(de), opacity: aparecer ? 0 : 1 }];
    if (aparecer) quadros.push({ left: px(de + (ate - de) * 0.25), opacity: 1 });
    quadros.push({ left: px(ate), opacity: 1 });
    return linu.animate(quadros, { duration: Math.abs(ate - de) * MS_POR_PIXEL, fill: "forwards" }).finished.then(function () {
      linu.removeAttribute("data-andando");
      parar(ate, "frente");
    });
  }

  function pulinho() {
    return linu.animate([
      { transform: "none" }, { transform: "translateY(-9%) scaleY(1.04)", offset: 0.4 }, { transform: "translateY(1%) scaleY(.96)", offset: 0.8 }, { transform: "none" }
    ], { duration: 340, easing: "ease-out" }).finished;
  }

  /* a luz da cena muda, e a página junto, no instante em que o lampião fica apagado (ou aceso) de vez.
     As camadas: o dia, a noite com o lampião aceso e, por cima, a noite com ele apagado. */
  async function trocarLuz(tema) {
    var acesa = cena.querySelector(".cena-acesa");
    var apagada = cena.querySelector(".cena-apagada");
    var noite = raiz.dataset.hora === "noite";
    if (tema === "dark") {
      if (!noite) {
        await acesa.animate([{ opacity: 0 }, { opacity: 1 }], { duration: 420, easing: "ease-out", fill: "forwards" }).finished;
        await esperar(120);
      }
      await apagada.animate([
        { opacity: 0 }, { opacity: 0.85, offset: 0.12 }, { opacity: 0.1, offset: 0.22 }, { opacity: 0.9, offset: 0.4 },
        { opacity: 0.45, offset: 0.52 }, { opacity: 1, offset: 0.68 }, { opacity: 1 }
      ], { duration: 900, fill: "forwards" }).finished;
      aplicar(tema, true);
    } else {
      acesa.animate([{ opacity: 1 }, { opacity: 1 }], { fill: "forwards" });
      await apagada.animate([
        { opacity: 1 }, { opacity: 0.2, offset: 0.15 }, { opacity: 0.9, offset: 0.28 }, { opacity: 0, offset: 0.45 },
        { opacity: 0.5, offset: 0.55 }, { opacity: 0 }
      ], { duration: 760, fill: "forwards" }).finished;
      aplicar(tema, true);
      if (!noite) {
        await esperar(380);
        await acesa.animate([{ opacity: 1 }, { opacity: 0 }], { duration: 900, easing: "ease-in-out", fill: "forwards" }).finished;
      }
    }
    // o CSS do tema novo já mostra a camada certa: as animações saem sem pular
    acesa.getAnimations().concat(apagada.getAnimations()).forEach(function (a) { a.cancel(); });
  }

  async function luzNaObra(tema) {
    var de = Number(linu.dataset.x) || REPOUSO;
    if (!linu.hasAttribute("data-parado")) { await andar(PORTA, REPOUSO, true); de = REPOUSO; }
    await andar(de, LAMPIAO);
    linu.dataset.pose = "costas";
    await esperar(220);
    await pulinho();
    await trocarLuz(tema);
    await esperar(250);
    linu.dataset.pose = "frente";
    await esperar(450);
    await andar(LAMPIAO, REPOUSO);
  }

  function obraNaTela() {
    if (!obra || obra.hidden) return false;
    var r = obra.getBoundingClientRect();
    var visivel = Math.min(r.bottom, window.innerHeight) - Math.max(r.top, 0);
    return visivel >= r.height * 0.5;
  }

  /* com a planta: o cianotipo abre num círculo que sai do botão */
  function luzNaPlanta(tema, botao) {
    if (poucoMovimento.matches || !document.startViewTransition) { aplicar(tema, true); return Promise.resolve(); }
    var r = botao.getBoundingClientRect();
    var x = r.left + r.width / 2;
    var y = r.top + r.height / 2;
    var raio = Math.hypot(Math.max(x, innerWidth - x), Math.max(y, innerHeight - y));
    var troca = document.startViewTransition(function () { aplicar(tema, false); });
    return troca.ready.then(function () {
      raiz.animate({ clipPath: ["circle(0px at " + x + "px " + y + "px)", "circle(" + raio + "px at " + x + "px " + y + "px)"] },
        { duration: 520, easing: "cubic-bezier(.4, 0, .2, 1)", pseudoElement: "::view-transition-new(root)" });
      return troca.finished;
    }).catch(function () {});
  }

  botoes.forEach(function (botao) {
    botao.addEventListener("click", function () {
      if (ocupado) return;
      var tema = temaAtual() === "dark" ? "light" : "dark";
      ocupado = true;
      botoes.forEach(function (b) { if (b.classList.contains("obra-luz")) b.disabled = true; });
      var feito = (obraNaTela() && !poucoMovimento.matches && Element.prototype.animate) ? luzNaObra(tema) : luzNaPlanta(tema, botao);
      feito.catch(function () { aplicar(tema, false); }).then(function () {
        ocupado = false;
        botoes.forEach(function (b) { b.disabled = false; });
      });
    });
  });

  /* ---- As abas da prancha: a planta e a obra pronta ---- */
  var vistas = document.querySelector(".vistas");
  if (vistas && folha && obra && linu) {
    var planta = folha.querySelector(".vista-planta");
    var abas = [].slice.call(vistas.querySelectorAll("[data-vista-botao]"));
    var imagens = [].slice.call(obra.querySelectorAll("img"));
    vistas.hidden = false;
    // as imagens da obra só baixam quando alguém mostra interesse (passar o mouse, focar ou tocar na aba)
    var carregar = function () { imagens.forEach(function (i) { i.loading = "eager"; }); };
    var abaObra = vistas.querySelector('[data-vista-botao="obra"]');
    ["pointerenter", "focus", "touchstart"].forEach(function (ev) { abaObra.addEventListener(ev, carregar, { once: true, passive: true }); });

    var trocar = async function (qual) {
      if (ocupado || folha.dataset.vista === qual) return;
      ocupado = true;
      abas.forEach(function (a) { a.setAttribute("aria-pressed", String(a.dataset.vistaBotao === qual)); });
      var sai = qual === "obra" ? planta : obra;
      var entra = qual === "obra" ? obra : planta;
      var anima = !poucoMovimento.matches && Element.prototype.animate;
      if (anima) await sai.animate([{ opacity: 1 }, { opacity: 0 }], { duration: 180, easing: "ease-in" }).finished;
      sai.hidden = true;
      entra.hidden = false;
      // a obra só imprime com a cabana já carregada (senão saía o quadro preto)
      if (qual === "obra") { carregar(); await Promise.all(imagens.map(function (i) { return i.decode().catch(function () {}); })); }
      folha.dataset.vista = qual;
      if (qual === "obra") {
        linu.removeAttribute("data-parado");
        linu.style.left = "";
        if (anima) {
          // a obra “imprime” de cima para baixo, em faixas, como a planta saindo do plotter
          await cena.animate([{ clipPath: "inset(0 0 100% 0)" }, { clipPath: "inset(0 0 0% 0)" }], { duration: 700, easing: "steps(12, end)" }).finished;
          await esperar(150);
          await andar(PORTA, REPOUSO, true);
        } else {
          parar(REPOUSO, "frente");
        }
      } else if (anima) {
        await entra.animate([{ opacity: 0 }, { opacity: 1 }], { duration: 220, easing: "ease-out" }).finished;
      }
      ocupado = false;
    };
    abas.forEach(function (a) { a.addEventListener("click", function () { trocar(a.dataset.vistaBotao); }); });

    // tocar no Linu parado: um pulinho
    linu.addEventListener("click", function () {
      if (ocupado || poucoMovimento.matches || !linu.hasAttribute("data-parado")) return;
      pulinho();
    });
  }

  // a hora vira com a página aberta: confere a cada cinco minutos (sem mexer no meio de uma troca)
  setInterval(function () {
    if (ocupado) return;
    var h = new Date().getHours();
    raiz.dataset.hora = h >= 6 && h < 18 ? "dia" : "noite";
  }, 300000);

  sistemaEscuro.addEventListener("change", atualizarBotoes);
  atualizarBotoes();
})();
