"""
SEL0337 - Projetos em Sistemas Embarcados
Prática 3 - Checkpoint 2

Controle de PWM utilizando RPi.GPIO.

O usuário pode alterar a frequência e o duty cycle pelo terminal,
permitindo observar o comportamento do LED e a forma de onda
no osciloscópio.

Autores:
João Vitor Miranda Sousa - NUSP 14802702
Fernando Shoji Ogusuku - NUSP 15636682
Eduardo Yumoto Carvalheira - NUSP 15636150
"""

import RPi.GPIO as GPIO


LED_GPIO = 17
FREQUENCIA_INICIAL_HZ = 100.0


def solicitar_parametros_pwm() -> tuple[float, float]:
    """Solicita e valida frequência e duty cycle informados pelo usuário."""

    while True:
        try:
            frequencia = float(input("\nFrequência [Hz]: "))
            duty_cycle = float(input("Duty cycle [%]: "))

        except ValueError:
            print("Erro: digite valores numéricos.")
            continue

        if frequencia <= 0:
            print("Erro: a frequência deve ser maior que zero.")
            continue

        if not 0 <= duty_cycle <= 100:
            print("Erro: o duty cycle deve ficar entre 0 e 100%.")
            continue

        return frequencia, duty_cycle


def main() -> None:
    """Executa o controle interativo do sinal PWM."""

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(LED_GPIO, GPIO.OUT, initial=GPIO.LOW)

    pwm = GPIO.PWM(LED_GPIO, FREQUENCIA_INICIAL_HZ)
    pwm.start(0)

    print("PWM iniciado.")
    print(
        "Sugestões de teste: "
        "100 Hz / 25%, "
        "100 Hz / 50%, "
        "100 Hz / 75%, "
        "500 Hz / 50% e "
        "1000 Hz / 50%."
    )
    print("Use CTRL+C para encerrar.")

    try:
        while True:
            frequencia, duty_cycle = solicitar_parametros_pwm()

            pwm.ChangeFrequency(frequencia)
            pwm.ChangeDutyCycle(duty_cycle)

            print(
                f"Aplicado: f = {frequencia:.1f} Hz "
                f"| duty = {duty_cycle:.1f}%"
            )

    except KeyboardInterrupt:
        print("\nPWM interrompido pelo usuário.")

    finally:
        pwm.stop()
        GPIO.cleanup()
        print("PWM parado e GPIOs liberadas.")


if __name__ == "__main__":
    main()