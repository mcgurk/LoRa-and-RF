#define GPIO 5 // D1

volatile uint32_t counter = 0;
volatile uint32_t last_micros = 0;
volatile uint8_t flag = 0;
volatile uint8_t p = 0;
volatile uint8_t receiving = 0; 
uint32_t old_counter = 0;
volatile uint32_t buf[28];

ICACHE_RAM_ATTR void ISR() {
  counter++;
  static volatile uint32_t delta;
  uint32_t new_micros = micros();
  delta = new_micros - last_micros;
  last_micros = new_micros;

  if ( (delta < 2400) || (delta > 10100) ) {
    receiving = 0;
    return;
  }
  if ( (delta > 10000) && (delta < 10040) ) {
    p = 0;
    receiving = 1;
    return;
  }
  if (receiving) {
    buf[p++] = delta;
    if (p == 28) {
      flag = 1;
      receiving = 0;
    }
  }

}

void setup() {
  Serial.begin(115200);
  while(!Serial);
  attachInterrupt(digitalPinToInterrupt(GPIO), ISR, RISING);
}

//char message[29];
uint32_t message;

void loop() {
  if (flag) {
    for (int i = 0; i < 28; i++) {
      //uint8_t b = (buf[i] > 4000) ? 1 : 0;
      //bitWrite(message, 27-i, b);
      bitWrite(message, 27-i, ((buf[i] > 4000) ? 1 : 0) );
      //bitWrite(message, 27-i, 1);
    }
    Serial.println(message, BIN);
    flag = 0;
    //Serial.println("HEP!");
    /*for (int i = 0; i < 28; i++) {
      Serial.print(" ");
      Serial.print(buf[i]);
    }
    Serial.println();
    //Serial.print("Millis: "); Serial.print(millis()); Serial.print(" delta: "); Serial.println(delta);
    flag = 0;*/
  }
  /*uint32_t temp = counter;
  Serial.println(temp-old_counter);
  old_counter = temp;
  delay(1000);*/
}