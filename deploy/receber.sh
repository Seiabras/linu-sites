#!/usr/bin/env bash
# Único comando que a chave do GitHub Actions pode rodar na VM (comando forçado no authorized_keys do
# usuário linusites). Recebe pela entrada um .tar.gz com a pasta public/ e troca /opt/linu-sites/app.
# A versão anterior fica em app.anterior; se o pacote vier sem index.html, nada é trocado.
set -euo pipefail
BASE=/opt/linu-sites
NOVA="$BASE/app.nova"; VELHA="$BASE/app.anterior"

rm -rf "$NOVA"; mkdir -p "$NOVA"
head -c 50000000 | tar xzf - -C "$NOVA" --no-same-owner
[ -f "$NOVA/index.html" ] || { echo "Pacote inválido (sem index.html)."; rm -rf "$NOVA"; exit 1; }
chmod -R a+rX "$NOVA"

rm -rf "$VELHA"
[ -d "$BASE/app" ] && mv "$BASE/app" "$VELHA"
mv "$NOVA" "$BASE/app"
echo "Linu Sites atualizado."
