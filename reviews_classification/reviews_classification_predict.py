from flair.models import TextClassifier
from flair.data import Sentence
import pandas as pd

classifier = TextClassifier.load_from_file('C:/Users/jeanc/Documents/reviews/model/final-model.pt')

# create example sentence
test = pd.DataFrame()
# predict tags and print
def fun(x):
    sent = Sentence(x)
    classifier.predict(sent)
    for label in sent.labels:
        return label.value


test['label1'] = test['tweet'].apply(fun)