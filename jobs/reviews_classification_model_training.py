from pathlib import Path
from flair.data import TaggedCorpus
from flair.data_fetcher import NLPTaskDataFetcher, NLPTask
from flair.embeddings import WordEmbeddings, FlairEmbeddings, DocumentLSTMEmbeddings
from flair.models import TextClassifier
from flair.trainers import ModelTrainer
from flair.visual.training_curves import Plotter

#  we use our own data set
data_folder = Path('C:/Users/jeanc/Documents/reviews/classif')

# 1. load corpus containing training, test and dev data
corpus: TaggedCorpus = NLPTaskDataFetcher.load_classification_corpus(data_folder,
                                                       test_file='test.txt',
                                                       dev_file='dev.txt',
                                                       train_file='train.txt')
# statistics about the dataset
stats = corpus.obtain_statistics()
print(stats)

# 2. create the label dictionary
label_dict = corpus.make_label_dictionary()

# 3. make a list of word embeddings
word_embeddings = [WordEmbeddings('glove'),

                   # comment in flair embeddings for state-of-the-art results
                   # FlairEmbeddings('news-forward'),
                   # FlairEmbeddings('news-backward'),
                   ]

# 4. init document embedding by passing list of word embeddings
document_embeddings: DocumentLSTMEmbeddings = DocumentLSTMEmbeddings(word_embeddings,
                                                                     hidden_size=512,
                                                                     reproject_words=True,
                                                                     reproject_words_dimension=256,
                                                                     )

# 5. create the text classifier
classifier = TextClassifier(document_embeddings, label_dictionary=label_dict, multi_label=True)

# 6. initialize the text classifier trainer
trainer = ModelTrainer(classifier, corpus)

# 7. start the training
trainer.train('C:/Users/jeanc/Documents/reviews/model',
              learning_rate=0.1,
              mini_batch_size=32,
              anneal_factor=0.5,
              patience=5,
              max_epochs=150)

# 8. plot training curves (optional)
plotter = Plotter()
plotter.plot_training_curves('C:/Users/jeanc/Documents/reviews/model/loss.tsv')
plotter.plot_weights('C:/Users/jeanc/Documents/reviews/model/weights.txt')
