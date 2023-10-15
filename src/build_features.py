import os
import pandas as pd

from create_features.src.indicators import indicators

class buildIndicators:
    def __init__(self,data=None,ma_len=[],rsi_len=[]):
        """
        where data is the output from getData class in get_binance_data.src.utils
        """

        self.data = data

        # find unique assets by volume column
        self.asset_list = [y.split('_')[1] for y in [x for x in self.data.columns if x.find('Close_')>-1]]

        self.indicator_settings_dict = {
            'RSI':{
                'ASSETS':self.asset_list,
                'COL_TYPE':'close_returns',
                'RSI_PERIOD':rsi_len,
                
                },
            'MA':{
                'ASSETS':self.asset_list,
                'COL_TYPE':'close',
                'MA_LEN':ma_len,
                }
        }
    def create_returns(self,ret_col):
        for asset in self.asset_list:
            self.data[ret_col+'_returns_'+asset] = indicators.price_returns(self.data[ret_col+'_'+asset])
    
    def build(self,return_data=False,ret_col='Close'):
        self.create_returns(ret_col=ret_col)
        self.create_indicators()
        if return_data:
            return self.data
    
    def create_indicators(self):
        for indicator,details in self.indicator_settings_dict.items():
            for asset in details['ASSETS']:
                if indicator.lower()=='rsi':
                    tmp_col ,= [x for x in self.data.columns if x.lower().find(details['COL_TYPE'].lower()+'_'+asset.lower())>-1]
                    for rsi_p in details['RSI_PERIOD']:
                        tmp_rsi = indicators.RSI(rsi_period = rsi_p,ret_df = self.data[[tmp_col]])
                        self.data[tmp_rsi.columns[0]] = tmp_rsi

                if indicator.lower()=='ma':
                    tmp_col ,= [x for x in self.data.columns if x.lower().find(details['COL_TYPE'].lower()+'_'+asset.lower())>-1 and x.lower().find('_rsi')==-1]
                    for ma_len in details['MA_LEN']:
                        tmp_ma = indicators.MA(ma_len=ma_len,price_df=self.data[[tmp_col]])
                        self.data[tmp_ma.columns[0]] = tmp_ma

    def save_data(self):
        self.data.to_csv(os.path.join('not_implemented','feature_data.csv'),index=False)

