"""SEL0337 — Projetos em Sistemas Embarcados
Prática 3 — Checkpoint 2
Programa 1 — Controle de LED por PWM.

Autores:
    João Vitor Miranda Sousa — NUSP 14802702
    Fernando Shoji Ogusuku — NUSP 15636682
    Eduardo Yumoto Carvalheira — NUSP 15636150

Hardware:
    - LED: GPIO17 (BCM), pino físico 11

A aplicação permite alterar, pelo terminal, a frequência e o duty cycle
do sinal PWM para observação no LED e no osciloscópio.
"""

import RPi.GPIO as GPIO


LED_GPIO = 17
FREQUENCIA_INICIAL_HZ = 100.0
DUTY_INICIAL_PERCENTUAL = 0.0


def solicitar_float(mensagem: str) -> float:
    """Solicita um valor numérico ao usuário."""
    while True:
        try:
            return float(input(mensagem))
        except ValueError:
            print("Erro: digite um valor numérico.")


def solicitar_parametros_pwm() -> tuple[float, float]:
    """Solicita e valida frequência e duty cycle."""
    while True:
        frequencia = solicitar_float("\nFrequência [Hz]: ")
        duty_cycle = solicitar_float("Duty cycle [%]: ")

        if frequencia <= 0:
            print("Erro: a frequência deve ser maior que zero.")
            continue

        if not 0 <= duty_cycle <= 100:
            print("Erro: o duty cycle deve estar entre 0 e 100%.")
            continue

        return frequencia, duty_cycle


def main() -> None:
    """Inicializa o PWM e processa novas configurações até CTRL+C."""
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(LED_GPIO, GPIO.OUT, initial=GPIO.LOW)

    pwm = GPIO.PWM(LED_GPIO, FREQUENCIA_INICIAL_HZ)
    pwm.start(DUTY_INICIAL_PERCENTUAL)

    print("PWM iniciado.")
    print("Testes sugeridos:")
    print("  100 Hz / 25%")
    print("  100 Hz / 50%")
    print("  100 Hz / 75%")
    print("  500 Hz / 50%")
    print("  1000 Hz / 50%")
    print("Pressione CTRL+C para encerrar.")

    try:
        while True:
            frequencia, duty_cycle = solicitar_parametros_pwm()
            pwm.ChangeFrequency(frequencia)
            pwm.ChangeDutyCycle(duty_cycle)
            print(
                f"Aplicado: frequência = {frequencia:.1f} Hz | "
                f"duty cycle = {duty_cycle:.1f}%"
            )
    except KeyboardInterrupt:
        print("\nPWM interrompido pelo usuário.")
    finally:
        pwm.stop()
        GPIO.cleanup()
        print("PWM parado e GPIO.cleanup() executado.")


if __name__ == "__main__":
    main()
