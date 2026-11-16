#!/usr/bin/env bash
# Demonstra a interface GPIO sysfs legado do roteiro, quando disponivel.
# ATENCAO: executar APENAS na Raspberry e com permissao do laboratorio.
set -euo pipefail
GPIO=18
ROOT=/sys/class/gpio
GPIO_DIR="$ROOT/gpio$GPIO"
EXPORTED_BY_SCRIPT=0

if [[ ! -e "$ROOT/export" ]]; then
  echo 'GPIO sysfs indisponivel neste kernel; utilize a versao Python/gpiozero.' >&2
  exit 1
fi

cleanup() {
  if [[ -d "$GPIO_DIR" ]]; then
    printf '0\n' > "$GPIO_DIR/value" 2>/dev/null || true
  fi
  if [[ "$EXPORTED_BY_SCRIPT" -eq 1 ]]; then
    printf '%s\n' "$GPIO" > "$ROOT/unexport" 2>/dev/null || true
  fi
}
trap cleanup EXIT
trap 'exit 0' INT TERM

if [[ ! -d "$GPIO_DIR" ]]; then
  printf '%s\n' "$GPIO" > "$ROOT/export"
  EXPORTED_BY_SCRIPT=1
fi
printf 'out\n' > "$GPIO_DIR/direction"

while true; do
  printf '1\n' > "$GPIO_DIR/value"
  sleep 0.2
  printf '0\n' > "$GPIO_DIR/value"
  sleep 0.2
done
