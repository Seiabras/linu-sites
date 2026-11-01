// O guia sem internet (1/11/2026): registra o service worker (sw.js) e cuida da caixa "Guardar o guia".
// Sem suporte a service worker, nada muda: a caixa continua escondida e o site funciona como antes.
(() => {
    if (!('serviceWorker' in navigator) || !(location.protocol === 'https:' || location.hostname === 'localhost' || location.hostname === '127.0.0.1')) return;
    navigator.serviceWorker.register('sw.js', { scope: './' }).catch(() => {});
    const caixa = document.querySelector('.guardar-guia');
    if (!caixa) return;
    const botao = caixa.querySelector('.guardar-botao');
    const estado = caixa.querySelector('.guardar-estado');
    const pronto = () => { botao.disabled = true; botao.textContent = 'Guia guardado'; estado.textContent = 'Pronto: o guia funciona sem internet neste aparelho. Ele se atualiza sozinho quando houver sinal.'; };
    navigator.serviceWorker.addEventListener('message', (e) => {
        const d = e.data || {};
        if (d.tipo === 'estado' && d.guardado) pronto();
        if (d.tipo === 'progresso') estado.textContent = `Guardando… ${d.feito} de ${d.total}`;
        if (d.tipo === 'pronto') pronto();
    });
    navigator.serviceWorker.ready.then((reg) => {
        caixa.hidden = false;
        reg.active.postMessage('estado');
        botao.addEventListener('click', () => {
            botao.disabled = true;
            estado.textContent = 'Começando…';
            reg.active.postMessage('guardar');
        });
    });
})();
