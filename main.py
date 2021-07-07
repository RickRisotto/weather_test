import requests

from datetime import datetime
from datetime import timedelta
from datetimerange import DateTimeRange
API_KEY = "41494fb24a51d8360f3cf4bdd80d2835"
CITY = "Moscow"

#get max pressure
response = requests.get(f"https://api.openweathermap.org/data/2.5/forecast?q={CITY}&units=metric&appid={API_KEY}").json()
pressure = []
for i in range(0, 5):
    pressure.append(response['list'][i]['main'].get('pressure'))
    pressure.sort()
print(f"max pressure for five days is {pressure[-1]}")

#get max delta
data = {}
for i in range(0, 40):
    timestamp = response['list'][i]['dt_txt']
    for k, v in response['list'][i]['main'].items():
        temp_max = response['list'][i]['main']['temp_max']
        temp_min = response['list'][i]['main']['temp_min']
    data[timestamp] = temp_max, temp_min


base = datetime.now()
base__ = base.replace(minute=0, hour=0, second=0, microsecond=0)  # base to start from 00:00
base_ = base.replace(minute=0, hour=6, second=0, microsecond=0)  # base to start from 06:00


def datetime_range(start, end, delta):
    current = start
    while current < end:
        yield current
        current += delta


dts = [dt.strftime('%Y-%m-%d T%H:%M Z') for dt in
       datetime_range(base__, base_ + timedelta(hours=120), timedelta(hours=12))]
res = [x for i, x in enumerate(dts) if i%2 == 0]

ds = [dt.strftime('%Y-%m-%d T%H:%M Z') for dt in
       datetime_range(base_, base_ + timedelta(hours=120), timedelta(hours=12))]
res__ = [x for i, x in enumerate(ds) if i%2 == 0]

date = []
for x in res:
    f = (x.replace("T", "").replace("Z", " ").replace("", "").strip())

    date.append(datetime.strptime(f, '%Y-%m-%d %H:%M'))

date__ = []
for x in res__:
    f = (x.replace("T", "").replace("Z", " ").replace("", "").strip())
    date__.append(datetime.strptime(f, '%Y-%m-%d %H:%M'))
merge_range = date+date__


def time_filter(data, merge_range):
    import operator
    res = {}
    for key, values in data.items():
        for m in merge_range:
            time_range = DateTimeRange(m, m + timedelta(hours=6))
            if key in time_range:
                x = values[0]
                y = values[1]
                result = x - y
                res[key] = result
    res_ = max(res.items(), key=operator.itemgetter(1))[0]
    msg = f"highest delta between morning/night is {res_}"
    print(msg)
    return msg


time_filter(data, merge_range)  # start time_filter





