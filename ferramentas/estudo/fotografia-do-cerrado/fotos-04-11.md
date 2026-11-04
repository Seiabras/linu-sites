# Fotos do Guia do Cerrado: 04/11/2026

Todas as fotos vêm do Wikimedia Commons, com licença CC0, domínio público, CC BY ou CC BY-SA. Autor e licença foram lidos pela API (`extmetadata`). Cada foto foi conferida a olho em folhas de contato e depois já recortada.

## Resultado

- **Espécies:** 106 de 109 ganharam foto em `img/especies/` (`<id>.webp`, `-640`, `-144` e crédito em `creditos.json`). As outras 5 (lobo-guará, tamanduá-bandeira, arara-canindé, seriema e tucano-toco) já tinham foto própria em `img/` e não foram mexidas. No total, 111 das 114 têm foto.
- **Paisagens:** 8 de 11 ganharam foto: campo limpo, campo sujo, campo rupestre, cerrado sentido restrito, palmeiral, vereda, mata seca e mata ciliar.
- **Expedições:** os 3 parques ganharam foto de paisagem: `img/paisagens/expedicao-veadeiros`, `expedicao-emas` e `expedicao-brasilia`. O crédito delas também está em `img/paisagens/creditos.json`.
- **Tamanho adicionado:** cerca de 18,1 MB (18.056.814 bytes, contando todos os .webp de `img/especies` e `img/paisagens`).
- Todos os arquivos respeitam o limite de peso: até 150 KB no grande, 70 KB no de 640 e 12 KB no de 144. Quatro deles foram recomprimidos com `webp:target-size`.

## Ficaram sem foto

- **Sempre-viva (Comanthera elegans):** o Commons não tem foto identificada da espécie. As que existem são de outras Comanthera ou de sempre-vivas sem identificação.
- **Piranha-vermelha:** as fotos livres são de aquário, de peixe empalhado ou de peixe fisgado no anzol.
- **Capim-flecha (Tristachya leiostachya):** nenhuma foto da espécie no Commons.
- **Parque de cerrado (murundus):** não achei foto de murundus com árvores. Só há campo com cupinzeiros, que é outra coisa.
- **Cerradão:** as fotos com esse nome são de cachoeira, de solo ou de paisagem distante. Nenhuma mostra a formação com clareza.
- **Mata de galeria:** a única candidata do Brasil está na categoria "Blurred images" (foto tremida).

## Em dúvida, para conferir

- **Arnica-do-cerrado:** a identificação vem só da legenda ("Arnica do Cerrado", Serra da Canastra). A forma e as flores lilases batem com *Lychnophora*, mas a espécie *L. ericoides* não está confirmada.
- **Capim-dourado:** a foto é da comunidade Mumbuca, no Jalapão, e mostra a touceira de hastes douradas. Não tem categoria de espécie.
- **Chuveirinho:** a foto está identificada como "cf. *Paepalanthus chiquitensis*", na Chapada dos Veadeiros.
- **Pau-de-tucano:** árvores floridas vistas de longe, em Avaré (SP). A identificação vem só do nome do arquivo.
- **Morcego-beija-flor:** pendurado num prego, dentro de uma construção. É bicho livre, mas não está no ambiente natural.
- **Jabuti-piranga:** bicho livre, mas fotografado em St. Barts, no Caribe. Não há foto boa e livre do Brasil.
- **Sucuri, cachorro-vinagre e tatu-canastra:** bichos livres, mas fotografados fora do Brasil ou em armadilha fotográfica (Equador, Bolívia, câmera-trap).
- **Bacupari:** frutos colhidos e fotografados sobre uma mesa. **Pequi:** fruto na palma da mão. Os dois são planta, então a regra de "bicho na mão" não vale, mas não é a planta no pé.
- **Mamangava:** está numa quaresmeira (*Tibouchina*), que pode ser planta de jardim.
- **Expedição Emas:** pelo lugar, o veado entre os cupinzeiros deve ser um veado-campeiro, e o texto alternativo diz isso.
- **Fotos de original pequeno (cerca de 1000 px):** baru, cagaita, pau-santo, tingui, algodãozinho, caraíba, jacarandá-do-cerrado, puçá, sucupira-branca e sumaré (*Cyrtopodium eugenii*). Saíram da miniatura de 960 px do Commons, ampliada para 1000 px.

## Trocas pelo iNaturalist (04/11/2026, mais tarde)

As dúvidas acima foram resolvidas com observações do iNaturalist, com identificação “grau de pesquisa” (conferida pela
comunidade), feitas no Brasil e em CC0/CC BY/CC BY-SA (`linuarquivos/modelos/ferramentas/inaturalist.py`):

- capim-flecha: *Tristachya leiostachya*, Mineiros (GO). Mario Barroso, CC BY 4.0
- arnica: *Lychnophora ericoides* confirmada, São Roque de Minas (MG, Serra da Canastra). Thomaz Ricardo Favreto Sinani, CC BY 4.0
- chuveirinho: *Paepalanthus pulvinatus*, Bahia. Riccardo Rocca, CC BY 4.0
- pau-de-tucano: *Vochysia tucanorum* em flor, de perto, Jaboticatubas (MG). agujaceratops, CC BY 4.0
- jabuti-piranga: *Chelonoidis carbonarius*, Rio de Janeiro (RJ). filipeprates, CC0
- sucuri: *Eunectes murinus*, Presidente Figueiredo (AM). Henrique Nogueira, CC BY 4.0
- bacupari: *Salacia crassifolia* com frutos no pé, Alto Paraíso de Goiás (GO). Jonathan Lorencetti Ehlert, CC BY-SA 4.0
- tingui: *Magonia pubescens* com fruto, Alto Paraíso de Goiás (GO). Fabrício Mil Homens Riella, CC BY 4.0
- baru: *Dipteryx alata* com frutos, Campo Grande (MS). NINA WENÓLI, CC0

Ficaram como estavam: pequi, cagaita e tatu-canastra (nada melhor e livre no Brasil). A piranha continua sem foto (as
livres são todas de peixe na mão ou no anzol), e a sempre-viva e o capim-dourado também (nenhuma foto livre boa).
Correção junto: o `guia-pt.py` deixava 4 espaços a mais antes do rodapé a cada vez que rodava; agora rodar de novo não
muda nada.

## Mudanças de código

- `ferramentas/estudo/fotografia-do-cerrado/guia-pt.py`, linhas 1914–1916: a foto do topo da ficha agora fica num `<figure class="ficha-foto">` com o crédito (autor com link para a página do arquivo e licença). Antes a ficha não citava o autor.
- `guia-pt.py`, linha 2566: o `LIMITE` do service worker, que era fixo em 400, passou a ser `max(400, endereços + 100)`. Com as fotos, o guia sem internet tem 531 endereços (cerca de 20,7 MB), e o limite antigo apagaria parte da cópia guardada.
- `sitios/fotografia-do-cerrado/css/estilo.css`, linhas 734–738: novas regras `.ficha-foto` e `.expedicao-foto`, com o crédito em cima da foto, no canto.
- Versão do CSS: `estilo.css?v=25` passou para `?v=26` em todos os `modelo/*.html` e em `paginas-pt.py` (linha 252).
- `modelo/expedicoes.html`, linhas 59, 68 e 77: as fotos de bicho deram lugar às fotos de paisagem dos parques, com crédito "© autor, licença".
- `textos/*.json` (os 13 idiomas): `expedicoes_063`, `064` e `065` foram reescritos para descrever as fotos novas.
