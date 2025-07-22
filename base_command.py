class CommandTypes:
    STATUS = 0
    VALVE = 1
    SERVO = 2
    FIRE = 3


    @classmethod
    def get_all_types_numbers(cls):
        res = []
        for attr, value in cls.__dict__.items():
            if attr[:2] != '__':
                res.append(value)
        return res

class Command:
    def __init__(self):
        if self.COMMAND_TYPE == None:
            raise NotImplementedError('Subclasses must define COMMAND_TYPE int')
        if self.COMMAND_TYPE not in CommandTypes.get_all_types_numbers():
            raise NotImplementedError('Unkwown COMMAND_TYPE')

    def execute(self, dict_command):
        raise NotImplementedError("Subclasses must implement the run method.")
