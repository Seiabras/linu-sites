# Sessão “Linu-sites modo escuro”

- **Sessão:** `session_01A968Mb44F2XgftVF8btbMy` (https://claude.ai/code/session_01A968Mb44F2XgftVF8btbMy)
- **Começou:** 21/10/2026, pelo celular. **Encerrada:** 22/10/2026, a pedido.
- **Repositórios:** linu-sites (principal), LinuLingo; losveganaestrada, v2tech-ranliao e marginalia só para leitura.
- **Branch de trabalho:** `ccr-5fafb49f-0cgkd8` (no linu-sites e no LinuLingo), já juntado na `main` / `master`.

## Situação: encerrada, nada pendente de commit

Tudo está commitado e no branch principal dos dois repositórios. A última publicação do linu-sites na
Oracle (commit `cdb0dd6`) terminou com sucesso. Nada está rodando.

## Atenção: outra sessão mexeu no mesmo site

A sessão `session_01H4UgJuHdxPD4jM2LHdUqXX` também trabalhou no linu-sites em 21/10/2026: fez um botão de
tema próprio (commit `4eada1b`), diretrizes de UX (`DIRETRIZES-UX.md`), animações (`public/js/movimento.js`)
e o “monte o seu pedido”, e juntou isso com o trabalho desta sessão (commit `edbbc2c`). Na `main` de agora
existe um botão de tema só, o do Linu e do lampião. Se for revisar, vale conferir se sobrou CSS do botão
antigo (chave `linu-sites-tema`) sem uso.

## O que foi feito

### linu-sites (https://sites.linupedia.com.br), tudo publicado

1. **Modo claro e escuro com o Linu.** Botão da lâmpada no topo: o Linu entra no quarto pela porta, vai até
   o lampião, apaga (modo escuro) ou acende (modo claro) e sai; a página troca de cor junto. A escolha fica
   guardada; sem escolha, segue o sistema. Com “reduzir movimento”, troca na hora. Se a cena estiver fora
   da tela, a animação aparece num cartão no canto. (`public/js/tema.js`, `public/js/tema-inicio.js`)
2. **Noite com o lampião apagado, só no site** (`img/abrigo-estacao-apagada.png`, gerada por
   `ferramentas/cena-apagada.py`).
3. **Linu de lado redesenhado**, com 4 quadros de caminhada (`ferramentas/desenhar-linu-lado.py`).
   Provisório: você vai redesenhar o Linu pelo Gemini.
4. **Imagem de compartilhamento** 1200 × 630 e ícones em PNG (`ferramentas/gerar-imagens.mjs`).
5. **WhatsApp (61) 99667-2610** no contato.
6. **Menu do celular** (botão ☰), `public/js/menu.js`.
7. **Preços de referência** nos cartões: site a partir de R$ 1.800, ferramentas a partir de R$ 6.000,
   apps a partir de R$ 9.000, hospedagem R$ 120/mês (domínio à parte, cerca de R$ 40/ano).
8. **Depoimentos:** seção pronta e escondida (`hidden`) até chegarem frases de verdade.
9. **sitemap.xml**, `robots.txt` apontando para ele, `canonical` e Open Graph.
10. **Página de cada projeto:** `/projetos/linupedia`, `/v2tech`, `/losvega`, `/marginalia`, com o desafio,
    o que foi feito e como funciona por dentro, tirados dos READMEs de cada repositório
    (`ferramentas/gerar-projetos.py`). Cada cartão da página inicial ganhou o link “Como foi feito”.
11. **Fonte Nunito no próprio site** (sem Google Fonts) e **CSP** na página.
12. **Publicação mais segura:** antes de publicar, o GitHub valida o HTML e confere se todo arquivo usado
    existe (`deploy/conferir-pagina.py`); suporte ao segredo `ORACLE_HOST_KEY`.
13. **Consertos:** botão “Ver projetos” sem texto no modo escuro; texto escuro nos botões do topo e do
    contato no modo escuro; topo quebrando em duas linhas no celular; cartão do Los Vega dizia “aviso por
    WhatsApp” (o painel tem resposta pronta pelo WhatsApp).

### LinuLingo (app), na `master`

- **Retângulo da porta à noite:** na estação de pesquisa, nas luzes “noite” e “sol da meia-noite”, a
  porta e a escotilha tinham um retângulo de paisagem por cima da cortina. Consertado
  (`assets/pixel/abrigo-estacao-*.png`), com a entrada 27.411 na aba Atualizações. O teste do changelog
  passa; a bateria inteira de testes não foi rodada (o servidor da Oracle roda antes de publicar).

## O que está fazendo agora

Nada. A sessão foi encerrada.

## O que ficaria para depois (sugestões, nada começado)

- Perguntas frequentes no site (prazo, pagamento, quem fica dono do domínio e do código).
- Contador de visitas sem cookie, na própria VM.
- Levar o Linu redesenhado para o app (12 cores e roupinhas).
- Ideia 8: o Linu ficar no quarto depois de trocar a luz (ir para a cama no modo escuro).

## Esperando ação sua

1. **Segredo `ORACLE_HOST_KEY`** no repositório linu-sites (Settings → Secrets and variables → Actions).
   Na sua máquina:
   `ssh -i ~/.ssh/id_ed25519_linulingo ubuntu@168.138.155.95 'echo "168.138.155.95 $(cut -d" " -f1,2 /etc/ssh/ssh_host_ed25519_key.pub)"'`
   e cole a linha inteira no segredo. Depois, Actions → Publicar na Oracle Cloud → Run workflow: o aviso
   amarelo deve sumir.
2. **Aplicar o novo `deploy/Caddyfile-bloco` na VM** (com sudo), para valerem os cabeçalhos de segurança
   completos. Passo a passo em `deploy/ORACLE.md`. Já foi validado com o Caddy 2.10.
3. **Google Search Console:** cadastrar `sites.linupedia.com.br` (registro TXT no Registro.br) e enviar o
   `sitemap.xml`. Perfil de Empresa no Google com o WhatsApp.
4. **Revisar as 4 páginas de projeto**, principalmente V²Tech e Marginalia (falam de outras pessoas).
5. **Linu pelo Gemini:** o prompt foi passado na conversa; quando sair, mandar as imagens para recortar
   na grade 52 × 61 e colocar no site.

## Perguntas para você

- Tem depoimentos de verdade (frase, nome e projeto) dos donos do Los Vega, do V²Tech e da Marginalia?
- Quer a ideia 8 (o Linu ficar no quarto)?
- Como funcionam prazo médio, forma de pagamento e propriedade do domínio e do código, para as
  perguntas frequentes?
