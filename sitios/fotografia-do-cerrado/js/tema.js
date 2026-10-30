// Botão de tema: troca entre o claro e o escuro e guarda a escolha no navegador; sem escolha, segue o sistema.
// O rótulo do botão diz para onde ele leva, nos textos data-escuro e data-claro do próprio botão.
const botaoTema = document.querySelector('.botao-tema');
if (botaoTema) {
    const raiz = document.documentElement;
    const sistema = window.matchMedia('(prefers-color-scheme: dark)');
    const atual = () => raiz.dataset.theme || (sistema.matches ? 'dark' : 'light');
    const rotular = () => {
        const texto = atual() === 'dark' ? botaoTema.dataset.claro : botaoTema.dataset.escuro;
        botaoTema.setAttribute('aria-label', texto);
        botaoTema.title = texto;
    };
    botaoTema.addEventListener('click', () => {
        raiz.dataset.theme = atual() === 'dark' ? 'light' : 'dark';
        try { localStorage.setItem('tema', raiz.dataset.theme); } catch (e) {}
        rotular();
    });
    sistema.addEventListener('change', rotular);
    rotular();
}
