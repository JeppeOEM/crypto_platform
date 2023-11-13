list2 = [['random', {'ind': 'RSI_15'}, {'cond': '<'}, {'val': 12}], ['random', {'ind': 'volume'}, {'cond':
                                                                                                   '>'}, {'val': 44}]]

list3 = [['random', {'ind': 'RSI_15'}, {'cond': '<'}, {'val': 12}], ['random', {'ind': 'volume'}, {'cond':
                                                                                                   '>'}, {'val': 44}]]

parameters = {'RSI_15_SELL': 71, 'RSI_15_BUY': 36, 'volume_BUY': 44}
val = parameters["RSI_15_BUY"]
val2 = parameters["RSI_15_SELL"]
val3 = parameters["volume_BUY"]
opti = [['RSI_15', val], ['volume', val]]


def update_val(indicator, val, conds):
    flag = False
    for l in conds:
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
    # val = parameters["RSI_15_BUY"]
    # val2 = parameters["RSI_15_SELL"]
    # val3 = parameters["volume_BUY"]
    # print(val, val2, val3)
    # sell = conditions['conds_sell']
    # buy = conditions['conds_buy']

    # opti_buy = [['RSI_15', val], ['volume', val3]]
    # opti_sell = [['RSI_15', val2]]

    # def up(conds, opti_val):

    #     for item in opti_val:
    #         conds = update_val(item[0], item[1], conds)
    #         print("conds", conds)
    #     return conds
    # condition_buy = up(buy, opti_buy)
    # condition_sell = up(sell, opti_sell)

    # def update_val(indicator, val, conds):
    #     flag = False
    #     for l in conds:
    #         for inner in l:
    #             try:
    #                 if inner['ind'] == indicator:
    #                     flag = True

    #             except:
    #                 continue
    #             try:
    #                 if flag and inner['val']:
    #                     print(inner['val'])
    #                     inner['val'] = val
    #                     flag = False
    #             except:
    #                 continue
    #     return conds

    # def update_val2(indicator, val, conds):
    #     flag = False
    #     for l in conds:
    #         for inner in l:
    #             try:
    #                 if inner['ind'] == indicator:
    #                     flag = True

    #             except:
    #                 continue
    #             try:
    #                 if flag and inner['val']:
    #                     print(inner['val'])
    #                     inner['val'] = val
    #                     flag = False
    #             except:
    #                 continue
    #     return conds