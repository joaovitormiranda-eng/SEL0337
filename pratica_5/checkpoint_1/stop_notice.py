#!/usr/bin/env python3
"""Acao ExecStop: registra a solicitacao de parada do servico."""

# O systemd envia SIGTERM ao processo principal apos ExecStop retornar.
# O blink_python.py trata esse sinal e desliga o LED no bloco finally.
print("[SEL0337] ExecStop executado; solicitando parada do blink.", flush=True)
