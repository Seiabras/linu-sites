# Roda uma vez na VM 1: leva o site das Abelhas para picanaopica.linupedia.com.br. O endereço antigo passa a redirecionar.
set -e
sudo cp /etc/caddy/Caddyfile /etc/caddy/Caddyfile.antes-picanaopica
sudo python3 - <<"PY"
p="/etc/caddy/Caddyfile"; s=open(p).read()
a="abelhas.linupedia.com.br {\n\tencode"
b="abelhas.linopedia.com.br {\n\tredir https://abelhas.linupedia.com.br{uri} permanent\n}\n"
assert s.count(a)==1 and s.count(b)==1
s=s.replace(a,"picanaopica.linupedia.com.br {\n\tencode")
s=s.replace(b,"abelhas.linupedia.com.br {\n\tredir https://picanaopica.linupedia.com.br{uri} permanent\n}\nabelhas.linopedia.com.br {\n\tredir https://picanaopica.linupedia.com.br{uri} permanent\n}\n")
open(p,"w").write(s)
PY
if sudo caddy validate --config /etc/caddy/Caddyfile --adapter caddyfile 2>&1 | tail -1 | grep -q "Valid configuration"; then
  sudo systemctl reload caddy; sleep 12
  curl -sS -o /dev/null -m 20 -w 'novo: %{http_code}\n' https://picanaopica.linupedia.com.br/
  curl -sS -o /dev/null -m 20 -w 'antigo: %{http_code} -> %{redirect_url}\n' https://abelhas.linupedia.com.br/
  echo troca-feita
else
  sudo cp /etc/caddy/Caddyfile.antes-picanaopica /etc/caddy/Caddyfile
  echo "Configuração inválida. Voltei o arquivo antigo e nada mudou."; exit 1
fi
