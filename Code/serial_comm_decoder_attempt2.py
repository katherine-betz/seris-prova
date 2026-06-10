import serial
import struct
import time

BAUD = 19200
PORT = b'/dev/ttyUSB0'

def establish_comms(ser):         
    ser.reset_input_buffer()

    ser.dtr = False
    ser.rts = False
    time.sleep(0.5)

    ser.dtr = True
    ser.rts = True
    time.sleep(0.5)
    
    data = b''
    
    while (data != b'\x00\x00\x00'):
        print("Sending %")
        ser.write(b'%')

        time.sleep(0.5)

        data = ser.read(100)
        print("Reply:", data.hex())
        print(data)
    
    print("Sending setup")
    ser.write(b'S0000000400\r')

    time.sleep(1)

    data = ser.read(5000)
    print("Reply:", data.hex()) # will probably need to use these parameters at some point to figure out how it infulences decoder, if it does
    
def decode(dat, packet_size = 8):
    data = dat.hex()
    num_points = len(data)
    print("data length:", num_points)
    
    data_header = data[0:16]
    print("header", data_header)
    measurements = [data[i:i + packet_size] for i in range(16, num_points, packet_size)]
    print(measurements)

def autoscan(ser):
    data = ""
    while (data != b'\x05\x00'): #HERE -- check what type data is returned as, acknowledge is 0500
        print("Attempting autoscan")
        ser.write(b'A')

        time.sleep(1)
        data = ser.read(10000)
        print("Reply:", data.hex())

    time.sleep(10)
    packet = bytearray()

    while True:
        chunk = ser.read(4096)

        if not chunk:
            break

        packet.extend(chunk)

    print("Received", len(packet), "bytes")
    print(len(packet))

    words = []

    for i in range(0, len(packet), 4):
        if i + 4 <= len(packet):
            words.append(
                struct.unpack(">I", packet[i:i+4])[0]
            )
    for i in range(0, min(100, len(words))):
        print(i, words[i])
    
    return packet    

