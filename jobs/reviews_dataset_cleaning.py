import pandas as pd

#start_date = '2018-11-1'
#end_date = '2018-12-31'
product = "razer"

# csv cleaning
df = pd.read_csv('C:/Users/jeanc/Documents/reviews/items_trustpilot_' + razer + '.csv', parse_dates=['time'])
df = df.drop(columns='_type')
df = df.drop(columns='data_type')
df["vote"] = df["vote"].astype(int)
df["reviewer_review_count"] = df["reviewer_review_count"].astype(int)
df["product"] = df["product"].str.lower()
df['time'] = pd.to_datetime(df['time'])

# selection by date
#mask = (df['time'] > start_date) & (df['time'] <= end_date)
#df = df.loc[mask]

#export clean dataset
csv_data = df.to_csv('C:/Users/jeanc/Documents/reviews/items_trustpilot_' + razer + '_clean.csv', encoding='utf-8', index=False)