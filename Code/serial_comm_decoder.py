import serial
import time

def test_comms(ser):
    print("Sending %")
    ser.write(b'%')

    time.sleep(0.5)

    data = ser.read(100)
    print("Reply:", data.hex())

    print("Sending setup")
    ser.write(b'S0000000400\r')

    time.sleep(1)

    data = ser.read(5000)
    print("Reply:", data.hex())
    
    print("Sending A message")
    ser.write(b'A')
    
    time.sleep(1)
    data = ser.read(10000)
    print("Reply:", data.hex())
    
    time.sleep(10)
    data = ser.read(10000)
    print("Reply:", data.hex())
    

if __name__ == "__main__":
    for baud in [19200]:
        ser = serial.Serial(
            '/dev/ttyUSB0',
            baudrate=baud,
            bytesize=8,
            parity='N',
            stopbits=1,
            timeout=1
        )
        
        print(baud)
        print()
        
        ser.reset_input_buffer()

        ser.dtr = False
        ser.rts = False
        time.sleep(0.5)

        ser.dtr = True
        ser.rts = True
        time.sleep(0.5)
        
        
        test_comms(ser)
