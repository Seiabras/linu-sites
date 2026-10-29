// Menu do celular: o botão abre e fecha a lista de links e mantém o aria-expanded em dia.
const botao = document.querySelector('.botao-menu');
const menu = document.getElementById('menu');
if (botao && menu) {
    botao.addEventListener('click', () => {
        const aberto = menu.classList.toggle('aberto');
        botao.setAttribute('aria-expanded', String(aberto));
    });
}
