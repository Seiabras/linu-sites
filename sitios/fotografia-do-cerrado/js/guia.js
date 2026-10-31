// Guia do cerrado (31/10/2026): as partes que a pessoa usa com as mãos nas páginas do guia.
// - O bioma: os botões destacam um bioma no mapa e dizem quanto do Brasil ele ocupa.
// - Paisagens: tocar num trecho do corte desenhado, ou num botão, mostra a ficha daquela paisagem (sem JavaScript,
//   as onze fichas aparecem uma embaixo da outra).
// - O índice da página marca a seção que está na tela.
(() => {
    // ---- mapa dos biomas
    const mapa = document.querySelector('.mapa-biomas');
    const botoesBioma = [...document.querySelectorAll('.biomas-botoes button')];
    const legenda = document.querySelector('.bioma-legenda');
    if (mapa && botoesBioma.length) {
        const escolher = (botao) => {
            const id = botao.dataset.bioma;
            botoesBioma.forEach((b) => b.setAttribute('aria-pressed', String(b === botao)));
            mapa.dataset.destaque = id;
            const nome = botao.childNodes[1].textContent.trim();
            legenda.textContent = `${nome}: ${botao.querySelector('.bioma-pct').textContent} do Brasil.`;
        };
        botoesBioma.forEach((b) => b.addEventListener('click', () => escolher(b)));
        mapa.addEventListener('click', (e) => {
            const alvo = e.target.closest('[data-bioma]');
            const botao = alvo && botoesBioma.find((b) => b.dataset.bioma === alvo.dataset.bioma);
            if (botao) escolher(botao);
        });
        mapa.dataset.destaque = 'cerrado';
    }

    // ---- as paisagens
    const fichas = [...document.querySelectorAll('.paisagem')];
    const botoesTipo = [...document.querySelectorAll('.tipo')];
    const corte = document.querySelector('.corte');
    if (fichas.length && botoesTipo.length) {
        document.querySelector('.paisagens-layout').classList.add('uma-por-vez');
        const mostrar = (id, rolar) => {
            fichas.forEach((f) => { f.hidden = f.dataset.tipo !== id; });
            botoesTipo.forEach((b) => b.setAttribute('aria-pressed', String(b.dataset.tipo === id)));
            corte?.querySelectorAll('.trecho').forEach((t) => t.classList.toggle('escolhido', t.dataset.tipo === id));
            if (rolar) {
                // só quando a pessoa escolhe: gravar no endereço ao abrir a página fazia o navegador rolar até a ficha
                history.replaceState(null, '', '#tipo-' + id);
                const ficha = document.getElementById('tipo-' + id);
                // no celular a ficha fica embaixo dos botões: rola até ela; no computador, ela já está ao lado
                if (ficha.getBoundingClientRect().top > innerHeight * 0.7) ficha.scrollIntoView({ behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth', block: 'start' });
            }
        };
        botoesTipo.forEach((b) => b.addEventListener('click', () => mostrar(b.dataset.tipo, true)));
        corte?.addEventListener('click', (e) => {
            const t = e.target.closest('.trecho');
            if (t) mostrar(t.dataset.tipo, true);
        });
        const doEndereco = location.hash.replace('#tipo-', '');
        mostrar(fichas.some((f) => f.dataset.tipo === doEndereco) ? doEndereco : 'cerrado-sentido-restrito', false);
        // no celular, o corte começa no trecho escolhido
        const rolagem = document.querySelector('.corte-rolagem');
        const trecho = corte?.querySelector('.trecho.escolhido');
        if (rolagem && trecho && rolagem.scrollWidth > rolagem.clientWidth) {
            const caixa = trecho.getBoundingClientRect(), fora = rolagem.getBoundingClientRect();
            rolagem.scrollLeft += caixa.left - fora.left - (fora.width - caixa.width) / 2;
        }
    }

    // ---- o índice marca a seção que está na tela
    const links = [...document.querySelectorAll('.indice a')];
    if (links.length && 'IntersectionObserver' in window) {
        const secoes = links.map((a) => document.querySelector(a.getAttribute('href'))).filter(Boolean);
        const vistas = new Set();
        const obs = new IntersectionObserver((entradas) => {
            for (const e of entradas) (e.isIntersecting ? vistas.add(e.target) : vistas.delete(e.target));
            const atual = secoes.find((s) => vistas.has(s));
            if (!atual) return;
            links.forEach((a) => {
                const agora = a.getAttribute('href') === '#' + atual.id;
                if (agora) a.setAttribute('aria-current', 'true'); else a.removeAttribute('aria-current');
            });
            // no celular o índice é uma faixa que rola de lado: o item atual fica à vista
            const ativo = links.find((a) => a.hasAttribute('aria-current'));
            const faixa = ativo?.closest('ol');
            if (faixa && faixa.scrollWidth > faixa.clientWidth) faixa.scrollLeft = ativo.offsetLeft - 16;
        }, { rootMargin: '-30% 0px -60% 0px' });
        secoes.forEach((s) => obs.observe(s));
    }
})();

// ---- o catálogo de espécies: busca, grupo, paisagem e "só as ameaçadas", tudo junto
(() => {
    const lista = document.querySelector('.especies-lista');
    if (!lista) return;
    const itens = [...lista.querySelectorAll('.esp')];
    const busca = document.getElementById('busca-especie');
    const paisagem = document.getElementById('paisagem-especie');
    const ameacadas = document.getElementById('so-ameacadas');
    const chips = [...document.querySelectorAll('[data-filtro-grupo]')];
    const contagem = document.getElementById('contagem');
    const vazio = document.querySelector('.vazio');
    let grupo = '';
    // sem acento e em minúsculas: "tamandua" acha "Tamanduá"
    const limpo = (t) => t.normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase().trim();
    const filtrar = () => {
        const q = limpo(busca.value);
        let n = 0;
        for (const it of itens) {
            const ok = (!q || limpo(it.dataset.busca).includes(q))
                && (!grupo || it.dataset.grupo === grupo)
                && (!paisagem.value || it.dataset.paisagens.split(' ').includes(paisagem.value))
                && (!ameacadas.checked || it.dataset.ameaca);
            it.hidden = !ok;
            if (ok) n++;
        }
        contagem.textContent = n;
        vazio.hidden = n > 0;
    };
    chips.forEach((c) => c.addEventListener('click', () => {
        grupo = c.dataset.filtroGrupo;
        chips.forEach((o) => o.setAttribute('aria-pressed', String(o === c)));
        filtrar();
    }));
    busca.addEventListener('input', filtrar);
    paisagem.addEventListener('change', filtrar);
    ameacadas.addEventListener('change', filtrar);
    document.getElementById('limpar-filtros').addEventListener('click', () => {
        busca.value = ''; paisagem.value = ''; ameacadas.checked = false; grupo = '';
        chips.forEach((o) => o.setAttribute('aria-pressed', String(o.dataset.filtroGrupo === '')));
        filtrar();
        busca.focus();
    });
    // vindo de uma paisagem (especies.html?paisagem=vereda), já chega filtrado
    const p = new URLSearchParams(location.search).get('paisagem');
    if (p && [...paisagem.options].some((o) => o.value === p)) paisagem.value = p;
    filtrar();
})();
