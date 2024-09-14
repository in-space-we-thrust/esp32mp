# sensor.py

class Sensor:

    def __init__(self, name):
        self.name = name
        self.SENSE_RESULTS = {
            # словарь формата "ID_датчика: значение"
            # используется для возврата из функции sense
        }
        if self.SENSOR_IDS == None:
            #TODO добавить более жёсткую проверку на соответствие SENSE_RESULTS формату
            raise NotImplementedError('Subclasses must define SENSOR_IDS enum')
        if self.PERIOD == None:
            raise NotImplementedError('Subclasses must define PERIOD value')

    def sense(self):
        raise NotImplementedError("Subclasses must implement the run method.")

    def run(self):
        # прокси-метод для принудительной очистки словаря, чтобы не забывали в нём предыдущие значения
        self.SENSE_RESULTS = {}
        self.sense()
        return self.SENSE_RESULTS

