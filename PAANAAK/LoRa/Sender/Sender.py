from machine import Pin,SPI
from LoRa.sx127x import SX127x
from LoRa import LoRaSender

lora_default = {
    'frequency': 433000000,           # Set frequency to 433 MHz (433000000 Hz)
    'frequency_offset': 0,
    'tx_power_level': 14,             # Transmit power level
    'signal_bandwidth': 125e3,        # Bandwidth (125 kHz)
    'spreading_factor': 9,            # SF9 (spreading factor)
    'coding_rate': 5,                 # Coding rate (4/5)
    'preamble_length': 8,             # Preamble length
    'implicitHeader': False,          # Implicit header mode disabled
    'sync_word': 0x12,                # Sync word (default value)
    'enable_CRC': True,               # Enable CRC for error detection
    'invert_IQ': False,               # Invert IQ (set to False unless needed)
    'debug': False,                   # Set debug mode to False for normal operation
}


lora_pins = {
    'dio_0': 32,     # DIO0 pin (interrupt pin)
    'ss': 33,        # Chip select (SS) pin
    'reset': 19,     # Reset pin
    'sck': 14,       # SPI clock pin (SCK)
    'miso': 12,      # SPI MISO pin (Master In Slave Out)
    'mosi': 13,      # SPI MOSI pin (Master Out Slave In)
}

lora_spi = SPI(
    baudrate=10000000, polarity=0, phase=0,
    bits=8, firstbit=SPI.MSB,
    sck=Pin(lora_pins['sck'], Pin.OUT, Pin.PULL_DOWN),
    mosi=Pin(lora_pins['mosi'], Pin.OUT, Pin.PULL_UP),
    miso=Pin(lora_pins['miso'], Pin.IN, Pin.PULL_UP),
)

lora = SX127x(lora_spi, pins=lora_pins, parameters=lora_default)

type = 'sender'

if __name__ == '__main__':
    if type == 'sender':
        LoRaSender.send(lora)

