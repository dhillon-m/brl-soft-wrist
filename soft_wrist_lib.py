import serial
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
    
def move_wrist(ser, flexion_extension, ulnar_radial):
    """
    Move the wrist to the specified positions.
    :param ser: Open serial port
    :param flexion_extension: Position value for wrist flexion/extension (servo 1)
    :param ulnar_radial: Position value for ulnar/radial deviation (servo 2)
    """
    # Ensure angles are within safe range
    flexion_extension = max(-90, min(90, flexion_extension))
    ulnar_radial = max(-20, min(20, ulnar_radial))
    
    # Convert wrist angles to servo positions
    flexion_pos = int(round((flexion_extension * 1.8 + 180) * (4095 / 360)))
    ulnar_pos = int(round((ulnar_radial * 3.05 + 180) * (4095 / 360)))
    
    # Move servos to the calculated positions
    move_servo(ser, servo_id=1, position=flexion_pos)
    move_servo(ser, servo_id=4, position=ulnar_pos)
    
def close_hand(ser):
    """
    Close the hand.
    :param ser: Open serial port
    """
    move_servo(ser, servo_id=2, position=0)
    move_servo(ser, servo_id=3, position=0)

def open_hand(ser):
    """
    Open the hand.
    :param ser: Open serial port
    """
    move_servo(ser, servo_id=2, position=4095)
    move_servo(ser, servo_id=3, position=4095)
    
def home_hand(ser):
    """
    Move the hand to the home position.
    :param ser: Open serial port
    """
    open_hand(ser)  # Open the hand
    move_wrist(ser, flexion_extension=0, ulnar_radial=0)  # Reset wrist position