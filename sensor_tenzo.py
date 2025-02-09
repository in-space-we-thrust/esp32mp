# sensors/temperature_sensor.py
from base_sensor import Sensor
from machine import I2C, Pin, freq
from hx711 import HX711

class TenzoSensor(Sensor):

    def __init__(self, name):
        super().__init__(name)
        # инициируем тут всякие тяжелые штуки, которые нам понадобятся при каждом считывании сигнала
        freq(160000000)
        self.driver = HX711(d_out=4, pd_sck=18)


    class SENSOR_IDS:
        # эмуляция enum типа для объявления ID датчиков (чтобы далее пользоваться именами переменных, а не числами)
        PRESSURE_PP1 = 15

    PERIOD = 1 / 10 # период опроса, 10 раз в секунду

    async def sense(self):
        # Здесь вы можете вставить код для работы с датчиком
        # он должен работать максимально быстро
        while True:
            if self.driver.is_ready():
                self.SENSE_RESULTS[self.SENSOR_IDS.PRESSURE_PP1] = self.driver.read()
                break
