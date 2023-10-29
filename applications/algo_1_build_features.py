import pandas as pd
import sys
sys.path.insert(0,'./')
from binance.client import Client

from get_binance_data.src.get_data_utils import getData
from create_features.src.build_features import buildIndicators
from create_features.config import cred


client = cred.client


ma_len = [5,7,10,12,15]
asset_list = ["BNBBTC","ADABTC","LTCBTC","SOLBTC","ETHBTC","XRPBTC"]


def build(
    asset_list = [],
    ma_len = [],
    time_str = "5 hours ago UTC",
    backtest=False
):

    # extract raw data
    gd = getData()
    raw_data = gd.run(
        asset_list=asset_list,
        time_str = time_str,
        kline_interval = Client.KLINE_INTERVAL_15MINUTE
    )
    
    if not backtest:
        # need to come back and make sure that there are not NAN values on 'current' row
        feature_col = 'Close'
        open_time_col = 'Open time formatted'

        # current prices
        curr_buy_prices = {}
        for asset in asset_list:
            curr_buy_prices[feature_col+'_'+asset] = float(client.get_order_book(symbol=asset,limit=1)['bids'][0][0])
        curr_buy_prices[open_time_col] = 'current'
        

        # append current prices
        raw_data = raw_data.append(curr_buy_prices, ignore_index=True)
        raw_data['is_current'] = raw_data[open_time_col] == 'current'

    # append indicators
    bi = buildIndicators(
        data = raw_data.copy(),
        ma_len=ma_len)
    data_features = bi.build(return_data=True,ret_col='Close')
    data_features = data_features.merge(raw_data[['Open time', 'Open time formatted']],how='left',on='Open time')

    return data_features



