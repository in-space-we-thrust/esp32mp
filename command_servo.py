from base_command import CommandTypes, Command
import machine
import time
import uasyncio as asyncio
from servo import Servo


class ServoCommand(Command):
    COMMAND_TYPE = CommandTypes.SERVO

    def __init__(self):
        super().__init__()
        self.servo_160kg_pin = 16
        self.servo_35kg_pin = 17


    def execute(self, dict_command):
        """
        Execute servo scenarios based on servo_scenario_num
        
        Expected command format:
        {
            "type": CommandTypes.SERVO,
            "servo_scenario_num": int,
            "servo_pin": int
        }
        """
        print('Executing servo command')
        
        try:
            scenario_num = dict_command.get('servo_scenario_num')
            servo_pin = dict_command.get('servo_pin')
            
            if scenario_num is None or servo_pin is None:
                return {
                    'type': dict_command['type'],
                    'command_id': dict_command.get('command_id'),
                    'result': 0,
                    'error': 'Missing servo_scenario_num or servo_pin'
                }
            
            # Initialize servo
            self.servo_160kg = Servo(self.servo_160kg_pin, max_angle=270)
            self.servo_35kg = Servo(self.servo_35kg_pin, max_angle=270)
            
            # Execute scenario
            if scenario_num == 1:
                self._scenario_1()
            elif scenario_num == 2:
                self._scenario_2()
            else:
                return {
                    'type': dict_command['type'],
                    'command_id': dict_command.get('command_id'),
                    'result': 0,
                    'error': f'Unknown scenario number: {scenario_num}'
                }
            
            result_msg = dict_command.copy()
            result_msg['result'] = 1
            result_msg['message'] = f'Scenario {scenario_num} executed successfully'
            return result_msg
            
        except Exception as e:
            return {
                'type': dict_command['type'],
                'command_id': dict_command.get('command_id'),
                'result': 0,
                'error': str(e)
            }
    
    def _scenario_1(self):
        """
        Scenario 1: Servo sweep from 0 to 180 degrees and back to center
        """
        print('Executing servo scenario 1: Sweep movement')
        
        # Move servo to 0 degrees
        self.servo_160kg.move(0)
        time.sleep(1)
        
        # Sweep from 0 to 180 degrees with smooth movement
        self.servo_160kg.move(90, speed=30)  # Move to 90 degrees at 30 deg/sec
        time.sleep(3)  # Wait for movement to complete
        
        self.servo_160kg.move(180, speed=30)  # Move to 180 degrees
        time.sleep(3)  # Wait for movement to complete
        
        # Move back to center position
        self.servo_160kg.move(90, speed=60)  # Faster return to center
        time.sleep(2)
        print('Servo scenario 1 completed')
    
    def _scenario_2(self):
        """
        Scenario 2: Servo oscillation between two positions
        """
        print('Executing servo scenario 2: Oscillation movement')
        
        # Start at center position
        self.servo_35kg.move(90)
        time.sleep(1)
        
        # Oscillate 3 times between 45 and 135 degrees
        for i in range(3):
            print(f'Oscillation cycle {i+1}/3')
            
            # Move to 45 degrees
            self.servo_35kg.move(45, speed=45)
            time.sleep(2)
            
            # Move to 135 degrees
            self.servo_35kg.move(135, speed=45)
            time.sleep(2)
        
        # Return to center
        self.servo_35kg.move(90, speed=60)
        time.sleep(2)
        print('Servo scenario 2 completed')
