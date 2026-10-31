// Galeria: filtro por grupo (mamíferos/aves) e foto ampliada num <dialog>.
const filtros = document.querySelectorAll('.filtros button');
const fotos = document.querySelectorAll('.foto[data-grupo]');

filtros.forEach(botao => {
    botao.addEventListener('click', () => {
        const grupo = botao.dataset.filtro;
        filtros.forEach(b => b.setAttribute('aria-pressed', String(b === botao)));
        fotos.forEach(foto => {
            foto.hidden = grupo !== 'todos' && foto.dataset.grupo !== grupo;
        });
    });
});

const janela = document.getElementById('ampliada');
if (janela) {
    const imagem = janela.querySelector('img');
    const titulo = janela.querySelector('.titulo');
    document.querySelectorAll('.foto button').forEach(botao => {
        botao.addEventListener('click', () => {
            const img = botao.querySelector('img');
            imagem.src = img.src;
            imagem.alt = img.alt;
            titulo.textContent = botao.closest('.foto').querySelector('h2, h3').textContent;
            janela.showModal();
        });
    });
    janela.querySelector('.fechar').addEventListener('click', () => janela.close());
    janela.addEventListener('click', e => { if (e.target === janela) janela.close(); });
}
