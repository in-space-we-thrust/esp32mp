# sensors/temperature_sensor.py
from base_sensor import Sensor
from machine import I2C, Pin
from ads1x15 import ADS1115

class PressureSensor(Sensor):

    def __init__(self, name):
        super().__init__(name)
        # инициируем тут всякие тяжелые штуки, которые нам понадобятся при каждом считывании сигнала
        self.i2c=I2C(0, sda=Pin(21), scl=Pin(22))
        self.adc = ADS1115(self.i2c, address=72, gain=0)


    class SENSOR_IDS:
        # эмуляция enum типа для объявления ID датчиков (чтобы далее пользоваться именами переменных, а не числами)
        PRESSURE_PP1 = 1

    PERIOD = 1 / 10 # период опроса, 10 раз в секунду

    def sense(self):
        # Здесь вы можете вставить код для работы с датчиком
        # он должен работать максимально быстро
        raw = self.adc.read(7, 1, 3)
        voltage = self.adc.raw_to_v(raw)
        current = voltage/220
        self.SENSE_RESULTS[self.SENSOR_IDS.PRESSURE_PP1] = current
