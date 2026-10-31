// Aprender brincando (31/10/2026): o quiz por tema, o "Qual paisagem é esta?" e a busca no glossário.
// O retorno de cada resposta é escrito ("Certo!" ou "Não é essa."), não só a cor, e vem com o link para o guia.
(() => {
    const embaralhar = (lista) => { const a = [...lista]; for (let i = a.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); [a[i], a[j]] = [a[j], a[i]]; } return a; };
    const ler = (id) => { try { return JSON.parse(document.getElementById(id).textContent); } catch { return null; } };

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
                pergunta.textContent = `Você acertou ${a} de ${n}.`;
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
                placar.textContent = `Você reconheceu ${ac} de ${n} paisagens.`;
                const b = Object.assign(document.createElement('button'), { type: 'button', className: 'botao', textContent: 'Jogar de novo' });
                b.addEventListener('click', () => a.comecar());
                caixaAdv.querySelector('.quiz-opcoes').replaceChildren(b);
                caixaAdv.querySelector('.quiz-retorno').hidden = true;
                document.getElementById('adivinha-proxima').hidden = true;
            },
        });
        a.comecar();
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
