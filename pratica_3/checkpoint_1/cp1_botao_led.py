"""SEL0337 — Projetos em Sistemas Embarcados
Prática 3 — Checkpoint 1
Programa 1 — Controle de LED por botão com detecção de eventos.

Autores:
    João Vitor Miranda Sousa — NUSP 14802702
    Fernando Shoji Ogusuku — NUSP 15636682
    Eduardo Yumoto Carvalheira — NUSP 15636150

Hardware:
    - LED: GPIO17 (BCM), pino físico 11
    - Botão: GPIO18 (BCM), pino físico 12
    - O botão utiliza o resistor de pull-up interno da Raspberry Pi.
"""

from signal import pause

import RPi.GPIO as GPIO


LED_GPIO = 17
BOTAO_GPIO = 18
DEBOUNCE_MS = 100


def tratar_evento_botao(_canal: int) -> None:
    """Atualiza o LED de acordo com o estado atual do botão."""
    botao_pressionado = GPIO.input(BOTAO_GPIO) == GPIO.LOW
    GPIO.output(LED_GPIO, GPIO.HIGH if botao_pressionado else GPIO.LOW)

    estado_botao = "pressionado" if botao_pressionado else "solto"
    estado_led = "aceso" if botao_pressionado else "apagado"
    print(f"Botão {estado_botao} -> LED {estado_led}")


def configurar_gpio() -> None:
    """Configura a numeração e os pinos utilizados pela aplicação."""
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(LED_GPIO, GPIO.OUT, initial=GPIO.LOW)
    GPIO.setup(BOTAO_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_UP)


def main() -> None:
    """Executa a aplicação até a interrupção pelo usuário."""
    configurar_gpio()

    GPIO.add_event_detect(
        BOTAO_GPIO,
        GPIO.BOTH,
        callback=tratar_evento_botao,
        bouncetime=DEBOUNCE_MS,
    )

    print("Programa iniciado.")
    print("Pressione o botão para acender o LED.")
    print("Solte o botão para apagar o LED.")
    print("Pressione CTRL+C para encerrar.")

    try:
        pause()
    except KeyboardInterrupt:
        print("\nPrograma interrompido pelo usuário.")
    finally:
        GPIO.cleanup()
        print("GPIO.cleanup() executado.")


if __name__ == "__main__":
    main()
