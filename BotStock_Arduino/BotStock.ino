#include <Servo.h>

Servo garra;

const int LED1 = 12;
const int LED2 = 11;
const int LED3 = 10;
const int LED4 = 9;
const int LED5 = 8;

int posAtual = 180;

void setup() {
  Serial.begin(9600);

  garra.attach(A5);
  garra.write(posAtual);

  pinMode(LED1, OUTPUT);
  pinMode(LED2, OUTPUT);
  pinMode(LED3, OUTPUT);
  pinMode(LED4, OUTPUT);
  pinMode(LED5, OUTPUT);
}

void piscarLed(int pino) {
  for (int i = 0; i < 20; i++) {
    digitalWrite(pino, HIGH);
    delay(250);
    digitalWrite(pino, LOW);
    delay(250);
  }
}

void loop() {

  if (Serial.available()) {

    String cmd = Serial.readStringUntil('\n');
    cmd.trim();

    if (cmd == "OPEN") {
      garra.write(180);
      posAtual = 180;
    }

    else if (cmd == "CLOSE") {
      garra.write(150);
      posAtual = 150;
    }

    else if (cmd == "B1") {
      piscarLed(LED1);
    }

    else if (cmd == "B2") {
      piscarLed(LED2);
    }

    else if (cmd == "B3") {
      piscarLed(LED3);
    }

    else if (cmd == "B4") {
      piscarLed(LED4);
    }

    else if (cmd == "B5") {
      piscarLed(LED5);
    }
  }
}
