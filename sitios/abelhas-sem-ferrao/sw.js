// O guia sem internet (1/11/2026). Gerado pelo guia-pt.py do Pica ou Não Pica? (copiado do Guia do Cerrado): não edite à mão.
// Uma cache só, com a versão no nome; quando o guia muda, a versão muda e as caches antigas são apagadas.
// Páginas: primeiro a rede, e a cópia guardada se não houver sinal. Arquivos (CSS, JS, fontes, fotos): a cópia guardada.
const VERSAO = 'pica-bbdb1838b4';
const BASE = ["./", "index.html", "emergencia.html", "socorro.html", "cartao.html", "soro.html", "identificar.html", "bichos.html", "manifest.webmanifest", "css/estilo.css?v=7", "img/icone-192.png", "img/icone-512.png", "img/icone.svg", "js/guia.js?v=2", "js/offline.js?v=1", "js/percurso.js?v=2", "js/tema-inicio.js?v=2", "js/tema.js?v=2", "js/teste.js?v=2"];
const TUDO = ["./", "achei-um-ninho.html", "aprender.html", "bicho-abelha-africanizada.html", "bicho-abelha-sem-ferrao.html", "bicho-agua-viva.html", "bicho-aranha-marrom.html", "bicho-armadeira.html", "bicho-arraia.html", "bicho-caranguejeira.html", "bicho-cascavel.html", "bicho-coral.html", "bicho-escorpiao-amarelo.html", "bicho-escorpiao-marrom.html", "bicho-falsa-coral.html", "bicho-jararaca.html", "bicho-jiboia.html", "bicho-lacraia.html", "bicho-lagarta-urticante.html", "bicho-lagartixa.html", "bicho-lava-pes.html", "bicho-opiliao.html", "bicho-poto.html", "bicho-sapo-cururu.html", "bicho-sucuri.html", "bicho-surucucu.html", "bicho-taturana.html", "bicho-tocandira.html", "bicho-vespa.html", "bicho-viuva-negra.html", "bichos.html", "cartao.html", "creditos.html", "criar.html", "css/estilo.css?v=7", "descobrir.html", "diferencas.html", "emergencia.html", "escola.html", "fontes.html", "identificar.html", "img/icone-192.png", "img/icone-512.png", "img/icone.svg", "img/jatai.jpg", "img/mandacaia.jpg", "img/ninho-jatai.jpg", "img/ninho-urucu.jpg", "index.html", "jogo.html", "js/guia.js?v=2", "js/offline.js?v=1", "js/percurso.js?v=2", "js/tema-inicio.js?v=2", "js/tema.js?v=2", "js/teste.js?v=2", "manifest.webmanifest", "mitos.html", "numeros.html", "prevenir.html", "socorro.html", "soro.html", "teste.html"];
const LIMITE = 400; // nunca mais que isso na cache (o guia inteiro tem 189 endereços)
const MARCA = './__guardado';

self.addEventListener('install', (e) => {
    e.waitUntil(caches.open(VERSAO).then((c) => c.addAll(BASE)).then(() => self.skipWaiting()));
});
self.addEventListener('activate', (e) => {
    e.waitUntil((async () => {
        let estavaGuardado = false;
        for (const nome of await caches.keys()) {
            if (nome === VERSAO || !nome.startsWith('pica-')) continue;
            if (await (await caches.open(nome)).match(MARCA)) estavaGuardado = true;
            await caches.delete(nome);
        }
        await self.clients.claim();
        // quem tinha guardado o guia inteiro continua com ele inteiro na versão nova
        if (estavaGuardado) await guardarTudo(() => {});
    })());
});
async function aparar(cache) {
    const chaves = await cache.keys();
    for (let i = 0; i < chaves.length - LIMITE; i++) await cache.delete(chaves[i]);
}
async function guardarTudo(avisar) {
    const cache = await caches.open(VERSAO);
    let feito = 0;
    for (const u of TUDO) {
        try { if (!(await cache.match(u))) await cache.add(u); } catch { /* segue com o resto */ }
        avisar(++feito, TUDO.length);
    }
    await cache.put(MARCA, new Response('sim'));
}
self.addEventListener('message', (e) => {
    const responder = (dados) => e.source && e.source.postMessage(dados);
    if (e.data === 'estado') e.waitUntil(caches.open(VERSAO).then((c) => c.match(MARCA)).then((m) => responder({ tipo: 'estado', guardado: !!m, total: TUDO.length })));
    if (e.data === 'guardar') e.waitUntil(guardarTudo((feito, total) => responder({ tipo: 'progresso', feito, total })).then(() => responder({ tipo: 'pronto' })));
});
self.addEventListener('fetch', (e) => {
    const req = e.request;
    if (req.method !== 'GET' || new URL(req.url).origin !== location.origin) return;
    if (req.mode === 'navigate') {
        e.respondWith((async () => {
            const cache = await caches.open(VERSAO);
            try {
                const resp = await fetch(req);
                if (resp.ok) { cache.put(req, resp.clone()).then(() => aparar(cache)); }
                return resp;
            } catch {
                return (await cache.match(req, { ignoreSearch: true })) || (await cache.match('index.html')) || Response.error();
            }
        })());
        return;
    }
    e.respondWith((async () => {
        const cache = await caches.open(VERSAO);
        const guardado = await cache.match(req);
        if (guardado) return guardado;
        const resp = await fetch(req);
        if (resp.ok) cache.put(req, resp.clone()).then(() => aparar(cache));
        return resp;
    })());
});
