#!/usr/bin/env python3
"""SEL0337 / Pratica 5 / CP1: LED em GPIO18 com parada segura."""

import signal
import time

from gpiozero import LED

GPIO_PIN = 18  # Numeracao BCM; pino fisico 12.
BLINK_DELAY_SECONDS = 0.2
stop_requested = False


def handle_shutdown(signum, _frame):
    """Solicita a finalizacao apos SIGTERM ou SIGINT."""
    global stop_requested
    stop_requested = True
    print(f"[SEL0337] Sinal {signum} recebido; encerrando.", flush=True)


def main() -> None:
    signal.signal(signal.SIGTERM, handle_shutdown)
    signal.signal(signal.SIGINT, handle_shutdown)

    led = LED(GPIO_PIN)
    try:
        print(f"[SEL0337] Blink ativo no GPIO {GPIO_PIN}.", flush=True)
        while not stop_requested:
            led.on()
            time.sleep(BLINK_DELAY_SECONDS)
            led.off()
            time.sleep(BLINK_DELAY_SECONDS)
    finally:
        led.off()
        led.close()
        print("[SEL0337] LED desligado; GPIO liberada.", flush=True)


if __name__ == "__main__":
    main()
