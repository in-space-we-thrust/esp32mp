class MessageFormat(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def validate_and_format(self, telemetry_data):
        formatted_data = {}
        for key, expected_types in self.items():
            if key in telemetry_data:
                actual_value = telemetry_data[key]
                if isinstance(expected_types, type):
                    # Special handling for string type
                    if expected_types is str and isinstance(actual_value, (str, bytes)):
                        formatted_data[key] = str(actual_value)
                    elif isinstance(actual_value, expected_types):
                        formatted_data[key] = actual_value
                    else:
                        print(f'Wrong value format for {self.__class__.__name__}')
                        return None
                else:  # handle tuple of types
                    if any(isinstance(actual_value, t) for t in expected_types):
                        formatted_data[key] = actual_value
                    else:
                        print(f'Wrong value format for {self.__class__.__name__}')
                        return None
            else:
                print(f'Key missing format for {self.__class__.__name__}')
                return None

        return formatted_data
