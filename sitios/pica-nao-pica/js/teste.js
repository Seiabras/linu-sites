// Teste rápido: cinco perguntas, uma por vez, com a resposta certa ou errada na hora e a nota no fim.
// Os textos vêm no idioma da página (o bloco #textos-estudo, do ferramentas/gerar-estudo.mjs do linu-sites, com as
// chaves js de cada textos/<código>.json). {n} e {total} são trocados pelos números.
const bloco = document.getElementById('textos-estudo');
const T = bloco ? JSON.parse(bloco.textContent) : {};
const PERGUNTAS = T.perguntas;
const numeros = (s, n) => s.replace('{n}', n).replace('{total}', PERGUNTAS.length);

const area = document.getElementById('teste');
let atual = 0, acertos = 0;

function mostrar(focar = true) {
    const q = PERGUNTAS[atual];
    area.innerHTML = `
        <p id="contador">${numeros(T.contador, atual + 1)}</p>
        <div class="progresso" aria-hidden="true">${PERGUNTAS.map((_, i) => `<span class="${i <= atual ? 'feito' : ''}"></span>`).join('')}</div>
        <h1 tabindex="-1">${q.p}</h1>
        <div class="opcoes">${q.o.map((t, i) => `<button type="button" data-i="${i}">${t}</button>`).join('')}</div>
        <div class="retorno" role="status" hidden></div>
        <div class="acoes"><span></span><button class="botao" type="button" id="seguir" hidden>${T.proxima}</button></div>`;
    if (focar) area.querySelector('h1').focus();
    area.querySelectorAll('.opcoes button').forEach(b => b.addEventListener('click', () => responder(Number(b.dataset.i))));
}

function responder(i) {
    const q = PERGUNTAS[atual];
    const botoes = [...area.querySelectorAll('.opcoes button')];
    botoes.forEach(b => { b.disabled = true; });
    botoes[q.c].classList.add('certa');
    const certo = i === q.c;
    if (certo) acertos++; else botoes[i].classList.add('errada');
    const retorno = area.querySelector('.retorno');
    retorno.hidden = false;
    retorno.className = `retorno ${certo ? 'certo' : 'errado'}`;
    retorno.textContent = `${certo ? T.certo : T.nao_e} ${q.e}`;
    const seguir = document.getElementById('seguir');
    seguir.hidden = false;
    seguir.textContent = atual === PERGUNTAS.length - 1 ? T.ver_resultado : T.proxima;
    seguir.addEventListener('click', () => { atual++; atual < PERGUNTAS.length ? mostrar() : fim(); });
    seguir.focus();
}

function fim() {
    const frase = acertos === PERGUNTAS.length ? T.frase_todas : acertos >= 3 ? T.frase_boa : T.frase_fraca;
    area.innerHTML = `
        <h1 tabindex="-1">${numeros(T.resultado, acertos)}</h1>
        <p class="abre">${frase}</p>
        <div class="acoes"><a class="botao contorno" href="descobrir.html">${T.fazer_percurso}</a>
        <button class="botao" type="button" id="denovo">${T.tentar}</button></div>`;
    area.querySelector('h1').focus();
    document.getElementById('denovo').addEventListener('click', () => { atual = 0; acertos = 0; mostrar(); });
}

mostrar(false);
