import numpy as np
import pandas as pd


class Backtest:

    def run(self, df):
        df['datetime'] = pd.to_datetime(df.index, unit='ms')

        df_signal_buy = self.filter_signals(df, "buy_")
        df_signal_sell = self.filter_signals(df, "sell_")
        df_signal_buy = df_signal_buy.values
        df_signal_sell = df_signal_sell.values
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
        test_cond1 = df.loc[:, 'cond1'].values
        test_cond2 = df.loc[:, 'cond2'].values
        test_groups = self.groups_from_conditions(test_cond1, test_cond2)
        df['groups'] = test_groups

        # sums the PNL pr trade
        dfgroup = df.groupby(["groups"], as_index=False)[
            "pnl"].sum()

        dfgroup['cum_pnl'] = dfgroup['pnl'].cumsum()
        dfgroup["max_cum_pnl"] = dfgroup["cum_pnl"].cummax()
        dfgroup["drawdown"] = dfgroup["max_cum_pnl"] - dfgroup["cum_pnl"]

        return dfgroup["pnl"].sum(), dfgroup["drawdown"].max()

    def filter_signals(self, df, column_prefix):
        selected_columns = [
            col for col in df.columns if col.startswith(column_prefix)]
        filtered_df = df[selected_columns]
        return filtered_df

    def analyse(self, df):
        # print(df.head(100))
        df.reset_index(drop=True, inplace=True)
        df.dropna(inplace=True)

        try:
            df['pnl'] = df.close.pct_change()
        except:
            print("EMPTY DATAFRAME, TOO BIG OPTIMIZER PARAMS")
            print(df.tail(110))
            exit()
        df['cond1'] = np.where(df['open_trade'] == 1, 1, 0)
        df['cond2'] = np.where(df['close_trade'] == 1, 1, 0)
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
