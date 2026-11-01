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
        let grupo = '', perigo = '';
        const filtrar = () => {
            const q = limpo(busca.value);
            let n = 0;
            for (const it of itens) {
                const ok = (!q || limpo(it.dataset.busca).includes(q)) && (!grupo || it.dataset.grupo === grupo) && (!perigo || it.dataset.perigo === perigo);
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
        busca.addEventListener('input', filtrar);
        const q = new URLSearchParams(location.search).get('q');
        if (q) busca.value = q;
        filtrar();
    }

    // ---- Que bicho é esse?
    const dados = ler('id-dados');
    const caixa = document.querySelector('.id-caixa');
    if (dados && caixa) {
        const caminho = ['inicio'];
        const mostrar = () => {
            const atual = caminho[caminho.length - 1];
            const blocos = [];
            if (atual.startsWith('=')) {
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
                blocos.push(el('p', 'id-passo', `Pergunta ${caminho.length}`));
                const h = el('h2', 'id-pergunta', no.p); h.tabIndex = -1; blocos.push(h);
                const ops = el('div', 'id-opcoes');
                no.o.forEach(([texto, destino]) => {
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
                zero.addEventListener('click', () => { caminho.length = 1; mostrar(); });
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
})();
