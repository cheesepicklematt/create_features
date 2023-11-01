import pandas as pd
import sys
sys.path.insert(0,'./')
from binance.client import Client

from get_binance_data.src.get_data_utils import getData
from create_features.config import cred


client = cred.client

def build(asset_list,time_str):
    # extract raw data
    gd = getData()
    raw_data = gd.run(
        asset_list=asset_list,
        time_str = time_str,
        kline_interval = Client.KLINE_INTERVAL_15MINUTE
    )

    return raw_data