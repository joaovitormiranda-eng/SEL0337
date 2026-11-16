#!/usr/bin/env bash
# Gera o unit file conforme o usuario e diretorio reais da Raspberry.
# NAO instala nem habilita automaticamente o servico no sistema.
set -euo pipefail
BASE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON="$(command -v python3)"
USER_NAME="$(id -un)"
UNIT="$BASE/sel0337-p5-blink.service"

if [[ "$BASE" =~ [[:space:]] ]]; then
  echo 'Erro: mova a pasta para um caminho sem espacos antes de gerar o unit.' >&2
  exit 1
fi

sed \
  -e "s|@USER@|$USER_NAME|g" \
  -e "s|@CHECKPOINT_DIR@|$BASE|g" \
  -e "s|@PYTHON@|$PYTHON|g" \
  "$BASE/sel0337-p5-blink.service.template" > "$UNIT"

printf 'Unit gerado: %s\n' "$UNIT"
printf 'Usuario: %s | Python: %s\n' "$USER_NAME" "$PYTHON"
printf 'Revise com: cat %q\n' "$UNIT"
