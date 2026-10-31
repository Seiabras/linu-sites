// Monte sua visita (1/11/2026): parque + mês. Junta as paisagens do parque, as espécies dessas paisagens (os destaques
// do parque primeiro) e o que acontece no mês, a partir do <script id="roteiro-dados">. Tudo montado com textContent.
(() => {
    const dados = (() => { try { return JSON.parse(document.getElementById('roteiro-dados').textContent); } catch { return null; } })();
    const selParque = document.getElementById('roteiro-parque');
    const selMes = document.getElementById('roteiro-mes');
    const saida = document.querySelector('.roteiro-resultado');
    if (!dados || !selParque || !selMes || !saida) return;
    const NOMES = ['janeiro', 'fevereiro', 'março', 'abril', 'maio', 'junho', 'julho', 'agosto', 'setembro', 'outubro', 'novembro', 'dezembro'];
    const estacao = (m) => (m >= 5 && m <= 7 ? 'seca' : m === 8 || m === 9 ? 'auge' : 'chuvas');
    const NOTA = {
        chuvas: ['Época das chuvas', 'O cerrado fica verde e as frutas amadurecem. As trilhas podem ter lama e os rios sobem: prefira as saídas curtas e confira as cachoeiras antes de ir.'],
        seca: ['Começo da seca', 'O capim baixa e fica mais fácil ver os bichos de longe. As noites esfriam nas chapadas.'],
        auge: ['Auge da seca', 'Os ipês florescem e os bichos se juntam perto da água. É também a época do fogo: siga as regras do parque e não acenda nada.'],
    };
    const el = (tag, cls, texto) => { const e = document.createElement(tag); if (cls) e.className = cls; if (texto != null) e.textContent = texto; return e; };
    const link = (href, texto) => Object.assign(document.createElement('a'), { href, textContent: texto });
    const secao = (titulo) => { const s = el('section', 'roteiro-bloco'); s.append(el('h2', 'sub', titulo)); return s; };

    function montar(daPessoa) {
        const parque = dados.parques.find((p) => p.n === Number(selParque.value)) || dados.parques[0];
        const mes = Number(selMes.value) || 1;
        const est = estacao(mes);
        const blocos = [];

        const topo = el('div', `roteiro-topo estacao-${est}`);
        topo.append(el('p', 'roteiro-titulo', `${parque.nome}, em ${NOMES[mes - 1]}`), el('p', 'roteiro-estacao', NOTA[est][0]), el('p', null, NOTA[est][1]));
        const sobre = el('p', 'roteiro-sobre', parque.texto + ' ');
        sobre.append(link(`onde-ver.html#parque-${parque.n}`, 'Ver no mapa'));
        topo.append(sobre);
        blocos.push(topo);

        const sp = secao('Paisagens que você vai ver');
        const lp = el('ul', 'roteiro-chips');
        parque.pais.forEach((id) => { const li = el('li'); li.append(link(`paisagem-${id}.html`, dados.paisagens[id])); lp.append(li); });
        sp.append(lp); blocos.push(sp);

        // as espécies das paisagens do parque: os destaques primeiro, depois as que têm algo acontecendo no mês
        const noMes = new Set(dados.eventos.filter((e) => e.m.includes(mes)).map((e) => (e.l.match(/especie-(.+)\.html/) || [])[1]).filter(Boolean));
        const lista = dados.especies.filter((e) => parque.dest.includes(e.id) || e.p.some((x) => parque.pais.includes(x)));
        const peso = (e) => (parque.dest.includes(e.id) ? 0 : noMes.has(e.id) ? 1 : 2);
        lista.sort((a, b) => peso(a) - peso(b) || a.n.localeCompare(b.n, 'pt-BR'));
        const se = secao(`Para procurar (${lista.length} espécies)`);
        se.classList.add('roteiro-bloco-especies');
        const le = el('ul', 'roteiro-especies');
        lista.forEach((e, i) => {
            const li = el('li'); li.append(link(`especie-${e.id}.html`, e.n));
            if (peso(e) === 0) li.append(el('span', 'roteiro-marca', 'destaque do parque'));
            else if (peso(e) === 1) li.append(el('span', 'roteiro-marca', 'em época'));
            li.append(el('span', 'roteiro-grupo', e.g));
            if (i >= 12) li.hidden = true;
            le.append(li);
        });
        se.append(le);
        if (lista.length > 12) {
            const mais = el('button', 'botao botao-linha roteiro-mais', `Mostrar todas as ${lista.length}`);
            mais.type = 'button';
            mais.addEventListener('click', () => { le.querySelectorAll('li[hidden]').forEach((li) => { li.hidden = false; }); mais.remove(); });
            se.append(mais);
        }
        blocos.push(se);

        const ev = dados.eventos.filter((e) => e.m.includes(mes));
        if (ev.length) {
            const sa = secao(`Acontecendo em ${NOMES[mes - 1]}`);
            const la = el('ul', 'roteiro-eventos');
            ev.forEach((e) => { const li = el('li'); li.append(link(e.l, e.n), document.createTextNode(': ' + e.t)); la.append(li); });
            const ver = el('p', 'roteiro-sobre'); ver.append(link(`mes-a-mes.html?mes=${mes}`, `Tudo de ${NOMES[mes - 1]} no Mês a mês`));
            sa.append(la, ver); blocos.push(sa);
        }
        saida.replaceChildren(...blocos);
        if (daPessoa) history.replaceState(null, '', `?parque=${parque.n}&mes=${mes}`);
    }
    const q = new URLSearchParams(location.search);
    if (dados.parques.some((p) => String(p.n) === q.get('parque'))) selParque.value = q.get('parque');
    const m = Number(q.get('mes'));
    selMes.value = String(m >= 1 && m <= 12 ? m : new Date().getMonth() + 1);
    selParque.addEventListener('change', () => montar(true));
    selMes.addEventListener('change', () => montar(true));
    montar(false);
})();
