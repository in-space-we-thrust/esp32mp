import sys
import uselect
import json
import uasyncio as asyncio
import time
from base_sensor import Sensor
from base_command import Command
import sensors
import command_handlers
from message_formatting import MessageFormat


THREADS_TERMINATE = False

INCOMING_COMMAND_FORMAT = {
    "type": 1, # type: int
    "command_id": None, # type: int
    "payload": {}, # type: dict
}

OUTGOING_COMMAND_FORMAT = {
    "type": 1, # type: int
    "command_id": None, # type: int
    "payload": {}, # type: dict
}

OUTGOING_TELEMETRY_FORMAT = MessageFormat({
    "type": int, # type: int
    "sensor_id": int, # type: int
    "value": (int, float) # type: float
})


def send_to_serial(dict_msg):
    json.dump(dict_msg, sys.stdout.buffer)
    sys.stdout.buffer.write("\n")

serialPoll = uselect.poll()
serialPoll.register(sys.stdin, uselect.POLLIN)


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
    command_handler = COMMAND_CLASSES.get(command_type)
    if command_handler:
        command_res = command_handler.execute(dict_msg)
        send_to_serial(command_res)
    else:
        print('Unknown command type')

def read_from_serial():
    """
    reads a single character over serial.

    :return: returns the character which was read, otherwise returns None
    """
    return sys.stdin.readline().strip()

async def handle_serial_input():
    while True:
        if serialPoll.poll(0):
            message = read_from_serial()
            handle_command(message)
        await asyncio.sleep(0.01)


def load_sensor_classes():
    sensor_classes = []

    for obj in sensors.__dict__.values():
        if obj and isinstance(obj, type) and issubclass(obj, Sensor) and obj is not Sensor:
            sensor_classes.append(obj)
    print('SC', sensor_classes)
    return sensor_classes

def load_command_classes():
    command_classes = {}

    for obj in command_handlers.__dict__.values():
        if obj and isinstance(obj, type) and issubclass(obj, Command) and obj is not Command:
            command_classes[obj.COMMAND_TYPE] = obj()
    print('CC', command_classes)
    return command_classes

async def run_sensor(sensor_class):
    sensor_instance = sensor_class(f"Sensor with ids: #{sensor_class.SENSOR_IDS}")
    while True:
        try:
            sensor_res = await sensor_instance.run()  # Add await here
            for sensor_id, value in sensor_res.items():
                out_data = OUTGOING_TELEMETRY_FORMAT.validate_and_format({'type': 1, 'sensor_id': sensor_id, 'value': value})
                if out_data:
                    send_to_serial(out_data)
        except Exception as e:
            print('Error running sensor:', e)
        await asyncio.sleep(sensor_instance.PERIOD)

COMMAND_CLASSES = load_command_classes()


async def main():
    sensor_classes = load_sensor_classes()
    for sensor_class in sensor_classes:
        asyncio.create_task(run_sensor(sensor_class))

    # Задача для обработки серийного ввода
    asyncio.create_task(handle_serial_input())

    while True:
        await asyncio.sleep(1/100)  # Основной цикл программы


try:
    asyncio.run(main())
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