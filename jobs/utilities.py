import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud


def search_interest_label(i, df):
    with pd.plotting.plot_params.use('x_compat', True):
        df.plot(color='r', title='Search interest for {}'.format(i))
    plt.gcf().subplots_adjust(bottom=0.15)
    plt.savefig('output/interest_over_time_{}.png'.format(i), dpi=100)


def bar_chart_label(py_trend, label, name):
    py_trend.related_queries()[label][name].plot.bar(x="query", rot=90)
    plt.gcf().subplots_adjust(bottom=0.5)
    plt.savefig('output/related_queries_{}_{}.png'.format(name, label))


def word_cloud_by_label(py_trend, yp, name):
    for term in yp.terms:
        query = py_trend.related_queries()[term][name]["query"]
        value = py_trend.related_queries()[term][name]["value"]
        j = [(query[i].replace(' ', '-').capitalize() + ' ') * value[i].item() for i in range(len(query))]
        text = ''
        for i in j:
            text += i
        # Create the wordcloud object
        word_cloud = WordCloud(width=480, height=480, collocations=False).generate(text)
        plt.figure()
        plt.imshow(word_cloud, interpolation="bilinear")
        plt.axis("off")
        plt.margins(x=0, y=0)
        plt.savefig('output/related_queries_{}_word_{}.png'.format(name, term))

