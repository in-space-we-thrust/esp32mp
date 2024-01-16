import sys
import uselect
import json
import _thread
import time
from base_sensor import Sensor
import sensors


THREADS_TERMINATE = False

INCOMING_COMMAND_FORMAT = {
    "type": 1, # type: int
    "command": None, # type: int
    "valve": None, # type: int
    "result": 0 # type: int
}

OUTGOING_COMMAND_FORMAT = {
    "type": 1, # type: int
    "command": None, # type: int
    "valve": None, # type: int
    "result": 0 # type: int
}

OUTGOING_TELEMETRY_FORMAT = {
    "type": 1, # type: int
    "sensor": None, # type: int
    "value": None # type: float
}


def send_to_serial(dict_msg):
    json.dump(dict_msg, sys.stdout.buffer)
    sys.stdout.buffer.write("\n")

serialPoll = uselect.poll()
serialPoll.register(sys.stdin, uselect.POLLIN)

def valve_handler(dict_command):
    result_msg = dict_command.copy()
    result_msg['result'] = 1
    send_to_serial(result_msg)

def other_handler(dict_command):
    send_to_serial({'type': dict_command['type'], 'command': dict_command['command'], 'result': 0})


def handle_command(command):
    
    if command == None:
        return
    print('raw command:', command)
    try:
        dict_msg = json.loads(command)
    except ValueError:
        print('not a command')
        return
    command_type = dict_msg.get('type')
    if command_type == 1:
        valve_handler(dict_msg)
        #send_to_serial({'type': 2, 'command': 17, 'valve': 3, 'result': 1})
        #sys.stdout.buffer.write("test\n")
    else:
        other_handler(dict_msg)
        
        #sys.stdout.buffer.write("error\n")

def read_from_serial():
    """
    reads a single character over serial.

    :return: returns the character which was read, otherwise returns None
    """
    return sys.stdin.readline().strip()


def load_sensor_classes():
    sensor_classes = []

    for obj in sensors.__dict__.values():
        if obj and isinstance(obj, type) and issubclass(obj, Sensor) and obj is not Sensor:
            sensor_classes.append(obj)
    print('SC', sensor_classes)
    return sensor_classes

def run_sensor(sensor_class):
    sensor_instance = sensor_class(f"Sensor #{sensor_class.ID}")
    while True:
        if THREADS_TERMINATE:
            _thread.exit()
        value = sensor_instance.sense()
        send_to_serial({'type': 1, 'sensor': sensor_instance.ID, 'value': value})
        time.sleep(sensor_instance.PERIOD)

sensor_classes = load_sensor_classes()

for sensor_class in sensor_classes:
    _thread.start_new_thread(run_sensor, (sensor_class,))

try:
    while True:
        if serialPoll.poll(0): #пытааемся считать только если нам уже начали что-то сувать в порт
            print('inc')
            message = read_from_serial()
            handle_command(message)
        time.sleep(1/100) # тут слип нужен чтобы соседние треды не тормозились
except KeyboardInterrupt:
    # CTRL+C ловим чтобы останавливать треды
    THREADS_TERMINATE = True
    try:
        sys.exit(130)
    except SystemExit:
        os._exit(130)
except Exception as e:
    THREADS_TERMINATE = True
    raise(e)