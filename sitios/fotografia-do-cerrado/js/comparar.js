// Comparar duas espécies quaisquer (1/11/2026): as duas lado a lado, a partir do <script id="comparar-dados">.
// O tamanho vai em barras na mesma escala (a maior ocupa a largura toda). O endereço guarda a escolha (?a=&b=).
(() => {
    let dados;
    try { dados = JSON.parse(document.getElementById('comparar-dados').textContent); } catch { return; }
    const selA = document.getElementById('comp-a'), selB = document.getElementById('comp-b');
    const saida = document.querySelector('.comparar-resultado');
    if (!selA || !selB || !saida) return;
    const porId = new Map(dados.esp.map((e) => [e.id, e]));
    const el = (tag, cls, texto) => { const e = document.createElement(tag); if (cls) e.className = cls; if (texto != null) e.textContent = texto; return e; };
    const link = (href, texto) => Object.assign(document.createElement('a'), { href, textContent: texto });

    function coluna(e, outra) {
        const c = el('article', 'comp-col');
        const h = el('h2'); h.append(link(`especie-${e.id}.html`, e.n)); c.append(el('p', 'comp-grupo', e.g), h, el('p', 'cientifico', e.c));
        if (e.a) c.append(el('span', 'selo', e.a));
        c.append(el('p', 'comp-abre', e.ab));
        if (e.f.length) { const dl = el('dl', 'ficha-fatos'); e.f.forEach(([k, v]) => dl.append(el('dt', null, k), el('dd', null, v))); c.append(el('h3', 'comp-sub', 'Em poucas palavras'), dl); }
        if (e.rc.length) { const ul = el('ul', 'lista'); e.rc.forEach((r) => ul.append(el('li', null, r))); c.append(el('h3', 'comp-sub', 'Como reconhecer'), ul); }
        const ul = el('ul', 'roteiro-chips comp-pais');
        e.p.forEach((id) => { const li = el('li'); const a = link(`paisagem-${id}.html`, dados.pais[id]); if (outra.p.includes(id)) { li.className = 'comum'; a.setAttribute('aria-label', `${dados.pais[id]} (as duas)`); } li.append(a); ul.append(li); });
        c.append(el('h3', 'comp-sub', 'Paisagens'), ul);
        return c;
    }
    function montar(daPessoa) {
        const a = porId.get(selA.value), b = porId.get(selB.value);
        if (!a || !b) return;
        const blocos = [];
        // a diferença, quando o par está em "Não confunda com"
        const dif = dados.pares[`${a.id}|${b.id}`] || dados.pares[`${b.id}|${a.id}`];
        if (dif) { const p = el('p', 'comp-diferenca'); p.append(el('strong', null, 'A diferença: '), dif); blocos.push(p); }
        if (a.id === b.id) blocos.push(el('p', 'comp-diferenca', 'Escolha duas espécies diferentes.'));
        // o tamanho, na mesma escala
        if (a.m && b.m) {
            const t = el('section', 'comp-tamanho'); t.append(el('h3', 'comp-sub', 'Do tamanho de quê?'));
            const maior = Math.max(a.m, b.m);
            [a, b].forEach((e) => {
                const linha = el('div', 'comp-barra-linha'); linha.append(el('span', 'comp-barra-nome', `${e.n}: ${e.mt}`));
                const barra = el('div', 'comp-barra'); const s = el('span'); s.style.setProperty('--pct', `${Math.max(2, (e.m / maior) * 100)}%`); barra.append(s);
                linha.append(barra); t.append(linha);
            });
            t.append(el('p', 'comp-nota', 'Comprimento dos bichos e altura das plantas, como nas fichas.'));
            blocos.push(t);
        }
        const lado = el('div', 'comp-lado'); lado.append(coluna(a, b), coluna(b, a)); blocos.push(lado);
        const comuns = a.p.filter((x) => b.p.includes(x));
        blocos.push(el('p', 'comp-nota', comuns.length ? `Em comum: ${comuns.map((x) => dados.pais[x].toLowerCase()).join(', ')} (marcadas nas duas).` : 'As duas não dividem nenhuma paisagem.'));
        saida.replaceChildren(...blocos);
        if (daPessoa) history.replaceState(null, '', `?a=${a.id}&b=${b.id}`);
    }
    const q = new URLSearchParams(location.search);
    if (porId.has(q.get('a'))) selA.value = q.get('a');
    if (porId.has(q.get('b'))) selB.value = q.get('b');
    else if (q.get('a') && selB.value === selA.value) selB.selectedIndex = (selA.selectedIndex + 1) % selB.options.length;
    selA.addEventListener('change', () => montar(true));
    selB.addEventListener('change', () => montar(true));
    document.querySelector('.comparar-trocar').addEventListener('click', () => { const x = selA.value; selA.value = selB.value; selB.value = x; montar(true); });
    montar(false);
})();
