import pandas as pd
from nltk.corpus import stopwords
import nltk
import ssl
import matplotlib.pyplot as plt
from wordcloud import WordCloud

list_comment = ['razer', 'acer', 'hp', 'alienware', 'asus', 'msi']


def generate_word_cloud(yp, date_min, date_max):

    label_comment = [i for i in yp.terms if i.lower() in list_comment]

    try:
        _create_unverified_https_context = ssl._create_unverified_context
    except AttributeError:
        pass
    else:
        ssl._create_default_https_context = _create_unverified_https_context

    nltk.download('stopwords')
    start_date = date_min
    end_date = date_max

    for j in label_comment:
        product = j

        # csv cleaning
        df = pd.read_csv('dataset/reviews/items_trustpilot_' + product + '.csv', parse_dates=['time'])
        df = df.drop(columns='_type')
        df = df.drop(columns='data_type')
        df["vote"] = df["vote"].astype(int)
        df["reviewer_review_count"] = df["reviewer_review_count"].astype(int)
        df["product"] = df["product"].str.lower()
        df['time'] = pd.to_datetime(df['time'])

        mask = (df['time'] >= start_date) & (df['time'] <= end_date)

        neutral_string = str()
        positive_string = str()
        negative_string = str()

        df = df.loc[mask]
        print(df)
        for i in range(len(df.index.values)):
            vote = df['vote'].values[i]
            comment = df["comment"].values[i]
            if vote == 3:
                neutral_string += ' '.join([word for word in comment.split()
                                            if word not in stopwords.words("english")])
            elif vote < 3:
                negative_string += ' '.join([word for word in comment.split()
                                             if word not in stopwords.words("english")])
            else:
                positive_string += ' '.join([word for word in comment.split()
                                             if word not in stopwords.words("english")])
        if len(positive_string) != 0:
            word_cloud = WordCloud(width=480, height=480, collocations=False).generate(positive_string)
            plt.figure()
            plt.title('Word most frequent')
            plt.imshow(word_cloud, interpolation="bilinear")
            plt.axis("off")
            plt.margins(x=0, y=0)
            plt.savefig('output/positif_{}.png'.format(product))
            plt.clf()
        if len(negative_string) != 0:
            word_cloud = WordCloud(width=480, height=480, collocations=False).generate(negative_string)
            plt.figure()
            plt.title('Word most frequent')
            plt.imshow(word_cloud, interpolation="bilinear")
            plt.axis("off")
            plt.margins(x=0, y=0)
            plt.savefig('output/negatif_{}.png'.format(product))
            plt.clf()
        if len(neutral_string) != 0:
            word_cloud = WordCloud(width=480, height=480, collocations=False).generate(neutral_string)
            plt.figure()
            plt.title('Word most frequent')
            plt.imshow(word_cloud, interpolation="bilinear")
            plt.axis("off")
            plt.margins(x=0, y=0)
            plt.savefig('output/neutre_{}.png'.format(product))
            plt.clf()
# selection by date
#mask = (df['time'] > start_date) & (df['time'] <= end_date)
#df = df.loc[mask]

#export clean dataset
#csv_data = df.to_csv('C:/Users/jeanc/Documents/reviews/items_trustpilot_' + razer + '_clean.csv', encoding='utf-8', index=False)