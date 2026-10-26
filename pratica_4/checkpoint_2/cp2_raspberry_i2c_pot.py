#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
SEL0337 - Projetos em Sistemas Embarcados
Pratica 4 - Checkpoint 2
Leitura de potenciometro via I2C: Arduino Uno -> Raspberry Pi

O Arduino responde no endereco I2C 0x08 e envia o valor ADC de 10 bits
(0..1023) dividido em dois bytes:

    byte 0 = byte alto
    byte 1 = byte baixo

A Raspberry Pi reconstrui o valor original por:

    valor = (byte_alto << 8) | byte_baixo

Autores:
Joao Vitor Miranda Sousa - NUSP 14802702
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
        print("[ERRO] Biblioteca SMBus nao encontrada.")
        print("Instale python3-smbus ou smbus2 antes de executar.")
        sys.exit(1)


I2C_ADDRESS = 0x08
I2C_BUS_ID = 1

# read_i2c_block_data envia um byte de comando antes da leitura.
# O Arduino simplesmente descarta esse byte no callback onReceive().
COMMAND_BYTE = 0x00

READ_LENGTH = 2
POLL_INTERVAL_S = 0.50
ADC_MAX = 1023
ADC_REFERENCE_V = 5.0


def open_bus():
    """Abre o barramento I2C da Raspberry Pi."""
    try:
        return smbus.SMBus(I2C_BUS_ID)
    except OSError as error:
        print(
            f"[ERRO] Nao foi possivel abrir o barramento "
            f"I2C {I2C_BUS_ID}: {error}"
        )
        return None


def decode_adc(high_byte: int, low_byte: int) -> int:
    """Reconstrói e valida um valor ADC de 10 bits."""

    if not 0 <= high_byte <= 255:
        raise ValueError("Byte alto inválido.")

    if not 0 <= low_byte <= 255:
        raise ValueError("Byte baixo inválido.")

    value = (high_byte << 8) | low_byte

    if not 0 <= value <= ADC_MAX:
        raise ValueError(
            f"Valor ADC fora da faixa: {value}"
        )

    return value


def read_adc(bus) -> int:
    """Lê dois bytes do barramento I2C."""

    data = bus.read_i2c_block_data(
        I2C_ADDRESS,
        COMMAND_BYTE,
        READ_LENGTH,
    )

    if len(data) != READ_LENGTH:
        raise RuntimeError(
            f"Quantidade inesperada de bytes: {len(data)}"
        )

    return decode_adc(data[0], data[1])


def main() -> int:
    print("=" * 62)
    print(" SEL0337 - Pratica 4 - Checkpoint 2")
    print(" Raspberry Pi -> controladora I2C")
    print(f" Arduino responder -> endereco 0x{I2C_ADDRESS:02X}")
    print(" Leitura esperada do ADC -> 0 a 1023")
    print(" Pressione Ctrl+C para encerrar.")
    print("=" * 62)

    bus = open_bus()
    if bus is None:
        print("Verifique se o I2C esta habilitado e execute:")
        print("  sudo i2cdetect -y 1")
        return 1

    try:
        while True:
            try:
                adc_value = read_adc(bus)
                voltage = adc_value * ADC_REFERENCE_V / ADC_MAX

                print(
                    f"ADC recebido: {adc_value:4d} "
                    f"| tensao aproximada: {voltage:5.3f} V"
                )

            except OSError as error:
                print(
                    f"[ERRO I2C] Falha ao comunicar com "
                    f"0x{I2C_ADDRESS:02X}: {error}"
                )
                print(
                    "Confira i2cdetect, SDA, SCL, GND comum "
                    "e o level shifter."
                )

            except (RuntimeError, ValueError) as error:
                print(f"[ERRO DE DADOS] {error}")

            time.sleep(POLL_INTERVAL_S)

    except KeyboardInterrupt:
        print("\n[INFO] Encerramento solicitado pelo usuario.")

    finally:
        bus.close()
        print("[INFO] Barramento I2C liberado.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
