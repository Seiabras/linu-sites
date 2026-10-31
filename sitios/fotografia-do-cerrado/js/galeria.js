// Galeria: filtro por grupo (mamíferos/aves) e foto ampliada num <dialog>, com o nome, o nome científico e o texto da
// espécie. Dentro dela, anterior e próxima pelos botões, pelas setas do teclado e deslizando o dedo; só passa pelas
// fotos que o filtro deixou à vista (31/10/2026).
const filtros = document.querySelectorAll('.filtros button');
const fotos = [...document.querySelectorAll('.foto[data-grupo]')];

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
    let t = {};
    try { t = JSON.parse(document.getElementById('textos-estudo').textContent); } catch { /* fica em português */ }
    const imagem = janela.querySelector('.moldura img');
    const titulo = janela.querySelector('.titulo');
    const cientifico = janela.querySelector('.cientifico');
    const texto = janela.querySelector('.texto');
    const posicao = janela.querySelector('.posicao');
    const anterior = janela.querySelector('.anterior');
    const proxima = janela.querySelector('.proxima');
    anterior.setAttribute('aria-label', t.anterior || 'Foto anterior');
    proxima.setAttribute('aria-label', t.proxima || 'Próxima foto');
    const calmo = matchMedia('(prefers-reduced-motion: reduce)');
    let atual = 0;
    let espera = 0;

    const visiveis = () => fotos.filter(f => !f.hidden);
    function mostrar(foto) {
        const lista = visiveis();
        atual = lista.indexOf(foto);
        const img = foto.querySelector('img');
        const trocar = () => {
            // a foto grande, não a de 640 px que o celular pode ter escolhido para a grade
            imagem.src = img.getAttribute('src');
            imagem.alt = img.alt;
            imagem.setAttribute('width', img.getAttribute('width'));
            imagem.setAttribute('height', img.getAttribute('height'));
            titulo.textContent = foto.querySelector('h2, h3').textContent;
            cientifico.textContent = foto.querySelector('.cientifico').textContent;
            texto.textContent = foto.querySelector('.legenda > p:not(.cientifico)')?.textContent || '';
            posicao.textContent = (t.posicao || '{n} de {total}').replace('{n}', atual + 1).replace('{total}', lista.length);
            imagem.classList.remove('trocando');
        };
        clearTimeout(espera);
        if (janela.open && !calmo.matches) {
            imagem.classList.add('trocando');
            espera = setTimeout(trocar, 150);
        } else trocar();
        anterior.hidden = proxima.hidden = lista.length < 2;
    }
    const passo = (n) => {
        const lista = visiveis();
        mostrar(lista[(atual + n + lista.length) % lista.length]);
    };

    fotos.forEach(foto => {
        foto.querySelector('button').addEventListener('click', () => {
            mostrar(foto);
            janela.showModal();
        });
    });
    anterior.addEventListener('click', () => passo(-1));
    proxima.addEventListener('click', () => passo(1));
    janela.addEventListener('keydown', e => {
        if (e.key === 'ArrowLeft') { e.preventDefault(); passo(-1); }
        if (e.key === 'ArrowRight') { e.preventDefault(); passo(1); }
    });
    // deslizar o dedo na foto: mais de 50 px para o lado, e mais de lado do que para cima
    let inicio = null;
    const moldura = janela.querySelector('.moldura');
    // sem isso, o navegador começa a arrastar a imagem e cancela o gesto
    imagem.draggable = false;
    moldura.addEventListener('dragstart', e => e.preventDefault());
    moldura.addEventListener('pointerdown', e => { inicio = { x: e.clientX, y: e.clientY }; });
    moldura.addEventListener('pointerup', e => {
        if (!inicio) return;
        const dx = e.clientX - inicio.x, dy = e.clientY - inicio.y;
        inicio = null;
        if (Math.abs(dx) > 50 && Math.abs(dx) > Math.abs(dy)) passo(dx < 0 ? 1 : -1);
    });
    moldura.addEventListener('pointercancel', () => { inicio = null; });
    janela.querySelector('.fechar').addEventListener('click', () => janela.close());
    janela.addEventListener('click', e => { if (e.target === janela) janela.close(); });
}
