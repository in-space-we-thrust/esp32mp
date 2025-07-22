from base_command import CommandTypes, Command
import machine
import time


class FireCommand(Command):
    COMMAND_TYPE = CommandTypes.FIRE

    def __init__(self):
        super().__init__()
        self.relay_pin = None

    def execute(self, dict_command):
        """
        Execute relay/fire scenarios based on fire_scenario_num
        
        Expected command format:
        {
            "type": CommandTypes.FIRE,
            "fire_scenario_num": int,
            "relay_pin": int,
            "duration": float (optional, default 3.0 seconds)
        }
        """
        print('Executing fire command')
        
        try:
            scenario_num = dict_command.get('fire_scenario_num')
            relay_pin = dict_command.get('relay_pin')
            duration = dict_command.get('duration', 3.0)  # Default 3 seconds
            
            if scenario_num is None or relay_pin is None:
                return {
                    'type': dict_command['type'],
                    'command_id': dict_command.get('command_id'),
                    'result': 0,
                    'error': 'Missing fire_scenario_num or relay_pin'
                }
            
            # Initialize relay pin
            self.relay_pin = machine.Pin(relay_pin, machine.Pin.OUT)
            self.relay_pin.value(0)  # Ensure relay starts OFF
            
            # Execute scenario
            if scenario_num == 1:
                self._scenario_1(duration)
            elif scenario_num == 2:
                self._scenario_2()
            else:
                return {
                    'type': dict_command['type'],
                    'command_id': dict_command.get('command_id'),
                    'result': 0,
                    'error': f'Unknown fire scenario number: {scenario_num}'
                }
            
            result_msg = dict_command.copy()
            result_msg['result'] = 1
            result_msg['message'] = f'Fire scenario {scenario_num} executed successfully'
            return result_msg
            
        except Exception as e:
            return {
                'type': dict_command['type'],
                'command_id': dict_command.get('command_id'),
                'result': 0,
                'error': str(e)
            }
    
    def _scenario_1(self, duration=3.0):
        """
        Scenario 1: Simple relay trigger for specified duration
        """
        print(f'Executing fire scenario 1: Single trigger for {duration} seconds')
        
        self.relay_pin.value(1)  # Turn ON relay
        print('Relay turned ON')
        time.sleep(duration)
        self.relay_pin.value(0)  # Turn OFF relay
        print('Relay turned OFF')
    
    def _scenario_2(self):
        """
        Scenario 2: Multiple relay pulses (3 short pulses + 1 long pulse)
        """
        print('Executing fire scenario 2: Multiple pulse sequence')
        
        # Three short pulses (0.5 seconds each with 0.5 second breaks)
        for i in range(3):
            print(f'Short pulse {i+1}/3')
            self.relay_pin.value(1)
            time.sleep(0.5)
            self.relay_pin.value(0)
            time.sleep(0.5)
        
        # Wait 1 second before final long pulse
        time.sleep(1.0)
        
        # Final long pulse (3 seconds)
        print('Final long pulse (3 seconds)')
        self.relay_pin.value(1)
        time.sleep(3.0)
        self.relay_pin.value(0)
        print('Fire scenario 2 completed')
