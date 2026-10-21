#!/usr/bin/env bash
# Prepara a VM para receber o Linu Sites pelo GitHub Actions. Rodar uma vez, como administrador:
#   sudo bash instalar-uma-vez.sh "<chave pública do GitHub Actions>"
# Cria o usuário linusites (sem sudo), dono de /opt/linu-sites, e prende a chave ao receber.sh.
# Pode rodar de novo sem estragar nada.
set -euo pipefail
CHAVE="${1:?passe a chave pública}"
BASE=/opt/linu-sites

id linusites >/dev/null 2>&1 || useradd --system --create-home --shell /bin/bash linusites
mkdir -p "$BASE"
install -m 755 -o root -g root receber.sh "$BASE/receber.sh"
if [ ! -d "$BASE/app" ]; then
  if [ -d /srv/linu-sites ]; then cp -a /srv/linu-sites "$BASE/app"; else mkdir -p "$BASE/app"; fi
fi
chown linusites: "$BASE" && chown -R linusites: "$BASE/app"
chmod 755 "$BASE"

install -d -m 700 -o linusites -g linusites /home/linusites/.ssh
echo "restrict,command=\"$BASE/receber.sh\" $CHAVE" > /home/linusites/.ssh/authorized_keys
chown linusites: /home/linusites/.ssh/authorized_keys && chmod 600 /home/linusites/.ssh/authorized_keys

# o Caddy passa a servir /opt/linu-sites/app (antes era /srv/linu-sites)
if grep -q "root \* /srv/linu-sites" /etc/caddy/Caddyfile; then
  cp /etc/caddy/Caddyfile /etc/caddy/Caddyfile.antes-linu-sites-auto
  sed -i "s|root \* /srv/linu-sites|root * $BASE/app|" /etc/caddy/Caddyfile
  if caddy validate --config /etc/caddy/Caddyfile --adapter caddyfile >/dev/null 2>&1; then
    systemctl reload caddy
  else
    cp /etc/caddy/Caddyfile.antes-linu-sites-auto /etc/caddy/Caddyfile
    echo "O Caddyfile novo não validou; voltei o anterior."; exit 1
  fi
fi
echo "Pronto: linusites recebe versões novas em $BASE/app."
