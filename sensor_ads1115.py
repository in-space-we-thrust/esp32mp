from base_sensor import Sensor

from machine import I2C, Pin
from ads1115 import ADS1115

class PressureSensor(Sensor):

    def __init__(self, name):
        super().__init__(name)
        # Инициализируем необходимые ресурсы
        self.i2c = I2C(0, sda=Pin(21), scl=Pin(22))
        self.adc = ADS1115(self.i2c, address=0x48, gain=1)

    class SENSOR_IDS:
        # Объявляем ID датчиков
        PRESSURE_PP1 = 1
        PRESSURE_PP2 = 2
        PRESSURE_PP3 = 3       

    PERIOD = 1 / 10  # Период опроса, 10 раз в секунду

    async def sense(self):
        # Чтение данных с каждого датчика давления и сохранение результатов
        for channel, sensor_id in enumerate([self.SENSOR_IDS.PRESSURE_PP1, self.SENSOR_IDS.PRESSURE_PP2, self.SENSOR_IDS.PRESSURE_PP3]):
            raw = self.adc.read(7, channel)
            voltage = self.adc.raw_to_v(raw)
            self.SENSE_RESULTS[sensor_id] = voltage