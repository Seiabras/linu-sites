/* Identidade visual (6/11/2026): tocar numa cor copia o código. O mesmo do bloco 8 do js/digital.js do Digital Linu. */
(function () {
  "use strict";
  var copiado = document.querySelector("[data-copiado]");
  if (!copiado) return;
  var limparAviso;
  document.querySelectorAll("[data-copiar]").forEach(function (b) {
    b.addEventListener("click", function () {
      var codigo = b.dataset.copiar;
      function avisar(ok) {
        copiado.textContent = ok ? codigo + " copiado." : "Copie à mão: " + codigo;
        clearTimeout(limparAviso);
        limparAviso = setTimeout(function () { copiado.textContent = ""; }, 2500);
      }
      if (navigator.clipboard) navigator.clipboard.writeText(codigo).then(function () { avisar(true); }, function () { avisar(false); });
      else avisar(false);
    });
  });
})();
