# sensors/temperature_sensor.py
from base_sensor import Sensor
from machine import I2C, Pin, freq
from hx711 import HX711

class TenzoSensor(Sensor):

    def __init__(self, name):
        super().__init__(name)
        # инициируем тут всякие тяжелые штуки, которые нам понадобятся при каждом считывании сигнала
        freq(160000000)
        self.driver1 = HX711(d_out=27, pd_sck=26, channel=2)
        self.driver2 = HX711(d_out=22, pd_sck=21, channel=2)
        self.driver3 = HX711(d_out=19, pd_sck=18, channel=2)
        self.driver4 = HX711(d_out=17, pd_sck=16, channel=2)


    class SENSOR_IDS:
        # эмуляция enum типа для объявления ID датчиков (чтобы далее пользоваться именами переменных, а не числами)
        PRESSURE_PP1 = 51
        PRESSURE_PP2 = 52
        PRESSURE_PP3 = 53
        PRESSURE_PP4 = 54

    PERIOD = 1 / 10 # период опроса, 10 раз в секунду

    async def sense(self):
        # Здесь вы можете вставить код для работы с датчиком
        # он должен работать максимально быстро
        if self.driver1.is_ready():
            self.SENSE_RESULTS[self.SENSOR_IDS.PRESSURE_PP1] = self.driver1.read()
        if self.driver2.is_ready():
            self.SENSE_RESULTS[self.SENSOR_IDS.PRESSURE_PP2] = self.driver2.read()    
        if self.driver3.is_ready():
            self.SENSE_RESULTS[self.SENSOR_IDS.PRESSURE_PP3] = self.driver3.read()
        if self.driver4.is_ready():
            self.SENSE_RESULTS[self.SENSOR_IDS.PRESSURE_PP4] = self.driver4.read()