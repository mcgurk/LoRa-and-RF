#!/usr/bin/env python3

import time
from datetime import datetime
import struct
from SX127x.LoRa import *
from SX127x.board_config import BOARD

BOARD.setup()
BOARD.reset()

c = 0

from threading import Timer

class RepeatTimer(Timer):
  def run(self):
    while not self.finished.wait(self.interval):
      self.function(*self.args, **self.kwargs)

def watchdog():
  global c
  if c != -1: # -1 = already off
    if c == 0: # 0 = watchdog triggers
      BOARD.led_off()
      print("OFF")
    c -= 1

timer = RepeatTimer(1, watchdog)
timer.start()

class mylora(LoRa):
    def __init__(self, verbose=False):
        super(mylora, self).__init__(verbose)
        self.set_mode(MODE.SLEEP)
        self.set_dio_mapping([0] * 6)

    def on_rx_done(self):
        BOARD.led_on()
        print("\nRxDone")
        print(datetime.now())
        #print(self.get_irq_flags())
        #print(self.spi.xfer([0x1C, 0])[1]) # REG.LORA.MODEM_CONFIG_2
        if not self.get_hop_channel()['crc_on_payload']:
          print("No CRC in payload!")
        if not self.get_irq_flags()['valid_header']:
          print("Invalid header in payload!")
        if self.get_irq_flags()['rx_timeout']:
          print("rx timeout!")
        if self.get_irq_flags()['crc_error']:
          print("crc_error!")
        self.clear_irq_flags(RxDone=1, ValidHeader=1)
        payload = self.read_payload(nocheck=False)
        print("pkt_rssi: ", self.get_pkt_rssi_value())
        print("pkt_snr: ", self.get_pkt_snr_value())
        print ("Receive: ")
        print(payload)
        if (payload):
          print("counter:", payload[0])
          (t, h) = struct.unpack('<hh', bytearray(payload[1:5]))
          print(t/10.0, "  C")
          print(h/10.0, "%rh")
        global c
        c = 60
        time.sleep(2)
        self.reset_ptr_rx()
        self.set_mode(MODE.RXCONT)

    def on_tx_done(self):
        print("\nTxDone")
        print(self.get_irq_flags())

    def on_cad_done(self):
        print("\non_CadDone")
        print(self.get_irq_flags())

    def on_rx_timeout(self):
        print("\non_RxTimeout")
        print(self.get_irq_flags())

    def on_valid_header(self):
        print("\non_ValidHeader")
        print(self.get_irq_flags())

    def on_payload_crc_error(self):
        print("\non_PayloadCrcError")
        print(self.get_irq_flags())

    def on_fhss_change_channel(self):
        print("\non_FhssChangeChannel")
        print(self.get_irq_flags())

    def start(self):
        while True:
            self.reset_ptr_rx()
            self.set_mode(MODE.RXCONT) # Receiver mode
            print(datetime.now())
            while True:
                print(c)
                time.sleep(2)
                #pass;

#lora = mylora(verbose=False)
lora = mylora(verbose=True)
#lora.set_pa_config(pa_select=1, max_power=21, output_power=15)
lora.set_freq(868.0)
lora.set_bw(BW.BW125)
lora.set_spreading_factor(10)
lora.set_sync_word(0x77)

print(datetime.now())

assert(lora.get_agc_auto_on() == 1)

try:
    print("START")
    lora.start()
except KeyboardInterrupt:
    sys.stdout.flush()
    print("Exit")
    sys.stderr.write("KeyboardInterrupt\n")
finally:
    sys.stdout.flush()
    timer.cancel()
    print("Exit")
    lora.set_mode(MODE.SLEEP)
BOARD.teardown()
