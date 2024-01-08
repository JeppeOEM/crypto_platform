import pandas_ta as ta
import numpy as np

# help(ta.adx)
# help(ta.ma)
original_format = [[('kind', 'ao'), ('fast', 'int', 5), ('slow', 'int', 34), ('offset', 'int', 0)], [('kind', 'rsi'), ('length',
                                                                                                     'int', 14), ('scalar', 'float', 100), ('talib', 'bool', False), ('drift', 'int', 1), ('offset', 'int', 0)]]

[{'kind': 'ao', 'fast': 'int', 'slow': 'int', 'offset': 'int'}, {'kind': 'rsi',
                                                                 'length': 'int', 'scalar': 'float', 'talib': 'bool', 'offset': 'int'}]

original_format = np.array([[{'kind': 'ao', 'fast': 'int', 'slow': 'int', 'offset': 'int'}], [
                           {'kind': 'rsi', 'length': 'int', 'scalar': 'float', 'talib': 'bool', 'drift': 'int', 'offset': 'int'}]])


d = original_format.flatten('F')
dd = d.tolist()
print(dd)


transformed_format = []

# for sublist in original_format:
#     # Create a dictionary for each sublist
#     obj = {key: value for key, *value in sublist}
#     transformed_format.append(obj)
