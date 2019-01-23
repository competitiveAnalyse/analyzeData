from jobs.yaml_parser import YamlParser
from pytrends.request import TrendReq
import jobs.utilities as ut
import matplotlib.pyplot as plt
from jobs.stats import Stats
import warnings
import datetime
warnings.simplefilter(action='ignore', category=FutureWarning)


yp = YamlParser()

py_trend = TrendReq()
list_pandas = list()
for i in yp.terms:
    py_trend.build_payload(kw_list=[i], timeframe=yp.date, geo=yp.geo)
    list_pandas.append(py_trend.interest_over_time())
py_trend.build_payload(kw_list=yp.terms, timeframe=yp.date, geo=yp.geo)
pds = py_trend.interest_over_time()

fig = plt.figure(1, figsize=(10, 3))
pds.plot(title='Popularity over time')
plt.gcf().subplots_adjust(bottom=0.15)
plt.savefig('output/interest_over_time.png')

count = 0
for i in yp.terms:
    ut.search_interest_label(i, list_pandas[count])
    count += 1

for i in yp.terms:
    ut.bar_chart_label(py_trend, i, 'top')
    ut.bar_chart_label(py_trend, i, 'rising')

ut.word_cloud_by_label(py_trend, yp, 'top')
ut.word_cloud_by_label(py_trend, yp, 'rising')

yp = YamlParser()
py_trend = TrendReq()
list_pandas = list()

for i in yp.terms:
    py_trend.build_payload(kw_list=[i], timeframe=yp.date, geo=yp.geo)
    list_pandas.append(py_trend.interest_over_time())

x = list_pandas[0].index.values
max_date = datetime.datetime.utcfromtimestamp(max(x).tolist() / 1e9)
min_date = datetime.datetime.utcfromtimestamp(min(x).tolist() / 1e9)
min_date, max_date = min_date - (max_date - min_date), min_date

st = Stats(yp, min_date, max_date)
for i in list_pandas:
    st.check_value(i, yp)

st.generate_to_csv()





