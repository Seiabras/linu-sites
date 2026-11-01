// Pica ou Não Pica? (1/11/2026): as partes que a pessoa usa com as mãos no guia em português.
// - Bichos: busca, grupo e perigo, tudo junto.
// - Que bicho é esse?: perguntas em árvore até o bicho, com "Voltar" e "Começar de novo"; o resultado diz se é perigoso.
// - Mitos: o jogo "Verdade ou mito?", com o placar guardado neste navegador.
// Tudo montado com textContent. Sem JavaScript, as páginas mostram a lista inteira.
(() => {
    const el = (tag, cls, texto) => { const e = document.createElement(tag); if (cls) e.className = cls; if (texto != null) e.textContent = texto; return e; };
    const ler = (id) => { try { return JSON.parse(document.getElementById(id).textContent); } catch { return null; } };
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
        };
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
        for (const [chave, attr] of [['lugar', 'data-filtro-lugar'], ['regiao', 'data-filtro-regiao']]) {
            const v = params.get(chave);
            if (v) document.querySelector(`[${attr}="${CSS.escape(v)}"]`)?.click();
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
                blocos.push(el('p', 'id-passo', 'Para começar'));
                const h = el('h2', 'id-pergunta', 'Onde você está?'); h.tabIndex = -1; blocos.push(h);
                const ops = el('div', 'id-opcoes');
                [...dados.lugares, ['', 'Prefiro pular']].forEach(([v, texto]) => {
                    const b = el('button', null, texto); b.type = 'button';
                    b.addEventListener('click', () => { lugar = v; caminho.push('inicio'); mostrar(); });
                    ops.append(b);
                });
                blocos.push(ops);
            } else if (atual.startsWith('=')) {
                const b = dados.bichos[atual.slice(1)];
                const r = el('div', `id-resultado perigo-caixa-${b.p}`);
                r.append(el('p', 'id-passo', 'Pode ser:'));
                const h = el('h2'); const a = el('a', null, b.n); a.href = `bicho-${atual.slice(1)}.html`; h.append(a);
                const selo = el('span', `perigo perigo-${b.p}`); selo.append(el('strong', null, b.pn), ' ' + b.ps);
                r.append(h, el('p', 'resposta', b.pica), selo, el('p', null, b.r));
                const acoes = el('p', 'id-acoes');
                const ver = el('a', 'botao', 'Ver a ficha'); ver.href = `bicho-${atual.slice(1)}.html`;
                const soc = el('a', 'botao botao-socorro', 'O que fazer se picar'); soc.href = `socorro.html#${b.soc}`;
                acoes.append(ver, soc); r.append(acoes);
                r.append(el('p', 'id-aviso', 'As perguntas ajudam, mas não dão certeza. Na dúvida, trate como perigoso e procure o serviço de saúde.'));
                blocos.push(r);
            } else {
                const no = dados.arvore[atual];
                blocos.push(el('p', 'id-passo', `Pergunta ${caminho.length - 1}`));
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
                const volta = el('button', 'botao botao-claro', 'Voltar'); volta.type = 'button';
                volta.addEventListener('click', () => { caminho.pop(); mostrar(); });
                const zero = el('button', 'botao botao-claro', 'Começar de novo'); zero.type = 'button';
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
            placar.textContent = `Pergunta ${i + 1} de ${rodada.length} · ${acertos} certas`;
            pergunta.textContent = `“${m.f}”`;
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
            const rot = { mito: 'Mito.', verdade: 'Verdade.', emparte: 'Em parte.' }[m.v];
            retorno.replaceChildren(el('strong', null, (certa ? 'Certo! ' : 'Não é. ') + rot + ' '), m.e);
            retorno.className = 'mito-retorno ' + (certa ? 'certo' : 'errado'); retorno.hidden = false;
            proxima.textContent = i + 1 < rodada.length ? 'Próxima' : 'Ver o resultado'; proxima.hidden = false; proxima.focus();
        }));
        let fim = false;
        proxima.addEventListener('click', () => {
            if (fim) { fim = false; comecar(); pergunta.focus(); return; }
            if (++i < rodada.length) { mostrar(); pergunta.focus(); return; }
            fim = true;
            let rec = '';
            try {
                const antes = Number(localStorage.getItem('pica-recorde-mitos') || 0);
                if (acertos > antes) { localStorage.setItem('pica-recorde-mitos', String(acertos)); rec = antes ? ' Novo recorde!' : ''; } else rec = ` Seu recorde: ${antes} de ${RODADAS}.`;
            } catch { /* sem recorde */ }
            placar.textContent = 'Resultado';
            pergunta.textContent = `Você acertou ${acertos} de ${rodada.length}.${rec}`;
            botoes.forEach((b) => { b.hidden = true; });
            retorno.hidden = true;
            proxima.textContent = 'Jogar de novo';
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
            const filhos = [el('p', 'meu-hospital-t', 'Meu hospital de referência'), el('p', 'meu-hospital-nome', h.nome)];
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
            estado.textContent = ok ? 'Guardado neste aparelho. Aparece no “Fui picado” e no cartão para o hospital.' : 'Este navegador não deixou guardar. Anote num papel.';
            apagar.hidden = !ok;
        });
        apagar.addEventListener('click', () => { guardar('pica-hospital', null); hf.reset(); apagar.hidden = true; estado.textContent = 'Apagado.'; nome.focus(); });
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
            const mais = el('a', null, 'Mais detalhes no Socorro'); mais.href = a.getAttribute('href');
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
        const parar = () => { speechSynthesis.cancel(); ouvir.setAttribute('aria-pressed', 'false'); ouvir.textContent = 'Ouvir os passos'; };
        ouvir.addEventListener('click', () => {
            if (speechSynthesis.speaking) { parar(); return; }
            const partes = [...document.querySelectorAll('.emerg-ja li')].map((li) => li.textContent.replace(/\d+$/, ''));
            const r = document.querySelector('.emerg-resposta');
            if (r && r.textContent.trim()) partes.push(...[...r.querySelectorAll('h3, li')].map((x) => x.textContent));
            partes.push('Não faça: ' + [...document.querySelectorAll('.emerg-nunca li')].map((x) => x.textContent).join('. '));
            const fala = new SpeechSynthesisUtterance(partes.join('. '));
            fala.lang = 'pt-BR'; fala.rate = 0.95;
            fala.onend = parar;
            ouvir.setAttribute('aria-pressed', 'true'); ouvir.textContent = 'Parar a leitura';
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
            const bicho = c.bicho || (esc ? esc.textContent.toLowerCase() : 'um bicho');
            const d = new Date(); const hora = c.hora || `${String(d.getHours()).padStart(2, '0')}:${String(d.getMinutes()).padStart(2, '0')}`;
            const h = guardado('pica-hospital');
            let m = `Fui picado por ${bicho} às ${hora}.`;
            m += h && h.nome ? ` Estou indo para o ${h.nome}${h.end ? ` (${h.end})` : ''}.` : ' Estou indo para o serviço de saúde.';
            if (onde) m += ` Estou aqui: ${onde}`;
            texto.textContent = m;
            link.href = 'https://wa.me/?text=' + encodeURIComponent(m);
        };
        local.addEventListener('change', () => {
            if (!local.checked) { onde = ''; montarMsg(); return; }
            if (!navigator.geolocation) { texto.textContent = 'Este aparelho não informa a localização.'; local.checked = false; return; }
            texto.textContent = 'Procurando onde você está…';
            navigator.geolocation.getCurrentPosition((pos) => {
                onde = `https://maps.google.com/?q=${pos.coords.latitude.toFixed(5)},${pos.coords.longitude.toFixed(5)}`; montarMsg();
            }, () => { local.checked = false; onde = ''; montarMsg(); texto.append(' (Não deu para pegar a localização: diga onde está na mensagem.)'); }, { timeout: 10000, maximumAge: 60000 });
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
            return min < 60 ? `há ${min} min` : `há ${Math.floor(min / 60)} h ${min % 60} min`;
        };
        const linha = (rot, val) => { const p = el('p', 'ch-linha'); p.append(el('span', 'ch-rot', rot), el('strong', null, val)); return p; };
        const mostrar = (d) => {
            const tempo = el('strong', null, passou(d.hora));
            const hora = el('p', 'ch-linha ch-hora'); hora.append(el('span', 'ch-rot', 'Picada às'), el('strong', null, d.hora), ' (', tempo, ')');
            const filhos = [el('p', 'ch-aviso', 'Mostre esta tela à equipe de saúde'), el('h2', 'ch-bicho', d.bicho), hora];
            if (d.parte) filhos.push(linha('Parte do corpo', d.parte));
            if (d.onde) filhos.push(linha('Onde', d.onde));
            filhos.push(linha('Sente', d.sintomas.length ? d.sintomas.join(', ') : 'não anotado'));
            if (d.idade || d.peso) filhos.push(linha('Idade e peso', [d.idade && `${d.idade} anos`, d.peso && `${d.peso} kg`].filter(Boolean).join(', ')));
            if (d.alergia) filhos.push(linha('Alergias e remédios', d.alergia));
            filhos.push(linha('Foto do bicho', d.foto ? 'sim, no celular' : 'não'));
            const acoes = el('p', 'ch-acoes');
            const editar = el('button', 'botao botao-claro', 'Editar'); editar.type = 'button';
            const apagar = el('button', 'botao botao-claro', 'Apagar o cartão'); apagar.type = 'button';
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
            const msg = k === casa.length ? msgs[0] : k >= 7 ? ' Quase lá.' : k >= 4 ? ' Bom começo: veja o que falta.' : '';
            nota.lastChild.nodeType === 3 ? (nota.lastChild.textContent = ` de ${casa.length}.${msg}`) : nota.append(` de ${casa.length}.${msg}`);
            if (barra) barra.style.setProperty('transform', `scaleX(${k / casa.length})`);
            guardar(chave, casa.filter((c) => c.checked).map((c) => c.getAttribute(attr)));
        };
        casa.forEach((c) => { c.checked = marcados.has(c.getAttribute(attr)); c.addEventListener('change', contar); });
        contar();
    }
    };
    lista_('data-casa', 'pica-casa', '.casa-n', '.casa-nota', '.casa-barra span', [' Casa em dia: continue assim.']);
    lista_('data-trilha', 'pica-trilha', '.trilha-n', '.trilha-nota', null, [' Tudo pronto: boa viagem.']);
    const agoraEpoca = document.querySelector('.epoca-agora');
    if (agoraEpoca) {
        const m = new Date().getMonth() + 1;
        document.querySelectorAll(`.mes[data-mes="${m}"]`).forEach((c) => c.classList.add('mes-agora'));
        const nome = new Intl.DateTimeFormat('pt-BR', { month: 'long' }).format(new Date());
        const altas = [...document.querySelectorAll('.epoca')].filter((e) => e.querySelector(`.mes[data-mes="${m}"]`).classList.contains('mes-sim')).map((e) => e.querySelector('.epoca-t').textContent);
        agoraEpoca.textContent = altas.length ? `Estamos em ${nome}, um dos meses com mais acidentes: ${altas.join('; ')}. Redobre o cuidado.` : `Estamos em ${nome}: fora dos meses de mais acidentes, mas eles acontecem o ano todo.`;
    }

    // ---- um jogo de perguntas com placar e recorde (o "Qual dos dois?" e o "Pica ou não pica?")
    const jogoDe = (caixa, { rodadas, chave, montar, tempo, turma, times }) => {
        let pontos = [0, 0];
        const emTurma = () => !!(turma && turma.checked);
        const placarTimes = () => { if (!times) return; times.hidden = !emTurma(); times.textContent = `Time A: ${pontos[0]} · Time B: ${pontos[1]} · agora joga o time ${'AB'[i % 2]}`; };
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
            retorno.replaceChildren(el('strong', null, escolhido ? (certa ? 'Certo! ' : 'Não é. ') : 'Acabou o tempo. '), ...explicacao);
            retorno.className = 'jogo-retorno ' + (certa ? 'certo' : 'errado'); retorno.hidden = false;
            proxima.textContent = i + 1 < lista.length ? 'Próxima' : 'Ver o resultado'; proxima.hidden = false; proxima.focus();
        };
        const mostrar = () => {
            const q = montar(lista[i], responder);
            placar.textContent = `Rodada ${i + 1} de ${lista.length} · ${acertos} certas`;
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
                placar.textContent = 'Resultado';
                pergunta.textContent = pontos[0] === pontos[1] ? `Empate: ${pontos[0]} a ${pontos[1]}.` : `O time ${pontos[0] > pontos[1] ? 'A' : 'B'} venceu: ${Math.max(...pontos)} a ${Math.min(...pontos)}.`;
                if (times) times.hidden = true;
                botoes.hidden = true; retorno.hidden = true; proxima.textContent = 'Jogar de novo';
                return;
            }
            const antes = Number(guardado(chave) || 0); let rec = '';
            if (acertos > antes) { guardar(chave, acertos); rec = antes ? ' Novo recorde!' : ''; } else rec = ` Seu recorde: ${antes} de ${rodadas}.`;
            placar.textContent = 'Resultado';
            pergunta.textContent = `Você acertou ${acertos} de ${lista.length}.${rec}`;
            botoes.hidden = true; retorno.hidden = true; proxima.textContent = 'Jogar de novo';
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
                pergunta: (p) => { p.textContent = `“${q.traco}”: qual dos dois?`; },
                botoes: embaralhar([q.d.a, q.d.b]).map((n) => botao(n, 'botao', (b) => responder(n === certo, explicacao(), b))),
                explicacao,
            };
        };
        montar.todos = difs.flatMap((d) => [{ d, lado: 'a', traco: d.ta }, { d, lado: 'b', traco: d.tb }]);
        jogoDe(difCaixa, { rodadas: 8, chave: 'pica-recorde-diferencas', montar });
    }

    const bichosJogo = ler('jogo-dados'), picaCaixa = document.querySelector('.pica-jogo');
    if (bichosJogo && picaCaixa) {
        const grupo = picaCaixa.querySelector('.jogo-grupo');
        let modo = 'pica';
        const TIPOS = [['peconhento', 'Peçonhento'], ['venenoso', 'Venenoso'], ['outro', 'Nenhum dos dois']];
        const montar = (b, responder) => {
            const ficha = () => { const a = el('a', null, 'Ver a ficha'); a.href = `bicho-${b.id}.html`; return a; };
            if (modo === 'tipo') {
                const certo = ['peconhento', 'venenoso'].includes(b.t) ? b.t : 'outro';
                const explicacao = () => [`${b.n}: ${b.tn}. `, ficha()];
                return {
                    pergunta: (p) => { p.textContent = b.n; grupo.textContent = `${b.g} · peçonhento, venenoso ou nenhum dos dois?`; },
                    botoes: TIPOS.map(([v, t]) => botao(t, 'botao', (x) => responder(v === certo, explicacao(), x))),
                    explicacao,
                };
            }
            const explicacao = () => [`${b.n}: ${b.pica.toLowerCase()}. ${b.r} `, ficha()];
            return {
                pergunta: (p) => { p.textContent = b.n; grupo.textContent = b.g; },
                botoes: [botao('Cuidado!', 'botao botao-socorro', (x) => responder(b.cuidado, explicacao(), x)), botao('Sem perigo', 'botao', (x) => responder(!b.cuidado, explicacao(), x))],
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
