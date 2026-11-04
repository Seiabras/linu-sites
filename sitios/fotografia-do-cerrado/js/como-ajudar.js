// Como ajudar (1/11/2026): "Vou fazer isto" em cada ação. A lista fica guardada só neste navegador (localStorage);
// se o navegador não deixar guardar, as marcas funcionam do mesmo jeito, só não ficam para a próxima visita.
(() => {
    // as frases vêm no idioma da página: o grupo "como-ajudar" do #textos-estudo (o scripts-pt.json do gerador, traduzido
    // pelo catálogo de cada língua); {n} e afins são trocados pelos valores
    const TX = (() => { try { return JSON.parse(document.getElementById('textos-estudo').textContent)['como-ajudar'] || {}; } catch { return {}; } })();
    const tr = (k, v = {}) => String(TX[k] ?? k).replace(/\{(\w+)\}/g, (_, x) => v[x] ?? '');
    const caixas = [...document.querySelectorAll('input[data-acao]')];
    const placar = document.querySelector('.acoes-placar');
    if (!caixas.length || !placar) return;
    const CHAVE = 'cerrado-como-ajudar';
    let marcadas = [];
    try { marcadas = JSON.parse(localStorage.getItem(CHAVE) || '[]'); } catch { marcadas = []; }
    const atualizar = () => {
        const n = caixas.filter((c) => c.checked).length;
        placar.textContent = n ? tr('marcou', { n, total: caixas.length }) : tr('marque', { total: caixas.length });
        caixas.forEach((c) => c.closest('.acao').classList.toggle('marcada', c.checked));
    };
    caixas.forEach((c) => {
        c.checked = marcadas.includes(c.dataset.acao);
        c.addEventListener('change', () => {
            atualizar();
            try { localStorage.setItem(CHAVE, JSON.stringify(caixas.filter((x) => x.checked).map((x) => x.dataset.acao))); } catch { /* fica só nesta visita */ }
        });
    });
    placar.hidden = false;
    atualizar();
})();
