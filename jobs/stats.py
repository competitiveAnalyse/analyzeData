from pytrends.request import TrendReq
import datetime, time
import numpy as np
import csv


class Stats:

    def __init__(self, yp, min_date, max_date):
        self.conditions = dict()
        self.generate_condition(yp, min_date, max_date)
        self.to_csv = dict()


    @staticmethod
    def hours_to_day(pd, label):
        dict_days = dict()
        for i in pd.index.values:
            i_datetime = datetime.datetime.utcfromtimestamp(i.tolist() / 1e9)
            string = '{}-{}-{}'.format(i_datetime.year, i_datetime.month, i_datetime.day)
            if dict_days.get(string) is None:
                if isinstance(pd.get_value(i, label), np.int64):
                    dict_days.update({string: pd.get_value(i, label).item()})
                else:
                    dict_days.update({string: int(pd.get_value(i, label).tolist()[0])})
            else:
                if isinstance(pd.get_value(i, label), np.int64):
                    dict_days.update({string: dict_days.get(string) + pd.get_value(i, label).item()})
                else:
                    dict_days.update({string: dict_days.get(string) + pd.get_value(i, label).tolist()[0]})
        return dict_days

    def model_condition(self, pd, label):
        head = str([i for i in pd.head()][0])
        condition = (np.std(pd[head]), np.average(pd[head]))
        self.conditions.update({label: condition})

    def generate_condition(self, yp, min_date, max_date):
        py_trend = TrendReq()
        time_frame = '{}-{}-{} {}-{}-{}'.format(min_date.year, min_date.month, min_date.day,
                                                max_date.year, max_date.month, max_date.day)
        for i in yp.terms:
            py_trend.build_payload(kw_list=[i], timeframe=time_frame, geo=yp.geo)
            pd = py_trend.interest_over_time()
            self.model_condition(pd, i)

    def check_value(self, df, yp):
        py_trend = TrendReq()
        label = list(df)[0]
        std, average = self.conditions.get(label)

        x = df.index.values
        max_date = datetime.datetime.utcfromtimestamp(max(x).tolist() / 1e9)
        min_date = datetime.datetime.utcfromtimestamp(min(x).tolist() / 1e9)
        time_frame = '{}-{}-{} {}-{}-{}'.format(min_date.year, min_date.month, min_date.day,
                                                max_date.year, max_date.month, max_date.day)

        py_trend.build_payload(kw_list=[label], timeframe=time_frame, geo=yp.geo)
        pd = py_trend.interest_over_time()

        dict_days = self.hours_to_day(pd, label)

        dict_days_out_pattern = dict()
        for key, value in dict_days.items():
            date = datetime.datetime.strptime(key, "%Y-%m-%d")
            if value == 0:
                dict_days_out_pattern.update({date: 'No data'})
            elif not ((average - 2 * std) < value < (average + 2 * std)):
                dict_days_out_pattern.update({date: ((value/average - 1) * 100)})

        new_dict = dict()
        for key in sorted(dict_days_out_pattern.keys()):
            new_dict.update({key: dict_days_out_pattern.get(key)})
        self.to_csv.update({label: dict_days_out_pattern})

    def generate_to_csv(self):
        set_date = set()
        for key, value in self.to_csv.items():
            for i in value.keys():
                set_date.add(i)

        set_date = sorted(set_date)
        fieldnames = ['date'] + list(self.to_csv.keys())
        list_json = list()
        for i in set_date:
            dic = dict()
            for j in self.to_csv.keys():
                dic.update({j: self.to_csv.get(j).get(i)})
            dic.update({'date': i})
            list_json.append(dic)

        with open('output/outsiders.csv', 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for i in list_json:
                writer.writerow(i)



