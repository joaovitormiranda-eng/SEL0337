"""SEL0337 — Projetos em Sistemas Embarcados
Prática 3 — Checkpoint 2
Programa 2 — Sensor ultrassônico HC-SR04 com acionamento de LED.

Autores:
    João Vitor Miranda Sousa — NUSP 14802702
    Fernando Shoji Ogusuku — NUSP 15636682
    Eduardo Yumoto Carvalheira — NUSP 15636150

Hardware:
    - Trigger do HC-SR04: GPIO23 (BCM), pino físico 16
    - Echo do HC-SR04: GPIO24 (BCM), pino físico 18
    - LED: GPIO17 (BCM), pino físico 11

Observação:
    A saída Echo do HC-SR04 deve ser conectada ao GPIO24 por meio de
    adequação de nível para 3,3 V, conforme a montagem utilizada em bancada.
"""

from time import sleep

from gpiozero import DistanceSensor, LED


TRIGGER_GPIO = 23
ECHO_GPIO = 24
LED_GPIO = 17

LIMIAR_DISTANCIA_M = 0.20
DISTANCIA_MAXIMA_M = 4.0
INTERVALO_LEITURA_S = 0.2


def objeto_proximo(led: LED) -> None:
    """Acende o LED quando o objeto entra na faixa configurada."""
    led.on()
    print("\nObjeto dentro do limite -> LED aceso")


def objeto_distante(led: LED) -> None:
    """Apaga o LED quando o objeto sai da faixa configurada."""
    led.off()
    print("\nObjeto fora do limite -> LED apagado")


def main() -> None:
    """Inicializa o sensor e monitora continuamente a distância medida."""
    sensor = DistanceSensor(
        echo=ECHO_GPIO,
        trigger=TRIGGER_GPIO,
        max_distance=DISTANCIA_MAXIMA_M,
        threshold_distance=LIMIAR_DISTANCIA_M,
    )
    led = LED(LED_GPIO)

    sensor.when_in_range = lambda: objeto_proximo(led)
    sensor.when_out_of_range = lambda: objeto_distante(led)

    print(
        f"Sensor iniciado. Limiar = "
        f"{LIMIAR_DISTANCIA_M * 100:.0f} cm."
    )
    print("Pressione CTRL+C para encerrar.")

    try:
        while True:
            distancia_cm = sensor.distance * 100
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
