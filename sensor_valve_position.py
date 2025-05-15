# sensors/temperature_sensor.py
from base_sensor import Sensor
import machine
import uasyncio

class PositionSensor(Sensor):

    def __init__(self, name):
        super().__init__(name)
        # инициируем пины для всех клапанов
        self.pins = {}
        for attr_name, pin_number in self.SENSOR_IDS.__dict__.items():
            if not attr_name.startswith('_'):  # Пропускаем служебные атрибуты
                self.pins[pin_number] = machine.Pin(pin_number, machine.Pin.IN, machine.Pin.PULL_UP)


    class SENSOR_IDS:
        # эмуляция enum типа для объявления ID датчиков (чтобы далее пользоваться именами переменных, а не числами)
        VALVE_1 = 12
        VALVE_2 = 13
        VALVE_3 = 14
        VALVE_4 = 25
        VALVE_5 = 26
        VALVE_6 = 27
        VALVE_7 = 32
        VALVE_8 = 33

    PERIOD = 1 / 10 # период опроса, 10 раз в секунду

    async def sense(self):
        # Читаем значение со всех пинов и обновляем словарь результатов
        for pin_id, pin in self.pins.items():
            self.SENSE_RESULTS[pin_id] = pin.value()
        
