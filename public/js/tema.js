// Tema claro/escuro. Carregado no <head>, antes de pintar a página, para não piscar.
// Sem escolha salva, segue o aparelho (prefers-color-scheme). O botão #tema troca e guarda a escolha.
(function () {
  const raiz = document.documentElement;
  try {
    const t = localStorage.getItem('linu-sites-tema');
    if (t === 'dark' || t === 'light') raiz.dataset.theme = t;
  } catch (e) { /* sem armazenamento: segue o aparelho */ }

  const escuroDoAparelho = window.matchMedia('(prefers-color-scheme: dark)');
  const atual = () => raiz.dataset.theme || (escuroDoAparelho.matches ? 'dark' : 'light');

  // A ilustração da abertura troca de dia para noite pelo <source media>; com escolha manual, a escolha manda.
  const ajustarImagens = () => {
    const t = raiz.dataset.theme;
    document.querySelectorAll('source[data-escuro]').forEach((s) => {
      s.media = t === 'dark' ? 'all' : t === 'light' ? 'not all' : '(prefers-color-scheme: dark)';
    });
  };

  window.addEventListener('DOMContentLoaded', () => {
    ajustarImagens();
    const b = document.getElementById('tema');
    if (!b) return;
    const rotular = () => {
      const escuro = atual() === 'dark';
      b.setAttribute('aria-pressed', String(escuro));
      b.setAttribute('aria-label', escuro ? 'Mudar para o modo claro' : 'Mudar para o modo escuro');
      b.title = escuro ? 'Modo claro' : 'Modo escuro';
    };
    rotular();
    b.addEventListener('click', () => {
      const novo = atual() === 'dark' ? 'light' : 'dark';
      raiz.dataset.theme = novo;
      try { localStorage.setItem('linu-sites-tema', novo); } catch (e) { /* ok */ }
      rotular();
      ajustarImagens();
    });
    escuroDoAparelho.addEventListener('change', rotular);
  });
})();
