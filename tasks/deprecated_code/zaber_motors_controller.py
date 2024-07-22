import serial
import serial.tools.list_ports
"""ports = serial.tools.list_ports.comports()
for port, desc, hwid in sorted(ports):
        print("{}: {} [{}]".format(port, desc, hwid))
"""
def devide_data(data):
    """
    gets integer data returns in byte sized chunks in reverse order
    """
    byte6 = data//256**3
    data = data - byte6*256**3
    byte5 = data//256**2
    data = data - byte5*256**2
    byte4 = data//256
    data = data - byte4*256
    return (data,byte4,byte5,byte5)


def create_move_absolute_cmd(motor_num,position):
    """
    create a bytearray that contains the byte data for a move absolute command
    """
    if(motor_num>=0 and motor_num<=3):
      byte3,byte4,byte5,byte6 = devide_data(position)
      command = bytearray()
      command.append(motor_num) #set target for command
      command.append(20) #set command (20 - move absolute)
      #add command data in reverse order
      command.append(byte3)
      command.append(byte4)
      command.append(byte5)
      command.append(byte6)
      return command
    else:
        raise ValueError("motor number out of range")
    
def get_home_reply(motor_num=0):
    commands=[]
    if(motor_num == 0 ):
        for i in range(1,4):
          command = bytearray()
          command.append(i) #set target for command
          command.append(1) #set command (20 - move absolute)
          #add command data in reverse order
          command.append(0)
          command.append(0)
          command.append(0)
          command.append(0)
          commands.append(command)
    return commands


with serial.Serial('COM3',9600,timeout=0.03) as ser:
    home_cmd = bytearray(b'\x00\x01\x00\x00\x00\x00')
    ser.write(home_cmd) #home all motors
    print('all motors home')

    position=10000
    command = create_move_absolute_cmd(3,position)
    ser.write(command)
    for i in range(100):
        print(ser.readline())

