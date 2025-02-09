from base_sensor import Sensor
import tpr

class FlowSensor(Sensor):

    def __init__(self, name):
        super().__init__(name)
        # Инициализируем расходомеры
        self.tpr11 = tpr.TPR(pulsPin=5, dimNumber=10, timeout=20000)

    class SENSOR_IDS:
        # Объявляем ID датчиков
        FLOW_METR1 = 5

    PERIOD = 1/100  # Период опроса, раз в секунду

    async def sense(self):
        # Чтение данных с каждого расходомера и сохранение результатов
        flowMetr1 = await self.tpr11.flow_measurement()
         
        self.SENSE_RESULTS[self.SENSOR_IDS.FLOW_METR1] = flowMetr1

class FlowSensor2(Sensor):

    def __init__(self, name):
        super().__init__(name)
        # Инициализируем расходомеры
        self.tpr11 = tpr.TPR(pulsPin=4, dimNumber=10, timeout=20000)

    class SENSOR_IDS:
        # Объявляем ID датчиков
        FLOW_METR2 = 4

    PERIOD = 1/100  # Период опроса, раз в секунду

    async def sense(self):
        # Чтение данных с каждого расходомера и сохранение результатов
        flowMetr1 = await self.tpr11.flow_measurement()
         
        self.SENSE_RESULTS[self.SENSOR_IDS.FLOW_METR2] = flowMetr1
