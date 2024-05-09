from machine import UART

uart = UART(2, baudrate=9600, tx=17, rx=16)  # Adjust UART number, baud rate, tx, and rx pins

while True:
    data = uart.read(11)  # Read 11 bytes (adjust the number as needed)
    if data:
       #data = int(data)   //if we need integer Data
        text = data.decode('urf-8')
        print(text)
