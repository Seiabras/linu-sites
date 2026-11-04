// Vi no campo (1/11/2026): o caderno de campo pessoal. Fica só neste navegador (localStorage), numa lista de
// avistamentos {id, d (data AAAA-MM-DD), p (lugar)}. Serve às fichas (o botão), ao catálogo (a marca "vista")
// e à página Meu caderno (contagem, por grupo, lista, copiar e baixar). Sem localStorage, o botão avisa e não quebra.
(() => {
    // as frases vêm no idioma da página: o grupo "caderno" do #textos-estudo (o scripts-pt.json do gerador, traduzido
    // pelo catálogo de cada língua); {n} e afins são trocados pelos valores
    const TX = (() => { try { return JSON.parse(document.getElementById('textos-estudo').textContent).caderno || {}; } catch { return {}; } })();
    const tr = (k, v = {}) => String(TX[k] ?? k).replace(/\{(\w+)\}/g, (_, x) => v[x] ?? '');
    const CHAVE = 'cerrado-caderno';
    const ler = () => { try { const d = JSON.parse(localStorage.getItem(CHAVE) || '[]'); return Array.isArray(d) ? d : []; } catch { return null; } };
    const gravar = (lista) => { try { localStorage.setItem(CHAVE, JSON.stringify(lista)); return true; } catch { return false; } };
    const hoje = () => new Date().toISOString().slice(0, 10);
    const dataBR = (iso) => iso.split('-').reverse().join('/');
    const el = (tag, cls, texto) => { const e = document.createElement(tag); if (cls) e.className = cls; if (texto != null) e.textContent = texto; return e; };

    // ---- na ficha: "Vi no campo"
    const caixa = document.querySelector('.vi-campo');
    if (caixa) {
        const id = caixa.dataset.id, nome = caixa.dataset.nome;
        let parques = [];
        try { parques = JSON.parse(caixa.dataset.parques); } catch { /* sem a lista, só "outro lugar" */ }
        const montar = (aviso) => {
            const lista = ler();
            caixa.replaceChildren();
            caixa.append(el('h2', 'sub', tr('vi_no_campo')));
            if (lista === null) { caixa.append(el('p', null, tr('sem_guardar'))); caixa.hidden = false; return; }
            const minhas = lista.filter((v) => v.id === id).sort((a, b) => b.d.localeCompare(a.d));
            if (minhas.length) {
                const u = minhas[0];
                caixa.append(el('p', 'vi-resumo', tr(minhas.length === 1 ? 'viu_uma' : 'viu_vezes', { n: minhas.length, data: dataBR(u.d) + (u.p ? ', ' + u.p : '') })));
            } else caixa.append(el('p', null, tr('viu_por_ai', { nome: nome.toLowerCase().startsWith('o ') ? nome : tr('esta_especie') })));
            const abrir = el('button', 'botao', minhas.length ? tr('vi_de_novo') : tr('vi_no_campo'));
            abrir.type = 'button';
            const acoes = el('div', 'vi-acoes'); acoes.append(abrir);
            if (minhas.length) {
                const desfazer = el('button', 'botao botao-linha', tr('desfazer'));
                desfazer.type = 'button';
                desfazer.addEventListener('click', () => { const l = ler(); const i = l.findIndex((v) => v === l.filter((x) => x.id === id).sort((a, b) => b.d.localeCompare(a.d))[0]); if (i >= 0) l.splice(i, 1); gravar(l); montar(tr('desfeito')); });
                acoes.append(desfazer);
            }
            const ver = el('a', 'vi-caderno', tr('meu_caderno')); ver.href = 'caderno.html'; acoes.append(ver);
            caixa.append(acoes);
            if (aviso) caixa.append(el('p', 'vi-aviso', aviso));
            abrir.addEventListener('click', () => {
                const form = el('form', 'vi-form');
                const ld = el('label', null, tr('quando')); const d = el('input'); d.type = 'date'; d.value = hoje(); d.max = hoje(); d.required = true; d.id = 'vi-data'; ld.htmlFor = 'vi-data';
                const lp = el('label', null, tr('onde')); const s = el('select'); s.id = 'vi-lugar'; lp.htmlFor = 'vi-lugar';
                [tr('outro_lugar_op'), ...parques].forEach((n, i) => { const o = el('option', null, n); o.value = i ? n : ''; s.append(o); });
                const ok = el('button', 'botao', tr('guardar')); ok.type = 'submit';
                const c1 = el('div', 'campo'); c1.append(ld, d); const c2 = el('div', 'campo'); c2.append(lp, s);
                form.append(c1, c2, ok);
                form.addEventListener('submit', (ev) => {
                    ev.preventDefault();
                    const l = ler() || []; l.push({ id, d: d.value || hoje(), p: s.value }); gravar(l);
                    montar(tr('guardado'));
                    caixa.querySelector('.vi-aviso')?.focus?.();
                });
                abrir.replaceWith(form);
                d.focus();
            });
            caixa.hidden = false;
        };
        montar();
    }

    // ---- no catálogo: a marca "vista" nos cartões
    const cartoes = document.querySelectorAll('.especies-lista .esp');
    if (cartoes.length) {
        const vistas = new Set((ler() || []).map((v) => v.id));
        cartoes.forEach((c) => {
            const a = c.querySelector('h2 a'); const id = a && (a.getAttribute('href').match(/especie-(.+)\.html/) || [])[1];
            if (id && vistas.has(decodeURIComponent(id))) c.querySelector('.esp-texto').append(el('span', 'selo selo-vista', tr('vista')));
        });
    }

    // ---- a página Meu caderno
    const resumo = document.querySelector('.caderno-resumo');
    if (resumo) {
        let especies = [];
        try { especies = JSON.parse(document.getElementById('caderno-dados').textContent); } catch { return; }
        const porId = new Map(especies.map((e) => [e.id, e]));
        const listaEl = document.querySelector('.caderno-lista');
        const montar = () => {
            const lista = ler();
            resumo.replaceChildren(); listaEl.replaceChildren();
            if (lista === null) { resumo.append(el('p', null, tr('sem_guardar'))); return; }
            const validas = lista.filter((v) => porId.has(v.id));
            const vistas = new Set(validas.map((v) => v.id));
            const n = vistas.size, total = especies.length;
            const topo = el('div', 'caderno-total');
            topo.append(el('p', 'caderno-numero', tr('n_de_total', { n, total })), el('p', null, n ? tr('ja_viu') : tr('nada_marcado')));
            const barra = el('div', 'caderno-barra'); const enche = el('span'); enche.style.setProperty('--pct', `${(n / total) * 100}%`); barra.append(enche);
            barra.setAttribute('role', 'img'); barra.setAttribute('aria-label', tr('pct_especies', { pct: Math.round((n / total) * 100) }));
            topo.append(barra);
            resumo.append(topo);
            // por grupo
            const grupos = [...new Set(especies.map((e) => e.g))];
            const ul = el('ul', 'caderno-grupos');
            grupos.forEach((g) => {
                const doG = especies.filter((e) => e.g === g); const vistoG = doG.filter((e) => vistas.has(e.id)).length;
                const li = el('li'); li.append(el('span', 'caderno-grupo-nome', g), el('span', 'caderno-grupo-num', tr('n_de_total', { n: vistoG, total: doG.length })));
                const b = el('div', 'caderno-barra pequena'); const s = el('span'); s.style.setProperty('--pct', `${(vistoG / doG.length) * 100}%`); b.append(s); li.append(b);
                ul.append(li);
            });
            resumo.append(ul);
            if (!validas.length) return;
            // a lista de avistamentos, os mais novos primeiro
            listaEl.append(el('h2', 'sub', tr('avistamentos', { n: validas.length })));
            const ol = el('ol', 'caderno-avist');
            [...validas].sort((a, b) => b.d.localeCompare(a.d)).forEach((v) => {
                const li = el('li'); const a = el('a', null, porId.get(v.id).n); a.href = `especie-${v.id}.html`;
                li.append(el('span', 'caderno-data', dataBR(v.d)), a, el('span', 'caderno-lugar', v.p || tr('outro_lugar')));
                const x = el('button', 'caderno-apagar', '×'); x.type = 'button'; x.setAttribute('aria-label', tr('apagar_um', { nome: porId.get(v.id).n, data: dataBR(v.d) }));
                x.addEventListener('click', () => { const l = ler(); const i = l.findIndex((w) => w.id === v.id && w.d === v.d && w.p === v.p); if (i >= 0) l.splice(i, 1); gravar(l); montar(); });
                li.append(x); ol.append(li);
            });
            listaEl.append(ol);
            // copiar e baixar
            const texto = () => [...validas].sort((a, b) => a.d.localeCompare(b.d)).map((v) => `${dataBR(v.d)}\t${porId.get(v.id).n}\t${v.p || tr('outro_lugar')}`).join('\n');
            const acoes = el('div', 'vi-acoes');
            const copiar = el('button', 'botao', tr('copiar')); copiar.type = 'button';
            const aviso = el('p', 'vi-aviso'); aviso.setAttribute('aria-live', 'polite');
            copiar.addEventListener('click', async () => { try { await navigator.clipboard.writeText(texto()); aviso.textContent = tr('copiada'); } catch { aviso.textContent = tr('nao_copiou'); } });
            const baixar = el('a', 'botao botao-linha', tr('baixar'));
            const csv = tr('csv_cabecalho') + '\n' + [...validas].sort((a, b) => a.d.localeCompare(b.d)).map((v) => [v.d, porId.get(v.id).n, v.p || ''].map((c) => `"${String(c).replace(/"/g, '""')}"`).join(',')).join('\n');
            baixar.href = URL.createObjectURL(new Blob([csv], { type: 'text/csv' })); baixar.download = 'caderno-de-campo-cerrado.csv';
            const apagar = el('button', 'botao botao-linha', tr('apagar_tudo')); apagar.type = 'button';
            apagar.addEventListener('click', () => { if (confirm(tr('apagar_confirma'))) { gravar([]); montar(); } });
            acoes.append(copiar, baixar, apagar); listaEl.append(acoes, aviso);
        };
        montar();
    }
})();
