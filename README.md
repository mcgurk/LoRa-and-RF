# LoRa
- https://www.mouser.com/datasheet/2/761/down-767039.pdf

## LoRa Python links
- https://pypi.org/project/pyLoRa/
- https://github.com/rpsreal/pySX127x
- https://github.com/rpsreal/pySX127x/blob/master/LORA_CLIENT.py

## Raspberry Pi
[Raspberry Pi](RASPBERRYPI.md)
## Orange Pi
[Orange Pi](ORANGEPI.md)



## Arduino IDE / ESP8266 / Wemos

https://wiki.wemos.cc/products:retired:d1_mini_v2.2.0

### ESP8266 support for Aduino IDE

Start Arduino and open the Preferences window. Enter https://arduino.esp8266.com/stable/package_esp8266com_index.json into the Additional Board Manager URLs field (you can add multiple URLs, separating them with commas).
Open Boards Manager from Tools > Board menu and install esp8266 platform.

### Libraries
- RadioLib by Jan Gromes (4.0.3)
  - https://github.com/jgromes/RadioLib
  - https://jgromes.github.io/RadioLib/
- Optional: DHT sensor library for ESPx by beegee_tokyo 1.17.0


### Arduino IDE settings
Select right board from board settings (in my case "LOLIN(WEMOS) D1 R2 & mini"). Wrong board might give weird results.

### Wiring

