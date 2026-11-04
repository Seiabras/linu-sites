// Buscar no guia (1/11/2026): procura no índice que vem dentro da página (<script id="busca-dados">), sem servidor.
// Sem acento e sem maiúsculas; todas as palavras precisam aparecer. O nome conta mais que o texto. O endereço guarda
// a busca (?q=), para dar para mandar o link. Os resultados são montados com textContent.
(() => {
    // as frases vêm no idioma da página: o grupo "busca" do #textos-estudo (o scripts-pt.json do gerador, traduzido
    // pelo catálogo de cada língua); {n} e afins são trocados pelos valores
    const TX = (() => { try { return JSON.parse(document.getElementById('textos-estudo').textContent).busca || {}; } catch { return {}; } })();
    const tr = (k, v = {}) => String(TX[k] ?? k).replace(/\{(\w+)\}/g, (_, x) => v[x] ?? '');
    const campo = document.getElementById('busca-q');
    const saida = document.querySelector('.busca-resultados');
    const contagem = document.querySelector('.busca-contagem');
    const sugestoes = document.querySelector('.busca-sugestoes');
    let itens = [];
    try { itens = JSON.parse(document.getElementById('busca-dados').textContent); } catch { return; }
    if (!campo || !saida) return;
    const limpo = (t) => t.normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase();
    const prontos = itens.map((it) => ({ it, nome: limpo(it.n), resto: limpo(`${it.s} ${it.k} ${it.d}`) }));
    // os tipos, na ordem; são os mesmos textos do campo "t" do índice (traduzidos pelo mesmo catálogo)
    const ORDEM = ['especies', 'paisagens', 'parques', 'povos', 'glossario', 'mes_a_mes', 'paginas'].map((k) => tr(k));

    // o nome com a parte achada em <mark>, sem innerHTML
    const nomeMarcado = (nome, termos) => {
        const base = limpo(nome);
        let ini = -1, fim = -1;
        for (const t of termos) { const i = base.indexOf(t); if (i >= 0) { ini = i; fim = i + t.length; break; } }
        if (ini < 0) return [document.createTextNode(nome)];
        return [document.createTextNode(nome.slice(0, ini)), Object.assign(document.createElement('mark'), { textContent: nome.slice(ini, fim) }), document.createTextNode(nome.slice(fim))];
    };
    function buscar(q, daPessoa) {
        const termos = limpo(q).split(/\s+/).filter((t) => t.length > 1);
        sugestoes.hidden = termos.length > 0;
        if (!termos.length) { saida.replaceChildren(); contagem.textContent = ''; if (daPessoa) history.replaceState(null, '', location.pathname); return; }
        const achados = [];
        for (const p of prontos) {
            if (!termos.every((t) => p.nome.includes(t) || p.resto.includes(t))) continue;
            const s = termos.reduce((soma, t) => soma + (p.nome.startsWith(t) ? 0 : p.nome.includes(t) ? 1 : 3), 0);
            achados.push({ ...p, s });
        }
        achados.sort((a, b) => a.s - b.s || a.it.n.localeCompare(b.it.n, document.documentElement.lang));
        contagem.textContent = achados.length ? tr(achados.length === 1 ? 'um_resultado' : 'resultados', { n: achados.length, q: q.trim() }) : tr('nada', { q: q.trim() });
        const blocos = [];
        for (const tipo of ORDEM) {
            const doTipo = achados.filter((a) => a.it.t === tipo);
            if (!doTipo.length) continue;
            const sec = document.createElement('section');
            sec.className = 'busca-grupo';
            sec.append(Object.assign(document.createElement('h2'), { className: 'sub', textContent: `${tipo} (${doTipo.length})` }));
            const ul = document.createElement('ul');
            doTipo.forEach(({ it }, i) => {
                const li = document.createElement('li');
                const a = document.createElement('a');
                a.href = it.u; a.append(...nomeMarcado(it.n, termos));
                li.append(a);
                if (it.s) li.append(Object.assign(document.createElement('span'), { className: 'busca-sub', textContent: it.s }));
                li.append(Object.assign(document.createElement('p'), { textContent: it.d }));
                if (i >= 8) li.hidden = true;
                ul.append(li);
            });
            sec.append(ul);
            if (doTipo.length > 8) {
                const mais = Object.assign(document.createElement('button'), { type: 'button', className: 'botao botao-linha busca-mais', textContent: tr('mostrar_mais', { n: doTipo.length - 8 }) });
                mais.addEventListener('click', () => { ul.querySelectorAll('li[hidden]').forEach((li) => { li.hidden = false; }); mais.remove(); });
                sec.append(mais);
            }
            blocos.push(sec);
        }
        saida.replaceChildren(...blocos);
        if (daPessoa) history.replaceState(null, '', '?q=' + encodeURIComponent(q.trim()));
    }
    let espera = 0;
    campo.addEventListener('input', () => { clearTimeout(espera); espera = setTimeout(() => buscar(campo.value, true), 120); });
    campo.form.addEventListener('submit', (e) => { e.preventDefault(); buscar(campo.value, true); });
    const q = new URLSearchParams(location.search).get('q') || '';
    campo.value = q;
    buscar(q, false);
    if (!q) campo.focus();
})();
