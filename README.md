# LoRa

## Python / Raspberry Pi 2
https://pypi.org/project/pyLoRa/

https://github.com/rpsreal/pySX127x

https://www.mouser.com/datasheet/2/761/down-767039.pdf

https://github.com/rpsreal/pySX127x/blob/master/LORA_CLIENT.py

```
 $ gpio readall
 +-----+-----+---------+------+---+---Pi 2---+---+------+---------+-----+-----+
 | BCM | wPi |   Name  | Mode | V | Physical | V | Mode | Name    | wPi | BCM |
 +-----+-----+---------+------+---+----++----+---+------+---------+-----+-----+
 |     |     |    3.3v |      |   |  1 || 2  |   |      | 5v      |     |     |
 |   2 |   8 |   SDA.1 |   IN | 1 |  3 || 4  |   |      | 5v      |     |     |
 |   3 |   9 |   SCL.1 |   IN | 1 |  5 || 6  |   |      | 0v      |     |     |
 |   4 |   7 | GPIO. 7 |   IN | 0 |  7 || 8  | 1 | ALT0 | TxD     | 15  | 14  |
 |     |     |      0v |      |   |  9 || 10 | 1 | ALT0 | RxD     | 16  | 15  |
 |  17 |   0 | GPIO. 0 |  OUT | 1 | 11 || 12 | 0 | IN   | GPIO. 1 | 1   | 18  |
 |  27 |   2 | GPIO. 2 |   IN | 0 | 13 || 14 |   |      | 0v      |     |     |
 |  22 |   3 | GPIO. 3 |   IN | 0 | 15 || 16 | 0 | IN   | GPIO. 4 | 4   | 23  |
 |     |     |    3.3v |      |   | 17 || 18 | 0 | IN   | GPIO. 5 | 5   | 24  |
 |  10 |  12 |    MOSI | ALT0 | 0 | 19 || 20 |   |      | 0v      |     |     |
 |   9 |  13 |    MISO | ALT0 | 0 | 21 || 22 | 1 | OUT  | GPIO. 6 | 6   | 25  |
 |  11 |  14 |    SCLK | ALT0 | 0 | 23 || 24 | 1 | OUT  | CE0     | 10  | 8   |
 |     |     |      0v |      |   | 25 || 26 | 1 | OUT  | CE1     | 11  | 7   |
 |   0 |  30 |   SDA.0 |   IN | 1 | 27 || 28 | 1 | IN   | SCL.0   | 31  | 1   |
 |   5 |  21 | GPIO.21 |   IN | 1 | 29 || 30 |   |      | 0v      |     |     |
 |   6 |  22 | GPIO.22 |   IN | 1 | 31 || 32 | 0 | IN   | GPIO.26 | 26  | 12  |
 |  13 |  23 | GPIO.23 |   IN | 0 | 33 || 34 |   |      | 0v      |     |     |
 |  19 |  24 | GPIO.24 |   IN | 0 | 35 || 36 | 0 | IN   | GPIO.27 | 27  | 16  |
 |  26 |  25 | GPIO.25 |   IN | 0 | 37 || 38 | 0 | IN   | GPIO.28 | 28  | 20  |
 |     |     |      0v |      |   | 39 || 40 | 0 | IN   | GPIO.29 | 29  | 21  |
 +-----+-----+---------+------+---+----++----+---+------+---------+-----+-----+
 | BCM | wPi |   Name  | Mode | V | Physical | V | Mode | Name    | wPi | BCM |
 +-----+-----+---------+------+---+---Pi 2---+---+------+---------+-----+-----+
```

| RFM95 | Raspi 2, physical pin number in gpio header |
| --- | --- |
| MISO (SPI) (ruskea) | 21 (*GPIO9) |
| MOSI (SPI) (oranssi) | 19 (*GPIO10) |
| SCK/SCLK (SPI) (keltainen) | 23 (*GPIO11) |
| RESET (sininen) | 15 (*GPIO22) |
| NSS/SS/CS (SPI) (vihreä) | 24 (*GPIO8) |
| DIO0 (IRQ) (harmaa) | 7 (*GPIO4) |
| GND (musta) | 6 |
| 3.3V (punainen) | 1 |
| Optional: |
| DIO1 (purppura) | 11 (*GPIO17) |
| DIO2 (valkoinen) | 12 (*GPIO18) |
| DIO3 (valko/sini) | 13 (*GPIO27) |
| LED | 33 (*GPIO13) |

