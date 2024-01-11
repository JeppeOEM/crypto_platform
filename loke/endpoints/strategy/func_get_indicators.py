import importlib
import os

import numpy as np


def get_indicators(category):
    print("GET INDICATORS", category)
    indicators = []
    # __init__ must import all classes from the folder
    module_path = f'loke.trading_engine.indicators.{category}'
    folder_path = f'loke/trading_engine/indicators/{category}'

    class_files = [file for file in os.listdir(
        folder_path) if file.endswith(".py") and file != "__init__.py"]

    # Loop through the Python files and import the classes
    for file_name in class_files:
        # Remove the ".py" extension
        module_name = os.path.splitext(file_name)[0]
        module = importlib.import_module(f"{module_path}")
        Obj = getattr(module, f"{module_name}")
        obj = Obj()
        print(obj.type_only())
        indicators.append(obj.type_only())
    # convert to numpy and back again to flatten
    indicators = np.array(indicators)
    # from [[{}],[{}]] to [{},{}]
    indicators = indicators.flatten('F')
    return indicators.tolist()
