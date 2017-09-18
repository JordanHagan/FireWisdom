import spacy, re
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from keras.preprocessing.text import Tokenizer
from string import punctuation, printable
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import NMF

from sklearn.datasets import fetch_20newsgroups


class NMF_class:
    def __init__(self, sql_code_str):
        self.engine = create_engine('postgresql://jordanhelen:password@localhost:5432/firewise')
        self.sql_code_str = sql_code_str
        self.df = None
        self.contents = None
        self.nmf_model = None
        self.tfidf = None
        self.tfidf_feature_names = None
        self.vocabulary = None
        self.vectorizer_model = None
        self.error = None

    def df_from_sql(self):
        print("Bringing data in...")
        self.df = pd.read_sql(self.sql_code_str, self.engine)
        self.contents = self.df[self.df.columns[0]].values

    def load_dataset(self):
        '''
        Test Data Set to ensure model works properly
        '''
        dataset = fetch_20newsgroups(shuffle=True, random_state=1,
                             remove=('headers', 'footers', 'quotes'))
        self.contents = dataset.data[:2000]

    def tfid(self):
        print("Extracting tf-idf features for NMF...")
        tfidf_vectorizer = TfidfVectorizer(max_df=0.95, min_df=.05, max_features=2000, stop_words='english', sublinear_tf=True)
        self.X = tfidf_vectorizer.fit_transform(self.contents)
        self.tfidf_feature_names = tfidf_vectorizer.get_feature_names()


    def run_nmf(self):
        print("Running NMF model...")
        self.nmf_model = NMF(n_components=5, max_iter=10000, alpha=.1, l1_ratio=.5)
        W = self.nmf_model.fit_transform(self.X)
        H = self.nmf_model.components_
        self.error = self.nmf_model.reconstruction_err_


    def print_top_words(self, model, feature_names, n_top_words=20):
        for topic_idx, topic in enumerate(model.components_):
            message = "Topic #%d: " % topic_idx
            message += " ".join([feature_names[i] for i in topic.argsort()[:-n_top_words - 1:-1]])
            print(message)
        print()


if __name__ == '__main__':
    sql = "SELECT event_desc, event_type FROM clean_event_mapping WHERE event_type <> 'GIS';"
    #sql = "SELECT description::text FROM old_community_event where description is not null;"
    nmf = NMF_class(sql)
    #nmf.load_dataset()
    nmf.df_from_sql()
    nmf.tfid()
    nmf.run_nmf()
    print(nmf.error)
    print(nmf.print_top_words(nmf.nmf_model, nmf.tfidf_feature_names, 10))
