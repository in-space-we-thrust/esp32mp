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
        # Initialize servo
        self.servo_160kg = Servo(self.servo_160kg_pin, max_angle=270)
        self.servo_35kg = Servo(self.servo_35kg_pin, max_angle=270)


    def execute(self, dict_command):
        """
        Execute servo scenarios based on servo_scenario_num
        
        Expected command format:
        {
            "type": CommandTypes.SERVO,
            "servo_scenario_num": int
        }
        """
        print('Executing servo command')
        
        try:
            scenario_num = dict_command.get('servo_scenario_num')
            
            if scenario_num is None:
                return {
                    'type': dict_command['type'],
                    'command_id': dict_command.get('command_id'),
                    'result': 0,
                    'error': 'Missing servo_scenario_num'
                }
            
            # Execute scenario
            if scenario_num == 1:
                self._scenario_1()
            elif scenario_num == 2:
                self._scenario_2()
            elif scenario_num == 3:
                self._scenario_3()
            elif scenario_num == 4:
                self._scenario_4()
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
        self.servo_160kg.move(0, speed=30)
        time.sleep(2)
        
        # Sweep from 0 to 180 degrees with smooth movement
        self.servo_35kg.move(0, speed=30)  # Move to 90 degrees at 30 deg/sec
        time.sleep(2)  # Wait for movement to complete
        
        self.servo_160kg.move(100, speed=30)  # Move to 180 degrees
        
        print('Servo scenario 1 completed')
    
    def _scenario_2(self):
        """
        Scenario 2: Servo oscillation between two positions
        """
        print('Executing servo scenario 2: Oscillation movement')
        
        # Move servo to 0 degrees
        self.servo_160kg.move(0, speed=30)
        time.sleep(2)
        
        # Sweep from 0 to 180 degrees with smooth movement
        self.servo_35kg.move(90, speed=30)  # Move to 90 degrees at 30 deg/sec
        time.sleep(2)  # Wait for movement to complete
        
        self.servo_160kg.move(100, speed=30)  # Move to 180 degrees
        
        print('Servo scenario 2 completed')

    def _scenario_3(self):
        """
        Scenario 2: Servo oscillation between two positions
        """
        print('Executing servo scenario 2: Oscillation movement')
        
        # Move servo to 0 degrees
        self.servo_160kg.move(0, speed=30)
        time.sleep(2)
        
        # Sweep from 0 to 180 degrees with smooth movement
        self.servo_35kg.move(180, speed=30)  # Move to 90 degrees at 30 deg/sec
        time.sleep(2)  # Wait for movement to complete
        
        self.servo_160kg.move(100, speed=30)  # Move to 180 degrees
        
        print('Servo scenario 1 completed')

    def _scenario_4(self):
        """
        Scenario 2: Servo oscillation between two positions
        """
        print('Executing servo scenario 4: Oscillation movement')
        
        # Move servo to 0 degrees FAST
        self.servo_160kg.move(0)
        
        print('Servo scenario 4 completed')
