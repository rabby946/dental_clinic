from datetime import time, timedelta, datetime as dt

START_TIME = time(17, 0)   # 5:00 PM
SLOT_MINUTES = 15

def get_time_by_serial(serial):
    base = dt.combine(dt.today(), START_TIME)
    return (base + timedelta(minutes=(serial - 1) * SLOT_MINUTES)).time()
