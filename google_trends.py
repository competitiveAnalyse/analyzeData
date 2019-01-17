from jobs.yaml_parser import YamlParser
from pytrends.request import TrendReq
import matplotlib.pyplot as plt

yp = YamlParser()

py_trend = TrendReq()
print(yp.geo)
py_trend.build_payload(kw_list=yp.terms, timeframe=yp.date, geo=yp.geo)

pd = py_trend.interest_over_time()

plt.figure(num=None, figsize=(8, 6), dpi=80, facecolor='w', edgecolor='k')
pd.plot()
plt.show()
plt.savefig('output/interest_over_time.png')