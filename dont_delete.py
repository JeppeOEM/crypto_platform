list2 = [['random', {'ind': 'RSI_15'}, {'cond': '<'}, {'val': 12}], ['random', {'ind': 'volume'}, {'cond':
                                                                                                   '>'}, {'val': 44}]]

list3 = [['random', {'ind': 'RSI_15'}, {'cond': '<'}, {'val': 12}], ['random', {'ind': 'volume'}, {'cond':
                                                                                                   '>'}, {'val': 44}]]

opti = [['RSI_15', 12], ['volume', 40]]
parameters = {'RSI_15_SELL': 71, 'RSI_15_BUY': 36, 'volume_BUY': 44}
val = parameters["RSI_15_BUY"]
val2 = parameters["RSI_15_SELL"]
val3 = parameters["volume_BUY"]


def update_val(indicator, val):
    flag = False
    for l in list2:
        for inner in l:
            try:
                if inner['ind'] == indicator:
                    print(inner['ind'])
                    flag = True

            except:
                print("nope")
            try:
                if flag and inner['val']:
                    print(inner['val'])
                    inner['val'] = val
                    flag = False
            except:
                print("no val")


for item in opti:
    update_val(item[0], item[1])

print(list2)
print(list3)
