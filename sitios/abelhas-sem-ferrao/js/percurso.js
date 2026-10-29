// Percurso "Descobrir em 3 minutos": mostra uma tela por vez e atualiza a barra de progresso.
const telas = [...document.querySelectorAll('.tela')];
const marcas = [...document.querySelectorAll('.progresso span')];
const contador = document.getElementById('contador');
const voltar = document.getElementById('voltar');
const avancar = document.getElementById('avancar');
let atual = 0;

function mostrar(n, focar = true) {
    atual = n;
    telas.forEach((t, i) => { t.hidden = i !== n; });
    marcas.forEach((m, i) => m.classList.toggle('feito', i <= n));
    contador.textContent = `Tela ${n + 1} de ${telas.length}`;
    voltar.disabled = n === 0;
    const ultima = n === telas.length - 1;
    avancar.textContent = ultima ? 'Fazer o teste rápido →' : 'Próxima →';
    if (focar) telas[n].querySelector('h2').focus();
}

voltar.addEventListener('click', () => mostrar(Math.max(0, atual - 1)));
avancar.addEventListener('click', () => {
    if (atual === telas.length - 1) { location.href = 'teste.html'; return; }
    mostrar(atual + 1);
});
mostrar(0, false);
