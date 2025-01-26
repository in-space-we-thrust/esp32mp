# sensor.py

class Sensor:
    _used_ids = set()  # Статический набор для хранения всех использованных ID

    def __init__(self, name):
        self.name = name
        self.SENSE_RESULTS = {
            # словарь формата "ID_датчика: значение"
            # используется для возврата из функции sense
        }
        if self.SENSOR_IDS == None:
            #TODO добавить более жёсткую проверку на соответствие SENSE_RESULTS формату
            raise NotImplementedError('Subclasses must define SENSOR_IDS enum')

        # Проверка уникальности ID
        new_ids = set()
        for attr_name, value in self.SENSOR_IDS.__dict__.items():
            if not attr_name.startswith('_'):  # Пропускаем служебные атрибуты
                if value in self._used_ids:
                    raise ValueError(f"Duplicate sensor ID: {value} in {self.__class__.__name__}")
                new_ids.add(value)
                
        # Если проверка прошла успешно, добавляем новые ID в набор
        self._used_ids.update(new_ids)

        if self.PERIOD == None:
            raise NotImplementedError('Subclasses must define PERIOD value')

    async def sense(self):
        raise NotImplementedError("Subclasses must implement the sense method.")

    async def run(self):
        # прокси-метод для принудительной очистки словаря, чтобы не забывали в нём предыдущие значения
        self.SENSE_RESULTS = {}
        await self.sense()
        return self.SENSE_RESULTS

