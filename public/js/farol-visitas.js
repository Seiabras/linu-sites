/* Cópia do linu-farol/v.js (11/11/2026): mudou lá, muda aqui. O contador de visitas do Linu Farol, sem cookie (https://farol.linupedia.com.br). Avisa que uma página foi aberta:
   o caminho, o site de onde veio (só o nome) e o utm_source (ou o ?origem= dos links da família), se houver. Nada fica no navegador de quem visita, e quem
   pediu para não ser rastreado (Do Not Track ou Global Privacy Control) não é contado. */
(function () {
  var n = navigator, alvo = "https://farol.linupedia.com.br/api/visita";
  if (n.webdriver || n.doNotTrack === "1" || n.globalPrivacyControl || location.protocol !== "https:") return;
  function avisar() {
    var r = "", u = "";
    try { if (document.referrer) r = new URL(document.referrer).hostname; } catch (e) {}
    try { var q = new URLSearchParams(location.search); u = q.get("utm_source") || q.get("origem") || ""; } catch (e) {}
    var d = JSON.stringify({ p: location.pathname, r: r, u: u.slice(0, 40) });
    if (n.sendBeacon && n.sendBeacon(alvo, d)) return;
    try { fetch(alvo, { method: "POST", body: d, keepalive: true, mode: "no-cors", credentials: "omit" }); } catch (e) {}
  }
  if (document.prerendering) document.addEventListener("prerenderingchange", avisar, { once: true });
  else avisar();
})();
