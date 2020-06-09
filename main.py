import time
from machine import Pin, SPI


def hexPrint(array):
    print(''.join('{:02x}'.format(x) for x in array))


def sendCommand(command):
    nss.off()
    spi.write(command)
    nss.on()


def beep():
    command = bytearray(b'\x53\x3e\x00\x91')
    sendCommand(command)


def setChannel(ch):
    if 1 <= ch <= 8:
        command = bytearray(b'\x43\x3d\x01\x00\x00')
        command[4] = ch
        command[3] = (sum(command) & 0xFF)
        sendCommand(command)
    else:
        print("invalid input")


def setBand(band):
    if 1 <= band <= 7:
        command = bytearray(b'\x42\x3d\x01\x00\x00')
        command[4] = band
        command[3] = (sum(command) & 0xFF)
        sendCommand(command)
    else:
        print("invalid input")


def setOsdMode(mode):
    if 0 <= mode <= 10:
        command = bytearray(b'\x4f\x3d\x01\x00\x00')
        command[4] = mode
        command[3] = (sum(command) & 0xFF)
        hexPrint(command)
        sendCommand(command)
    else:
        print("invalid input")


def setOsdText(text):
    if len(text) <= 25:
        command = bytearray(b'\x54\x3d\x00\x00')
        command += bytearray(text)
        command[2] = len(text)
        command[3] = (sum(command) & 0xFF)
        hexPrint(command)
        sendCommand(command)
    else:
        print("invalid input")


# init pins
clk = Pin(0, Pin.OUT)
data = Pin(1, Pin.OUT)
nss = Pin(2, Pin.OUT)

# wait for RF to boot
time.sleep_ms(2000)

# enter SPI mode
clk.on()
data.on()
nss.on()
time.sleep_ms(300)
clk.off()
data.off()
nss.off()
time.sleep_ms(300)
nss.on()

# init SPI
spi = SPI(-1, baudrate=80000, polarity=0, phase=0,
          sck=clk, mosi=data, miso=Pin(14))

# beep when ready
beep()
