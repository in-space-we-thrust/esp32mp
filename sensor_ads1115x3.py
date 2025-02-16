from base_sensor import Sensor

from machine import I2C, Pin
from ads1115 import ADS1115

class PressureSensor(Sensor):

    def __init__(self, name):
        super().__init__(name)
        # Инициализируем необходимые ресурсы
        self.i2c = I2C(0, sda=Pin(21), scl=Pin(22))
        self.adc1 = ADS1115(self.i2c, address=0x48, gain=1)
        self.adc2 = ADS1115(self.i2c, address=0x4B, gain=1)
        self.adc3= ADS1115(self.i2c, address=0x4A, gain=1)

    class SENSOR_IDS:
        # Объявляем ID датчиков
        PRESSURE_PP1 = 1
        PRESSURE_PP2 = 2
        PRESSURE_PP3 = 3
        PRESSURE_PP4 = 4
        PRESSURE_PP5 = 11
        PRESSURE_PP6 = 12
        PRESSURE_PP7 = 13       
        PRESSURE_PP8 = 14
        PRESSURE_PP9 = 21
        PRESSURE_PP10 = 22
        PRESSURE_PP11 = 23       
        PRESSURE_PP12 = 24


    PERIOD = 1 / 10  # Период опроса, 10 раз в секунду

    async def sense_adc1(self):
        for channel, sensor_id in enumerate([self.SENSOR_IDS.PRESSURE_PP1, self.SENSOR_IDS.PRESSURE_PP2, self.SENSOR_IDS.PRESSURE_PP3, self.SENSOR_IDS.PRESSURE_PP4]):
            raw = self.adc1.read(7, channel)
            voltage = self.adc1.raw_to_v(raw)
            self.SENSE_RESULTS[sensor_id] = voltage
    
    async def sense_adc2(self):
        for channel, sensor_id in enumerate([self.SENSOR_IDS.PRESSURE_PP5, self.SENSOR_IDS.PRESSURE_PP6, self.SENSOR_IDS.PRESSURE_PP7, self.SENSOR_IDS.PRESSURE_PP8]):
            raw = self.adc2.read(7, channel)
            voltage = self.adc2.raw_to_v(raw)
            self.SENSE_RESULTS[sensor_id] = voltage

    async def sense_adc3(self):
        for channel, sensor_id in enumerate([self.SENSOR_IDS.PRESSURE_PP9, self.SENSOR_IDS.PRESSURE_PP10, self.SENSOR_IDS.PRESSURE_PP11, self.SENSOR_IDS.PRESSURE_PP12]):
            raw = self.adc3.read(7, channel)
            voltage = self.adc3.raw_to_v(raw)
            self.SENSE_RESULTS[sensor_id] = voltage

    async def sense(self):
        # Чтение данных с каждого датчика давления и сохранение результатов
        await self.sense_adc1()
        await self.sense_adc2()
        await self.sense_adc3()