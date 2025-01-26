# sensors/temperature_sensor.py
from base_sensor import Sensor
import yf_s201

class StatusSensor(Sensor):
    class SENSOR_IDS:
        # эмуляция enum типа для объявления ID датчиков (чтобы далее пользоваться именами переменных, а не числами)
        STATUS = 0

    PERIOD = 1

    async def sense(self):
        # Здесь вы можете вставить код для работы с датчиком температуры
        self.SENSE_RESULTS[self.SENSOR_IDS.STATUS] = 1


class TemperatureSensor(Sensor):

    class SENSOR_IDS:
        # эмуляция enum типа для объявления ID датчиков (чтобы далее пользоваться именами переменных, а не числами)
        TEMPERATURE_PT1 = 1
        TEMPERATURE_PT2 = 0
        PRESSURE_PP1 = 17

    PERIOD = 1 / 10 # период опроса, 10 раз в секунду

    prev_value = 0 # хранение предыдущего значения, т.к. пока у нас синглтон-архитектура, храним прям в атрибуте класса/

    async def sense(self):
        # Здесь вы можете вставить код для работы с датчиком температуры
        new_value = self.prev_value + 1
        self.prev_value = new_value
        self.SENSE_RESULTS[self.SENSOR_IDS.TEMPERATURE_PT1] = new_value
        self.SENSE_RESULTS[self.SENSOR_IDS.PRESSURE_PP1] = new_value + 10


# class FlowSensor(Sensor):

#     def __init__(self, name):
#         super().__init__(name)
#         # Инициализируем расходомеры
#         self.yf = yf_s201.WaterFlowMeter(pulsPin=4)

#     class SENSOR_IDS:
#         # Объявляем ID датчиков
#         FLOW_METR1 = 4
#         FLOW_METR2 = 5       

#     PERIOD = 1/100  # Период опроса, раз в секунду

#     async def sense(self):
#         # Чтение данных с каждого расходомера и сохранение ре��ультатов
#         flowMetr2 = await self.yf.measure_flow()
#         self.SENSE_RESULTS[self.SENSOR_IDS.FLOW_METR2] = flowMetr2
