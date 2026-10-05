"""
SEL0337 - Projetos em Sistemas Embarcados
Prática 3 - Checkpoint 3

Aplicação concorrente com GPIO utilizando threading.

Funcionalidades:
- um LED pisca continuamente;
- um botão alterna a frequência do LED entre dois valores;
- o botão é tratado por detecção de eventos, sem polling;
- um Timer realiza a temporização em uma thread separada;
- ao final da temporização, um callback encerra a aplicação;
- um Lock protege o acesso à frequência compartilhada.

Autores:
João Vitor Miranda Sousa - NUSP 14802702
Fernando Shoji Ogusuku - NUSP 15636682
Eduardo Yumoto Carvalheira - NUSP 15636150
"""

import threading

import RPi.GPIO as GPIO


# ---------------------------------------------------------------------
# Configuração de hardware
# ---------------------------------------------------------------------

LED_GPIO = 17       # BCM 17 = pino físico 11
BOTAO_GPIO = 18     # BCM 18 = pino físico 12

FREQUENCIA_LENTA_HZ = 1.0
FREQUENCIA_RAPIDA_HZ = 5.0

DEBOUNCE_MS = 200


# ---------------------------------------------------------------------
# Recursos compartilhados entre as threads
# ---------------------------------------------------------------------

fim_programa = threading.Event()
lock_frequencia = threading.Lock()

frequencia_atual_hz = FREQUENCIA_LENTA_HZ


def solicitar_tempo() -> float:
    """Solicita e valida o tempo total de execução em segundos."""

    while True:
        entrada = input(
            "Digite o tempo da contagem, em segundos: "
        ).strip()

        try:
            tempo = float(entrada)

        except ValueError:
            print("Entrada inválida. Digite um valor numérico.")
            continue

        if tempo <= 0:
            print("O tempo deve ser maior que zero.")
            continue

        return tempo


def configurar_gpio() -> None:
    """Configura o LED e o botão utilizando numeração BCM."""

    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)

    GPIO.setup(
        LED_GPIO,
        GPIO.OUT,
        initial=GPIO.LOW,
    )

    GPIO.setup(
        BOTAO_GPIO,
        GPIO.IN,
        pull_up_down=GPIO.PUD_UP,
    )


def obter_frequencia() -> float:
    """Retorna a frequência atual de forma sincronizada."""

    with lock_frequencia:
        return frequencia_atual_hz


def alternar_frequencia(_canal: int) -> None:
    """
    Callback associado ao botão.

    Alterna a frequência do LED entre os valores lento e rápido.
    O Lock garante acesso exclusivo à variável compartilhada.
    """

    global frequencia_atual_hz

    with lock_frequencia:

        if frequencia_atual_hz == FREQUENCIA_LENTA_HZ:
            frequencia_atual_hz = FREQUENCIA_RAPIDA_HZ

        else:
            frequencia_atual_hz = FREQUENCIA_LENTA_HZ

        nova_frequencia = frequencia_atual_hz

    print(
        f"\nBotão pressionado -> "
        f"frequência = {nova_frequencia:.1f} Hz"
    )


def piscar_led() -> None:
    """Controla o pisca do LED enquanto a aplicação estiver ativa."""

    estado_led = False

    while not fim_programa.is_set():

        frequencia = obter_frequencia()

        # Cada alteração de estado corresponde a meio período.
        meio_periodo = 1.0 / (2.0 * frequencia)

        estado_led = not estado_led

        GPIO.output(
            LED_GPIO,
            GPIO.HIGH if estado_led else GPIO.LOW,
        )

        # Diferentemente de sleep(), Event.wait() permite que a thread
        # seja acordada imediatamente caso a aplicação seja encerrada.
        fim_programa.wait(meio_periodo)

    GPIO.output(LED_GPIO, GPIO.LOW)


def fim_contagem() -> None:
    """Callback executado automaticamente ao término do Timer."""

    print("\n\nContagem concluída.")
    print(
        "Callback do Timer executado "
        "-> encerrando a aplicação."
    )

    fim_programa.set()


def main() -> None:
    """Inicializa os periféricos e coordena as tarefas concorrentes."""

    tempo_total = solicitar_tempo()

    configurar_gpio()

    GPIO.add_event_detect(
        BOTAO_GPIO,
        GPIO.FALLING,
        callback=alternar_frequencia,
        bouncetime=DEBOUNCE_MS,
    )

    thread_led = threading.Thread(
        target=piscar_led,
        name="ThreadLED",
    )

    timer = threading.Timer(
        tempo_total,
        fim_contagem,
    )

    print("\nAplicação iniciada.")
    print(f"Tempo total: {tempo_total:.1f} s")
    print(
        f"Frequência inicial: "
        f"{FREQUENCIA_LENTA_HZ:.1f} Hz"
    )
    print(
        "Pressione o botão para alternar entre "
        f"{FREQUENCIA_LENTA_HZ:.1f} Hz e "
        f"{FREQUENCIA_RAPIDA_HZ:.1f} Hz."
    )
    print("Use CTRL+C para interromper antes do fim.\n")

    try:
        thread_led.start()
        timer.start()

        # Aguarda o Timer ou uma interrupção encerrar a aplicação.
        fim_programa.wait()

    except KeyboardInterrupt:
        print("\nPrograma interrompido pelo usuário.")

    finally:
        # Garante que todas as tarefas recebam o sinal de término.
        fim_programa.set()

        # Se o Timer ainda estiver ativo, ele é cancelado.
        timer.cancel()

        # Aguarda o término seguro da thread responsável pelo LED.
        thread_led.join()

        GPIO.remove_event_detect(BOTAO_GPIO)
        GPIO.output(LED_GPIO, GPIO.LOW)
        GPIO.cleanup()

        print("GPIOs liberadas. Programa finalizado.")


if __name__ == "__main__":
    main()