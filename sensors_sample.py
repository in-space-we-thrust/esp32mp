# sensors/temperature_sensor.py
from base_sensor import Sensor

class TemperatureSensor(Sensor):

    class SENSOR_IDS:
        # эмуляция enum типа для объявления ID датчиков (чтобы далее пользоваться именами переменных, а не числами)
        TEMPERATURE_PT1 = 1
        TEMPERATURE_PT2 = 2
        PRESSURE_PP1 = 17

    PERIOD = 1 / 10 # период опроса, 10 раз в секунду

    prev_value = 0 # хранение предыдущего значения, т.к. пока у нас синглтон-архитектура, храним прям в атрибуте класса/

    def sense(self):
        # Здесь вы можете вставить код для работы с датчиком температуры
        sense_result = {}
        new_value = self.prev_value + 1
        self.prev_value = new_value
        self.SENSE_RESULTS[self.SENSOR_IDS.TEMPERATURE_PT1] = new_value
        self.SENSE_RESULTS[self.SENSOR_IDS.PRESSURE_PP1] = new_value + 10
