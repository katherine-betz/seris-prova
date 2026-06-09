import serial
import time

def establish_comms(ser):         
    ser.reset_input_buffer()

    ser.dtr = False
    ser.rts = False
    time.sleep(0.5)

    ser.dtr = True
    ser.rts = True
    time.sleep(0.5)
    
    do{
        print("Sending %")
        ser.write(b'%')

        time.sleep(0.5)

        data = ser.read(100)
        print("Reply:", data.hex())
    } while (data != b'000000')
    
    print("Sending setup")
    ser.write(b'S0000000400\r')

    time.sleep(1)

    data = ser.read(5000)
    print("Reply:", data.hex()) # will probably need to use these parameters at some point to figure out how it infulences decoder, if it does
    
def decode(data, packet_size = 8):
    num_points = len(data)
    print("data length:", num_points)
    
    measurements = [data[i:i + packet_size] for i in range(0, num_points, packet_size)]
    

def autoscan(ser):
    do {
        print("Attempting autoscan")
        ser.write(b'A')

        time.sleep(1)
        data = ser.read(10000)
        print("Reply:", data.hex())
    } while (data != b'0500') #HERE -- check what type data is returned as, acknowledge is 0500

    time.sleep(10)
    data = ser.read(10000)
    print("Reply:", data.hex())
    
    decode(data)    
    

if __name__ == "__main__":
#     ser = serial.Serial(
#         '/dev/ttyUSB0',
#         baudrate=baud,
#         bytesize=8,
#         parity='N',
#         stopbits=1,
#         timeout=1
#     )
#     
#     establish_comms(ser)
    data = b'0000'
    decode(data)