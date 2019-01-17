from flair.models import TextClassifier
from flair.data import Sentence

classifier = TextClassifier.load_from_file('C:/Users/jeanc/Documents/reviews/model/final-model.pt')

# create example sentence
sentence = Sentence('you can build your own computer which will be more powerful and probably better looking for less than the price they are selling them for.')

# predict tags and print
classifier.predict(sentence)

print(sentence.labels)