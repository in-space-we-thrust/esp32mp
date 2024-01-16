# sensors/temperature_sensor.py
from base_sensor import Sensor
import utime

__all__ = ['TemperatureSensor']

class TemperatureSensor(Sensor):
    ID = 1 # уникальный айдишник датчика
    PERIOD = 1 / 10 # период опроса, 10 раз в секунду

    prev_value = 0 # хранение предыдущего значения

    def sense(self):
        # Здесь вы можете вставить код для работы с датчиком температуры
        new_value = self.prev_value + 1
        self.prev_value = new_value
        return new_value
