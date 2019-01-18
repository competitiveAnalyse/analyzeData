from pytrends.request import TrendReq
import datetime, time
import numpy as np
import csv

class Stats:

    def __init__(self, yp):
        self.conditions = dict()
        self.generate_condition(yp)
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
        print(label)
        dict_days = self.hours_to_day(pd, label)
        days = dict()
        for key, value in dict_days.items():
            date = datetime.datetime.strptime(key, "%Y-%m-%d")
            day = date.weekday()
            if days.get(day) is None:
                days.update({day: [value]})
            else:
                days.update({day: days.get(day) + [value]})

        condition = dict()
        for key in days.keys():
            data = days.get(key)
            condition.update({key: (np.std(data), np.average(data))})

        self.conditions.update({label: condition})

    def generate_condition(self, yp):
        py_trend = TrendReq()

        for i in yp.terms:
            pd = py_trend.get_historical_interest([i], year_start=2017, month_start=1, day_start=1,
                                                  hour_start=0, year_end=2018, month_end=1, day_end=1,
                                                  hour_end=23, cat=0, geo='', gprop='', sleep=0)
            self.model_condition(pd, i)
        print("END")

    def check_value(self, df):
        py_trend = TrendReq()
        label = list(df)[0]
        condition = self.conditions.get(label)
        print(condition)
        x = df.index.values
        max_date = datetime.datetime.utcfromtimestamp(max(x).tolist() / 1e9)
        min_date = datetime.datetime.utcfromtimestamp(min(x).tolist() / 1e9)
        print(type(min_date.year),min_date.year, min_date.month, type(min_date.month),  type(min_date.day), min_date.day)
        pd = py_trend.get_historical_interest([label], year_start=min_date.year, month_start=min_date.month,
                                              day_start=min_date.day, hour_start=0, year_end=max_date.year,
                                              month_end=max_date.month, day_end=max_date.day, hour_end=23,
                                              cat=0, geo='', gprop='', sleep=0)
        dict_days = self.hours_to_day(pd, label)
        print(label)
        dict_days_out_pattern = dict()
        for key, value in dict_days.items():
            date = datetime.datetime.strptime(key, "%Y-%m-%d")
            day = date.weekday()
            std, average = condition.get(day)
            if value == 0:
                dict_days_out_pattern.update({date: 'No data'})
            elif not ((average - 2 * std) < value < (average + 2 * std)):
                dict_days_out_pattern.update({date: (value/average)})

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
        print(set_date)
        fieldnames = ['date'] + list(self.to_csv.keys())
        print(fieldnames)
        list_json = list()
        for i in set_date:
            dic = dict()
            for j in self.to_csv.keys():
                dic.update({j: self.to_csv.get(j).get(i)})
            dic.update({'date': i})
            list_json.append(dic)

            print(self.to_csv.get(j))
            print(self.to_csv.get(j).get(i))

        with open('names.csv', 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for i in list_json:
                writer.writerow(i)



