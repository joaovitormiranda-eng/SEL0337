/*
 * SEL0337 - Projetos em Sistemas Embarcados
 * Prática 4 - Protocolos de Comunicação em Sistemas Embarcados de Alto Nível
 * Checkpoint 1 - Comunicação I2C entre Raspberry Pi e Arduino Uno
 *
 * Arduino Uno configurado como dispositivo I2C responder.
 *
 * Comportamento:
 *   1 -> acende o LED_BUILTIN
 *   0 -> apaga o LED_BUILTIN
 *
 * Quando solicitado pela controladora, o Arduino também retorna
 * o estado atual do LED:
 *   1 -> LED aceso
 *   0 -> LED apagado
 *
 * Endereço I2C: 0x08
 *
 * Autores:
 * João Vitor Miranda Sousa - NUSP 14802702
 * Fernando Shoji Ogusuku - NUSP 15636682
 * Eduardo Yumoto Carvalheira - NUSP 15636150
 */

#include <Wire.h>


// -----------------------------------------------------------------------------
// Configurações
// -----------------------------------------------------------------------------

namespace {

constexpr uint8_t I2C_ADDRESS = 0x08;
constexpr unsigned long SERIAL_BAUD = 9600;

// Variáveis compartilhadas entre os callbacks I2C e o loop principal.
volatile uint8_t receivedCommand = 0;
volatile bool commandAvailable = false;
volatile uint8_t ledState = LOW;

}  // namespace


// -----------------------------------------------------------------------------
// Callbacks I2C
// -----------------------------------------------------------------------------

void onI2CReceive(int byteCount) {
  /*
   * Callback executado quando a Raspberry Pi envia dados ao Arduino.
   *
   * O processamento é mantido curto: apenas o último byte recebido
   * é armazenado para posterior tratamento no loop principal.
   */

  (void)byteCount;

  while (Wire.available() > 0) {
    receivedCommand = static_cast<uint8_t>(Wire.read());
    commandAvailable = true;
  }
}


void onI2CRequest() {
  /*
   * Callback executado quando a Raspberry Pi solicita informação.
   *
   * Retorna em um único byte o estado atual do LED.
   */

  Wire.write(ledState == HIGH ? 1 : 0);
}


// -----------------------------------------------------------------------------
// Inicialização
// -----------------------------------------------------------------------------

void setup() {
  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, LOW);
  ledState = LOW;

  Serial.begin(SERIAL_BAUD);

  // Configura o Arduino como dispositivo I2C responder.
  Wire.begin(I2C_ADDRESS);

  // Registra os callbacks de recepção e requisição.
  Wire.onReceive(onI2CReceive);
  Wire.onRequest(onI2CRequest);

  Serial.println(F("============================================"));
  Serial.println(F("SEL0337 - Pratica 4 - Checkpoint 1"));
  Serial.println(F("Arduino Uno -> responder I2C"));
  Serial.print(F("Endereco I2C: 0x"));
  Serial.println(I2C_ADDRESS, HEX);
  Serial.println(F("Aguardando comandos da Raspberry Pi..."));
  Serial.println(F("============================================"));
}


// -----------------------------------------------------------------------------
// Loop principal
// -----------------------------------------------------------------------------

void loop() {
  bool processCommand = false;
  uint8_t command = 0;

  /*
   * Copia de forma protegida os dados compartilhados com o callback I2C.
   * O processamento propriamente dito ocorre fora da seção crítica.
   */
  noInterrupts();

  if (commandAvailable) {
    command = receivedCommand;
    commandAvailable = false;
    processCommand = true;
  }

  interrupts();

  if (!processCommand) {
    return;
  }

  if (command == 1) {
    digitalWrite(LED_BUILTIN, HIGH);
    ledState = HIGH;

    Serial.println(
        F("Comando recebido: 1 -> LED_BUILTIN ACESO")
    );

  } else if (command == 0) {
    digitalWrite(LED_BUILTIN, LOW);
    ledState = LOW;

    Serial.println(
        F("Comando recebido: 0 -> LED_BUILTIN APAGADO")
    );

  } else {
    Serial.print(F("Comando recebido e ignorado: "));
    Serial.println(command);
  }
}