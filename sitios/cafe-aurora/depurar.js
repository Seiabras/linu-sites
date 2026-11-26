/* A depuração do Café Aurora (26/11/2026): com ela ligada (no painel de acessibilidade), tocar ou clicar em qualquer
   parte da tela mostra como aquela parte foi feita: o que ela é e em que arquivos está, a caixa (tamanho, margem,
   recuo), o estilo calculado, as regras do CSS que pegam nela, na ordem em que o navegador aplica, e o HTML.
   Só é baixado na primeira vez que alguém liga (recursos.js). Os textos vêm do bloco #textos-cafe (chave "ux"),
   e a explicação de cada parte, da lista "dep_partes": [seletor, o que é, arquivos].
   Enquanto está ligada, o clique não faz o que faria (não abre link nem envia formulário): só inspeciona.
   Esc, ou "Sair" na barra do alto, desliga. No teclado: Tab até a parte e a tecla I inspeciona. */
(() => {
  'use strict';
  if (window.AuroraDepurar) return;
  const raiz = document.documentElement;
  const $ = (s, d = document) => d.querySelector(s), $$ = (s, d = document) => [...d.querySelectorAll(s)];
  const el = (tag, attrs = {}, texto) => {
    const e = document.createElement(tag);
    for (const [k, v] of Object.entries(attrs)) e.setAttribute(k, v);
    if (texto != null) e.textContent = texto;
    return e;
  };
  const f = (txt, dados) => String(txt || '').replace(/\{(\w+)\}/g, (_, k) => dados[k] ?? '');
  let T = {}, ligada = false, selecionado = null, quadro = 0;

  // As peças da depuração: a barra do alto, as duas molduras (a do ponteiro e a da parte escolhida) e o inspetor
  const barra = el('div', { class: 'dep-barra', role: 'status' });
  const moldura = el('div', { class: 'dep-moldura', 'aria-hidden': 'true' });
  const rotulo = el('span', { class: 'dep-moldura__rotulo' });
  moldura.append(rotulo);
  const escolha = el('div', { class: 'dep-moldura dep-moldura--sel', 'aria-hidden': 'true' });
  const insp = el('aside', { class: 'dep-insp hud', id: 'depInsp', tabindex: '-1' });
  const ehDaDepuracao = (n) => !!(n && n.closest && n.closest('.dep-barra, .dep-insp, .dep-moldura'));

  /* ---------- o que mostrar de uma parte ---------- */
  const nomeDe = (n) => {
    let s = n.tagName.toLowerCase();
    if (n.id) s += '#' + n.id;
    const cls = [...n.classList].filter((c) => !/^(in|reveal|so-noite|so-dia|carrossel__atual)$/.test(c)).slice(0, 2);
    if (cls.length) s += '.' + cls.join('.');
    return s;
  };

  // A explicação: a primeira parte da lista que pega na própria peça ou, subindo, na mais próxima que a contém
  function explicar(n) {
    const partes = T.dep_partes || [];
    for (let p = n; p && p.nodeType === 1; p = p.parentElement) {
      for (const [sel, texto, arquivos] of partes) {
        try { if (p.matches(sel)) return { texto, arquivos, de: p === n ? null : p }; } catch (e) {}
      }
    }
    return null;
  }

  const ARQ = (href) => (href ? decodeURIComponent(new URL(href).pathname.split('/').pop()) : 'index.html');
  // pseudoelementos e estados não "pegam" com matches(): tira e anota
  const PSEUDO = /::?(before|after|backdrop|placeholder|selection|marker|first-letter|first-line|-webkit-[\w-]+|-moz-[\w-]+)(\([^)]*\))?/g;
  const ESTADO = /:(hover|focus-visible|focus-within|focus|active|visited|checked|disabled|placeholder-shown)\b/g;

  // As regras de CSS do próprio site que pegam na peça (todas as folhas vêm do mesmo endereço, então dá para ler)
  function regrasDe(n) {
    const achadas = [];
    const ver = (lista, arquivo, condicao) => {
      for (const r of lista) {
        if (r.type === 4 || r.type === 12) { // @media, @supports
          const cond = r.conditionText || (r.media && r.media.mediaText) || '';
          if (r.type === 4 && !matchMedia(cond).matches) continue;
          try { if (r.type === 12 && !CSS.supports(cond)) continue; } catch (e) {}
          ver(r.cssRules, arquivo, '@' + (r.type === 4 ? 'media ' : 'supports ') + cond);
          continue;
        }
        if (r.cssRules && r.cssRules.length && !r.selectorText) { ver(r.cssRules, arquivo, condicao); continue; } // @layer, @container
        if (!r.selectorText) continue;
        const partes = r.selectorText.split(/,(?![^(]*\))/);
        let notas = [], pega = false;
        for (const parte of partes) {
          const base = parte.replace(PSEUDO, (m) => { notas.push(m.trim()); return ''; })
            .replace(ESTADO, (m) => { notas.push(m.trim()); return ''; }).trim();
          if (!base || /(^|[\s>])\*$/.test(base)) continue; // "*" e "html.x *" pegam em tudo: só fariam barulho
          try { if (n.matches(base)) { pega = true; break; } } catch (e) {}
        }
        if (pega) achadas.push({ seletor: r.selectorText, texto: r.style.cssText, arquivo, condicao, notas: [...new Set(notas)] });
      }
    };
    for (const folha of document.styleSheets) {
      let lista;
      try { lista = folha.cssRules; } catch (e) { continue; }
      ver(lista, ARQ(folha.href), '');
    }
    return achadas;
  }

  // O estilo calculado que vale contar (pula o que está no valor de sempre)
  const CAMPOS = [
    ['display', ''], ['position', 'static'], ['color', ''], ['background-color', 'rgba(0, 0, 0, 0)'],
    ['background-image', 'none'], ['font-family', ''], ['font-size', ''], ['font-weight', ''],
    ['letter-spacing', 'normal'], ['border', ''], ['border-radius', '0px'], ['box-shadow', 'none'],
    ['text-shadow', 'none'], ['transform', 'none'], ['filter', 'none'], ['backdrop-filter', 'none'],
    ['clip-path', 'none'], ['mix-blend-mode', 'normal'], ['opacity', '1'], ['z-index', 'auto'],
    ['animation-name', 'none'], ['grid-template-columns', 'none'], ['gap', 'normal'], ['pointer-events', 'auto'],
  ];

  function linha(dl, nome, valor, cor) {
    const dt = el('dt', {}, nome), dd = el('dd');
    if (cor) dd.append(el('span', { class: 'dep-cor', 'data-cor': '' }));
    dd.append(document.createTextNode(valor.length > 140 ? valor.slice(0, 140) + '…' : valor));
    if (cor) dd.firstChild.style.background = valor; // CSSOM: a CSP só barra o atributo style escrito no HTML
    dl.append(dt, dd);
  }

  function secao(titulo, aberta) {
    const d = el('details', { class: 'dep-secao' });
    if (aberta) d.open = true;
    d.append(el('summary', {}, titulo));
    insp.append(d);
    return d;
  }

  function html(n) {
    const copia = n.cloneNode(false);
    let s = copia.outerHTML;
    const fim = s.lastIndexOf('</');
    const abre = fim > 0 ? s.slice(0, fim) : s;
    const filhos = n.children.length, texto = (n.textContent || '').trim().replace(/\s+/g, ' ');
    let meio = '';
    if (filhos) meio = '\n  ' + f(T.dep_filhos, { n: filhos }) + '\n';
    else if (texto) meio = texto.length > 90 ? texto.slice(0, 90) + '…' : texto;
    return abre + meio + (fim > 0 ? s.slice(fim) : '');
  }

  /* ---------- desenhar o inspetor ---------- */
  function inspecionar(n) {
    selecionado = n;
    insp.textContent = '';
    insp.append(el('span', { class: 'hud__canto hud__canto--1', 'aria-hidden': 'true' }), el('span', { class: 'hud__canto hud__canto--2', 'aria-hidden': 'true' }));
    const topo = el('div', { class: 'dep-insp__topo' });
    const cab = el('div');
    cab.append(el('p', { class: 'hud__sistema', 'aria-hidden': 'true' }, T.dep_sys));
    const h = el('h2', { class: 'dep-insp__nome', id: 'depNome' });
    h.append(el('code', {}, nomeDe(n)));
    cab.append(h);
    const fechar = el('button', { type: 'button', class: 'janela__fechar', 'aria-label': T.dep_fechar }, '✕');
    fechar.addEventListener('click', () => { insp.hidden = true; escolha.hidden = true; selecionado = null; });
    topo.append(cab, fechar);
    insp.setAttribute('aria-labelledby', 'depNome');
    insp.append(topo);

    // o caminho até a parte: cada degrau leva a ela
    const caminho = el('ol', { class: 'dep-caminho', 'aria-label': T.dep_caminho });
    const subida = [];
    for (let p = n; p && p !== document.body && subida.length < 5; p = p.parentElement) subida.unshift(p);
    if (subida[0] && subida[0].parentElement !== document.body && subida[0] !== document.body) caminho.append(el('li', {}, '…'));
    subida.forEach((p) => {
      const li = el('li');
      const b = el('button', { type: 'button' }, nomeDe(p));
      if (p === n) b.setAttribute('aria-current', 'true');
      b.addEventListener('click', () => inspecionar(p));
      li.append(b);
      caminho.append(li);
    });
    insp.append(caminho);

    // como foi feito
    const exp = explicar(n);
    const como = secao(T.dep_como, true);
    if (exp) {
      if (exp.de) como.append(el('p', { class: 'dep-insp__de' }, f(T.dep_parte_de, { nome: nomeDe(exp.de) })));
      como.append(el('p', {}, exp.texto));
      if (exp.arquivos) {
        const arq = el('p', { class: 'dep-insp__arquivos' });
        arq.append(el('b', {}, T.dep_arquivos + ' '), el('code', {}, exp.arquivos));
        como.append(arq);
      }
    } else como.append(el('p', {}, f(T.dep_generico, { tag: '<' + n.tagName.toLowerCase() + '>' })));

    // a caixa
    const r = n.getBoundingClientRect(), cs = getComputedStyle(n);
    const caixa = secao(T.dep_caixa, true);
    const dl = el('dl', { class: 'dep-lista' });
    linha(dl, T.dep_tamanho, Math.round(r.width) + ' × ' + Math.round(r.height) + ' px');
    linha(dl, 'margin', cs.margin);
    linha(dl, 'padding', cs.padding);
    caixa.append(dl);

    // o estilo calculado
    const calc = secao(T.dep_calculado, false);
    const dl2 = el('dl', { class: 'dep-lista' });
    CAMPOS.forEach(([p, padrao]) => {
      const v = cs.getPropertyValue(p);
      if (!v || v === padrao || (p === 'border' && /^0px/.test(v))) return;
      linha(dl2, p, v, /color$/.test(p) && v !== 'rgba(0, 0, 0, 0)');
    });
    calc.append(dl2);

    // as regras do CSS: a última que aparece ganha quando as duas pesam o mesmo
    const regras = regrasDe(n);
    const css = secao(f(T.dep_regras, { n: regras.length }), true);
    if (!regras.length) css.append(el('p', {}, T.dep_sem_regras));
    const MAX = 12;
    regras.slice(-MAX).reverse().forEach((rg) => {
      const bloco = el('div', { class: 'dep-regra' });
      const onde = el('p', { class: 'dep-regra__onde' }, rg.arquivo + (rg.condicao ? ' · ' + rg.condicao : ''));
      bloco.append(onde);
      const pre = el('pre');
      const decl = rg.texto.split(/;\s(?![^(]*\))/).map((d) => '  ' + d.replace(/;$/, '') + ';').join('\n');
      pre.append(el('code', {}, rg.seletor + ' {\n' + decl + '\n}'));
      bloco.append(pre);
      if (rg.notas.length) bloco.append(el('p', { class: 'dep-regra__nota' }, f(T.dep_so_quando, { estados: rg.notas.join(' ') })));
      css.append(bloco);
    });
    if (regras.length > MAX) css.append(el('p', { class: 'dep-regra__nota' }, f(T.dep_mais, { n: regras.length - MAX })));

    // o HTML
    const cod = secao(T.dep_html, false);
    const pre = el('pre');
    pre.append(el('code', {}, html(n)));
    cod.append(pre);

    insp.hidden = false;
    escolha.hidden = false;
    // no celular o inspetor sobe de baixo: a página rola para a parte escolhida ficar à vista, acima dele
    if (matchMedia('(max-width: 699px)').matches) {
      const parte = n.getBoundingClientRect(), topo = insp.getBoundingClientRect().top, barra = 70;
      if (parte.bottom > topo - 12 || parte.top < barra) {
        const meio = barra + (topo - barra) / 2 - Math.min(parte.height, topo - barra) / 2;
        scrollBy({ top: parte.top - meio, behavior: 'auto' });
      }
    }
    posicionar();
  }

  /* ---------- as molduras acompanham a página ---------- */
  function por(m, n) {
    if (!n || !n.isConnected) { m.hidden = true; return; }
    const r = n.getBoundingClientRect();
    m.style.transform = `translate(${Math.round(r.left)}px, ${Math.round(r.top)}px)`;
    m.style.width = Math.round(r.width) + 'px';
    m.style.height = Math.round(r.height) + 'px';
  }
  let sobre = null;
  function posicionar() {
    cancelAnimationFrame(quadro);
    quadro = requestAnimationFrame(() => {
      if (sobre) {
        por(moldura, sobre);
        const r = sobre.getBoundingClientRect();
        rotulo.textContent = nomeDe(sobre) + '  ' + Math.round(r.width) + '×' + Math.round(r.height);
        moldura.classList.toggle('dep-moldura--embaixo', r.top < 26);
      }
      por(escolha, selecionado);
    });
  }

  /* ---------- os eventos enquanto está ligada ---------- */
  function alvo(e) {
    let n = e.target && e.target.nodeType === 1 ? e.target : e.target && e.target.parentElement;
    // o <span> que só guarda o texto de noite ou de dia não diz nada: vale a parte que o contém
    while (n && n.parentElement && n.classList.length === 1 && n.matches('span.so-noite, span.so-dia')) n = n.parentElement;
    return n && !ehDaDepuracao(n) && n !== raiz ? n : null;
  }
  function aoMover(e) {
    const n = alvo(e);
    if (n === sobre) return;
    sobre = n;
    moldura.hidden = !n;
    posicionar();
  }
  // o clique não faz o que faria: não abre link, não envia, não muda o filtro
  function aoClicar(e) {
    const n = alvo(e);
    if (!n) return;
    e.preventDefault();
    e.stopPropagation();
    e.stopImmediatePropagation();
    if (e.type === 'click') { inspecionar(n); if (matchMedia('(max-width: 699px)').matches) insp.focus({ preventScroll: true }); }
  }
  function aoTeclar(e) {
    if (e.key === 'Escape') {
      if (document.querySelector('dialog[open]')) return; // a janela aberta fecha primeiro
      e.preventDefault();
      desligar();
      return;
    }
    const n = document.activeElement;
    if ((e.key === 'i' || e.key === 'I') && !e.ctrlKey && !e.metaKey && !e.altKey && n && !ehDaDepuracao(n)
        && !/^(INPUT|TEXTAREA|SELECT)$/.test(n.tagName) && !n.isContentEditable) {
      e.preventDefault();
      inspecionar(n === document.body ? $('main') || n : n);
    }
  }
  const EVENTOS = ['click', 'pointerdown', 'mousedown', 'pointerup', 'mouseup', 'auxclick', 'dblclick', 'submit'];

  function ligar(textos) {
    if (textos) T = textos;
    if (ligada) return;
    ligada = true;
    if (!barra.isConnected) {
      const txt = el('p', { class: 'dep-barra__texto' });
      txt.append(el('b', { class: 'dep-barra__luz' }, T.dep_ativa), document.createTextNode(' ' + T.dep_dica));
      const sair = el('button', { type: 'button', class: 'btn dep-barra__sair' }, T.dep_sair);
      sair.addEventListener('click', desligar);
      barra.append(txt, sair);
      insp.hidden = true;
      escolha.hidden = true;
      moldura.hidden = true;
      document.body.append(moldura, escolha, barra, insp);
    } else barra.hidden = false;
    raiz.classList.add('depurando');
    EVENTOS.forEach((t) => addEventListener(t, aoClicar, true));
    addEventListener('pointermove', aoMover, { capture: true, passive: true });
    addEventListener('keydown', aoTeclar, true);
    addEventListener('scroll', posicionar, { capture: true, passive: true });
    addEventListener('resize', posicionar);
    $('.dep-barra__sair', barra).focus();
  }
  function desligar() {
    if (!ligada) return;
    ligada = false;
    raiz.classList.remove('depurando');
    EVENTOS.forEach((t) => removeEventListener(t, aoClicar, true));
    removeEventListener('pointermove', aoMover, { capture: true });
    removeEventListener('keydown', aoTeclar, true);
    removeEventListener('scroll', posicionar, { capture: true });
    removeEventListener('resize', posicionar);
    barra.hidden = true;
    insp.hidden = true;
    moldura.hidden = true;
    escolha.hidden = true;
    selecionado = sobre = null;
    const volta = $('.a11y-abrir');
    if (volta) volta.focus();
  }
  window.AuroraDepurar = { ligar, desligar };
})();
