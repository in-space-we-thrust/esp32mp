
from base_command import CommandTypes, Command
import machine

class ValveCommand(Command):
    COMMAND_TYPE = CommandTypes.VALVE

    def execute(self, dict_command):
        print('executing command')
        pin_num = dict_command['valve_pin']
        try:
            led = machine.Pin(pin_num, machine.Pin.OUT)
        except Exception as e:
            dict_command['message'] = str(e)
            return dict_command
        if led.value():
            led.value(0)
        else:
            led.value(1)
        result_msg = dict_command.copy()
        result_msg['result'] = 1
        return result_msg

class StatusCommand(Command):
    COMMAND_TYPE = CommandTypes.STATUS

    def execute(self, dict_command):
        return {'type': dict_command['type'], 'command': dict_command['command'], 'result': 0}