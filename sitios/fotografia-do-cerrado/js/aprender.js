// Aprender brincando (31/10/2026): o quiz por tema, os jogos (espécies, tamanhos, épocas, paisagens) e a busca no glossário.
// O retorno de cada resposta é escrito ("Certo!" ou "Não é essa."), não só a cor, e vem com o link para o guia.
(() => {
    const embaralhar = (lista) => { const a = [...lista]; for (let i = a.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); [a[i], a[j]] = [a[j], a[i]]; } return a; };
    const ler = (id) => { try { return JSON.parse(document.getElementById(id).textContent); } catch { return null; } };
    // o recorde de cada jogo, guardado só neste navegador (1/11/2026); sem localStorage, o jogo segue sem recorde
    const recorde = (chave, ac, n) => {
        let todos = {};
        try { todos = JSON.parse(localStorage.getItem('cerrado-recordes') || '{}'); } catch { return ''; }
        const antes = todos[chave];
        if (!antes || ac / n > antes[0] / antes[1]) {
            todos[chave] = [ac, n];
            try { localStorage.setItem('cerrado-recordes', JSON.stringify(todos)); } catch { /* sem recorde */ }
            return antes ? ' Novo recorde!' : '';
        }
        return ` Seu recorde: ${antes[0]} de ${antes[1]}.`;
    };

    // um jogo de perguntas: monta os botões, corrige, explica e passa para a próxima
    function jogo({ caixa, proxima, rodadas, mostrar, fim }) {
        const opcoes = caixa.querySelector('.quiz-opcoes');
        const retorno = caixa.querySelector('.quiz-retorno');
        let i = 0, acertos = 0, lista = [];
        const rodada = () => {
            const r = lista[i];
            mostrar(r, i, lista.length);
            retorno.hidden = true; proxima.hidden = true;
            opcoes.replaceChildren(...r.opcoes.map((texto, n) => {
                const b = document.createElement('button');
                b.type = 'button'; b.textContent = texto;
                b.addEventListener('click', () => {
                    const certo = n === r.certa;
                    if (certo) acertos++;
                    // a marca escrita, além da cor: ✓ na certa, ✗ na escolhida errada
                    const marca = (o, t) => o.append(Object.assign(document.createElement('span'), { className: 'marca', textContent: t }));
                    opcoes.querySelectorAll('button').forEach((o, k) => { o.disabled = true; if (k === r.certa) { o.classList.add('certa'); marca(o, ' ✓'); } });
                    if (!certo) { b.classList.add('errada'); marca(b, ' ✗'); }
                    retorno.classList.toggle('certo', certo);
                    retorno.classList.toggle('errado', !certo);
                    retorno.replaceChildren(Object.assign(document.createElement('strong'), { textContent: certo ? 'Certo! ' : 'Não é essa. ' }), r.explicacao);
                    if (r.link) { retorno.append(' '); retorno.append(Object.assign(document.createElement('a'), { href: r.link, textContent: 'Ler no guia' })); }
                    retorno.hidden = false;
                    proxima.textContent = i + 1 < lista.length ? proxima.dataset.texto : 'Ver o resultado';
                    proxima.hidden = false;
                    proxima.focus();
                });
                return b;
            }));
        };
        proxima.dataset.texto = proxima.textContent;
        proxima.addEventListener('click', () => {
            if (++i < lista.length) { rodada(); caixa.querySelector('[tabindex="-1"]')?.focus(); return; }
            fim(acertos, lista.length, () => comecar(lista));
        });
        const comecar = (nova) => { lista = nova; i = 0; acertos = 0; rodada(); };
        return { comecar: (r) => comecar(r ?? rodadas()) };
    }

    // ---- quiz por tema
    const dadosQuiz = ler('quiz-dados');
    const caixaQuiz = document.querySelector('.quiz-caixa');
    if (dadosQuiz && caixaQuiz) {
        const pergunta = caixaQuiz.querySelector('.quiz-pergunta');
        const contador = caixaQuiz.querySelector('.quiz-contador');
        const temas = [...document.querySelectorAll('[data-tema]')];
        let tema = '';
        const rodadas = () => embaralhar(dadosQuiz.filter((q) => !tema || q.t === tema)).map((q) => ({ texto: q.p, opcoes: q.o, certa: q.c, explicacao: q.e, link: q.l }));
        const q = jogo({
            caixa: caixaQuiz, proxima: document.getElementById('quiz-proxima'), rodadas,
            mostrar: (r, i, n) => { contador.textContent = `Pergunta ${i + 1} de ${n}`; pergunta.textContent = r.texto; },
            fim: (a, n, denovo) => {
                contador.textContent = 'Resultado';
                pergunta.textContent = `Você acertou ${a} de ${n}.` + recorde('quiz-' + (tema || 'todos'), a, n);
                const b = Object.assign(document.createElement('button'), { type: 'button', className: 'botao', textContent: 'Jogar de novo' });
                b.addEventListener('click', () => q.comecar());
                caixaQuiz.querySelector('.quiz-opcoes').replaceChildren(b);
                caixaQuiz.querySelector('.quiz-retorno').hidden = true;
                document.getElementById('quiz-proxima').hidden = true;
                pergunta.focus();
            },
        });
        temas.forEach((b) => b.addEventListener('click', () => {
            tema = b.dataset.tema;
            temas.forEach((o) => o.setAttribute('aria-pressed', String(o === b)));
            q.comecar();
        }));
        q.comecar();
    }

    // ---- qual é esta espécie? (1/11/2026): dez espécies por partida; as erradas são do mesmo grupo, quando dá
    const dadosQual = ler('qual-dados');
    const caixaQual = document.querySelector('.qual-caixa');
    if (dadosQual && caixaQual) {
        const placar = caixaQual.querySelector('.qual-placar');
        const lista = caixaQual.querySelector('.qual-pistas');
        const mais = caixaQual.querySelector('.qual-mais');
        let atual = null, vistas = 0;
        const pista = (texto) => Object.assign(document.createElement('li'), { textContent: texto });
        mais.addEventListener('click', () => {
            if (!atual || vistas >= atual.p.length) return;
            const li = pista(atual.p[vistas++]);
            li.classList.add('nova');
            lista.append(li);
            mais.hidden = vistas >= atual.p.length;
        });
        const rodadas = () => embaralhar(dadosQual).slice(0, 10).map((s) => {
            const mesmoGrupo = dadosQual.filter((o) => o.id !== s.id && o.g === s.g);
            const mesmoReino = dadosQual.filter((o) => o.id !== s.id && o.r === s.r && o.g !== s.g);
            const outras = [...embaralhar(mesmoGrupo), ...embaralhar(mesmoReino)].slice(0, 2);
            const opcoes = embaralhar([s, ...outras]);
            return { s, opcoes: opcoes.map((o) => o.n), certa: opcoes.indexOf(s), explicacao: `É ${s.n}. ${s.e}`, link: `especie-${s.id}.html` };
        });
        const q = jogo({
            caixa: caixaQual, proxima: document.getElementById('qual-proxima'), rodadas,
            mostrar: (r, i, n) => {
                atual = r.s; vistas = 2;
                placar.textContent = `Espécie ${i + 1} de ${n} · ${r.s.g}`;
                lista.replaceChildren(...r.s.p.slice(0, 2).map(pista));
                mais.hidden = r.s.p.length <= 2;
            },
            fim: (ac, n) => {
                atual = null;
                placar.textContent = `Você reconheceu ${ac} de ${n} espécies.` + recorde('qual', ac, n);
                lista.replaceChildren(); mais.hidden = true;
                const b = Object.assign(document.createElement('button'), { type: 'button', className: 'botao', textContent: 'Jogar de novo' });
                b.addEventListener('click', () => q.comecar());
                caixaQual.querySelector('.quiz-opcoes').replaceChildren(b);
                caixaQual.querySelector('.quiz-retorno').hidden = true;
                document.getElementById('qual-proxima').hidden = true;
            },
        });
        q.comecar();
    }

    // ---- do maior para o menor (1/11/2026): cinco rodadas de quatro; vale a rodada com a ordem toda certa
    const dadosTam = ler('tamanho-dados');
    const caixaTam = document.querySelector('.tamanho-caixa');
    if (dadosTam && caixaTam) {
        const placar = caixaTam.querySelector('.tamanho-placar');
        const opcoes = caixaTam.querySelector('.tamanho-opcoes');
        const retorno = caixaTam.querySelector('.tamanho-retorno');
        const proxima = document.getElementById('tamanho-proxima');
        let rodada = 0, acertos = 0;
        const RODADAS = 5;
        // quatro com tamanhos bem diferentes (pelo menos 20% de um para o outro), para não virar loteria
        const sortear = () => {
            for (let tentativa = 0; tentativa < 50; tentativa++) {
                const q = embaralhar(dadosTam).slice(0, 4);
                const m = q.map((x) => x.m).sort((a, b) => a - b);
                if (m.every((v, i) => i === 0 || v >= m[i - 1] * 1.2)) return q;
            }
            return embaralhar(dadosTam).slice(0, 4);
        };
        const comecarRodada = () => {
            const itens = sortear();
            const certa = [...itens].sort((a, b) => b.m - a.m);
            const escolhidos = [];
            placar.textContent = `Rodada ${rodada + 1} de ${RODADAS}: toque do maior para o menor.`;
            retorno.hidden = true; proxima.hidden = true;
            opcoes.replaceChildren(...itens.map((it) => {
                const b = document.createElement('button');
                b.type = 'button';
                b.append(Object.assign(document.createElement('span'), { className: 'tamanho-ordem', textContent: '' }), it.n);
                b.addEventListener('click', () => {
                    escolhidos.push(it);
                    b.disabled = true;
                    b.querySelector('.tamanho-ordem').textContent = String(escolhidos.length);
                    b.setAttribute('aria-label', `${it.n}, ${escolhidos.length}º`);
                    if (escolhidos.length < itens.length) return;
                    const ok = escolhidos.every((x, i) => x === certa[i]);
                    if (ok) acertos++;
                    retorno.classList.toggle('certo', ok); retorno.classList.toggle('errado', !ok);
                    const lista = document.createElement('ol');
                    certa.forEach((x) => { const li = document.createElement('li'); li.append(Object.assign(document.createElement('a'), { href: `especie-${x.id}.html`, textContent: x.n }), ` (${x.t})`); lista.append(li); });
                    retorno.replaceChildren(Object.assign(document.createElement('strong'), { textContent: ok ? 'Certo! ' : 'Não é essa ordem. ' }), 'Do maior para o menor:', lista);
                    retorno.hidden = false;
                    proxima.textContent = rodada + 1 < RODADAS ? 'Próxima rodada' : 'Ver o resultado';
                    proxima.hidden = false; proxima.focus();
                });
                return b;
            }));
        };
        proxima.addEventListener('click', () => {
            if (++rodada < RODADAS) { comecarRodada(); return; }
            placar.textContent = `Você acertou a ordem em ${acertos} de ${RODADAS} rodadas.` + recorde('tamanho', acertos, RODADAS);
            retorno.hidden = true; proxima.hidden = true;
            const b = Object.assign(document.createElement('button'), { type: 'button', className: 'botao', textContent: 'Jogar de novo' });
            b.addEventListener('click', () => { rodada = 0; acertos = 0; comecarRodada(); });
            opcoes.replaceChildren(b);
        });
        comecarRodada();
    }

    // ---- de que época é? (1/11/2026): os acontecimentos do Mês a mês, com três épocas para escolher
    const dadosEp = ler('epoca-dados');
    const caixaEp = document.querySelector('.epoca-caixa');
    if (dadosEp && caixaEp) {
        const pergunta = caixaEp.querySelector('.epoca-pergunta');
        const placar = caixaEp.querySelector('.epoca-placar');
        const rodadas = () => embaralhar(dadosEp).slice(0, 8).map((e) => {
            const outras = embaralhar([...new Set(dadosEp.map((x) => x.q).filter((q) => q !== e.q))]).slice(0, 2);
            const opcoes = embaralhar([e.q, ...outras]);
            return { e, texto: e.n, opcoes, certa: opcoes.indexOf(e.q), explicacao: `${e.n}: ${e.q}. ${e.t}`, link: e.l };
        });
        const ep = jogo({
            caixa: caixaEp, proxima: document.getElementById('epoca-proxima'), rodadas,
            mostrar: (r, i, n) => { placar.textContent = `Pergunta ${i + 1} de ${n}`; pergunta.textContent = `Quando: ${r.texto}?`; },
            fim: (ac, n) => {
                placar.textContent = 'Resultado';
                pergunta.textContent = `Você acertou ${ac} de ${n}.` + recorde('epoca', ac, n);
                const b = Object.assign(document.createElement('button'), { type: 'button', className: 'botao', textContent: 'Jogar de novo' });
                b.addEventListener('click', () => ep.comecar());
                caixaEp.querySelector('.quiz-opcoes').replaceChildren(b);
                caixaEp.querySelector('.quiz-retorno').hidden = true;
                document.getElementById('epoca-proxima').hidden = true;
            },
        });
        ep.comecar();
    }

    // ---- qual paisagem é esta?
    const dadosAdivinha = ler('adivinha-dados');
    const caixaAdv = document.querySelector('.adivinha-caixa');
    if (dadosAdivinha && caixaAdv) {
        const figura = caixaAdv.querySelector('.adivinha-figura');
        const placar = caixaAdv.querySelector('.adivinha-placar');
        const ids = Object.keys(dadosAdivinha.nomes);
        const rodadas = () => embaralhar(ids).map((id) => {
            const outras = embaralhar(ids.filter((x) => x !== id)).slice(0, 2);
            const opcoes = embaralhar([id, ...outras]);
            return { id, opcoes: opcoes.map((x) => dadosAdivinha.nomes[x]), certa: opcoes.indexOf(id), explicacao: dadosAdivinha.dicas[id], link: 'paisagens.html#tipo-' + id };
        });
        const a = jogo({
            caixa: caixaAdv, proxima: document.getElementById('adivinha-proxima'), rodadas,
            // o desenho é o mesmo do corte, sem o nome
            mostrar: (r, i, n) => { figura.innerHTML = dadosAdivinha.desenhos[r.id]; placar.textContent = `Paisagem ${i + 1} de ${n}`; },
            fim: (ac, n) => {
                figura.replaceChildren();
                placar.textContent = `Você reconheceu ${ac} de ${n} paisagens.` + recorde('paisagem', ac, n);
                const b = Object.assign(document.createElement('button'), { type: 'button', className: 'botao', textContent: 'Jogar de novo' });
                b.addEventListener('click', () => a.comecar());
                caixaAdv.querySelector('.quiz-opcoes').replaceChildren(b);
                caixaAdv.querySelector('.quiz-retorno').hidden = true;
                document.getElementById('adivinha-proxima').hidden = true;
            },
        });
        a.comecar();
    }

    // ---- três versões (1/11/2026): no celular e no tablet, o índice vira abas e aparece um jogo por vez;
    // no computador, os jogos ficam lado a lado em duas colunas (o CSS cuida disso pela classe .aprender-grade)
    const texto = document.querySelector('.guia-texto');
    const secoes = texto ? [...texto.querySelectorAll(':scope > section[id]')] : [];
    const abas = [...document.querySelectorAll('.indice a')];
    if (secoes.length > 1 && abas.length) {
        texto.classList.add('aprender-grade');
        const estreito = matchMedia('(max-width: 1099px)');
        let atual = secoes.some((s) => '#' + s.id === location.hash) ? location.hash.slice(1) : secoes[0].id;
        const mostrar = (id) => {
            atual = id;
            secoes.forEach((s) => { s.hidden = estreito.matches && s.id !== id; });
            abas.forEach((a) => { if (estreito.matches) a.setAttribute('aria-current', String(a.getAttribute('href') === '#' + id)); });
        };
        abas.forEach((a) => a.addEventListener('click', (e) => {
            if (!estreito.matches) return;
            e.preventDefault();
            mostrar(a.getAttribute('href').slice(1));
            history.replaceState(null, '', a.getAttribute('href'));
            a.scrollIntoView({ block: 'nearest', inline: 'center', behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth' });
        }));
        estreito.addEventListener('change', () => mostrar(atual));
        mostrar(atual);
    }

    // ---- glossário: procurar sem acento
    const busca = document.getElementById('busca-termo');
    if (busca) {
        const limpo = (t) => t.normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase().trim();
        const termos = [...document.querySelectorAll('.termo')];
        const vazio = document.querySelector('.vazio-glossario');
        busca.addEventListener('input', () => {
            const q = limpo(busca.value);
            let n = 0;
            termos.forEach((t) => { const ok = !q || limpo(t.textContent).includes(q); t.hidden = !ok; if (ok) n++; });
            vazio.hidden = n > 0;
        });
    }
})();
