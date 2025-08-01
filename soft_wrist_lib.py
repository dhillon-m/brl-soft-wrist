import time

def checksum(packet):
    """
    Calculate the checksum for a given packet.
    :param packet: List of integers representing the packet
    """
    return (~sum(packet[2:])) & 0xFF

def move_servo(ser, servo_id, position):
    """
    Move a specific servo to the given position.
    :param ser: Open serial port
    :param servo_id: ID of the servo to move
    :param position: Position value to move the servo to (0-4095)
    """
    pos_l = position & 0xFF         # Low byte of position
    pos_h = (position >> 8) & 0xFF  # High byte of position
    
    packet = [0xFF, 0xFF, servo_id, 5, 0x03, 0x2A, pos_l, pos_h]
    packet.append(checksum(packet))
    
    ser.write(bytearray(packet))
    
def move_wrist(ser, flexion_angle, ulnar_angle):
    """
    Move the wrist to the specified positions.
    :param ser: Open serial port
    :param flexion_angle: Position value for wrist flexion/extension (servo 1)
    :param ulnar_angle: Position value for ulnar/radial deviation (servo 2)
    """
    # Joint mapping
    flexion_deg_per_pos = 360 / (1.8 * (4095 - 0))
    flexion_min_angle = (0 - 2048) * flexion_deg_per_pos
    flexion_max_angle = (4095 - 2048) * flexion_deg_per_pos
    
    ulnar_deg_per_pos = 360 / (3.05 * (3100 - 1200))
    ulnar_min_angle = (1200 - 2150) * ulnar_deg_per_pos
    ulnar_max_angle = (3100 - 2150) * ulnar_deg_per_pos
    
    # Convert wrist angles to servo positions
    flexion_pos = int(round(2048 + (flexion_angle / flexion_deg_per_pos)))
    flexion_pos = max(1500, min(4095, flexion_pos))

    ulnar_pos = int(round(2150 + (ulnar_angle / ulnar_deg_per_pos)))
    ulnar_pos = max(1200, min(3100, ulnar_pos))
    
    # Move servos to the calculated positions
    move_servo(ser, servo_id=1, position=flexion_pos)
    time.sleep(0.05)
    move_servo(ser, servo_id=4, position=ulnar_pos)
    time.sleep(0.05)
    
def close_hand(ser):
    """
    Close the hand.
    :param ser: Open serial port
    """
    move_servo(ser, servo_id=2, position=2200)
    time.sleep(0.05)
    move_servo(ser, servo_id=3, position=2100)
    time.sleep(0.05)

def open_hand(ser):
    """
    Open the hand.
    :param ser: Open serial port
    """
    move_servo(ser, servo_id=2, position=700)
    time.sleep(0.05)
    move_servo(ser, servo_id=3, position=1070)
    time.sleep(0.05)
    
def home_hand(ser):
    """
    Move the hand to the home position.
    :param ser: Open serial port
    """
    open_hand(ser)  # Open the hand
    move_wrist(ser, flexion_angle=0, ulnar_angle=0)  # Reset wrist position