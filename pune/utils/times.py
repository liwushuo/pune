# -*- coding: utf-8 -*-

import calendar
from datetime import datetime
from datetime import timedelta
from datetime import date

def to_timestamp(dt):
    if not dt:
        return dt
    return calendar.timegm(dt.utctimetuple())


def to_iso_datetime(ts):
    if not ts:
        return ts
    dt = datetime.utcfromtimestamp(ts)
    cn_dt = dt + timedelta(hours = 8)
    return cn_dt.strftime("%Y-%m-%d %H:%M:%S")


def to_iso_date(ts):
    dt = datetime.utcfromtimestamp(ts)
    cn_dt = dt + timedelta(hours = 8)
    return cn_dt.strftime("%Y-%m-%d")
