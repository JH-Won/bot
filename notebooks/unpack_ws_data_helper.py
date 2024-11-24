from multiprocess import Pool
import pandas as pd

def get_total_df(csv_list):
    p = Pool(4)
    df_list = p.map(pd.read_csv, csv_list)
    return pd.concat(df_list)