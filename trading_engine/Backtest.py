import numpy as np
import pandas as pd


class Backtest:

    def run(self, df):
        df['datetime'] = pd.to_datetime(df.index, unit='ms')
        # df['buy_name'] = df['buy_name1112221'].copy()
        # df['buy_name1112221'] = df['buy_name']
        # df['sell_name'] = df['sell_nam22221322'].copy()
        # df['sell_nam22221322'] = df['sell_name']
        # np.random.seed(42)
        # random_values = np.random.choice([-1, 1], size=len(df))
        # df['buy_name'] = random_values
        # df['sell_name'] = random_values
        df_signal_buy = self.filter_signals(df, "buy_")
        df_signal_sell = self.filter_signals(df, "sell_")

        print(df_signal_sell.columns)
        df_signal_buy = df_signal_buy.values
        df_signal_sell = df_signal_sell.values
        print(df_signal_buy)
        # WORKS ON TWO CONDS ONLY
        try:
            result_sell = df_signal_sell[:, 0] == df_signal_sell[:, 1]
            df['close_trade'] = result_sell
        except:
            df['close_trade'] = df_signal_buy

        try:
            result_buy = df_signal_buy[:, 0] == df_signal_buy[:, 1]
            df['open_trade'] = result_buy
        except:
            df['open_trade'] = df_signal_sell

        df = self.analyse(df)
        print(df.head(10))
        test_cond1 = df.loc[:, 'cond1'].values
        test_cond2 = df.loc[:, 'cond2'].values
        test_groups = self.groups_from_conditions(test_cond1, test_cond2)
        df['groups'] = test_groups
        # df.to_csv('data/groups.csv')
        dfgroup = df.groupby(["groups"], as_index=False)[
            "change"].sum()
        print("SUUUUUUUM")
        print(dfgroup['change'].sum())
        dfgroup = dfgroup['change'].sum()
        return dfgroup
    # print(self.dfgroup['change'].sum())
    # print(self.dfgroup['change'].sum())

    def filter_signals(self, df, column_prefix):
        selected_columns = [
            col for col in df.columns if col.startswith(column_prefix)]
        filtered_df = df[selected_columns]
        print("filter")
        return filtered_df

    def analyse(self, df):
        df.reset_index(drop=True, inplace=True)
        df.dropna(inplace=True)
        # df['change'] = 10 for sake for simplicity this is more logical to test
        df['change'] = df.close.pct_change()
        print("change")
        df['cond1'] = np.where(df['open_trade'] == 1, 1, 0)
        print("cond!")
        df['cond2'] = np.where(df['close_trade'] == 1, 1, 0)
        print("cond!")
        return df

    def groups_from_conditions(self, cond1, cond2):
        '''
        assign a unique non-NaN integer to each group as defined by the rules
        '''
        n = len(cond1)

        group_idx = -1
        groups = np.zeros(n)

        curr_state = 0  # 0 = not in a group, 1 = in a group
        for n in range(n):
            if curr_state == 0:
                # Currently not in a group
                if cond1[n] == 1:
                    # Detected start of a group. so:
                    # switch the state to 1 ie in a group
                    curr_state = 1
                    # get a new group_idx
                    group_idx = group_idx + 1
                    # assign it to the output for element n
                    groups[n] = group_idx
                else:
                    # no start of the group detected, we are not in a group so mark as NaN
                    groups[n] = np.NaN

            else:
                # current_state == 1 so we are in a group
                if cond2[n] == 1:
                    # detected end of group -- switch state to 0
                    curr_state = 0
                # as we are in a group assign current group_idx. Note that this happens for the element
                # for which cond2[n] == 1 as well, ie this element is included
                groups[n] = group_idx

        return groups
