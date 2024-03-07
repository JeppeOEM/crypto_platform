
def get_types(data_dict):
        value_types = {}
        for key, value in data_dict.items():
            if key != "kind":
                value_types[key] = type(value).__name__
        return value_types