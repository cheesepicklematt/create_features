import pandas as pd
import sys
sys.path.insert(0,'./')
from binance.client import Client

from get_binance_data.src.get_data_utils import getData
from create_features.src.build_features import buildIndicators
from create_features.config import cred


client = cred.client


ma_len = [5,7,10,12,15]
rsi_len = [5,7,10,12,15]
asset_list = ["BNBBTC","ADABTC","LTCBTC","SOLBTC","ETHBTC","XRPBTC"]


def build(
    asset_list = [],
    ma_len = [],
    rsi_len = [],
    time_str = "5 hours ago UTC"
):

    # extract raw data
    gd = getData()
    gd.extract_data(
        asset_list=asset_list,
        time_str = time_str,
        kline_interval = Client.KLINE_INTERVAL_15MINUTE
    )
    raw_data = gd.return_data(
        convert_timestamp=True,
        save_csv=False,
        return_data=True
    )

    feature_col = 'Close'
    open_time_col = 'Open time formatted'

    close_cols = [x for x in raw_data.columns if x.find(feature_col)>-1]
    col_list = [open_time_col] + close_cols
    raw_data = raw_data[col_list]

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
        ma_len=ma_len,
        rsi_len=rsi_len)
    data_features = bi.build(return_data=True,ret_col='Close')

    return data_features



