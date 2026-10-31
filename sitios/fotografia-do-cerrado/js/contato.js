// Formulário de contato: o site é estático, então a mensagem não sai daqui; a página só confirma o que foi preenchido.
//
// 31/10/2026:
// - chega preenchido pelo endereço: contato.html?expedicao=emas&mes=7 marca o assunto e o mês (o "Quero participar"
//   das Expedições e o "Quando ir?" mandam assim);
// - o erro aparece na hora, embaixo do campo, depois que a pessoa sai dele (a frase é a do próprio navegador, no idioma
//   dele), e some assim que o campo fica certo;
// - na página em português, o quadro "Sua saída" mostra a duração, o grupo e a melhor época da expedição escolhida, e
//   avisa quando o mês está fora dela.
const form = document.querySelector('form.contato');
const aviso = document.getElementById('aviso');
if (form) {
    const bloco = document.getElementById('textos-estudo');
    const T = bloco ? JSON.parse(bloco.textContent) : {};
    const campos = [...form.querySelectorAll('input[required], textarea[required]')];

    // o erro de cada campo, num parágrafo ligado a ele
    const erroDe = (campo) => {
        let p = document.getElementById('erro-' + campo.id);
        if (!p) {
            p = document.createElement('p');
            p.className = 'erro';
            p.id = 'erro-' + campo.id;
            p.hidden = true;
            campo.after(p);
            campo.setAttribute('aria-describedby', p.id);
        }
        return p;
    };
    const conferir = (campo) => {
        const p = erroDe(campo);
        const certo = campo.checkValidity();
        campo.setAttribute('aria-invalid', String(!certo));
        p.textContent = certo ? '' : campo.validationMessage;
        p.hidden = certo;
        return certo;
    };
    for (const campo of campos) {
        // só reclama depois que a pessoa passou pelo campo; daí em diante, o erro some assim que fica certo
        campo.addEventListener('blur', () => { if (campo.value.trim() || campo.dataset.tocado) conferir(campo); campo.dataset.tocado = '1'; });
        campo.addEventListener('input', () => { if (campo.getAttribute('aria-invalid') === 'true') conferir(campo); });
    }

    // chega preenchido pelo endereço
    const params = new URLSearchParams(location.search);
    const assunto = form.assunto;
    const mes = form.mes;
    if ([...assunto.options].some((o) => o.value === params.get('expedicao'))) assunto.value = params.get('expedicao');
    if (mes && /^([1-9]|1[0-2])$/.test(params.get('mes') || '')) mes.value = params.get('mes');

    // o quadro "Sua saída" (só na página em português)
    const dadosBloco = document.getElementById('expedicoes-dados');
    const corpo = document.querySelector('.resumo-corpo');
    if (dadosBloco && corpo) {
        const dados = JSON.parse(dadosBloco.textContent);
        const inicial = [...corpo.childNodes].map((n) => n.cloneNode(true));
        const nomeMes = (m) => {
            const n = new Intl.DateTimeFormat('pt-BR', { month: 'long' }).format(new Date(2026, m - 1, 15));
            return n.charAt(0).toUpperCase() + n.slice(1);
        };
        const resumir = () => {
            const d = dados[assunto.value];
            if (!d) { corpo.replaceChildren(...inicial.map((n) => n.cloneNode(true))); return; }
            const m = Number(mes?.value || 0);
            const dl = document.createElement('dl');
            for (const [k, v] of [['Expedição', d.nome], ['Duração', d.dias], ['Grupo', 'até 8 pessoas, com guia local'], ['Melhor época', d.epoca]]) {
                dl.append(Object.assign(document.createElement('dt'), { textContent: k }), Object.assign(document.createElement('dd'), { textContent: v }));
            }
            const nota = document.createElement('p');
            nota.className = 'resumo-nota';
            if (!m) nota.textContent = 'Escolha o mês, se já souber, para conferir se é uma boa época.';
            else if (d.meses.includes(m)) { nota.textContent = `${nomeMes(m)} está na melhor época desta saída.`; nota.classList.add('boa'); }
            else nota.textContent = `${nomeMes(m)} fica fora da melhor época (${d.epoca}). A saída acontece, mas os bichos aparecem menos.`;
            corpo.replaceChildren(dl, nota);
        };
        assunto.addEventListener('change', resumir);
        mes?.addEventListener('change', resumir);
        resumir();
    }

    form.addEventListener('submit', e => {
        e.preventDefault();
        const errados = campos.filter((c) => !conferir(c));
        if (errados.length) { errados[0].focus(); return; }
        const nome = form.nome.value.trim().split(' ')[0];
        aviso.hidden = false;
        // a frase vem no idioma da página (o bloco #textos-estudo, do ferramentas/gerar-estudo.mjs); sem ele, em português
        aviso.textContent = (T.obrigado || 'Obrigado, {nome}! Esta é uma página de demonstração: a mensagem não foi enviada de verdade.').replace('{nome}', nome);
        form.reset();
        for (const c of campos) { c.removeAttribute('aria-invalid'); delete c.dataset.tocado; erroDe(c).hidden = true; }
        assunto.dispatchEvent(new Event('change'));
        aviso.focus();
    });
}
