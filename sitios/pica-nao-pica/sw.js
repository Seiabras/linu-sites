// O guia sem internet (1/11/2026). Gerado pelo guia-pt.py do Pica ou Não Pica? (copiado do Guia do Cerrado): não edite à mão.
// Uma cache só, com a versão no nome; quando o guia muda, a versão muda e as caches antigas são apagadas.
// Páginas: primeiro a rede, e a cópia guardada se não houver sinal. Arquivos (CSS, JS, fontes, fotos): a cópia guardada.
const VERSAO = 'pica-0cfe420173';
const BASE = ["./", "index.html", "emergencia.html", "socorro.html", "cartao.html", "soro.html", "identificar.html", "bichos.html", "manifest.webmanifest", "css/estilo.css?v=11", "img/icone-192.png", "img/icone-512.png", "img/icone.svg", "js/guia.js?v=6", "js/offline.js?v=2", "js/percurso.js?v=3", "js/tema-inicio.js?v=2", "js/tema.js?v=2", "js/teste.js?v=3"];
const TUDO = ["./", "achei-um-ninho.html", "achei.html", "aprender.html", "bicho-abelha-africanizada.html", "bicho-abelha-sem-ferrao.html", "bicho-agua-viva.html", "bicho-anfisbena.html", "bicho-aranha-de-grama.html", "bicho-aranha-marrom.html", "bicho-armadeira.html", "bicho-arraia.html", "bicho-barbeiro.html", "bicho-caninana.html", "bicho-caramujo-africano.html", "bicho-caranguejeira.html", "bicho-carrapato.html", "bicho-cascavel.html", "bicho-cobra-cipo.html", "bicho-coral.html", "bicho-escorpiao-amarelo.html", "bicho-escorpiao-marrom.html", "bicho-escorpiao-preto.html", "bicho-falsa-coral.html", "bicho-jararaca.html", "bicho-jararacucu.html", "bicho-jiboia.html", "bicho-lacraia.html", "bicho-lagarta-urticante.html", "bicho-lagartixa.html", "bicho-lava-pes.html", "bicho-opiliao.html", "bicho-ourico.html", "bicho-poto.html", "bicho-sapo-cururu.html", "bicho-sucuri.html", "bicho-surucucu.html", "bicho-taturana.html", "bicho-tocandira.html", "bicho-vespa.html", "bicho-viuva-negra.html", "bichos.html", "cartao.html", "creditos.html", "criar.html", "css/estilo.css?v=11", "descobrir.html", "diferencas.html", "emergencia.html", "escola.html", "fontes.html", "identificar.html", "img/bichos/abelha-africanizada-240.webp", "img/bichos/abelha-africanizada-640.webp", "img/bichos/abelha-africanizada.webp", "img/bichos/abelha-sem-ferrao-240.webp", "img/bichos/abelha-sem-ferrao-640.webp", "img/bichos/abelha-sem-ferrao.webp", "img/bichos/agua-viva-240.webp", "img/bichos/agua-viva-640.webp", "img/bichos/agua-viva.webp", "img/bichos/anfisbena-240.webp", "img/bichos/anfisbena-640.webp", "img/bichos/anfisbena.webp", "img/bichos/aranha-de-grama-240.webp", "img/bichos/aranha-de-grama-640.webp", "img/bichos/aranha-de-grama.webp", "img/bichos/aranha-marrom-240.webp", "img/bichos/aranha-marrom-640.webp", "img/bichos/aranha-marrom.webp", "img/bichos/armadeira-240.webp", "img/bichos/armadeira-640.webp", "img/bichos/armadeira.webp", "img/bichos/arraia-240.webp", "img/bichos/arraia-640.webp", "img/bichos/arraia.webp", "img/bichos/barbeiro-240.webp", "img/bichos/barbeiro-640.webp", "img/bichos/barbeiro.webp", "img/bichos/caninana-240.webp", "img/bichos/caninana-640.webp", "img/bichos/caninana.webp", "img/bichos/caramujo-africano-240.webp", "img/bichos/caramujo-africano-640.webp", "img/bichos/caramujo-africano.webp", "img/bichos/caranguejeira-240.webp", "img/bichos/caranguejeira-640.webp", "img/bichos/caranguejeira.webp", "img/bichos/carrapato-240.webp", "img/bichos/carrapato-640.webp", "img/bichos/carrapato.webp", "img/bichos/cascavel-240.webp", "img/bichos/cascavel-640.webp", "img/bichos/cascavel.webp", "img/bichos/cobra-cipo-240.webp", "img/bichos/cobra-cipo-640.webp", "img/bichos/cobra-cipo.webp", "img/bichos/coral-240.webp", "img/bichos/coral-640.webp", "img/bichos/coral.webp", "img/bichos/escorpiao-amarelo-240.webp", "img/bichos/escorpiao-amarelo-640.webp", "img/bichos/escorpiao-amarelo.webp", "img/bichos/escorpiao-marrom-240.webp", "img/bichos/escorpiao-marrom-640.webp", "img/bichos/escorpiao-marrom.webp", "img/bichos/escorpiao-preto-240.webp", "img/bichos/escorpiao-preto-640.webp", "img/bichos/escorpiao-preto.webp", "img/bichos/falsa-coral-240.webp", "img/bichos/falsa-coral-640.webp", "img/bichos/falsa-coral.webp", "img/bichos/jararaca-240.webp", "img/bichos/jararaca-640.webp", "img/bichos/jararaca.webp", "img/bichos/jararacucu-240.webp", "img/bichos/jararacucu-640.webp", "img/bichos/jararacucu.webp", "img/bichos/jiboia-240.webp", "img/bichos/jiboia-640.webp", "img/bichos/jiboia.webp", "img/bichos/lacraia-240.webp", "img/bichos/lacraia-640.webp", "img/bichos/lacraia.webp", "img/bichos/lagarta-urticante-240.webp", "img/bichos/lagarta-urticante-640.webp", "img/bichos/lagarta-urticante.webp", "img/bichos/lagartixa-240.webp", "img/bichos/lagartixa-640.webp", "img/bichos/lagartixa.webp", "img/bichos/lava-pes-240.webp", "img/bichos/lava-pes-640.webp", "img/bichos/lava-pes.webp", "img/bichos/opiliao-240.webp", "img/bichos/opiliao-640.webp", "img/bichos/opiliao.webp", "img/bichos/ourico-240.webp", "img/bichos/ourico-640.webp", "img/bichos/ourico.webp", "img/bichos/poto-240.webp", "img/bichos/poto-640.webp", "img/bichos/poto.webp", "img/bichos/sapo-cururu-240.webp", "img/bichos/sapo-cururu-640.webp", "img/bichos/sapo-cururu.webp", "img/bichos/sucuri-240.webp", "img/bichos/sucuri-640.webp", "img/bichos/sucuri.webp", "img/bichos/surucucu-240.webp", "img/bichos/surucucu-640.webp", "img/bichos/surucucu.webp", "img/bichos/taturana-240.webp", "img/bichos/taturana-640.webp", "img/bichos/taturana.webp", "img/bichos/tocandira-240.webp", "img/bichos/tocandira-640.webp", "img/bichos/tocandira.webp", "img/bichos/vespa-240.webp", "img/bichos/vespa-640.webp", "img/bichos/vespa.webp", "img/bichos/viuva-negra-240.webp", "img/bichos/viuva-negra-640.webp", "img/bichos/viuva-negra.webp", "img/icone-192.png", "img/icone-512.png", "img/icone.svg", "img/jatai.jpg", "img/mandacaia.jpg", "img/ninho-jatai.jpg", "img/ninho-urucu.jpg", "index.html", "jogo.html", "js/guia.js?v=6", "js/offline.js?v=2", "js/percurso.js?v=3", "js/tema-inicio.js?v=2", "js/tema.js?v=2", "js/teste.js?v=3", "manifest.webmanifest", "mitos.html", "numeros.html", "origem.html", "prevenir.html", "socorro.html", "soro.html", "teste.html"];
const LIMITE = 634; // nunca mais que isso na cache (o guia inteiro tem 534 endereços; com as fotos das espécies passou de 400)
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
