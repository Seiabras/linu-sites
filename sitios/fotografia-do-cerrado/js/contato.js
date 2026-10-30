// Formulário de contato: o site é estático, então a mensagem não sai daqui; a página só confirma o que foi preenchido.
const form = document.querySelector('form.contato');
const aviso = document.getElementById('aviso');
if (form) {
    form.addEventListener('submit', e => {
        e.preventDefault();
        if (!form.checkValidity()) { form.reportValidity(); return; }
        const nome = form.nome.value.trim().split(' ')[0];
        aviso.hidden = false;
        // a frase vem no idioma da página (o bloco #textos-estudo, do ferramentas/gerar-estudo.mjs); sem ele, em português
        const bloco = document.getElementById('textos-estudo');
        const T = bloco ? JSON.parse(bloco.textContent) : {};
        aviso.textContent = (T.obrigado || 'Obrigado, {nome}! Esta é uma página de demonstração: a mensagem não foi enviada de verdade.').replace('{nome}', nome);
        form.reset();
        aviso.focus();
    });
}
