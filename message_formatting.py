class MessageFormat(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def validate_and_format(self, telemetry_data):
        formatted_data = {}
        for key, expected_types in self.items():
            if key in telemetry_data:
                actual_value = telemetry_data[key]
                if isinstance(expected_types, type):
                    if isinstance(actual_value, expected_types):
                        formatted_data[key] = actual_value
                    else:
                        print(f'Wrong value format for {self.__class__.__name__}')
                        return None  # Валидация не прошла
                else: # предполагаем что нам передали итерабл с типами
                    if any(issubclass(type(actual_value), t) for t in expected_types):
                        formatted_data[key] = actual_value
                    else:
                        print(f'Wrong value format for {self.__class__.__name__}')
                        return None  # Валидация не прошла
            else:
                print(f'Key missing format for {self.__class__.__name__}')
                return None  # Ключ отсутствует в данных

        return formatted_data   # Возвращаем результат валидации и отформатированные данные