#### LED for free use and I<sup>2</sup>C unaccessible
RFM95 | Direction | ESP8266/Wemos/NodeMCU | ESP32
--- | --- | --- | ---
MISO/SDO (SPI) (brown ![#brown](https://placehold.it/10/c68c53/000000?text=+)) | &leftarrow; | D6 (GPIO12) (SPI MISO) | GPIO19 (VSPI MISO)
MOSI/SDI (SPI) (orange ![#orange](https://placehold.it/10/ff8000/000000?text=+)) | &rightarrow; | D7 (GPIO13) (SPI MOSI) | GPIO23 (VSPI MOSI)
SCK/SCLK (SPI) (yellow ![#yellow](https://placehold.it/10/ffff00/000000?text=+)) | &leftarrow; | D5 (GPIO14) (SPI SCLK) | GPIO18 (VSPI SCLK)
NSS/SS/CS (SPI) (green ![#green](https://placehold.it/10/00ff00/000000?text=+)) | &leftarrow; | D8 (GPIO15) | GPIO5
RESET (blue ![#blue](https://placehold.it/10/0000ff/000000?text=+)) | &leftarrow; | D3 (GPIO0) | GPIO22
DIO0 (IRQ) (grey ![#grey](https://placehold.it/10/999999/000000?text=+)) | &rightarrow; | D2 (GPIO4) | GPIO21
GND (black ![#black](https://placehold.it/10/000000/000000?text=+)) | | G | GND
3.3V (red ![#red](https://placehold.it/10/ff0000/000000?text=+)) | | 3V3 | 3V3
ANA/ANT | | Antenna (86mm) |

#### Alternative wiring for ESP8266: LED used as CS and I<sup>2</sup>C useable
RFM95 | Direction | ESP8266/Wemos/NodeMCU
--- | --- | ---
MISO/SDO (SPI) (brown ![#brown](https://placehold.it/10/c68c53/000000?text=+)) | &leftarrow; | D6 (GPIO12) (SPI MISO)
MOSI/SDI (SPI) (orange ![#orange](https://placehold.it/10/ff8000/000000?text=+)) | &rightarrow; | D7 (GPIO13) (SPI MOSI)
SCK/SCLK (SPI) (yellow ![#yellow](https://placehold.it/10/ffff00/000000?text=+)) | &leftarrow; | D5 (GPIO14) (SPI SCLK)
NSS/SS/CS (SPI) (green ![#green](https://placehold.it/10/00ff00/000000?text=+)) | &leftarrow; | D4 (GPIO2)
RESET (blue ![#blue](https://placehold.it/10/0000ff/000000?text=+)) | &leftarrow; | D3 (GPIO0)
DIO0 (IRQ) (grey ![#grey](https://placehold.it/10/999999/000000?text=+)) | &rightarrow; | D8 (GPIO15)
GND (black ![#black](https://placehold.it/10/000000/000000?text=+)) | | G
3.3V (red ![#red](https://placehold.it/10/ff0000/000000?text=+)) | | 3V3
ANA/ANT | | Antenna (86mm)

**Warning:** if DIO0 interrupt signal is triggered, ESP8266 doesn't boot up. This is safe wiring only if interrupt is not used.

#### Deepsleep
ESP8266/Wemos/NodeMCU | Direction | ESP8266/Wemos/NodeMCU | notes
--- | --- | --- | ---
D0 (GPIO16) (violet ![#violet](https://placehold.it/10/cc0066/000000?text=+)) | &rightarrow; | RST (ESP8266) | unconnect when flashing!

#### Reset
High-Z = normal, low (>100us) = reset. Notice that Wemos/NodeMCU has pullup resistor for D3 and D4 and pulldown resistor for D8, so those cannot be in High-Z-state.  Nevertheless it looks like D3 and D4 works for reset.
#### DIO0/IRQ
Normally low, high when active. DIO0 could be connected to D8, but then there is small risk that SX1276 interrupt is triggered when ESP8266 resets itself. Then D8 would be up and ESP8266 would not boot.

### Wemos/NodeMCU pinout

Wemos/NodeMCU | GPIO | use | notes
--- | --- | --- | ---
D0 | GPIO16 | in/out | No interrupts, no pullup feature, no PWM. Used to wake up from deepsleep. User-button is sometimes connected to this.
D1 | GPIO5 | in/out/SCL | I<sup>2</sup>C (ESP32: GPIO22)
D2 | GPIO4 | in/out/SDA | I<sup>2</sup>C (ESP32: GPIO21)
D3 | GPIO0 | out | Flash-mode. Flash-button in some modules. Must be high at boot up (boot mode selection).
D4 | GPIO2 | out/led | Must be high at boot up (boot mode selection). Blue led in Wemos and NodeMCU.
D5 | GPIO14 | in/out/SCK | SPI
D6 | GPIO12 | in/out/MISO | SPI
D7 | GPIO13 | in/out/MOSI | SPI, if serial port flow control is used, this is CTS.
D8 | GPIO15 | out | Must be low at boot up (boot mode selection). If serial port flow control is used, this is RTS.
D9 | GPIO3 | x | Serial RX.
D10 | GPIO1 | x | Serial TX.

#### Using D9/GPIO/RX for your own uses (TX is D10/GPIO1)
https://github.com/esp8266/Arduino/issues/2430
```
Serial.begin(115200, SERIAL_8N1, SERIAL_TX_ONLY, D10);
```

## Misc

RegSyncWord (0x39) 7-0 SyncWord rw 0x12 LoRa Sync Word
(Value 0x34 is reserved for LoRaWAN networks)

# RF 433MHz

### Motonet
Motonet Kauko-ohjattava ulkopistorasia IP44 3600W (38-4663) / EMAX 6867 ja 68671

- 230V AC, 50Hz
- 16A, 3600W
- Frequency: 433,92MHz
- Protection: IP44
- For some reason, Arduino IDE rc-switch library example (simple and advance) didn't get anything.

button | code (0 = short, 1 = long)
--- | ---
A on |  01100011101001100000 1111 1101 1000 00
A off | 01100011101001100000 1110 1101 1001 00
B on |  01100011101001100000 1101 1101 1011 00
B off | 01100011101001100000 1100 1101 1010 00
C on |  01100011101001100000 1011 1101 1111 00
C off | 01100011101001100000 1010 1101 1110 00
D on |  01100011101001100000 0111 1101 0000 00
D off | 01100011101001100000 0110 1101 0001 00
All on | 01100011101001100000 0100 1101 0010 00
All off | 01100011101001100000 1000 1101 1100 00

- Code is 34 bits
- 34 bits take 38.8ms
- One bit takes 1.141ms
- 0 (short): mark 300µs + space 841µs
- 1 (long): mark 815µs + space 326µs
- Remote sends code 6 times. About 10ms between codes.

### LIDL
TR-502MSV
- Code is 21 bits
- 0 (short): space 1300µs + mark 600µs
- 1 (long): space 600µs + mark 1300µs
- Remote sends code 4 times. About 80ms between codes.
- 21 bits (13+2+4+2)
- 13 bits identification: randomly selected when reset button is pressed from remot
- 2 bit address: 11 = 1, 01 = 2, 10 = 3, 00 = 4 (dim sends last pressed BtnID and if "all" is pressed BtnID is 00)
- 4 bit opcode: 1011 = on, 1111 = off, 1101 = dim+, 1001 = dim-, 0011 = all on, 0111 = all off
- 2 bit checksum: last 3 bitpairs xorred with each other
Examples:

Button | RemoteID | BtnID | OpCode | Chksum
--- | --- | --- | --- | ---
1 on |  0011011101101 | 11 | 1011 | 10
1 off | 0011011101101 | 11 | 1111 | 11
2 on |  0011011101101 | 01 | 1011 | 00
2 off | 0011011101101 | 01 | 1111 | 01

## Python serial

sudo apt install python3-serial

```
#!/usr/bin/env python3

import serial, time, sys

#print('Number of arguments:', len(sys.argv), 'arguments.')
#print('Argument List:', str(sys.argv))

ser = serial.Serial('/dev/ttyUSB0', 115200)
#print(ser)
if sys.argv[1] == "on":
  print("on")
  ser.write(b'011000111010011000001111 1101100000')
if sys.argv[1] == "off":
  print("off")
  ser.write(b'011000111010011000001110 1101100100')

#ser.write(b'011000111010011000001111 1101100000')
#time.sleep(5)
#ser.write(b'011000111010011000001110 1101100100')
ser.close()

```

## Python rpi-rf
```
apt-get install python3-pip
sudo pip3 install rpi-rf

/usr/local/lib/python3.7/dist-packages/rpi_rf/rpi_rf.py:
            Protocol(350, 0, 100, 3, 8, 8, 3))

# Raspberry Pi 4: 350,0,100,3,8,8,3 (-p 100) -> 1:792 high 383 low 0:277 high 895 low
# rpi-rf_send doesn't use protocol first parameter in source file. must be given with rpi-rf_send parameter.

sleep 1; rpi-rf_send -g 17 -p 100 -t 7 -l 34 6687308644; sleep 1; rpi-rf_send -g 17 -p 100 -t 8 -l 34 6687309664
```
