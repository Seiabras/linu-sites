# Linu Sites na Oracle Cloud

Endereço: **https://sites.linupedia.com.br**. Mesma VM da LinuPedia (Ubuntu, IP 168.138.155.95).
O site é só arquivos: o Caddy entrega a pasta `/srv/linu-sites` direto, sem serviço Node.

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
scp deploy/Caddyfile-bloco ubuntu@168.138.155.95:
ssh ubuntu@168.138.155.95
sudo mkdir -p /srv/linu-sites && sudo chown ubuntu: /srv/linu-sites
sudo cp /etc/caddy/Caddyfile /etc/caddy/Caddyfile.antes-linu-sites
cat Caddyfile-bloco | sudo tee -a /etc/caddy/Caddyfile
sudo caddy validate --config /etc/caddy/Caddyfile && sudo systemctl reload caddy
```

Se o `validate` der erro, volte o arquivo: `sudo cp /etc/caddy/Caddyfile.antes-linu-sites /etc/caddy/Caddyfile`.

## 3. Publicar uma versão nova

```bash
rsync -av --delete public/ ubuntu@168.138.155.95:/srv/linu-sites/
```

O certificado HTTPS o Caddy tira sozinho na primeira visita, depois que o DNS apontar para a VM.
