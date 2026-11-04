// Pica ou Não Pica? (1/11/2026): as partes que a pessoa usa com as mãos no guia em português.
// - Bichos: busca, grupo e perigo, tudo junto.
// - Que bicho é esse?: perguntas em árvore até o bicho, com "Voltar" e "Começar de novo"; o resultado diz se é perigoso.
// - Mitos: o jogo "Verdade ou mito?", com o placar guardado neste navegador.
// Tudo montado com textContent. Sem JavaScript, as páginas mostram a lista inteira.
(() => {
    const el = (tag, cls, texto) => { const e = document.createElement(tag); if (cls) e.className = cls; if (texto != null) e.textContent = texto; return e; };
    const ler = (id) => { try { return JSON.parse(document.getElementById(id).textContent); } catch { return null; } };
    // as frases vêm no idioma da página: o grupo "guia" do #textos-estudo (o scripts-pt.json do gerador, traduzido pelo
    // catálogo de cada língua); {n} e afins são trocados pelos valores
    const T = (ler('textos-estudo') || {}).guia || {};
    const t = (k, v = {}) => String(T[k] ?? k).replace(/\{(\w+)\}/g, (_, x) => v[x] ?? '');
    const calmo = () => matchMedia('(prefers-reduced-motion: reduce)').matches;

    // ---- o catálogo de bichos
    const lista = document.querySelector('.catalogo .bichos-lista');
    if (lista) {
        const itens = [...lista.querySelectorAll('.bicho-cartao')];
        const busca = document.getElementById('busca-bicho');
        const contagem = document.getElementById('contagem');
        const vazio = document.querySelector('.vazio');
        const limpo = (t) => t.normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase().trim();
        let grupo = '', perigo = '', lugar = '', regiao = '';
        const tem = (lista, v) => !v || lista.split(' ').includes(v);
        const regioes = [...document.querySelectorAll('.mapa-regioes .regiao')];
        const filtrar = () => {
            const q = limpo(busca.value);
            let n = 0;
            regioes.forEach((r) => r.classList.toggle('ativa', r.dataset.regiao === regiao));
            for (const it of itens) {
                const ok = (!q || limpo(it.dataset.busca).includes(q)) && (!grupo || it.dataset.grupo === grupo) && (!perigo || it.dataset.perigo === perigo)
                    && tem(it.dataset.lugar, lugar) && tem(it.dataset.regiao, regiao);
                it.hidden = !ok; if (ok) n++;
            }
            contagem.textContent = n; vazio.hidden = n > 0;
            // quantos filtros recolhidos estão ligados, no "Mais filtros" (4/11/2026)
            if (ativos) { const k = [perigo, lugar, regiao].filter(Boolean).length; ativos.textContent = k ? String(k) : ''; }
        };
        const mais = document.querySelector('.mais-filtros');
        const ativos = mais && mais.querySelector('.filtros-ativos');
        // no computador os filtros ficam numa coluna ao lado, sempre abertos; no celular, recolhidos
        const largo = matchMedia('(min-width: 1100px)');
        const abrir = () => { if (mais && largo.matches) mais.open = true; };
        abrir(); largo.addEventListener('change', abrir);
        const chips = (attr, set) => {
            const bs = [...document.querySelectorAll(`[${attr}]`)];
            bs.forEach((b) => b.addEventListener('click', () => { set(b.getAttribute(attr)); bs.forEach((o) => o.setAttribute('aria-pressed', String(o === b))); filtrar(); }));
        };
        chips('data-filtro-grupo', (v) => { grupo = v; });
        chips('data-filtro-perigo', (v) => { perigo = v; });
        chips('data-filtro-lugar', (v) => { lugar = v; });
        chips('data-filtro-regiao', (v) => { regiao = v; });
        // tocar no mapa aperta o botão da região (o botão é o que vale para o teclado e o leitor de tela)
        regioes.forEach((r) => r.addEventListener('click', () => document.querySelector(`[data-filtro-regiao="${regiao === r.dataset.regiao ? '' : r.dataset.regiao}"]`)?.click()));
        busca.addEventListener('input', filtrar);
        const params = new URLSearchParams(location.search);
        if (params.get('q')) busca.value = params.get('q');
        for (const [chave, attr] of [['lugar', 'data-filtro-lugar'], ['regiao', 'data-filtro-regiao'], ['perigo', 'data-filtro-perigo']]) {
            const v = params.get(chave);
            if (v) { document.querySelector(`[${attr}="${CSS.escape(v)}"]`)?.click(); if (mais) mais.open = true; }
        }
        filtrar();
    }

    // ---- Que bicho é esse?
    const dados = ler('id-dados');
    const caixa = document.querySelector('.id-caixa');
    if (dados && caixa) {
        // o primeiro passo pergunta onde a pessoa está; as respostas que não levam a nenhum bicho daquele lugar somem
        const caminho = ['lugar'];
        let lugar = '';
        const doLugar = (ids) => !lugar || ids.some((i) => dados.bichos[i].lug.split(' ').includes(lugar));
        const mostrar = () => {
            const atual = caminho[caminho.length - 1];
            const blocos = [];
            if (atual === 'lugar') {
                blocos.push(el('p', 'id-passo', t('id_comecar')));
                const h = el('h2', 'id-pergunta', t('id_onde')); h.tabIndex = -1; blocos.push(h);
                const ops = el('div', 'id-opcoes');
                [...dados.lugares, ['', t('id_pular')]].forEach(([v, texto]) => {
                    const b = el('button', null, texto); b.type = 'button';
                    b.addEventListener('click', () => { lugar = v; caminho.push('inicio'); mostrar(); });
                    ops.append(b);
                });
                blocos.push(ops);
            } else if (atual.startsWith('=')) {
                const b = dados.bichos[atual.slice(1)];
                const r = el('div', `id-resultado perigo-caixa-${b.p}`);
                r.append(el('p', 'id-passo', t('id_pode_ser')));
                const h = el('h2'); const a = el('a', null, b.n); a.href = `bicho-${atual.slice(1)}.html`; h.append(a);
                const selo = el('span', `perigo perigo-${b.p}`); selo.append(el('strong', null, b.pn), ' ' + b.ps);
                r.append(h, el('p', 'resposta', b.pica), selo, el('p', null, b.r));
                const acoes = el('p', 'id-acoes');
                const ver = el('a', 'botao', t('ver_ficha')); ver.href = `bicho-${atual.slice(1)}.html`;
                const soc = el('a', 'botao botao-socorro', t('id_socorro')); soc.href = `socorro.html#${b.soc}`;
                acoes.append(ver, soc);
                if (b.ach) { const achou = el('a', 'botao botao-claro', t('id_achou')); achou.href = `achei.html#${b.ach}`; acoes.append(achou); }
                r.append(acoes);
                r.append(el('p', 'id-aviso', t('id_aviso')));
                blocos.push(r);
            } else {
                const no = dados.arvore[atual];
                blocos.push(el('p', 'id-passo', t('id_pergunta', { n: caminho.length - 1 })));
                const h = el('h2', 'id-pergunta', no.p); h.tabIndex = -1; blocos.push(h);
                const ops = el('div', 'id-opcoes');
                const opcoes = no.o.filter(([, , ids]) => doLugar(ids));
                (opcoes.length ? opcoes : no.o).forEach(([texto, destino]) => {
                    const b = el('button', null, texto); b.type = 'button';
                    b.addEventListener('click', () => { caminho.push(destino); mostrar(); });
                    ops.append(b);
                });
                blocos.push(ops);
            }
            if (caminho.length > 1) {
                const nav = el('div', 'id-navegar');
                const volta = el('button', 'botao botao-claro', t('voltar')); volta.type = 'button';
                volta.addEventListener('click', () => { caminho.pop(); mostrar(); });
                const zero = el('button', 'botao botao-claro', t('comecar_de_novo')); zero.type = 'button';
                zero.addEventListener('click', () => { caminho.length = 1; lugar = ''; mostrar(); });
                nav.append(volta, zero); blocos.push(nav);
            }
            caixa.replaceChildren(...blocos);
            caixa.classList.remove('entra'); void caixa.offsetWidth; if (!calmo()) caixa.classList.add('entra');
            const foco = caixa.querySelector('h2, .id-pergunta'); if (foco && caminho.length > 1) { foco.tabIndex = -1; foco.focus({ preventScroll: true }); }
            if (caminho.length > 1 && caixa.getBoundingClientRect().top < 0) caixa.scrollIntoView({ block: 'start', behavior: calmo() ? 'auto' : 'smooth' });
        };
        mostrar();
    }

    // ---- Verdade ou mito? (o jogo)
    const mitos = ler('mitos-dados');
    const jogo = document.querySelector('.mito-jogo');
    if (mitos && jogo) {
        const placar = jogo.querySelector('.mito-placar'), pergunta = jogo.querySelector('.mito-pergunta');
        const retorno = jogo.querySelector('.mito-retorno'), proxima = jogo.querySelector('.mito-proxima');
        const botoes = [...jogo.querySelectorAll('[data-resp]')];
        const embaralhar = (l) => { const a = [...l]; for (let i = a.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); [a[i], a[j]] = [a[j], a[i]]; } return a; };
        let rodada = [], i = 0, acertos = 0;
        const RODADAS = 8;
        const comecar = () => { rodada = embaralhar(mitos).slice(0, RODADAS); i = 0; acertos = 0; mostrar(); };
        const mostrar = () => {
            const m = rodada[i];
            placar.textContent = t('mitos_placar', { n: i + 1, total: rodada.length, certas: acertos });
            pergunta.textContent = t('mitos_frase', { f: m.f });
            retorno.hidden = true; proxima.hidden = true;
            botoes.forEach((b) => { b.disabled = false; b.hidden = false; b.classList.remove('certa', 'errada'); });
        };
        botoes.forEach((b) => b.addEventListener('click', () => {
            const m = rodada[i];
            // "em parte" conta como mito: a frase, do jeito que está, não é verdade
            const certa = (m.v === 'verdade') === (b.dataset.resp === 'verdade');
            if (certa) acertos++;
            botoes.forEach((o) => { o.disabled = true; });
            b.classList.add(certa ? 'certa' : 'errada');
            const rot = { mito: t('mito'), verdade: t('verdade'), emparte: t('em_parte') }[m.v];
            retorno.replaceChildren(el('strong', null, (certa ? t('certo') : t('nao_e')) + ' ' + rot + ' '), m.e);
            retorno.className = 'mito-retorno ' + (certa ? 'certo' : 'errado'); retorno.hidden = false;
            proxima.textContent = i + 1 < rodada.length ? t('proxima') : t('ver_resultado'); proxima.hidden = false; proxima.focus();
        }));
        let fim = false;
        proxima.addEventListener('click', () => {
            if (fim) { fim = false; comecar(); pergunta.focus(); return; }
            if (++i < rodada.length) { mostrar(); pergunta.focus(); return; }
            fim = true;
            let rec = '';
            try {
                const antes = Number(localStorage.getItem('pica-recorde-mitos') || 0);
                if (acertos > antes) { localStorage.setItem('pica-recorde-mitos', String(acertos)); rec = antes ? ' ' + t('novo_recorde') : ''; } else rec = ' ' + t('seu_recorde', { n: antes, total: RODADAS });
            } catch { /* sem recorde */ }
            placar.textContent = t('resultado');
            pergunta.textContent = t('acertou', { n: acertos, total: rodada.length }) + rec;
            botoes.forEach((b) => { b.hidden = true; });
            retorno.hidden = true;
            proxima.textContent = t('jogar_de_novo');
        });
        jogo.hidden = false;
        comecar();
    }

    // ---- guardar e ler neste aparelho, sem quebrar se o navegador não deixar
    const guardado = (chave) => { try { return JSON.parse(localStorage.getItem(chave)); } catch { return null; } };
    const guardar = (chave, v) => { try { if (v == null) localStorage.removeItem(chave); else localStorage.setItem(chave, JSON.stringify(v)); return true; } catch { return false; } };
    const embaralhar = (l) => { const a = [...l]; for (let i = a.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); [a[i], a[j]] = [a[j], a[i]]; } return a; };

    // ---- o hospital da minha cidade (soro.html), que aparece no "Fui picado" e no cartão
    const mostrarHospital = () => {
        const h = guardado('pica-hospital');
        document.querySelectorAll('.meu-hospital').forEach((caixa) => {
            if (!h || !h.nome) { caixa.hidden = true; return; }
            const filhos = [el('p', 'meu-hospital-t', t('hosp_titulo')), el('p', 'meu-hospital-nome', h.nome)];
            if (h.end) filhos.push(el('p', null, h.end));
            if (h.tel) { const p = el('p'); const a = el('a', null, h.tel); a.href = 'tel:' + h.tel.replace(/[^\d+]/g, ''); p.append(a); filhos.push(p); }
            caixa.replaceChildren(...filhos); caixa.hidden = false;
        });
    };
    const hf = document.querySelector('.hospital-form');
    if (hf) {
        const estado = hf.querySelector('.hf-estado'), apagar = hf.querySelector('.hf-apagar');
        const nome = hf.elements.nome, erro = document.getElementById('e-hnome');
        const validar = () => { const ok = nome.value.trim() !== ''; erro.hidden = ok; nome.setAttribute('aria-invalid', String(!ok)); return ok; };
        const h = guardado('pica-hospital');
        if (h) { hf.elements.nome.value = h.nome || ''; hf.elements.tel.value = h.tel || ''; hf.elements.end.value = h.end || ''; apagar.hidden = false; }
        nome.addEventListener('blur', () => { if (nome.value) validar(); });
        nome.addEventListener('input', () => { if (nome.getAttribute('aria-invalid') === 'true') validar(); });
        hf.addEventListener('submit', (e) => {
            e.preventDefault();
            if (!validar()) { nome.focus(); return; }
            const ok = guardar('pica-hospital', { nome: nome.value.trim(), tel: hf.elements.tel.value.trim(), end: hf.elements.end.value.trim() });
            estado.textContent = ok ? t('hosp_guardado') : t('hosp_nao_guardou');
            apagar.hidden = !ok;
        });
        apagar.addEventListener('click', () => { guardar('pica-hospital', null); hf.reset(); apagar.hidden = true; estado.textContent = t('apagado'); nome.focus(); });
    }
    mostrarHospital();

    // ---- Fui picado (emergencia.html): escolher o bicho mostra os passos dele, ali mesmo
    const emerg = ler('emerg-dados');
    const resp = document.querySelector('.emerg-resposta');
    if (emerg && resp) {
        const quais = [...document.querySelectorAll('.emerg-qual')];
        quais.forEach((a) => a.addEventListener('click', (e) => {
            e.preventDefault();
            const s = emerg.soc[a.dataset.soc];
            quais.forEach((o) => o.setAttribute('aria-current', String(o === a)));
            const lista = el('ol', 'passos'); s.passos.forEach((x) => lista.append(el('li', null, x)));
            const mais = el('a', null, t('emerg_mais')); mais.href = a.getAttribute('href');
            const p = el('p'); p.append(mais);
            resp.replaceChildren(el('h3', null, s.t), lista, p);
            resp.classList.remove('entra'); void resp.offsetWidth; if (!calmo()) resp.classList.add('entra');
            resp.focus({ preventScroll: true });
            resp.scrollIntoView({ block: 'nearest', behavior: calmo() ? 'auto' : 'smooth' });
        }));
    }

    // ---- ouvir os passos (a voz do próprio aparelho)
    const ouvir = document.querySelector('.ouvir');
    if (ouvir && 'speechSynthesis' in window) {
        ouvir.hidden = false;
        const parar = () => { speechSynthesis.cancel(); ouvir.setAttribute('aria-pressed', 'false'); ouvir.textContent = t('ouvir'); };
        ouvir.addEventListener('click', () => {
            if (speechSynthesis.speaking) { parar(); return; }
            const partes = [...document.querySelectorAll('.emerg-ja li')].map((li) => li.textContent.replace(/\d+$/, ''));
            const r = document.querySelector('.emerg-resposta');
            if (r && r.textContent.trim()) partes.push(...[...r.querySelectorAll('h3, li')].map((x) => x.textContent));
            partes.push(t('nao_faca') + ' ' + [...document.querySelectorAll('.emerg-nunca li')].map((x) => x.textContent).join('. '));
            const fala = new SpeechSynthesisUtterance(partes.join('. '));
            fala.lang = document.documentElement.lang; fala.rate = 0.95;
            fala.onend = parar;
            ouvir.setAttribute('aria-pressed', 'true'); ouvir.textContent = t('parar_leitura');
            speechSynthesis.speak(fala);
        });
        addEventListener('pagehide', parar);
    }
    // ---- avisar alguém: a mensagem pronta para o WhatsApp (bicho, hora, hospital e, se a pessoa quiser, onde está)
    const avisar = document.querySelector('.avisar');
    if (avisar) {
        avisar.hidden = false;
        const texto = avisar.querySelector('.avisar-texto'), link = avisar.querySelector('.avisar-botao'), local = avisar.querySelector('.avisar-local');
        let onde = '';
        const montarMsg = () => {
            const c = guardado('pica-cartao') || {};
            const esc = document.querySelector('.emerg-qual[aria-current="true"]');
            const bicho = c.bicho || (esc ? esc.textContent.toLowerCase() : t('um_bicho'));
            const d = new Date(); const hora = c.hora || `${String(d.getHours()).padStart(2, '0')}:${String(d.getMinutes()).padStart(2, '0')}`;
            const h = guardado('pica-hospital');
            let m = t('msg_picado', { bicho, hora });
            m += ' ' + (h && h.nome ? t('msg_indo_hospital', { hospital: h.nome + (h.end ? ` (${h.end})` : '') }) : t('msg_indo_servico'));
            if (onde) m += ' ' + t('msg_aqui', { onde });
            texto.textContent = m;
            link.href = 'https://wa.me/?text=' + encodeURIComponent(m);
        };
        local.addEventListener('change', () => {
            if (!local.checked) { onde = ''; montarMsg(); return; }
            if (!navigator.geolocation) { texto.textContent = t('sem_localizacao'); local.checked = false; return; }
            texto.textContent = t('procurando');
            navigator.geolocation.getCurrentPosition((pos) => {
                onde = `https://maps.google.com/?q=${pos.coords.latitude.toFixed(5)},${pos.coords.longitude.toFixed(5)}`; montarMsg();
            }, () => { local.checked = false; onde = ''; montarMsg(); texto.append(' ' + t('localizacao_falhou')); }, { timeout: 10000, maximumAge: 60000 });
        });
        document.querySelectorAll('.emerg-qual').forEach((a) => a.addEventListener('click', montarMsg));
        montarMsg();
    }
    const roteiroCartao = document.querySelector('.roteiro-cartao');
    if (roteiroCartao && guardado('pica-cartao')) roteiroCartao.hidden = false;

    // ---- Cartão para o hospital (cartao.html): fica só neste aparelho
    const cf = document.querySelector('.cartao-form');
    const cartao = document.querySelector('.cartao-hospital');
    if (cf && cartao) {
        let relogio = 0;
        const campos = { bicho: [cf.elements.bicho, document.getElementById('e-bicho')], hora: [cf.elements.hora, document.getElementById('e-hora')] };
        const validar = (k) => { const [c, e] = campos[k]; const ok = c.value !== ''; e.hidden = ok; c.setAttribute('aria-invalid', String(!ok)); return ok; };
        Object.keys(campos).forEach((k) => campos[k][0].addEventListener('change', () => validar(k)));
        const agora = () => { const d = new Date(); return `${String(d.getHours()).padStart(2, '0')}:${String(d.getMinutes()).padStart(2, '0')}`; };
        cf.querySelector('.c-agora').addEventListener('click', () => { cf.elements.hora.value = agora(); validar('hora'); });
        const ler_form = () => ({ bicho: cf.elements.bicho.value, hora: cf.elements.hora.value, parte: cf.elements.parte.value.trim(), onde: cf.elements.onde.value.trim(),
            sintomas: [...cf.querySelectorAll('[data-sintoma]:checked')].map((c) => c.value), idade: cf.elements.idade.value, peso: cf.elements.peso.value,
            alergia: cf.elements.alergia.value.trim(), foto: cf.elements.foto.checked });
        const preencher = (d) => {
            for (const k of ['bicho', 'hora', 'parte', 'onde', 'idade', 'peso', 'alergia']) if (d[k] != null) cf.elements[k].value = d[k];
            cf.querySelectorAll('[data-sintoma]').forEach((c) => { c.checked = (d.sintomas || []).includes(c.value); });
            cf.elements.foto.checked = !!d.foto;
        };
        const passou = (hora) => {
            const [h, m] = hora.split(':').map(Number); const d = new Date(); let min = d.getHours() * 60 + d.getMinutes() - (h * 60 + m);
            if (min < 0) min += 1440;
            return min < 60 ? t('ha_min', { min }) : t('ha_h_min', { h: Math.floor(min / 60), min: min % 60 });
        };
        const linha = (rot, val) => { const p = el('p', 'ch-linha'); p.append(el('span', 'ch-rot', rot), el('strong', null, val)); return p; };
        const mostrar = (d) => {
            const tempo = el('strong', null, passou(d.hora));
            const hora = el('p', 'ch-linha ch-hora'); hora.append(el('span', 'ch-rot', t('ch_picada')), el('strong', null, d.hora), ' (', tempo, ')');
            const filhos = [el('p', 'ch-aviso', t('ch_aviso')), el('h2', 'ch-bicho', d.bicho), hora];
            if (d.parte) filhos.push(linha(t('ch_parte'), d.parte));
            if (d.onde) filhos.push(linha(t('ch_onde'), d.onde));
            filhos.push(linha(t('ch_sente'), d.sintomas.length ? d.sintomas.join(', ') : t('ch_nao_anotado')));
            if (d.idade || d.peso) filhos.push(linha(t('ch_idade_peso'), [d.idade && t('ch_anos', { n: d.idade }), d.peso && t('ch_kg', { n: d.peso })].filter(Boolean).join(', ')));
            if (d.alergia) filhos.push(linha(t('ch_alergias'), d.alergia));
            filhos.push(linha(t('ch_foto'), d.foto ? t('ch_foto_sim') : t('ch_foto_nao')));
            const acoes = el('p', 'ch-acoes');
            const editar = el('button', 'botao botao-claro', t('editar')); editar.type = 'button';
            const apagar = el('button', 'botao botao-claro', t('ch_apagar')); apagar.type = 'button';
            acoes.append(editar, apagar); filhos.push(acoes);
            cartao.replaceChildren(...filhos); cartao.hidden = false; cf.hidden = true;
            clearInterval(relogio); relogio = setInterval(() => { tempo.textContent = passou(d.hora); }, 30000);
            editar.addEventListener('click', () => { clearInterval(relogio); cartao.hidden = true; cf.hidden = false; cf.elements.bicho.focus(); });
            apagar.addEventListener('click', () => { clearInterval(relogio); guardar('pica-cartao', null); cf.reset(); cartao.hidden = true; cf.hidden = false; cf.elements.bicho.focus(); });
            cartao.focus({ preventScroll: true }); cartao.scrollIntoView({ block: 'start', behavior: calmo() ? 'auto' : 'smooth' });
        };
        cf.addEventListener('input', () => { if (cf.elements.bicho.value || cf.elements.hora.value) guardar('pica-cartao-rascunho', ler_form()); });
        cf.addEventListener('submit', (e) => {
            e.preventDefault();
            const ok = ['bicho', 'hora'].map(validar).every(Boolean);
            if (!ok) { (cf.querySelector('[aria-invalid="true"]') || cf.elements.bicho).focus(); return; }
            const d = ler_form(); guardar('pica-cartao', d); guardar('pica-cartao-rascunho', null); mostrar(d);
        });
        addEventListener('pagehide', () => clearInterval(relogio));
        const salvo = guardado('pica-cartao') || guardado('pica-cartao-rascunho');
        if (salvo) preencher(salvo);
        if (guardado('pica-cartao')) mostrar(guardado('pica-cartao'));
    }

    // ---- Prevenir: o teste da casa e o mês de agora na época dos bichos
    const lista_ = (attr, chave, nSel, notaSel, barraSel, msgs) => {
    const casa = [...document.querySelectorAll(`[${attr}]`)];
    if (casa.length) {
        const n = document.querySelector(nSel), nota = document.querySelector(notaSel), barra = document.querySelector(barraSel);
        const marcados = new Set(guardado(chave) || []);
        const contar = () => {
            const k = casa.filter((c) => c.checked).length;
            n.textContent = k;
            const msg = k === casa.length ? msgs[0] : k >= 7 ? ' ' + t('casa_quase') : k >= 4 ? ' ' + t('casa_comeco') : '';
            const fim = ' ' + t('de_total', { total: casa.length }) + msg;
            nota.lastChild.nodeType === 3 ? (nota.lastChild.textContent = fim) : nota.append(fim);
            if (barra) barra.style.setProperty('transform', `scaleX(${k / casa.length})`);
            guardar(chave, casa.filter((c) => c.checked).map((c) => c.getAttribute(attr)));
        };
        casa.forEach((c) => { c.checked = marcados.has(c.getAttribute(attr)); c.addEventListener('change', contar); });
        contar();
    }
    };
    lista_('data-casa', 'pica-casa', '.casa-n', '.casa-nota', '.casa-barra span', [' ' + t('casa_em_dia')]);
    lista_('data-trilha', 'pica-trilha', '.trilha-n', '.trilha-nota', null, [' ' + t('trilha_pronta')]);
    const agoraEpoca = document.querySelector('.epoca-agora');
    if (agoraEpoca) {
        const m = new Date().getMonth() + 1;
        document.querySelectorAll(`.mes[data-mes="${m}"]`).forEach((c) => c.classList.add('mes-agora'));
        const nome = new Intl.DateTimeFormat(document.documentElement.lang, { month: 'long' }).format(new Date());
        const altas = [...document.querySelectorAll('.epoca')].filter((e) => e.querySelector(`.mes[data-mes="${m}"]`).classList.contains('mes-sim')).map((e) => e.querySelector('.epoca-t').textContent);
        agoraEpoca.textContent = altas.length ? t('epoca_alta', { mes: nome, bichos: altas.join('; ') }) : t('epoca_baixa', { mes: nome });
    }

    // ---- um jogo de perguntas com placar e recorde (o "Qual dos dois?" e o "Pica ou não pica?")
    const jogoDe = (caixa, { rodadas, chave, montar, tempo, turma, times }) => {
        let pontos = [0, 0];
        const emTurma = () => !!(turma && turma.checked);
        const placarTimes = () => { if (!times) return; times.hidden = !emTurma(); times.textContent = t('times', { a: pontos[0], b: pontos[1], vez: 'AB'[i % 2] }); };
        const placar = caixa.querySelector('.jogo-placar'), pergunta = caixa.querySelector('.jogo-pergunta');
        const botoes = caixa.querySelector('.jogo-botoes'), retorno = caixa.querySelector('.jogo-retorno'), proxima = caixa.querySelector('.jogo-proxima');
        const barra = caixa.querySelector('.tempo span'), semTempo = caixa.querySelector('.sem-tempo-caixa');
        let lista = [], i = 0, acertos = 0, fim = false, cronometro = 0;
        const parar = () => { clearTimeout(cronometro); if (barra) { barra.classList.remove('correndo'); barra.style.setProperty('transform', 'scaleX(1)'); } };
        const responder = (certa, explicacao, escolhido) => {
            parar();
            if (certa) { acertos++; pontos[i % 2]++; }
            botoes.querySelectorAll('button').forEach((b) => { b.disabled = true; });
            if (escolhido) escolhido.classList.add(certa ? 'certa' : 'errada');
            retorno.replaceChildren(el('strong', null, (escolhido ? (certa ? t('certo') : t('nao_e')) : t('acabou_tempo')) + ' '), ...explicacao);
            retorno.className = 'jogo-retorno ' + (certa ? 'certo' : 'errado'); retorno.hidden = false;
            proxima.textContent = i + 1 < lista.length ? t('proxima') : t('ver_resultado'); proxima.hidden = false; proxima.focus();
        };
        const mostrar = () => {
            const q = montar(lista[i], responder);
            placar.textContent = t('rodada_placar', { n: i + 1, total: lista.length, certas: acertos });
            retorno.hidden = true; proxima.hidden = true;
            q.pergunta(pergunta);
            botoes.replaceChildren(...q.botoes); botoes.hidden = false;
            placarTimes();
            if (tempo && !(semTempo && semTempo.checked)) {
                barra.style.setProperty('transform', 'scaleX(1)'); void barra.offsetWidth;
                barra.style.setProperty('transition-duration', `${tempo}ms`); barra.classList.add('correndo'); barra.style.setProperty('transform', 'scaleX(0)');
                cronometro = setTimeout(() => responder(false, q.explicacao(), null), tempo);
            }
        };
        const comecar = () => { parar(); lista = embaralhar(montar.todos).slice(0, emTurma() ? rodadas * 2 : rodadas); i = 0; acertos = 0; pontos = [0, 0]; fim = false; mostrar(); };
        proxima.addEventListener('click', () => {
            if (fim) { comecar(); pergunta.focus(); return; }
            if (++i < lista.length) { mostrar(); pergunta.focus(); return; }
            fim = true;
            if (emTurma()) {
                placar.textContent = t('resultado');
                pergunta.textContent = pontos[0] === pontos[1] ? t('empate', { a: pontos[0], b: pontos[1] }) : t('venceu', { time: pontos[0] > pontos[1] ? 'A' : 'B', a: Math.max(...pontos), b: Math.min(...pontos) });
                if (times) times.hidden = true;
                botoes.hidden = true; retorno.hidden = true; proxima.textContent = t('jogar_de_novo');
                return;
            }
            const k = typeof chave === 'function' ? chave() : chave;
            const antes = Number(guardado(k) || 0); let rec = '';
            if (acertos > antes) { guardar(k, acertos); rec = antes ? ' ' + t('novo_recorde') : ''; } else rec = ' ' + t('seu_recorde', { n: antes, total: rodadas });
            placar.textContent = t('resultado');
            pergunta.textContent = t('acertou', { n: acertos, total: lista.length }) + rec;
            botoes.hidden = true; retorno.hidden = true; proxima.textContent = t('jogar_de_novo');
        });
        addEventListener('pagehide', parar);
        if (turma) turma.addEventListener('change', () => comecar());
        caixa.hidden = false; comecar();
        return { comecar };
    };
    const botao = (texto, cls, quando) => { const b = el('button', cls, texto); b.type = 'button'; b.addEventListener('click', () => quando(b)); return b; };

    const difs = ler('dif-dados'), difCaixa = document.querySelector('.dif-jogo');
    if (difs && difCaixa) {
        const montar = (q, responder) => {
            const certo = q.lado === 'a' ? q.d.a : q.d.b;
            const explicacao = () => [`${q.traco}: ${certo}. ${q.d.c}`];
            return {
                pergunta: (p) => { p.textContent = t('dif_pergunta', { traco: q.traco }); },
                botoes: embaralhar([q.d.a, q.d.b]).map((n) => botao(n, 'botao', (b) => responder(n === certo, explicacao(), b))),
                explicacao,
            };
        };
        // a rodada "Abelhas e vespas" (4/11/2026): só os pares marcados, com as pistas a mais de cada um
        let rodada = '';
        const perguntas = () => rodada
            ? difs.filter((d) => d.r === rodada).flatMap((d) => [{ d, lado: 'a', traco: d.ta }, { d, lado: 'b', traco: d.tb }, ...(d.mais || []).map(([lado, traco]) => ({ d, lado, traco }))])
            : difs.flatMap((d) => [{ d, lado: 'a', traco: d.ta }, { d, lado: 'b', traco: d.tb }]);
        const rodadas = [...difCaixa.querySelectorAll('[data-rodada]')];
        const pedida = new URLSearchParams(location.search).get('rodada');
        if (pedida && rodadas.some((r) => r.dataset.rodada === pedida)) rodada = pedida;
        rodadas.forEach((o) => o.setAttribute('aria-pressed', String(o.dataset.rodada === rodada)));
        montar.todos = perguntas();
        const ctl = jogoDe(difCaixa, { rodadas: 8, chave: () => (rodada ? `pica-recorde-diferencas-${rodada}` : 'pica-recorde-diferencas'), montar });
        rodadas.forEach((r) => r.addEventListener('click', () => {
            rodada = r.dataset.rodada; rodadas.forEach((o) => o.setAttribute('aria-pressed', String(o === r)));
            montar.todos = perguntas(); ctl.comecar();
        }));
    }

    const bichosJogo = ler('jogo-dados'), picaCaixa = document.querySelector('.pica-jogo');
    if (bichosJogo && picaCaixa) {
        const grupo = picaCaixa.querySelector('.jogo-grupo');
        let modo = 'pica';
        const TIPOS = [['peconhento', t('peconhento')], ['venenoso', t('venenoso')], ['outro', t('nenhum')]];
        const montar = (b, responder) => {
            const ficha = () => { const a = el('a', null, t('ver_ficha')); a.href = `bicho-${b.id}.html`; return a; };
            if (modo === 'tipo') {
                const certo = ['peconhento', 'venenoso'].includes(b.t) ? b.t : 'outro';
                const explicacao = () => [`${b.n}: ${b.tn}. `, ficha()];
                return {
                    pergunta: (p) => { p.textContent = b.n; grupo.textContent = `${b.g} · ${t('tipo_pergunta')}`; },
                    botoes: TIPOS.map(([v, t]) => botao(t, 'botao', (x) => responder(v === certo, explicacao(), x))),
                    explicacao,
                };
            }
            const explicacao = () => [`${b.n}: ${b.pica.toLowerCase()}. ${b.r} `, ficha()];
            return {
                pergunta: (p) => { p.textContent = b.n; grupo.textContent = b.g; },
                botoes: [botao(t('cuidado'), 'botao botao-socorro', (x) => responder(b.cuidado, explicacao(), x)), botao(t('sem_perigo'), 'botao', (x) => responder(!b.cuidado, explicacao(), x))],
                explicacao,
            };
        };
        montar.todos = bichosJogo;
        const ctl = jogoDe(picaCaixa, { rodadas: 10, chave: 'pica-recorde-jogo', montar, tempo: 6000, turma: picaCaixa.querySelector('.modo-turma'), times: picaCaixa.querySelector('.jogo-times') });
        const modos = [...picaCaixa.querySelectorAll('[data-modo]')];
        modos.forEach((m) => m.addEventListener('click', () => { modo = m.dataset.modo; modos.forEach((o) => o.setAttribute('aria-pressed', String(o === m))); ctl.comecar(); }));
    }

    // ---- compartilhar: o menu do próprio celular quando existe; o link do WhatsApp sempre
    document.querySelectorAll('.compartilhar').forEach((c) => {
        const b = c.querySelector('.partilhar');
        if (!navigator.share) return;
        b.hidden = false;
        b.addEventListener('click', () => navigator.share({ title: document.title, text: c.dataset.texto, url: c.dataset.url }).catch(() => {}));
    });
    // ---- imprimir (escola.html)
    document.querySelectorAll('.imprimir').forEach((b) => { b.hidden = false; b.addEventListener('click', () => print()); });
})();
