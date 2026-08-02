#!/usr/bin/env bash
# Crea los issues del workshop en el repo de GitHub donde estes parado.
#
# Los forks de GitHub no copian los issues, asi que cada participante corre
# esto una vez sobre su propio fork para tener los mismos cuatro casos.
#
#   ./docs/crear-issues.sh
#
# Requiere: gh (autenticado) y estar dentro del repo destino.

set -euo pipefail

cd "$(dirname "$0")/.."

repo=$(gh repo view --json nameWithOwner -q .nameWithOwner)
echo "Repo destino: $repo"
echo

# Las etiquetas tienen que existir antes de usarlas.
crear_etiqueta() {
  gh label create "$1" --color "$2" --description "$3" --force >/dev/null 2>&1 || true
}
crear_etiqueta bug               d73a4a "Algo no funciona como deberia"
crear_etiqueta comercial         0e8a16 "Reportado por el equipo comercial"
crear_etiqueta datos             1d76db "Integridad de datos"
crear_etiqueta reglas-de-negocio 5319e7 "Validaciones del dominio"

for archivo in docs/issues/*.md; do
  titulo=$(python3 -c "
import re, sys
texto = open('$archivo', encoding='utf-8').read()
bloque = re.match(r'---\n(.*?)\n---\n', texto, re.S)
campos = bloque.group(1) if bloque else ''
m = re.search(r'^titulo:\s*\"?(.+?)\"?\s*$', campos, re.M)
print(m.group(1) if m else '')
")

  etiquetas=$(python3 -c "
import re
texto = open('$archivo', encoding='utf-8').read()
bloque = re.match(r'---\n(.*?)\n---\n', texto, re.S)
campos = bloque.group(1) if bloque else ''
m = re.search(r'^etiquetas:\s*(.+?)\s*\$', campos, re.M)
print(m.group(1).replace(' ', '') if m else '')
")

  # El cuerpo es todo lo que va despues del frontmatter.
  cuerpo=$(python3 -c "
import re
texto = open('$archivo', encoding='utf-8').read()
print(re.sub(r'^---\n.*?\n---\n', '', texto, count=1, flags=re.S).strip())
")

  if [ -z "$titulo" ]; then
    echo "  saltando $archivo (sin titulo en el frontmatter)"
    continue
  fi

  argumentos=(--title "$titulo" --body "$cuerpo")
  [ -n "$etiquetas" ] && argumentos+=(--label "$etiquetas")

  url=$(gh issue create "${argumentos[@]}")
  echo "  $titulo"
  echo "    $url"
done

echo
echo "Listo."
