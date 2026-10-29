# Linu Sites na Oracle Cloud

Endereço: **https://sites.linupedia.com.br**. Mesma VM da LinuPedia (Ubuntu, IP 168.138.155.95).
O site é só arquivos: o Caddy entrega a pasta `/opt/linu-sites/app` direto, sem serviço Node.

## 1. DNS (Registro.br, uma vez)

No Registro.br → linupedia.com.br → DNS → Editar zona, acrescente:

| Tipo | Nome | Valor |
|---|---|---|
| A | `sites` | `168.138.155.95` |
| A | `cafe` | `168.138.155.95` |
| A | `cerrado` | `168.138.155.95` |
| A | `abelhas` | `168.138.155.95` |

Os registros que já existem (os da LinuPedia) ficam como estão.

## 2. Caddy (uma vez)

Acrescente o bloco de [`Caddyfile-bloco`](Caddyfile-bloco) no fim de `/etc/caddy/Caddyfile`, valide e
recarregue. O `mudar-para-linupedia.sh` do repositório da LinuPedia só troca os blocos dele, então este
não é apagado.

```bash
scp -i ~/.ssh/id_ed25519_linulingo deploy/Caddyfile-bloco ubuntu@168.138.155.95:
ssh -i ~/.ssh/id_ed25519_linulingo ubuntu@168.138.155.95
sudo mkdir -p /srv/linu-sites && sudo chown ubuntu: /srv/linu-sites
sudo cp /etc/caddy/Caddyfile /etc/caddy/Caddyfile.antes-linu-sites
cat Caddyfile-bloco | sudo tee -a /etc/caddy/Caddyfile
sudo caddy validate --config /etc/caddy/Caddyfile && sudo systemctl reload caddy
```

Se o `validate` der erro, volte o arquivo: `sudo cp /etc/caddy/Caddyfile.antes-linu-sites /etc/caddy/Caddyfile`.

## 3. Publicação automática

A cada push na `main`, o GitHub Actions ([`oracle.yml`](../.github/workflows/oracle.yml)) manda a pasta
`public/` para a VM. Ele entra como o usuário `linusites`, **sem sudo**, com uma chave presa ao comando
`/opt/linu-sites/receber.sh`: ela só consegue trocar `/opt/linu-sites/app` (a versão anterior fica em
`app.anterior`). O Caddy serve `/opt/linu-sites/app`.

Preparação (uma vez, já feita em 21/10/2026): `sudo bash deploy/instalar-uma-vez.sh "<chave pública>"`
na VM, e a chave privada correspondente no segredo `ORACLE_SSH_KEY` do repositório (Settings → Secrets
and variables → Actions). **Para cortar o acesso do GitHub:** apagar `/home/linusites/.ssh/authorized_keys`.

### A chave da VM fixada (segredo `ORACLE_HOST_KEY`)

Para o GitHub ter certeza de que está falando com a VM de verdade, e não com alguém no caminho, a chave
pública do servidor fica num segredo. Sem ele, a publicação continua funcionando, com um aviso.

Na VM (pelo seu acesso de sempre), rode:

```bash
echo "168.138.155.95 $(cut -d' ' -f1,2 /etc/ssh/ssh_host_ed25519_key.pub)"
```

e cole a linha inteira no segredo `ORACLE_HOST_KEY` do repositório (Settings → Secrets and variables →
Actions). Se a VM for recriada, a chave muda: é só rodar de novo e trocar o segredo.

### Conferências antes de publicar

Antes de mandar para a VM, o Actions valida o HTML (`html-validate`) e confere que toda imagem, CSS e JS
que a página usa existe (`deploy/conferir-pagina.py`). Se algo falhar, nada é publicado. Para rodar no
computador: `npx html-validate@10.1.2 public/*.html && python3 deploy/conferir-pagina.py`.

### Cabeçalhos de segurança (aplicar à mão, com sudo)

O `Caddyfile-bloco` traz os cabeçalhos de segurança: a política de conteúdo (CSP), a proibição de pôr a
página dentro de outro site e o HTTPS obrigatório (HSTS). A publicação automática não mexe no Caddy (o
usuário `linusites` não tem sudo), então, quando o bloco mudar, troque o bloco antigo pelo novo em
`/etc/caddy/Caddyfile` e recarregue:

```bash
scp -i ~/.ssh/id_ed25519_linulingo deploy/Caddyfile-bloco ubuntu@168.138.155.95:
ssh -i ~/.ssh/id_ed25519_linulingo ubuntu@168.138.155.95
sudo cp /etc/caddy/Caddyfile /etc/caddy/Caddyfile.antes-cabecalhos
sudo nano /etc/caddy/Caddyfile   # apague o bloco "sites.linupedia.com.br { … }" e cole o de Caddyfile-bloco
sudo caddy validate --config /etc/caddy/Caddyfile && sudo systemctl reload caddy
```

Enquanto isso não for feito, a página já leva a mesma CSP numa `<meta>` do `index.html` (menos o
`frame-ancestors`, que só funciona como cabeçalho).

## Os subdomínios dos sites de estudo (29/10/2026)

`cafe`, `cerrado` e `abelhas` (`.linupedia.com.br`) vêm da pasta `sitios/` do repositório. A publicação automática
copia `sitios/` para `public/_sitios/` antes de empacotar, então eles chegam à VM em `/opt/linu-sites/app/_sitios/`
junto com o resto, pelo mesmo `receber.sh`. No `Caddyfile-bloco`, cada subdomínio tem o seu bloco, com a raiz na sua
subpasta, e o `sites.linupedia.com.br` responde 404 para `/_sitios`, para os sites só abrirem pelo próprio endereço.

O Café Aurora pode ser embutido só pelo `sites.linupedia.com.br` (o simulador): `frame-ancestors` no bloco do Café e
`frame-src https://cafe.linupedia.com.br` no do Linu Sites (e na `<meta>` do `index.html`). Os outros dois não podem
ser embutidos em lugar nenhum.