if __name__ == "__main__":
    ser = serial.Serial(
        '/dev/ttyUSB0',
        baudrate=BAUD,
        bytesize=8,
        parity='N',
        stopbits=1,
        timeout=1
    )
    
    establish_comms(ser)
    data = autoscan(ser)
    # data = b' 05 00 00 00 01 A1 00 00 00 8C 00 00 00 94 00 00 01 A1 00 00 00 00 00 00 01 A0 00 00 00 01 00 00 01 A0 00 00 00 02 00 00 01 A1 00 00 00 03 00 00 01 A0 00 00 00 04 00 00 01 A0 00 00 00 05 00 00 01 A1 00 00 00 06 00 00 01 A0 00 00 00 07 00 00 01 A0 00 00 00 08 00 00 01 A0 00 00 00 09 00 00 01 A1 00 00 00 0A 00 00 01 A1 00 00 00 0B 00 00 01 A0 00 00 00 0C 00 00 01 A0 00 00 00 0D 00 00 01 A0 00 00 00 0E 00 00 01 A0 00 00 00 0E 00 00 01 A0 00 00 00 0F 00 00 01 A0 00 00 00 10 00 00 01 A1 00 00 00 11 00 00 01 A1 00 00 00 12 00 00 01 A1 00 00 00 13 00 00 01 A1 00 00 00 14 00 00 01 A0 00 00 00 15 00 00 01 A0 00 00 00 16 00 00 01 A0 00 00 00 17 00 00 01 A0 00 00 00 18 00 00 01 A0 00 00 00 19 00 00 01 A1 00 00 00 1A 00 00 01 A1 00 00 00 1B 00 00 01 A0 00 00 00 1C 00 00 01 A0 00 00 00 1C 00 00 01 A1 00 00 00 1D 00 00 01 A1 00 00 00 1E 00 00 01 A0 00 00 00 1F 00 00 01 A0 00 00 00 20 00 00 01 A1 00 00 00 21 00 00 01 A0 00 00 00 22 00 00 01 A1 00 00 00 23 00 00 01 A0 00 00 00 24 00 00 01 A1 00 00 00 25 00 00 01 A0 00 00 00 26 00 00 01 A1 00 00 00 27 00 00 01 A0 00 00 00 28 00 00 01 A1 00 00 00 29 00 00 01 A0 00 00 00 2A 00 00 01 A0 00 00 00 2A 00 00 01 A1 00 00 00 2B 00 00 01 A0 00 00 00 2C 00 00 01 A0 00 00 00 2D 00 00 01 A1 00 00 00 2E 00 0 01 A1 00 00 00 2F 00 00 01 A0 00 00 00 30 00 00 01 A0 00 00 00 31 00 00 01 A0 00 00 00 32 00 00 01 A1 00 00 00 33 00 00 01 A1 00 00 00 34 00 00 01 A1 00 00 00 35 00 00 01 9E 00 00 00 36 00 00 01 9E 00 00 00 37 00 00 01 9E 00 00 00 38 00 00 01 9E 00 00 00 38 00 00 01 9D 00 00 00 39 00 00 01 9D 00 00 00 3A 00 00 01 9C 00 00 00 3B 00 00 01 9C 00 00 00 3C 00 00 01 9B 00 00 00 3D 00 00 01 9B 00 00 00 3E 00 00 01 9A 00 00 00 3F 00 00 01 9A 00 00 00 40 00 00 01 9A 00 00 00 41 00 00 01 99 00 00 00 42 00 00 01 98 00 00 00 43 00 00 01 98 00 00 00 44 00 00 01 98 00 00 00 45 00 00 01 97 00 00 00 46 00 00 01 97 00 00 00 46 00 00 01 96 00 00 00 47 00 00 01 96 00 00 00 48 00 00 01 96 00 00 00 49 00 00 01 95 00 00 00 4A 00 00 01 94 00 00 00 4B 00 00 01 94 00 00 00 4C 00 00 01 93 00 00 00 4D 00 00 01 93 00 00 00 4E 00 00 01 92 00 00 00 4F 00 00 01 92 00 00 00 50 00 00 01 91 00 00 00 51 00 00 01 90 00 00 00 52 00 00 01 90 00 00 00 53 00 00 01 90 00 00 00 54 00 00 01 90 00 00 00 54 00 00 01 8F 00 00 00 55 00 00 01 8E 00 00 00 56 00 00 01 8E 00 00 00 57 00 00 01 8E 00 00 00 58 00 00 01 8D 00 00 00 59 00 00 01 8C 00 00 00 5A 00 00 01 8B 00 00 00 5B 00 00 01 8A 00 00 00 5C 00 00 01 8A 00 00 00 5D 00 00 01 89 00 00 00 5E 00 00 01 89 00 00 00 5F 00 00 01 88 00 00 00 60 00 00 01 88 00 00 00 61 00 00 01 87 00 00 00 62 00 00 01 87 00 00 00 62 00 00 01 86 00 00 00 63 00 00 01 86 00 00 00 64 00 00 01 85 00 00 00 65 00 00 01 85 00 00 00 66 00 00 01 84 00 00 00 67 00 00 01 83 00 00 00 68 00 00 01 83 00 00 00 69 00 00 01 82 00 00 00 6A 00 00 01 81 00 00 00 6B 00 00 01 81 00 00 00 6C 00 00 01 7F 00 00 00 6D 00 00 01 7E 00 00 00 6E 00 00 01 7E 00 00 00 6F 00 00 01 7D 00 00 00 70 00 00 01 7D 00 00 00 70 00 00 01 7C 00 00 00 71 00 00 01 7C 00 00 00 72 00 00 01 7B 00 00 00 73 00 00 01 7A 00 00 00 74 00 00 01 7A 00 00 00 75 00 00 01 79 00 00 00 76 00 00 01 77 00 00 00 77 00 00 01 77 00 00 00 78 00 00 01 76 00 00 00 79 00 00 01 75 00 00 00 7A 00 00 01 74 00 00 00 7B 00 00 01 74 00 00 00 7C 00 00 01 73 00 00 00 7D 00 00 01 72 00 00 00 7E 00 00 01 72 00 00 00 7E 00 00 01 71 00 00 00 7F 00 00 01 70 00 00 00 80 00 00 01 6F 00 00 00 81 00 00 01 6E 00 00 00 82 00 00 01 6D 00 00 00 83 00 00 01 6C 00 00 00 84 00 00 01 6B 00 00 00 85 00 00 01 6A 00 00 00 86 00 00 01 6A 00 00 00 87 00 00 01 68 00 00 00 88 00 00 01 67 00 00 00 89 00 00 01 66 00 00 00 8A 00 00 01 65 00 00 00 8B 00 00 00 00 00 00 00 8C'
    decode(data)

