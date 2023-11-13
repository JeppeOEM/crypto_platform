import numpy as np
import pandas as pd


class Condition:
    def __init__(self, df):
        self.conditions = []
        self.df = df

    def get_df(self):
        return self.df

    def add_custom_condition(self, name, side, condition_string):
        self.df[f'{side}_{name}'] = np.where(
            pd.eval(condition_string, target=self.df), 1, -1)
        self.df[f'{side}_{name}'] = self.df[f'{side}_{name}'].shift(1)

    def filter_signals(self, df, column_prefix):
        selected_columns = [
            col for col in df.columns if col.startswith(column_prefix)]
        filtered_df = df[selected_columns]
        return filtered_df

    def combine_signals(self, np_array, side):
        # open/close
        row_all_same = (np_array == np_array[:, 0][:, None]).all(axis=1)
        # row_all_same = (np_array == self.df.iloc[:, 0]).all(axis=1)
        self.df[f'{side}_signal_combined'] = np.where(row_all_same, -1, 1)
        return self.df

    def make_condition(self, signal_name, side, *args):
        total_conditions = []
        test = len(args)
        # ZERO INDEX IS THE NAME
        for i in range(len(args)):  # Adjust the range as needed
            # print(i)
            if i % 4 == 1:
                # print(f"{i} is the first iteration.{args[i]['ind']}")
                total_conditions.append(args[i]['ind'])
            elif i % 4 == 2:
                # print(f"{i} is the second iteration.{args[i]['cond']}")
                total_conditions.append(args[i]['cond'])
            elif i % 4 == 3:
                # print(f"{i} is the third iteration.{args[i]['val']}")
                total_conditions.append(args[i]['val'])
            else:
                try:
                    # print(f"{i} is the fourth iteration.{args[i]['or_and']}")
                    total_conditions.append(args[i]['or_and'])
                except:
                    continue

        # create string to pass to eval
        expression_parts = []
        for i, value in enumerate(total_conditions):
            if i % 4 == 0:
                expression_parts.append(f'self.df.{value}')
            else:
                expression_parts.append(str(value))
        expression = " ".join(expression_parts)

        print("exp:", expression)
        # evaluate
        self.df[f'{side}_{signal_name}'] = np.where(
            pd.eval(expression, target=self.df), 1, -1)
        self.df[f'{side}_{signal_name}'] = self.df[f'{side}_{signal_name}'].shift(
            1)
