// Para a escola (1/11/2026): o botão "Imprimir tudo". Sem JavaScript, o botão fica escondido e o Ctrl+P do navegador basta.
(() => {
    document.querySelectorAll('.imprimir').forEach((b) => { b.hidden = false; b.addEventListener('click', () => print()); });
})();
