# sensor.py

class Sensor:

    def __init__(self, name):
        self.name = name

    def sense(self):
        raise NotImplementedError("Subclasses must implement the run method.")

