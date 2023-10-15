import pandas as pd


class indicators:
    """Class to hold static methods for calculating financial indicators
    """
    @staticmethod
    def RSI(rsi_period = 14,ret_df = None) -> pd.DataFrame:
        """Calculate relative strength index
        """
        ret_data = ret_df.copy()
        ret_col = ret_data.columns[0]

        ret_data['ret_pos'] = ret_data[ret_col]
        ret_data.loc[ret_data['ret_pos']<0,'ret_pos'] = 0 
        ret_data['ret_neg'] = ret_data[ret_col]
        ret_data.loc[ret_data['ret_neg']>0,'ret_neg'] = 0 

        ret_data['rolling_up'] = ret_data['ret_pos'].rolling(rsi_period).mean()
        ret_data['rolling_down'] = ret_data['ret_neg'].rolling(rsi_period).mean().abs()
        
        rsi_col = ret_col.replace('returns_','')+'_RSI'+str(rsi_period)
        ret_data[rsi_col] = 100*ret_data['rolling_up']/(ret_data['rolling_up'] +ret_data['rolling_down'])
        return ret_data[[rsi_col]]

    @staticmethod
    def MA(ma_len = 10,price_df=None) -> pd.DataFrame:
        price_df = price_df.copy()
        price_col = price_df.columns[0]
        
        ma_col = price_col+'_MA'+str(ma_len)
        price_df[ma_col] = price_df[price_col].rolling(ma_len).mean()
        return price_df[[ma_col]]


    @staticmethod
    def price_returns(pricesDF):
        return (pricesDF - pricesDF.shift(1))/pricesDF.shift(1)





