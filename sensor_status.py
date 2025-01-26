# sensors/temperature_sensor.py
from base_sensor import Sensor

class StatusSensor(Sensor):
    class SENSOR_IDS:
        # эмуляция enum типа для объявления ID датчиков (чтобы далее пользоваться именами переменных, а не числами)
        STATUS = 0

    PERIOD = 1

    async def sense(self):
        # Здесь вы можете вставить код для работы с датчиком температуры
        self.SENSE_RESULTS[self.SENSOR_IDS.STATUS] = 1
