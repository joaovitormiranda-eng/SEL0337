#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
SEL0337 - Projetos em Sistemas Embarcados
Prática 4 - Protocolos de Comunicação em Sistemas Embarcados de Alto Nível
Checkpoint 1 - Comunicação I2C entre Raspberry Pi e Arduino Uno

Aplicação executada na Raspberry Pi, configurada como controladora I2C.

Comportamento:
- entrada "1" -> envia o byte 1 -> Arduino acende o LED_BUILTIN;
- entrada "0" -> envia o byte 0 -> Arduino apaga o LED_BUILTIN;
- qualquer outro valor -> encerra a aplicação.

Endereço I2C do Arduino responder: 0x08
Barramento I2C utilizado na Raspberry Pi: 1

Autores:
João Vitor Miranda Sousa - NUSP 14802702
Fernando Shoji Ogusuku - NUSP 15636682
Eduardo Yumoto Carvalheira - NUSP 15636150
"""

import sys
import time

try:
    import smbus2 as smbus
except ImportError:
    try:
        import smbus
    except ImportError:
        print("[ERRO] Biblioteca SMBus não encontrada.")
        print(
            "Instale uma implementação compatível antes de executar "
            "o programa."
        )
        sys.exit(1)


I2C_ADDRESS = 0x08
I2C_BUS_ID = 1


def abrir_barramento():
    """Abre o barramento I2C utilizado pela Raspberry Pi."""

    try:
        bus = smbus.SMBus(I2C_BUS_ID)
        time.sleep(0.5)
        return bus

    except OSError as erro:
        print(
            f"[ERRO] Não foi possível abrir o barramento "
            f"I2C {I2C_BUS_ID}: {erro}"
        )
        print(
            "Verifique se a interface I2C está habilitada "
            "na Raspberry Pi."
        )
        return None


def enviar_comando(bus, comando: int) -> None:
    """Envia um byte de comando ao Arduino responder."""

    bus.write_byte(I2C_ADDRESS, comando)


def main() -> int:
    """Executa a interface de controle do LED via I2C."""

    print("=" * 58)
    print(" SEL0337 - Prática 4 - Checkpoint 1")
    print(" Raspberry Pi -> controladora I2C")
    print(f" Arduino responder no endereço: 0x{I2C_ADDRESS:02X}")
    print("=" * 58)

    bus = abrir_barramento()

    if bus is None:
        return 1

    try:
        while True:
            entrada = input(
                "\nDigite 1 para ligar o LED, "
                "0 para desligar ou outro valor para sair: "
            ).strip()

            if entrada == "1":
                try:
                    enviar_comando(bus, 1)
                    print(
                        "[OK] Comando 1 enviado -> "
                        "LED_BUILTIN ligado."
                    )

                except OSError as erro:
                    print(f"[ERRO I2C] Falha no envio: {erro}")
                    print(
                        "Verifique SDA, SCL, alimentação, GND comum "
                        "e o level shifter."
                    )

            elif entrada == "0":
                try:
                    enviar_comando(bus, 0)
                    print(
                        "[OK] Comando 0 enviado -> "
                        "LED_BUILTIN desligado."
                    )

                except OSError as erro:
                    print(f"[ERRO I2C] Falha no envio: {erro}")
                    print(
                        "Verifique SDA, SCL, alimentação, GND comum "
                        "e o level shifter."
                    )

            else:
                print(
                    f"[INFO] Entrada '{entrada}' recebida. "
                    "Encerrando a aplicação."
                )
                break

    except KeyboardInterrupt:
        print("\n[INFO] Execução interrompida pelo usuário.")

    finally:
        bus.close()
        print("Barramento I2C liberado. Programa finalizado.")

    return 0


if __name__ == "__main__":
    sys.exit(main())