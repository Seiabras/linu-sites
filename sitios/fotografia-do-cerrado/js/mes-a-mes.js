// O Cerrado mês a mês (1/11/2026): a pessoa escolhe o mês e vê só o que acontece nele. Sem JavaScript, a página mostra
// tudo, cada coisa com a sua época escrita. Os meses saem do Intl; a cor de baixo do botão é a estação, como nas Expedições.
(() => {
    const caixa = document.querySelector('.mes-escolha .meses');
    if (!caixa) return;
    const eventos = [...document.querySelectorAll('.evento[data-meses]')];
    const grupos = [...document.querySelectorAll('.mes-grupo')];
    const titulo = document.querySelector('.mes-titulo');
    const vazio = document.querySelector('.mes-vazio');
    const estacao = (m) => (m >= 5 && m <= 7 ? 'seca' : m === 8 || m === 9 ? 'auge' : 'chuvas');
    const nomeEstacao = { chuvas: 'época das chuvas', seca: 'começo da seca', auge: 'auge da seca' };
    const curto = new Intl.DateTimeFormat('pt-BR', { month: 'short' });
    const longo = new Intl.DateTimeFormat('pt-BR', { month: 'long' });
    const botoes = Array.from({ length: 12 }, (_, i) => {
        const data = new Date(2026, i, 15);
        const b = document.createElement('button');
        b.type = 'button';
        const c = curto.format(data).replace(/\.$/, ''), l = longo.format(data);
        // mostra "jan" e se chama "janeiro": o resto da palavra só para o leitor de tela
        b.append(c, Object.assign(document.createElement('span'), { className: 'so-leitor', textContent: l.slice(c.length) }));
        b.dataset.estacao = estacao(i + 1);
        b.setAttribute('aria-pressed', 'false');
        b.addEventListener('click', () => escolher(i + 1, true));
        caixa.append(b);
        return b;
    });
    function escolher(mes, daPessoa) {
        botoes.forEach((b, i) => b.setAttribute('aria-pressed', String(i + 1 === mes)));
        let n = 0;
        for (const ev of eventos) {
            const dentro = ev.dataset.meses.split(' ').map(Number).includes(mes);
            ev.hidden = !dentro;
            if (dentro) n++;
        }
        grupos.forEach((g) => { g.hidden = !g.querySelector('.evento:not([hidden])'); });
        const nome = longo.format(new Date(2026, mes - 1, 15));
        titulo.textContent = `${nome.charAt(0).toUpperCase()}${nome.slice(1)}, ${nomeEstacao[estacao(mes)]}: ${n} ${n === 1 ? 'coisa' : 'coisas'} para ver.`;
        vazio.hidden = n > 0;
        // o mês escolhido vai para o endereço só quando a pessoa escolhe (gravar ao abrir faria o navegador rolar)
        if (daPessoa) history.replaceState(null, '', '?mes=' + mes);
    }
    document.querySelector('.mes-escolha').hidden = false;
    const doEndereco = Number(new URLSearchParams(location.search).get('mes'));
    const mes = doEndereco >= 1 && doEndereco <= 12 ? doEndereco : new Date().getMonth() + 1;
    escolher(mes, false);
    // no celular, o mês escolhido aparece na faixa sem rolar a página
    const atual = botoes[mes - 1];
    caixa.scrollLeft = Math.max(0, atual.offsetLeft - caixa.offsetLeft - 8);
})();
