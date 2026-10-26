#!/usr/bin/env python3
"""Testes do protocolo ADC/I2C do Checkpoint 2, sem hardware."""

import sys
import types
import unittest
from pathlib import Path

# Permite importar a aplicacao sem a biblioteca SMBus da Raspberry Pi.
sys.modules["smbus2"] = types.ModuleType("smbus2")
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from cp2_raspberry_i2c_pot import decode_adc, read_adc


class FakeBus:
    """Simula a resposta de dois bytes de um dispositivo I2C."""

    def __init__(self, data):
        self.data = data
        self.last_call = None

    def read_i2c_block_data(self, address, command, length):
        self.last_call = (address, command, length)
        return self.data


class TestADCProtocol(unittest.TestCase):

    def test_all_1024_values(self):
        """Valida integralmente a faixa de 10 bits."""
        for expected in range(1024):
            with self.subTest(adc=expected):
                high = (expected >> 8) & 0xFF
                low = expected & 0xFF
                self.assertEqual(decode_adc(high, low), expected)

    def test_invalid_values(self):
        """Rejeita bytes invalidos e valores acima de 1023."""
        cases = [
            (-1, 0),
            (256, 0),
            (0, -1),
            (0, 256),
            (4, 0),
        ]

        for high, low in cases:
            with self.subTest(high=high, low=low):
                with self.assertRaises(ValueError):
                    decode_adc(high, low)

    def test_i2c_read(self):
        """Verifica parametros SMBus e reconstrucao da amostra."""
        bus = FakeBus([0x02, 0x0C])  # 524 decimal

        self.assertEqual(read_adc(bus), 524)
        self.assertEqual(bus.last_call, (0x08, 0x00, 2))

    def test_invalid_response_length(self):
        """Rejeita respostas com quantidade incorreta de bytes."""
        for data in ([0x00], [0x00, 0x00, 0x00]):
            with self.subTest(data=data):
                with self.assertRaises(RuntimeError):
                    read_adc(FakeBus(data))

    def test_out_of_range_i2c_response(self):
        """Rejeita amostras reconstruidas acima de 10 bits."""
        with self.assertRaises(ValueError):
            read_adc(FakeBus([0x04, 0x00]))


if __name__ == "__main__":
    unittest.main()
