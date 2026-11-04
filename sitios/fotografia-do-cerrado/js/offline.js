// O guia sem internet (1/11/2026): registra o service worker (sw.js) e cuida da caixa "Guardar o guia".
// Sem suporte a service worker, nada muda: a caixa continua escondida e o site funciona como antes.
(() => {
    // as frases vêm no idioma da página: o grupo "offline" do #textos-estudo (o scripts-pt.json do gerador, traduzido
    // pelo catálogo de cada língua); {n} e afins são trocados pelos valores
    const TX = (() => { try { return JSON.parse(document.getElementById('textos-estudo').textContent).offline || {}; } catch { return {}; } })();
    const tr = (k, v = {}) => String(TX[k] ?? k).replace(/\{(\w+)\}/g, (_, x) => v[x] ?? '');
    if (!('serviceWorker' in navigator) || !(location.protocol === 'https:' || location.hostname === 'localhost' || location.hostname === '127.0.0.1')) return;
    navigator.serviceWorker.register('sw.js', { scope: './' }).catch(() => {});
    const caixa = document.querySelector('.guardar-guia');
    if (!caixa) return;
    const botao = caixa.querySelector('.guardar-botao');
    const estado = caixa.querySelector('.guardar-estado');
    const pronto = () => { botao.disabled = true; botao.textContent = tr('guardado'); estado.textContent = tr('pronto'); };
    navigator.serviceWorker.addEventListener('message', (e) => {
        const d = e.data || {};
        if (d.tipo === 'estado' && d.guardado) pronto();
        if (d.tipo === 'progresso') estado.textContent = tr('guardando', { n: d.feito, total: d.total });
        if (d.tipo === 'pronto') pronto();
    });
    navigator.serviceWorker.ready.then((reg) => {
        caixa.hidden = false;
        reg.active.postMessage('estado');
        botao.addEventListener('click', () => {
            botao.disabled = true;
            estado.textContent = tr('comecando');
            reg.active.postMessage('guardar');
        });
    });
})();
