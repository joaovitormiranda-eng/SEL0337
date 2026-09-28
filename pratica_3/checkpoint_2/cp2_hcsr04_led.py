"""
SEL0337 - Projetos em Sistemas Embarcados
Prática 3 - Checkpoint 2

Aplicação com sensor ultrassônico HC-SR04 e LED utilizando gpiozero.

O LED é acionado quando um objeto é detectado a uma distância
menor ou igual a 20 cm.

Autores:
João Vitor Miranda Sousa - NUSP 14802702
Fernando Shoji Ogusuku - NUSP 15636682
Eduardo Yumoto Carvalheira - NUSP 15636150
"""

from time import sleep

from gpiozero import DistanceSensor, LED


TRIGGER_GPIO = 23
ECHO_GPIO = 24
LED_GPIO = 17

LIMIAR_M = 0.20
DISTANCIA_MAXIMA_M = 4.0
INTERVALO_LEITURA_S = 0.2


def main() -> None:
    """Executa a aplicação de medição de distância e controle do LED."""

    sensor = DistanceSensor(
        echo=ECHO_GPIO,
        trigger=TRIGGER_GPIO,
        max_distance=DISTANCIA_MAXIMA_M,
        threshold_distance=LIMIAR_M,
    )

    led = LED(LED_GPIO)

    def objeto_perto() -> None:
        """Acende o LED quando um objeto entra no limite definido."""
        led.on()
        print("\nObjeto dentro do limite -> LED aceso")

    def objeto_longe() -> None:
        """Apaga o LED quando o objeto sai do limite definido."""
        led.off()
        print("\nObjeto fora do limite -> LED apagado")

    sensor.when_in_range = objeto_perto
    sensor.when_out_of_range = objeto_longe

    print("Sensor iniciado.")
    print(f"Limiar de detecção: {LIMIAR_M * 100:.0f} cm")
    print("Use CTRL+C para encerrar.")

    try:
        while True:
            distancia_cm = sensor.distance * 100.0

            print(
                f"\rDistância: {distancia_cm:6.1f} cm",
                end="",
                flush=True,
            )

            sleep(INTERVALO_LEITURA_S)

    except KeyboardInterrupt:
        print("\nPrograma interrompido pelo usuário.")

    finally:
        led.off()
        sensor.close()
        led.close()
        print("Dispositivos liberados.")


if __name__ == "__main__":
    main()