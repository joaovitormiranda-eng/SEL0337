/*
 * SEL0337 - Projetos em Sistemas Embarcados
 * Pratica 4 - Checkpoint 2
 * Leitura analogica no Arduino e transmissao I2C para Raspberry Pi
 *
 * Arquitetura:
 *   Arduino Uno  -> responder I2C no endereco 0x08
 *   Potenciometro -> entrada analogica A0
 *   Raspberry Pi -> controladora I2C
 *
 * Protocolo de dados:
 *   O valor ADC possui 10 bits (0..1023).
 *   A cada requisicao I2C, o Arduino envia dois bytes:
 *     byte 0 = parte alta (high byte)
 *     byte 1 = parte baixa (low byte)
 *
 * A Raspberry Pi reconstrui:
 *   valor = (byte_alto << 8) | byte_baixo
 *
 * Autores:
 * Joao Vitor Miranda Sousa - NUSP 14802702
 * Fernando Shoji Ogusuku - NUSP 15636682
 * Eduardo Yumoto Carvalheira - NUSP 15636150
 */

#include <Wire.h>

namespace {

constexpr uint8_t I2C_ADDRESS = 0x08;
constexpr uint8_t POT_PIN = A0;
constexpr unsigned long SERIAL_BAUD = 9600;
constexpr unsigned long SAMPLE_INTERVAL_MS = 20;

volatile uint16_t latestAdcValue = 0;
volatile uint16_t lastSentValue = 0;
volatile bool requestServed = false;

unsigned long lastSampleMs = 0;

}  // namespace


void onI2CReceive(int byteCount) {
  /*
   * Algumas operacoes SMBus da Raspberry enviam um byte de comando
   * antes da leitura. Neste checkpoint esse byte nao representa um
   * registrador real, portanto ele apenas e descartado.
   */
  while (byteCount-- > 0 && Wire.available() > 0) {
    (void)Wire.read();
  }
}


void onI2CRequest() {
  /*
   * Envia o ultimo valor ADC completo em dois bytes.
   * A ordem escolhida e: byte alto primeiro, byte baixo depois.
   */
  const uint16_t value = latestAdcValue;

  const uint8_t payload[2] = {
      highByte(value),
      lowByte(value),
  };

  Wire.write(payload, sizeof(payload));

  lastSentValue = value;
  requestServed = true;
}


void setup() {
  pinMode(POT_PIN, INPUT);

  Serial.begin(SERIAL_BAUD);

  // Primeira leitura antes de disponibilizar o responder I2C.
  latestAdcValue = analogRead(POT_PIN);

  Wire.begin(I2C_ADDRESS);
  Wire.onReceive(onI2CReceive);
  Wire.onRequest(onI2CRequest);

  Serial.println(F("==================================================="));
  Serial.println(F("SEL0337 - Pratica 4 - Checkpoint 2"));
  Serial.println(F("Arduino Uno -> responder I2C"));
  Serial.print(F("Endereco I2C: 0x"));
  Serial.println(I2C_ADDRESS, HEX);
  Serial.println(F("Potenciometro conectado em A0"));
  Serial.println(F("Aguardando requisicoes da Raspberry Pi..."));
  Serial.println(F("==================================================="));
}


void loop() {
  const unsigned long now = millis();

  // Atualiza continuamente a leitura analogica.
  if (now - lastSampleMs >= SAMPLE_INTERVAL_MS) {
    lastSampleMs = now;

    const uint16_t sample = static_cast<uint16_t>(analogRead(POT_PIN));

    // Protege a escrita da variavel de 16 bits contra interrupcao
    // durante a atualizacao.
    noInterrupts();
    latestAdcValue = sample;
    interrupts();
  }

  /*
   * O callback I2C apenas registra que uma resposta foi enviada.
   * A escrita na Serial e feita aqui, fora do callback.
   */
  bool shouldPrint = false;
  uint16_t sentValue = 0;

  noInterrupts();
  if (requestServed) {
    sentValue = lastSentValue;
    requestServed = false;
    shouldPrint = true;
  }
  interrupts();

  if (shouldPrint) {
    Serial.print(F("ADC enviado: "));
    Serial.println(sentValue);
  }
}
