"""SEL0337 — Projetos em Sistemas Embarcados
Prática 3 — Checkpoint 1
Programa 2 — Contagem regressiva com acionamento de LED.

Autores:
    João Vitor Miranda Sousa — NUSP 14802702
    Fernando Shoji Ogusuku — NUSP 15636682
    Eduardo Yumoto Carvalheira — NUSP 15636150

Requisitos implementados:
    - entrada pelo terminal;
    - conversão de tipo;
    - validação de entrada;
    - tratamento de ValueError;
    - modularização por funções;
    - contagem no formato MM:SS;
    - atualização da contagem na mesma linha;
    - acionamento do LED somente ao final da contagem.
"""

import time
from signal import pause

import RPi.GPIO as GPIO


LED_GPIO = 17


def solicitar_tempo() -> int:
    """Solicita ao usuário um tempo inteiro e positivo, em segundos."""
    while True:
        try:
            tempo = int(input("Digite o tempo da contagem em segundos: "))
        except ValueError:
            print("Erro: o valor digitado deve ser um número inteiro.")
            continue

        if tempo <= 0:
            print("Erro: o número deve ser positivo.")
            continue

        return tempo


def exibir_tempo(segundos_restantes: int) -> None:
    """Exibe o tempo no formato MM:SS, atualizando a mesma linha."""
    minutos, segundos = divmod(segundos_restantes, 60)
    print(
        f"\rTempo restante: {minutos:02d}:{segundos:02d}",
        end="",
        flush=True,
    )


def executar_contagem_regressiva(tempo: int) -> None:
    """Executa a contagem e acende o LED ao atingir zero."""
    for segundos_restantes in range(tempo, 0, -1):
        exibir_tempo(segundos_restantes)
        time.sleep(1)

    print("\rTempo restante: 00:00")
    GPIO.output(LED_GPIO, GPIO.HIGH)
    print("Contagem finalizada! LED aceso.")


def main() -> None:
    """Configura o GPIO e executa a contagem regressiva."""
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(LED_GPIO, GPIO.OUT, initial=GPIO.LOW)

    try:
        tempo = solicitar_tempo()
        executar_contagem_regressiva(tempo)

        print("O LED permanecerá aceso. Pressione CTRL+C para encerrar.")
        pause()
    except KeyboardInterrupt:
        print("\nPrograma interrompido pelo usuário.")
    finally:
        GPIO.cleanup()
        print("GPIO.cleanup() executado.")


if __name__ == "__main__":
    main()
