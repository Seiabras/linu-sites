// Teste as cores (página Sobre, 31/10/2026): a pessoa escolhe a cor do texto e a do fundo entre as da paleta e vê a razão
// de contraste pela fórmula da WCAG 2.2 e se o par passa no AA e no AAA, para texto normal e grande.
(() => {
    const previa = document.getElementById('previa');
    if (!previa) return;
    const razaoEl = document.getElementById('razao');
    const veredito = document.getElementById('veredito');
    const escolhido = (nome) => document.querySelector(`input[name="${nome}"]:checked`);

    // luminância relativa de uma cor #RRGGBB (WCAG 2.2)
    const luminancia = (hex) => {
        const [r, g, b] = [1, 3, 5].map((i) => parseInt(hex.slice(i, i + 2), 16) / 255)
            .map((c) => (c <= 0.04045 ? c / 12.92 : ((c + 0.055) / 1.055) ** 2.4));
        return 0.2126 * r + 0.7152 * g + 0.0722 * b;
    };
    const contraste = (a, b) => {
        const [l1, l2] = [luminancia(a), luminancia(b)].sort((x, y) => y - x);
        return (l1 + 0.05) / (l2 + 0.05);
    };

    function atualizar() {
        const texto = escolhido('texto').value;
        const fundo = escolhido('fundo').value;
        previa.style.color = texto;
        previa.style.backgroundColor = fundo;
        const r = contraste(texto, fundo);
        // mostra com duas casas, como a paleta do Sobre; o "passa ou não passa" usa o valor exato
        const mostrado = Math.round(r * 100) / 100;
        razaoEl.textContent = `${mostrado.toLocaleString('pt-BR', { minimumFractionDigits: 2 })}:1`;
        const testes = [
            ['Texto normal, nível AA', 4.5], ['Texto normal, nível AAA', 7],
            ['Texto grande (24 px, ou 19 px em negrito), nível AA', 3], ['Texto grande, nível AAA', 4.5],
        ];
        veredito.replaceChildren(...testes.map(([nome, minimo]) => {
            const li = document.createElement('li');
            const passa = r >= minimo;
            li.className = passa ? 'passa' : 'nao-passa';
            li.textContent = `${passa ? 'Passa' : 'Não passa'}: ${nome} (mínimo ${String(minimo).replace('.', ',')}:1)`;
            return li;
        }));
    }

    document.querySelectorAll('.testador input[type="radio"]').forEach((i) => i.addEventListener('change', atualizar));
    document.getElementById('trocar-cores').addEventListener('click', () => {
        const t = escolhido('texto').value, f = escolhido('fundo').value;
        document.querySelector(`input[name="texto"][value="${f}"]`).checked = true;
        document.querySelector(`input[name="fundo"][value="${t}"]`).checked = true;
        atualizar();
    });
    atualizar();
})();
