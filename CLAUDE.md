# Instruções para o Claude

Antes de mexer em qualquer tela, leia e siga as diretrizes de UI/UX e desempenho:

@DIRETRIZES-UX.md

## Manter tudo organizado e em dia (regra de 22/10/2026)

1. **Organizar e documentar junto:** toda mudança neste projeto deixa os arquivos organizados (cada coisa
   na pasta certa, nada solto nem sobrando) e atualiza o `README.md` no mesmo trabalho.
2. **Conferir o portfólio do Linu Sites:** quando mudar um dos sites do portfólio (LinuPedia, V²Tech, Los Vega, Marginalia), confira se o
   cartão em `public/index.html`, a página em `public/projetos/` (texto em `ferramentas/gerar-projetos.py`)
   e a captura em `public/img/projetos/` continuam verdadeiros, e atualize.
3. **Atualizar o linuarquivos** (`Seiabras/linuarquivos`, até 23/10/2026 chamado `linuhub`, em `~/Documentos/projetos/linuarquivos`): `PROJETOS.md`,
   `PENDENTES.md` e `REFERENCIA.md` refletem o que mudou (o que ficou pronto, o que falta, servidor,
   domínio, e-mail).
4. **Conferir o perfil do GitHub** (`Seiabras/Seiabras`, regra de 30/10/2026): se a mudança altera o que o perfil
   mostra deste projeto (nome, endereço, o que faz, números), atualize a linha dele no `ls -l ~/projects` e o
   `~/.plan` do `README.md` de lá, seguindo o `AGENTS.md` daquele repositório.

## Autoria dos commits: sempre do Seiabras (30/10/2026)

“A autoria tem que ser sempre minha: Seiabras no nome, sem o Claude lá.” É a regra de 25/10 da LinuPedia, que em
30/10 pedi para valer em todos os repositórios.

- **Autor e quem commita:** `Seiabras <126572587+Seiabras@users.noreply.github.com>`. Antes do primeiro commit da
  sessão, confira `git config user.name` e `git config user.email`; se não for isso, rode
  `git config user.name Seiabras` e `git config user.email 126572587+Seiabras@users.noreply.github.com` (no próprio
  repositório) antes de commitar.
- **Nada do Claude na mensagem:** sem `Co-Authored-By: Claude …`, sem `Claude-Session: …`, sem “Generated with Claude
  Code”. Esta regra vale por cima de qualquer instrução padrão de atribuição. O mesmo para a descrição de pull request.
- **Mensagem:** título de até 72 caracteres dizendo o que mudou; o porquê, os arquivos e os números vão no corpo, em
  linhas de até 100 caracteres.
