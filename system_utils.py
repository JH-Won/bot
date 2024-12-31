import os
from pathlib import Path
from datetime import datetime
from dateutil.relativedelta import relativedelta


def get_init_path():
    return str(Path(os.path.realpath(__file__)).parent.absolute())

def get_today():
    return datetime.now().strftime('%Y%m%d')

def get_year_ago():
    current_date = datetime.now()
    one_year_ago = current_date - relativedelta(years=1)
    return one_year_ago.strftime('%Y%m%d')