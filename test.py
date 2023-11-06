import os
import importlib


def get_indicators():

    indicators = []
    module_path = "loke.trading_engine.indicators.momentum"
    folder_path = "loke/trading_engine/indicators/momentum"

    class_files = [file for file in os.listdir(
        folder_path) if file.endswith(".py") and file != "__init__.py"]

    #Loop through the Python files and import the classes
    for file_name in class_files:
        #Remove the ".py" extension
        module_name = os.path.splitext(file_name)[0]
        module = importlib.import_module(f"{module_path}")
        Obj = getattr(module, f"{module_name}")
        obj = Obj()
        indicators.append(obj.type_dict())
        print(indicators)

    return indicators


print(get_indicators())
