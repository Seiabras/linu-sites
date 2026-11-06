/* Digital Linu (6/11/2026): tema, menu do celular, filtro por área, o pacote que se monta, o formulário que escreve
   a mensagem e as entradas ao rolar. Sem biblioteca; tudo funciona sem JavaScript, menos o filtro e o pacote. */
(function () {
  "use strict";
  var raiz = document.documentElement;
  var menosMovimento = window.matchMedia("(prefers-reduced-motion: reduce)");
  function guardar(k, v) { try { localStorage.setItem(k, v); } catch (e) {} }
  function ler(k) { try { return localStorage.getItem(k); } catch (e) { return null; } }

  /* 1. Tema: sem escolha, segue o sistema; o botão alterna e guarda */
  var botaoTema = document.querySelector("[data-tema]");
  var sistemaEscuro = window.matchMedia("(prefers-color-scheme: dark)");
  function escuroAgora() { return raiz.dataset.theme ? raiz.dataset.theme === "dark" : sistemaEscuro.matches; }
  function rotularTema() {
    var escuro = escuroAgora();
    botaoTema.setAttribute("aria-label", escuro ? "Mudar para o modo claro" : "Mudar para o modo escuro");
    botaoTema.title = escuro ? "Modo claro" : "Modo escuro";
  }
  botaoTema.addEventListener("click", function () {
    raiz.dataset.theme = escuroAgora() ? "light" : "dark";
    guardar("tema", raiz.dataset.theme);
    rotularTema();
  });
  sistemaEscuro.addEventListener("change", rotularTema);
  rotularTema();

  /* 2. Menu do celular */
  var abrir = document.querySelector(".menu-abrir");
  var links = document.getElementById("menu-links");
  function fecharMenu() { abrir.setAttribute("aria-expanded", "false"); links.classList.remove("aberto"); }
  abrir.addEventListener("click", function () {
    var aberto = abrir.getAttribute("aria-expanded") === "true";
    abrir.setAttribute("aria-expanded", String(!aberto));
    abrir.setAttribute("aria-label", aberto ? "Abrir o menu" : "Fechar o menu");
    links.classList.toggle("aberto", !aberto);
  });
  links.addEventListener("click", function (e) { if (e.target.closest("a")) fecharMenu(); });
  document.addEventListener("keydown", function (e) { if (e.key === "Escape") fecharMenu(); });

  /* 3. Filtro por área */
  var areas = document.querySelector("[data-areas]");
  var servicos = Array.prototype.slice.call(document.querySelectorAll(".servico"));
  areas.hidden = false;
  function filtrar(area) {
    areas.querySelectorAll("[data-area]").forEach(function (b) {
      b.setAttribute("aria-pressed", String(b.dataset.area === area));
    });
    servicos.forEach(function (s) {
      var mostra = area === "todas" || s.dataset.cat === area;
      if (mostra && s.hidden) {
        s.hidden = false;
        s.classList.add("chegando");
        requestAnimationFrame(function () { requestAnimationFrame(function () { s.classList.remove("chegando"); }); });
      } else if (!mostra) {
        s.hidden = true;
      }
    });
    var ativo = areas.querySelector('[aria-pressed="true"]');
    if (ativo && ativo.scrollIntoView && areas.scrollWidth > areas.clientWidth) {
      ativo.scrollIntoView({ block: "nearest", inline: "center", behavior: menosMovimento.matches ? "auto" : "smooth" });
    }
  }
  areas.addEventListener("click", function (e) {
    var b = e.target.closest("[data-area]");
    if (b) filtrar(b.dataset.area);
  });
  document.querySelectorAll("[data-ir-area]").forEach(function (a) {
    a.addEventListener("click", function () { filtrar(a.dataset.irArea); });
  });

  /* 4. O pacote: guardado no navegador, mostrado ao lado (computador), na barra de baixo (celular e tablet) e no
        formulário */
  var nomes = {};
  servicos.forEach(function (s) { nomes[s.dataset.id] = s.querySelector("h3").textContent; });
  var escolhidos = [];
  try { escolhidos = (JSON.parse(ler("digital-pacote")) || []).filter(function (id) { return nomes[id]; }); } catch (e) {}

  var lista = document.querySelector("[data-pacote-lista]");
  var vazio = document.querySelector("[data-pacote-vazio]");
  var limpar = document.querySelector("[data-pacote-limpar]");
  var barra = document.querySelector("[data-barra]");
  var barraTexto = document.querySelector("[data-barra-texto]");
  var noFormulario = document.querySelector("[data-formulario-pacote]");

  function contagem(n) { return n === 1 ? "1 serviço" : n + " serviços"; }
  function mostrarPacote() {
    guardar("digital-pacote", JSON.stringify(escolhidos));
    servicos.forEach(function (s) {
      var dentro = escolhidos.indexOf(s.dataset.id) >= 0;
      var b = s.querySelector("[data-adicionar]");
      b.setAttribute("aria-pressed", String(dentro));
      b.textContent = dentro ? "No pacote ✓" : "Adicionar";
      s.classList.toggle("escolhido", dentro);
    });
    lista.textContent = "";
    escolhidos.forEach(function (id) {
      var li = document.createElement("li");
      var tirar = document.createElement("button");
      tirar.type = "button";
      tirar.className = "pacote-tirar";
      tirar.dataset.tirar = id;
      tirar.setAttribute("aria-label", "Tirar " + nomes[id] + " do pacote");
      tirar.textContent = "×";
      li.appendChild(document.createTextNode(nomes[id]));
      li.appendChild(tirar);
      lista.appendChild(li);
    });
    var n = escolhidos.length;
    vazio.hidden = n > 0;
    limpar.hidden = n === 0;
    barra.hidden = n === 0;
    barraTexto.textContent = n ? contagem(n) + " no pacote" : "";
    noFormulario.textContent = n ? escolhidos.map(function (id) { return nomes[id]; }).join(", ")
      : "Nenhum serviço escolhido: tudo bem, conte na mensagem.";
    escreverMensagem();
  }
  function alternar(id) {
    var i = escolhidos.indexOf(id);
    if (i >= 0) escolhidos.splice(i, 1); else escolhidos.push(id);
    mostrarPacote();
  }
  document.querySelector("[data-servicos]").addEventListener("click", function (e) {
    var b = e.target.closest("[data-adicionar]");
    if (b) alternar(b.closest(".servico").dataset.id);
  });
  lista.addEventListener("click", function (e) {
    var b = e.target.closest("[data-tirar]");
    if (b) alternar(b.dataset.tirar);
  });
  limpar.addEventListener("click", function () { escolhidos = []; mostrarPacote(); });
  document.querySelectorAll("[data-escolher-pacote]").forEach(function (b) {
    b.addEventListener("click", function () {
      escolhidos = b.dataset.escolherPacote.split(" ");
      mostrarPacote();
      filtrar("todas");
      var alvo = document.getElementById("servicos");
      alvo.scrollIntoView({ behavior: menosMovimento.matches ? "auto" : "smooth" });
    });
  });
  // a barra de baixo some quando o formulário já está à vista
  var contato = document.getElementById("contato");
  if ("IntersectionObserver" in window) {
    new IntersectionObserver(function (itens) {
      barra.classList.toggle("escondida", itens[0].isIntersecting);
    }, { threshold: 0.15 }).observe(contato);
  }

  /* 5. Formulário: validação na hora e a mensagem pronta para o WhatsApp e o e-mail */
  var form = document.querySelector("[data-formulario]");
  function campo(k) { return document.getElementById(k); }
  var campos = { nome: campo("nome"), negocio: campo("negocio") };
  var avisos = { nome: "Escreva o seu nome.", negocio: "Conte o tipo de negócio e a cidade." };
  // o que foi digitado não se perde ao recarregar
  ["nome", "negocio", "mensagem"].forEach(function (k) {
    var v = ler("digital-" + k);
    if (v) campo(k).value = v;
    campo(k).addEventListener("input", function () { guardar("digital-" + k, campo(k).value); escreverMensagem(); });
  });
  function conferir(k, mostrar) {
    var ok = campos[k].value.trim().length >= 2;
    if (mostrar || ok) {
      document.getElementById(k + "-erro").textContent = ok ? "" : avisos[k];
      campos[k].setAttribute("aria-invalid", String(!ok));
    }
    return ok;
  }
  Object.keys(campos).forEach(function (k) {
    campos[k].addEventListener("blur", function () { if (campos[k].value) conferir(k, true); });
    campos[k].addEventListener("input", function () { conferir(k, false); });
  });
  function texto() {
    var partes = ["Olá, Digital Linu! Quero um orçamento."];
    if (campo("nome").value.trim()) partes.push("Nome: " + campo("nome").value.trim());
    if (campo("negocio").value.trim()) partes.push("Negócio: " + campo("negocio").value.trim());
    if (escolhidos.length) partes.push("Pacote: " + escolhidos.map(function (id) { return nomes[id]; }).join(", "));
    if (campo("mensagem").value.trim()) partes.push(campo("mensagem").value.trim());
    return partes.join("\n");
  }
  var whats = form.querySelector('[data-enviar="whatsapp"]');
  var email = form.querySelector('[data-enviar="email"]');
  function escreverMensagem() {
    var t = encodeURIComponent(texto());
    whats.href = "https://wa.me/5561996672610?text=" + t;
    email.href = "mailto:contato@linupedia.com.br?subject=" + encodeURIComponent("Orçamento Digital Linu") + "&body=" + t;
  }
  [whats, email].forEach(function (a) {
    a.addEventListener("click", function (e) {
      var ok = conferir("nome", true) & conferir("negocio", true);
      if (!ok) {
        e.preventDefault();
        form.querySelector('[aria-invalid="true"]').focus();
        return;
      }
      a.classList.add("enviado");
      setTimeout(function () { a.classList.remove("enviado"); }, 1600);
    });
  });

  /* 6. Voltar ao topo, sem deixar o # no endereço */
  document.querySelector("[data-voltar]").addEventListener("click", function (e) {
    e.preventDefault();
    window.scrollTo({ top: 0, behavior: menosMovimento.matches ? "auto" : "smooth" });
  });

  /* 7. Entradas ao rolar: um observer só, uma vez por elemento, escalonado nas listas; o que já está na tela no
        carregamento não é escondido (DIRETRIZES-UX.md, seção 1) */
  if ("IntersectionObserver" in window && !menosMovimento.matches) {
    var alvos = document.querySelectorAll(".secao h2, .secao-sub, .servico, .pacote-pronto, .passos li, .duvidas details");
    var vistos = new IntersectionObserver(function (itens) {
      itens.forEach(function (item) {
        if (!item.isIntersecting) return;
        item.target.classList.remove("antes");
        vistos.unobserve(item.target);
      });
    }, { rootMargin: "0px 0px -8% 0px" });
    var altura = window.innerHeight;
    alvos.forEach(function (el) {
      if (el.getBoundingClientRect().top < altura) return;
      var irmaos = el.parentElement.children;
      var posicao = Array.prototype.indexOf.call(irmaos, el) % 6;
      el.style.setProperty("--atraso", posicao * 50 + "ms");
      el.classList.add("antes");
      vistos.observe(el);
    });
  }

  /* 8. Identidade visual: tocar numa cor copia o código */
  var copiado = document.querySelector("[data-copiado]");
  var limparAviso;
  document.querySelectorAll("[data-copiar]").forEach(function (b) {
    b.addEventListener("click", function () {
      var codigo = b.dataset.copiar;
      function avisar(ok) {
        copiado.textContent = ok ? codigo + " copiado." : "Copie à mão: " + codigo;
        clearTimeout(limparAviso);
        limparAviso = setTimeout(function () { copiado.textContent = ""; }, 2500);
      }
      if (navigator.clipboard) navigator.clipboard.writeText(codigo).then(function () { avisar(true); }, function () { avisar(false); });
      else avisar(false);
    });
  });

  /* 9. Raio-X: cada "não" (ou "sim", no site) aponta um serviço, com o motivo; o resultado vai para o pacote */
  var RAIOX = {
    maps: { nao: ["meu-negocio", "Quem procura no Google Maps ainda não acha você: é o primeiro passo, e o mais barato."] },
    perfil: { nao: ["perfil", "O perfil é a vitrine: quem chega de um anúncio ou de um Reels decide ali se segue."] },
    posta: { nao: ["gestao", "Sem constância, o Instagram mostra menos o que você posta. A gestão mensal resolve o calendário."] },
    video: { nao: ["reels", "Vídeo curto é o que mais leva o perfil para quem ainda não segue você."] },
    anuncio: { nao: ["meta", "Anúncio com orçamento pequeno e bem mirado traz gente da sua região já no primeiro mês."] },
    marca: { nao: ["identidade", "Logo e cores definidas fazem tudo o que você publica parecer da mesma marca."] },
    whats: { nao: ["whatsapp", "Resposta rápida no WhatsApp é cliente que não vai para o concorrente."] },
    site: { sim: ["seo", "Com site, o SEO básico ajuda o Google a mostrar você para quem procura."] }
  };
  var perguntas = document.querySelectorAll("[data-pergunta]");
  var rxLista = document.querySelector("[data-raiox-lista]");
  var rxVazio = document.querySelector("[data-raiox-vazio]");
  var rxContagem = document.querySelector("[data-raiox-contagem]");
  var rxSite = document.querySelector("[data-raiox-site]");
  var rxUsar = document.querySelector("[data-raiox-usar]");
  var rxIds = [];
  var respostas = {};
  try { respostas = JSON.parse(ler("digital-raiox")) || {}; } catch (e) {}
  function lerRaiox() {
    var n = 0;
    rxIds = [];
    rxLista.textContent = "";
    perguntas.forEach(function (f) {
      var k = f.dataset.pergunta;
      var marcada = f.querySelector("input:checked");
      if (!marcada) return;
      n++;
      respostas[k] = marcada.value;
      var rec = RAIOX[k][marcada.value];
      if (!rec) return;
      rxIds.push(rec[0]);
      var li = document.createElement("li");
      var b = document.createElement("b");
      b.textContent = nomes[rec[0]];
      li.appendChild(b);
      li.appendChild(document.createTextNode(rec[1]));
      rxLista.appendChild(li);
    });
    guardar("digital-raiox", JSON.stringify(respostas));
    rxContagem.textContent = n + " de " + perguntas.length + " respondidas";
    if (n === perguntas.length && rxIds.length === 0) {
      rxIds = ["google-ads"];
      var li = document.createElement("li");
      var b = document.createElement("b");
      b.textContent = nomes["google-ads"];
      li.appendChild(b);
      li.appendChild(document.createTextNode("Está tudo em dia. O próximo passo costuma ser aparecer no alto da busca do Google."));
      rxLista.appendChild(li);
    }
    rxVazio.hidden = rxIds.length > 0;
    rxSite.hidden = respostas.site !== "nao";
    rxUsar.hidden = rxIds.length === 0;
  }
  perguntas.forEach(function (f) {
    var k = f.dataset.pergunta;
    if (respostas[k]) {
      var r = f.querySelector('input[value="' + respostas[k] + '"]');
      if (r) r.checked = true;
    }
    f.addEventListener("change", lerRaiox);
  });
  rxUsar.addEventListener("click", function () {
    rxIds.forEach(function (id) { if (escolhidos.indexOf(id) < 0) escolhidos.push(id); });
    mostrarPacote();
    filtrar("todas");
    rxUsar.textContent = "No pacote ✓";
    setTimeout(function () { rxUsar.textContent = "Levar para o meu pacote"; }, 1600);
    document.getElementById("servicos").scrollIntoView({ behavior: menosMovimento.matches ? "auto" : "smooth" });
  });
  lerRaiox();

  mostrarPacote();
})();
