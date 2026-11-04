// Percurso "Descobrir em 3 minutos": mostra uma tela por vez e atualiza a barra de progresso.
const telas = [...document.querySelectorAll('.tela')];
const marcas = [...document.querySelectorAll('.progresso span')];
const contador = document.getElementById('contador');
const voltar = document.getElementById('voltar');
const avancar = document.getElementById('avancar');
let atual = 0;
// os textos no idioma da página (o bloco #textos-estudo); sem ele, em português
const bloco = document.getElementById('textos-estudo');
const T = Object.assign({ tela: 'Tela {n} de {total}', proxima: 'Próxima →', ir_teste: 'Fazer o teste rápido →' },
    bloco ? JSON.parse(bloco.textContent) : {});

function mostrar(n, focar = true) {
    atual = n;
    telas.forEach((t, i) => { t.hidden = i !== n; });
    marcas.forEach((m, i) => m.classList.toggle('feito', i <= n));
    contador.textContent = T.tela.replace('{n}', n + 1).replace('{total}', telas.length);
    voltar.disabled = n === 0;
    const ultima = n === telas.length - 1;
    avancar.textContent = ultima ? T.ir_teste : T.proxima;
    if (focar) telas[n].querySelector('h2').focus();
}

voltar.addEventListener('click', () => mostrar(Math.max(0, atual - 1)));
avancar.addEventListener('click', () => {
    if (atual === telas.length - 1) { location.href = 'teste.html'; return; }
    mostrar(atual + 1);
});
mostrar(0, false);
