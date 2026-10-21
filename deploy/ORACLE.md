# Linu Sites na Oracle Cloud

Endereço: **https://sites.linupedia.com.br**. Mesma VM da LinuPedia (Ubuntu, IP 168.138.155.95).
O site é só arquivos: o Caddy entrega a pasta `/opt/linu-sites/app` direto, sem serviço Node.

## 1. DNS (Registro.br, uma vez)

No Registro.br → linupedia.com.br → DNS → Editar zona, acrescente:

| Tipo | Nome | Valor |
|---|---|---|
| A | `sites` | `168.138.155.95` |

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
