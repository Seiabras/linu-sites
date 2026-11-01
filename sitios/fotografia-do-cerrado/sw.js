// O guia sem internet (1/11/2026). Gerado pelo guia-pt.py: não edite à mão.
// Uma cache só, com a versão no nome; quando o guia muda, a versão muda e as caches antigas são apagadas.
// Páginas: primeiro a rede, e a cópia guardada se não houver sinal. Arquivos (CSS, JS, fontes, fotos): a cópia guardada.
const VERSAO = 'cerrado-5f65add6a6';
const BASE = ["./", "index.html", "especies.html", "busca.html", "roteiro.html", "mes-a-mes.html", "onde-ver.html", "paisagens.html", "aprender.html", "bioma.html", "css/estilo.css?v=25", "fontes/newsreader-600.woff2", "img/icone-180.png", "img/icone-192.png", "img/icone-512.png", "img/icone.svg", "js/aprender.js?v=5", "js/busca.js?v=1", "js/caderno.js?v=1", "js/como-ajudar.js?v=1", "js/comparar.js?v=2", "js/contato.js?v=3", "js/contraste.js?v=1", "js/escola.js?v=1", "js/galeria.js?v=6", "js/guia.js?v=1", "js/menu.js?v=2", "js/mes-a-mes.js?v=1", "js/offline.js?v=1", "js/quando.js?v=3", "js/roteiro.js?v=2", "js/tema-inicio.js?v=3", "js/tema.js?v=2"];
const TUDO = ["./", "agua.html", "ameacas.html", "aprender.html", "bioma.html", "busca.html", "caderno.html", "como-ajudar.html", "como-fotografamos.html", "comparar.html", "contato.html", "creditos.html", "css/estilo.css?v=25", "diario.html", "escola.html", "especie-abacaxi-do-cerrado.html", "especie-algodaozinho.html", "especie-angico.html", "especie-anta.html", "especie-anu-branco.html", "especie-arara-azul-grande.html", "especie-arara-caninde.html", "especie-araticum.html", "especie-arnica.html", "especie-aroeira.html", "especie-babacu.html", "especie-bacupari.html", "especie-barbatimao.html", "especie-baru.html", "especie-beija-flor-tesoura.html", "especie-bem-te-vi.html", "especie-bugio.html", "especie-buriti.html", "especie-cachorro-do-mato.html", "especie-cachorro-vinagre.html", "especie-cagaita.html", "especie-caicaca.html", "especie-cajuzinho.html", "especie-calango.html", "especie-caliandra.html", "especie-canario-da-terra.html", "especie-canela-de-ema.html", "especie-capim-dourado.html", "especie-capim-flecha.html", "especie-capivara.html", "especie-caraiba.html", "especie-carcara.html", "especie-cascavel.html", "especie-cateto.html", "especie-chuveirinho.html", "especie-cigarra.html", "especie-copaiba.html", "especie-coral.html", "especie-coruja-buraqueira.html", "especie-cupim-de-mont\u00edculo.html", "especie-curicaca.html", "especie-cutia.html", "especie-dourado.html", "especie-ema.html", "especie-faveiro.html", "especie-gabiroba.html", "especie-gaviao-carijo.html", "especie-gralha-do-campo.html", "especie-guariroba.html", "especie-ipe-amarelo.html", "especie-ipe-roxo.html", "especie-irara.html", "especie-jabuti-piranga.html", "especie-jacaranda-do-cerrado.html", "especie-jacare-de-papo-amarelo.html", "especie-jaguatirica.html", "especie-jatai.html", "especie-jatoba.html", "especie-jenipapo.html", "especie-jiboia.html", "especie-joao-de-barro.html", "especie-lixeira.html", "especie-lobeira.html", "especie-lobo-guara.html", "especie-lontra.html", "especie-macaco-prego.html", "especie-macauba.html", "especie-mamangava.html", "especie-mangaba.html", "especie-mao-pelada.html", "especie-morcego-beija-flor.html", "especie-murici.html", "especie-onca-parda.html", "especie-onca-pintada.html", "especie-orquidea-cyrtopodium.html", "especie-paca.html", "especie-pacu.html", "especie-papagaio-galego.html", "especie-papagaio-verdadeiro.html", "especie-pato-mergulhao.html", "especie-pau-de-tucano.html", "especie-pau-santo.html", "especie-pau-terra.html", "especie-pequi.html", "especie-periquito-rei.html", "especie-pica-pau-do-campo.html", "especie-pimenta-de-macaco.html", "especie-piranha.html", "especie-puca.html", "especie-quati.html", "especie-queixada.html", "especie-ra-pimenta.html", "especie-raposa-do-campo.html", "especie-rola-bosta.html", "especie-sagui.html", "especie-sapo-cururu.html", "especie-sauva.html", "especie-sempre-viva.html", "especie-seriema.html", "especie-sucupira-branca.html", "especie-sucupira-preta.html", "especie-sucuri.html", "especie-tamandua-bandeira.html", "especie-tamandua-mirim.html", "especie-tatu-canastra.html", "especie-tatu-peba.html", "especie-teiu.html", "especie-tingui.html", "especie-tucano-toco.html", "especie-urubu-de-cabeca-preta.html", "especie-urubu-rei.html", "especie-vaga-lume-cupinzeiro.html", "especie-veado-campeiro.html", "especie-veado-catingueiro.html", "especies.html", "expedicoes.html", "fontes.html", "fontes/newsreader-600.woff2", "galeria.html", "img/abertura-seriema-ipe-640.webp", "img/abertura-seriema-ipe.webp", "img/arara-caninde-144.webp", "img/arara-caninde-640.webp", "img/arara-caninde.webp", "img/icone-180.png", "img/icone-192.png", "img/icone-512.png", "img/icone.svg", "img/lobo-guara-144.webp", "img/lobo-guara-640.webp", "img/lobo-guara.webp", "img/seriema-144.webp", "img/seriema-640.webp", "img/seriema.webp", "img/tamandua-bandeira-144.webp", "img/tamandua-bandeira-640.webp", "img/tamandua-bandeira.webp", "img/tucano-toco-144.webp", "img/tucano-toco-640.webp", "img/tucano-toco.webp", "index.html", "js/aprender.js?v=5", "js/busca.js?v=1", "js/caderno.js?v=1", "js/como-ajudar.js?v=1", "js/comparar.js?v=2", "js/contato.js?v=3", "js/contraste.js?v=1", "js/escola.js?v=1", "js/galeria.js?v=6", "js/guia.js?v=1", "js/menu.js?v=2", "js/mes-a-mes.js?v=1", "js/offline.js?v=1", "js/quando.js?v=3", "js/roteiro.js?v=2", "js/tema-inicio.js?v=3", "js/tema.js?v=2", "manifest.webmanifest", "mes-a-mes.html", "onde-ver.html", "paisagem-campo-limpo.html", "paisagem-campo-rupestre.html", "paisagem-campo-sujo.html", "paisagem-cerradao.html", "paisagem-cerrado-sentido-restrito.html", "paisagem-mata-ciliar.html", "paisagem-mata-de-galeria.html", "paisagem-mata-seca.html", "paisagem-palmeiral.html", "paisagem-parque-de-cerrado.html", "paisagem-vereda.html", "paisagens.html", "povos.html", "roteiro.html", "sobre.html"];
const LIMITE = 400; // nunca mais que isso na cache (o guia inteiro tem 191 endereços)
const MARCA = './__guardado';

self.addEventListener('install', (e) => {
    e.waitUntil(caches.open(VERSAO).then((c) => c.addAll(BASE)).then(() => self.skipWaiting()));
});
self.addEventListener('activate', (e) => {
    e.waitUntil((async () => {
        let estavaGuardado = false;
        for (const nome of await caches.keys()) {
            if (nome === VERSAO || !nome.startsWith('cerrado-')) continue;
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
