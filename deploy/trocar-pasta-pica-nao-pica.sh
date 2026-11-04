#!/usr/bin/env bash
# Roda uma vez na VM 1 (04/11/2026), ANTES do push que renomeia sitios/abelhas-sem-ferrao para sitios/pica-nao-pica:
# cria pica-nao-pica como atalho para a pasta de agora, aponta o Caddy para ela e leva as páginas antigas do
# sites.linupedia.com.br para as novas. O deploy seguinte troca o atalho pela pasta de verdade, sem o site sair do ar.
set -e
APP=/opt/linu-sites/app/_sitios
[ -e "$APP/pica-nao-pica" ] || sudo ln -s abelhas-sem-ferrao "$APP/pica-nao-pica"
sudo cp /etc/caddy/Caddyfile /etc/caddy/Caddyfile.antes-pica-nao-pica
sudo python3 - <<"PY"
p="/etc/caddy/Caddyfile"; s=open(p).read()
a="root * /opt/linu-sites/app/_sitios/abelhas-sem-ferrao"
b="\t@sitios path /_sitios /_sitios/*\n\terror @sitios 404\n"
c=("\t# o Pica ou Não Pica? se chamava abelhas-sem-ferrao até 04/11/2026: a página antiga leva à nova, em qualquer língua\n"
   "\t@abelhas path_regexp abelhas ^(.*)/projetos/abelhas-sem-ferrao(\\.html)?$\n"
   "\tredir @abelhas {re.abelhas.1}/projetos/pica-nao-pica permanent\n")
assert s.count(a)==1 and s.count(b)==1, (s.count(a), s.count(b))
s=s.replace(a,"root * /opt/linu-sites/app/_sitios/pica-nao-pica").replace(b,b+c)
open(p,"w").write(s)
PY
if sudo caddy validate --config /etc/caddy/Caddyfile --adapter caddyfile 2>&1 | tail -1 | grep -q "Valid configuration"; then
  sudo systemctl reload caddy; sleep 3
  curl -sS -o /dev/null -m 20 -w 'pica: %{http_code}\n' https://picanaopica.linupedia.com.br/
  curl -sS -o /dev/null -m 20 -w 'pagina antiga: %{http_code} -> %{redirect_url}\n' https://sites.linupedia.com.br/en/projetos/abelhas-sem-ferrao
  echo troca-feita
else
  sudo cp /etc/caddy/Caddyfile.antes-pica-nao-pica /etc/caddy/Caddyfile
  echo "Configuração inválida. Voltei o arquivo antigo e nada mudou."; exit 1
fi