**Notice! Python uses \*GPIO-numbers, but they are not same GPIO's as in pinout-charts. \*GPIO's are BCM-numbers.**

## Arduino IDE / ESP8266 / Wemos

https://wiki.wemos.cc/products:retired:d1_mini_v2.2.0

### ESP8266 support for Aduino IDE

Start Arduino and open the Preferences window. Enter https://arduino.esp8266.com/stable/package_esp8266com_index.json into the Additional Board Manager URLs field (you can add multiple URLs, separating them with commas).
Open Boards Manager from Tools > Board menu and install esp8266 platform.

### Libraries
- LoRa by Sandeep Mistry (0.7.0)
  - https://github.com/sandeepmistry/arduino-LoRa
  - https://github.com/sandeepmistry/arduino-LoRa/blob/master/API.md
- Optional: DHT sensor library for ESPx by beegee_tokyo 1.17.0


### Arduino IDE settings
Select right board from board settings (in my case "LOLIN(WEMOS) D1 R2 & mini"). Wrong board might give weird results.

### Wiring
RFM95 | Wemos D1 R2 & mini
--- | ---
MISO (SPI) | D6 (GPIO12)
MOSI (SPI) | D7 (GPIO13)
SCK/SCLK (SPI) | D5 (GPIO14)
NSS/SS/CS (SPI) | D8 (GPIO15)
RESET | D2 (GPIO4)
DIO0 (IRQ) | D1 (GPIO5)
GND | G
3.3V | 3V3

### Wemos pinout

NodeMCU | GPIO | notes
--- | --- | ---
D0 | GPIO16 | Ei tue keskeytyksiä. Ei ylösvetovastusominaisuutta. Ei PWM:ää. Käytetään syväunesta heräämiseen kytkemällä tämä RST:hen. Joissain moduuleissa user-nappi.
D1 | GPIO5 |
D2 | GPIO4 |
D3 | GPIO0 | Flash-moodi. Flash-nappi NodeMCU-moduulissa. Pitää olla ylhäällä bootatessa normaalisti.
D4 | GPIO2 | Pitää olla ylhäällä bootatessa. Sininen LED NodeMCU:ssa.
D5 | GPIO14 | SCK
D6 | GPIO12 | MISO
D7 | GPIO13 | MOSI, sarjaportin vuonohjausta käytettäessä CTS.
D8 | GPIO15 | SS, boottilähteen valinta. Pitää olla alhaalla bootatessa normaalisti. Sarjaportin vuonohjausta käytettäessä RTS.
D9 | GPIO3 | Sarjaportin RX.
D10 | GPIO1 | Sarjaportin TX.


# Misc

RegSyncWord (0x39) 7-0 SyncWord rw 0x12 LoRa Sync Word
(Value 0x34 is reserved for LoRaWAN networks)

# RF 433MHz
Motonet Kauko-ohjattava ulkopistorasia IP44 3600W (38-4663) / EMAX 6867 ja 68671

- 230V AC, 50Hz
- 16A, 3600W
- Frequency: 433,92MHz
- Protection: IP44

button | code (0 = short, 1 = long)
--- | ---
A on |  011000111010011000001111 1101100000
A off | 011000111010011000001110 1101100100
B on |  011000111010011000001101 1101101100
B off | 011000111010011000001100 1101101000
C on |  011000111010011000001011 1101111100
C off | 011000111010011000001010 1101111000
D on |  011000111010011000000111 1101000000
D off | 011000111010011000000110 1101000100
All on | 011000111010011000000100 1101001000
All off | 011000111010011000001000 1101110000

- Code is 34 bits
- 34 bits take 38.8ms
- One bit take 1.141ms
- 0 (short): mark 300us + space 841us
- 1 (long): mark 815us + space 326us
- Remote sends code 6 times. About 10ms between codes.
