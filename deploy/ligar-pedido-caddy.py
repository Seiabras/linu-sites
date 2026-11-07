"""Liga o /api/pedido do Linu Sites no Caddy da VM (07/11/2026). O dono roda, do computador dele:

    ssh -i ~/.ssh/id_ed25519_linulingo ubuntu@168.138.155.95 'sudo python3 -' < deploy/ligar-pedido-caddy.py

Guarda uma cópia do Caddyfile, põe o handle /api/pedido (o mesmo do deploy/Caddyfile-bloco) no começo do bloco
sites.linupedia.com.br, confere e recarrega o Caddy. Se a conferência falhar, volta a cópia e nada muda. Rodar de novo
não faz nada (já está ligado).
"""
import shutil
import subprocess
import sys
from pathlib import Path

CADDY = Path('/etc/caddy/Caddyfile')
COPIA = Path('/etc/caddy/Caddyfile.antes-pedido-sites')
ABRE = 'sites.linupedia.com.br {\n'
NOVO = ('\t# os pedidos do Monte o seu site (linu-pedidos no linuarquivos/servidor, 07/11/2026)\n'
        '\thandle /api/pedido {\n\t\trequest_body {\n\t\t\tmax_size 8KB\n\t\t}\n\t\treverse_proxy 127.0.0.1:8094\n\t}\n')

texto = CADDY.read_text()
i = texto.find(ABRE)
if i < 0:
    sys.exit('Não achei o bloco sites.linupedia.com.br no Caddyfile; nada mudou.')
fim = texto.find('\n}\n', i)
if '/api/pedido' in texto[i:fim]:
    print('Já estava ligado; nada mudou.')
    sys.exit(0)
shutil.copy2(CADDY, COPIA)
j = i + len(ABRE)
CADDY.write_text(texto[:j] + NOVO + texto[j:])
ok = subprocess.run(['caddy', 'validate', '--config', str(CADDY), '--adapter', 'caddyfile'], capture_output=True, text=True)
if ok.returncode != 0:
    shutil.copy2(COPIA, CADDY)
    sys.exit('O Caddy não aceitou a mudança; voltei a cópia, nada mudou.\n' + ok.stderr[-800:])
subprocess.run(['systemctl', 'reload', 'caddy'], check=True)
print('Pronto: os pedidos do Linu Sites passam a chegar no e-mail. Cópia do antes em ' + str(COPIA))
