// Quando ir? (31/10/2026): a pessoa escolhe o mês e vê a estação do cerrado e quais expedições estão na melhor época.
// Os meses saem do Intl, no idioma da página; as frases vêm do <script id="textos-estudo">. Sem JavaScript, o painel
// fica escondido e cada expedição continua dizendo a sua melhor época.
(() => {
    const painel = document.querySelector('.quando');
    const caixa = document.querySelector('.meses');
    if (!painel || !caixa) return;
    let t = {};
    try { t = JSON.parse(document.getElementById('textos-estudo').textContent); } catch { /* fica sem as frases */ }
    if (!t.est_chuvas) return;

    // outubro a abril, chuvas; maio a julho, começo da seca; agosto e setembro, o auge da seca
    const estacao = (m) => (m >= 5 && m <= 7 ? 'seca' : m === 8 || m === 9 ? 'auge' : 'chuvas');
    const lang = document.documentElement.lang || 'pt-BR';
    const curto = new Intl.DateTimeFormat(lang, { month: 'short' });
    const longo = new Intl.DateTimeFormat(lang, { month: 'long' });
    const nome = document.querySelector('.estacao-nome');
    const nota = document.querySelector('.estacao-nota');
    const lista = document.querySelector('.expedicoes');
    const expedicoes = [...document.querySelectorAll('.expedicao[data-meses]')];

    const botoes = Array.from({ length: 12 }, (_, i) => {
        const data = new Date(2026, i, 15);
        const b = document.createElement('button');
        b.type = 'button';
        b.textContent = curto.format(data).replace(/\.$/, '');
        b.setAttribute('aria-label', longo.format(data));
        b.dataset.mes = String(i + 1);
        b.dataset.estacao = estacao(i + 1);
        b.setAttribute('aria-pressed', 'false');
        b.addEventListener('click', () => escolher(i + 1));
        caixa.append(b);
        return b;
    });

    function escolher(mes) {
        botoes.forEach((b) => b.setAttribute('aria-pressed', String(Number(b.dataset.mes) === mes)));
        const e = estacao(mes);
        const m = longo.format(new Date(2026, mes - 1, 15));
        nome.textContent = `${m.charAt(0).toLocaleUpperCase(lang)}${m.slice(1)} · ${t['est_' + e]}`;
        nota.textContent = t['nota_' + e];
        lista.classList.add('escolhido');
        for (const exp of expedicoes) {
            const dentro = exp.dataset.meses.split(' ').map(Number).includes(mes);
            exp.classList.toggle('na-epoca', dentro);
            let selo = exp.querySelector('.selo-epoca');
            if (dentro && !selo) {
                selo = document.createElement('span');
                selo.className = 'selo-epoca';
                selo.textContent = t.boa_epoca;
                exp.querySelector('.texto').prepend(selo);
            } else if (!dentro && selo) selo.remove();
        }
    }

    painel.hidden = false;
    const agora = new Date().getMonth() + 1;
    escolher(agora);
    // no celular, o mês de agora aparece na faixa sem rolar a página
    const atual = botoes[agora - 1];
    caixa.scrollLeft = Math.max(0, atual.offsetLeft - caixa.offsetLeft - 8);
})();
