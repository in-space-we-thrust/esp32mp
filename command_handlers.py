
from base_command import CommandTypes, Command
import machine

class ValveCommand(Command):
    COMMAND_TYPE = CommandTypes.VALVE

    def execute(self, dict_command):
        led = machine.Pin(22, machine.Pin.OUT)
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