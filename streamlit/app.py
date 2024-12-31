import streamlit as st
import pandas as pd
import json
import sys
import os

sys.path.append('D:/bot')

from system_utils import get_today, get_year_ago
from logger import logger
from account import Account

accounts = [
    "81263805",
    "64643829"
]

def get_yearwise_trading_data():
    domestic_results = []
    foreign_results = []

    for cano in accounts:
        for is_foreign in [True, False]:
            account = Account(
                cano = cano,
                is_foreign = is_foreign
            )
            try:
                result = account.get_trading_report(
                    start_date=get_year_ago(),
                    end_date=get_today(),
                    currency="krw"
                )
                foreign_results.append(pd.DataFrame(result['output1'])) if is_foreign else domestic_results.append(pd.DataFrame(result['output1']))
            except Exception as e:
                logger.warning(str(e))

    if domestic_results:
        domestic_results = pd.concat(domestic_results)
    if foreign_results:
        foreign_results = pd.concat(foreign_results).sort_values("trad_day", ascending=True)
    return domestic_results, foreign_results


if __name__ == "__main__":

    st.set_page_config(layout="wide")

    domestic_results, foreign_results = get_yearwise_trading_data()

    st.title("Summarized Result")

    st.markdown("## 국내")
    st.dataframe(domestic_results)

    st.markdown('## 해외')
    st.dataframe(foreign_results)