/* A página de login do Café Aurora (projeto final de Desenvolvimento de Interfaces, 18/11/2026).
   O Café é fictício: a conta fica só neste navegador (localStorage) e nada sai daqui. A senha não é guardada: fica
   só o resumo SHA-256 dela com o e-mail. Num site de verdade, quem confere a senha é o servidor, por HTTPS. */
(() => {
  'use strict';
  const $ = (s, d = document) => d.querySelector(s), $$ = (s, d = document) => [...d.querySelectorAll(s)];
  const CONTAS = 'aurora-contas', SESSAO = 'aurora-sessao';
  const ler = (k, padrao) => { try { return JSON.parse(localStorage.getItem(k)) ?? padrao; } catch (e) { return padrao; } };
  const gravar = (k, v) => { try { localStorage.setItem(k, JSON.stringify(v)); } catch (e) {} };

  // ---- as abas Entrar e Criar conta (padrão de abas da WAI-ARIA: setas trocam, Tab entra no painel)
  const abas = $$('[role="tab"]');
  function abrirAba(aba, foco) {
    abas.forEach((a) => {
      const sim = a === aba;
      a.setAttribute('aria-selected', String(sim));
      a.tabIndex = sim ? 0 : -1;
      $('#' + a.getAttribute('aria-controls')).hidden = !sim;
    });
    if (foco) aba.focus();
    msg('');
  }
  abas.forEach((a, i) => {
    a.addEventListener('click', () => abrirAba(a));
    a.addEventListener('keydown', (e) => {
      const passo = { ArrowRight: 1, ArrowLeft: -1 }[e.key];
      if (passo) { e.preventDefault(); abrirAba(abas[(i + passo + abas.length) % abas.length], true); }
      if (e.key === 'Home') { e.preventDefault(); abrirAba(abas[0], true); }
      if (e.key === 'End') { e.preventDefault(); abrirAba(abas[abas.length - 1], true); }
    });
  });
  $$('[data-ir-aba]').forEach((b) => b.addEventListener('click', () => abrirAba($('#' + b.dataset.irAba), true)));

  // ---- mostrar ou esconder a senha
  $$('.senha button').forEach((b) => b.addEventListener('click', () => {
    const campo = b.previousElementSibling, ver = campo.type === 'password';
    campo.type = ver ? 'text' : 'password';
    b.setAttribute('aria-pressed', String(ver));
    b.textContent = ver ? b.dataset.esconder : b.dataset.mostrar;
  }));

  // ---- mensagens e erros de cada campo
  const caixaMsg = $('#entrarMsg');
  function msg(texto, erro) { caixaMsg.textContent = texto; caixaMsg.classList.toggle('entrar__msg--erro', !!erro); }
  function erroDe(campo, texto) {
    const p = $('#' + campo.id + 'Erro');
    campo.setAttribute('aria-invalid', texto ? 'true' : 'false');
    if (p) { p.textContent = texto || ''; p.hidden = !texto; }
    return !texto;
  }
  const EMAIL = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  const resumo = async (email, senha) => {
    const dados = new TextEncoder().encode(email.toLowerCase() + '\n' + senha);
    const h = await crypto.subtle.digest('SHA-256', dados);
    return [...new Uint8Array(h)].map((b) => b.toString(16).padStart(2, '0')).join('');
  };
  const T = JSON.parse($('#textos-entrar').textContent);

  // ---- criar conta
  const fCad = $('#formCadastro');
  fCad.addEventListener('submit', async (e) => {
    e.preventDefault();
    const nome = $('#cNome'), email = $('#cEmail'), senha = $('#cSenha'), conf = $('#cConfirma');
    const ok = [
      erroDe(nome, nome.value.trim().length >= 2 ? '' : T.e_nome),
      erroDe(email, EMAIL.test(email.value.trim()) ? '' : T.e_email),
      erroDe(senha, senha.value.length >= 8 && /\d/.test(senha.value) && /[a-z]/i.test(senha.value) ? '' : T.e_senha),
      erroDe(conf, conf.value && conf.value === senha.value ? '' : T.e_confirma),
    ];
    if (ok.includes(false)) { $('[aria-invalid="true"]', fCad).focus(); msg(T.corrija, true); return; }
    const contas = ler(CONTAS, []);
    const e1 = email.value.trim().toLowerCase();
    if (contas.some((c) => c.email === e1)) { erroDe(email, T.e_existe); email.focus(); msg(T.corrija, true); return; }
    contas.push({ nome: nome.value.trim(), email: e1, resumo: await resumo(e1, senha.value) });
    gravar(CONTAS, contas);
    entrou({ nome: nome.value.trim(), email: e1 }, T.ok_criada);
  });

  // ---- entrar
  const fEnt = $('#formEntrar');
  fEnt.addEventListener('submit', async (e) => {
    e.preventDefault();
    const email = $('#eEmail'), senha = $('#eSenha');
    const ok = [erroDe(email, EMAIL.test(email.value.trim()) ? '' : T.e_email), erroDe(senha, senha.value ? '' : T.e_vazia)];
    if (ok.includes(false)) { $('[aria-invalid="true"]', fEnt).focus(); msg(T.corrija, true); return; }
    const e1 = email.value.trim().toLowerCase();
    const conta = ler(CONTAS, []).find((c) => c.email === e1);
    if (!conta || conta.resumo !== await resumo(e1, senha.value)) {
      // a mesma mensagem para e-mail e para senha: não conta a quem tenta se o e-mail existe
      msg(T.e_login, true); senha.value = ''; senha.focus(); return;
    }
    entrou({ nome: conta.nome, email: e1 }, '', $('#eLembrar').checked);
  });

  // ---- depois de entrar, e sair
  const area = $('#entrarArea'), feito = $('#entrarOk');
  function entrou(sessao, aviso, lembrar = true) {
    if (lembrar) gravar(SESSAO, sessao);
    else { try { localStorage.removeItem(SESSAO); sessionStorage.setItem(SESSAO, JSON.stringify(sessao)); } catch (e) {} }
    mostrarSessao(sessao, aviso);
  }
  function mostrarSessao(sessao, aviso) {
    area.hidden = true; feito.hidden = false;
    $('#okTitulo').textContent = T.ola.replace('{nome}', sessao.nome.split(' ')[0]);
    $('#okTexto').textContent = (aviso ? aviso + ' ' : '') + T.ok_texto.replace('{email}', sessao.email);
    $('#okTitulo').focus();
  }
  $('#sair').addEventListener('click', () => {
    try { localStorage.removeItem(SESSAO); sessionStorage.removeItem(SESSAO); } catch (e) {}
    feito.hidden = true; area.hidden = false; fEnt.reset(); fCad.reset();
    abrirAba(abas[0], true);
    msg(T.saiu);
  });
  let sessao = ler(SESSAO, null);
  if (!sessao) { try { sessao = JSON.parse(sessionStorage.getItem(SESSAO)); } catch (e) {} }
  if (sessao) mostrarSessao(sessao);
})();
