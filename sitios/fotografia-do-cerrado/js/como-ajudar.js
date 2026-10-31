// Como ajudar (1/11/2026): "Vou fazer isto" em cada ação. A lista fica guardada só neste navegador (localStorage);
// se o navegador não deixar guardar, as marcas funcionam do mesmo jeito, só não ficam para a próxima visita.
(() => {
    const caixas = [...document.querySelectorAll('input[data-acao]')];
    const placar = document.querySelector('.acoes-placar');
    if (!caixas.length || !placar) return;
    const CHAVE = 'cerrado-como-ajudar';
    let marcadas = [];
    try { marcadas = JSON.parse(localStorage.getItem(CHAVE) || '[]'); } catch { marcadas = []; }
    const atualizar = () => {
        const n = caixas.filter((c) => c.checked).length;
        placar.textContent = n ? `Você marcou ${n} de ${caixas.length}. Obrigado!` : `Marque o que você vai fazer: são ${caixas.length} ações.`;
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
