import spacy, re
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from string import punctuation, printable
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import NMF, LatentDirichletAllocation
import pickle


class NMF_LDA_class:
    def __init__(self, sql_code_str):
        self.engine = create_engine('postgresql://jordanhelen:password@localhost:5432/firewise')
        self.sql_code_str = sql_code_str
        self.df = None
        self.contents = None
        self.X = None
        self.model = None
        self.feature_names = None
        self.error = None


    def df_from_sql(self):
        print("Bringing data in...")
        self.df = pd.read_sql(self.sql_code_str, self.engine)
        self.contents = self.df[self.df.columns[0]].values


    def clean_text(self):
        print("Lemmatizing, removing stop words, cleaning text...")
        punc_dict = {ord(punc): None for punc in punctuation}
        nlp = spacy.load("en")
        for i, line in enumerate(self.contents):
            line = line.translate(punc_dict)
            clean_doc = "".join([char for char in line if char in printable])
            line = nlp(clean_doc)
            line_list = [re.sub("\W+","",token.lemma_.lower()) for token in line if token.is_stop == False]
            line_list = [token for token in line_list if token not in ('2015','2014','2016','fire','firewise')]
            self.contents[i] = ' '.join(line_list)


    def tfid(self):
        print("Extracting tf-idf features for NMF and pickling model...")
        tfidf_vectorizer = TfidfVectorizer(max_df=.95, min_df=0.05, max_features=59)
        tfidf_model = tfidf_vectorizer.fit(self.contents)
        with open('/Users/jordanhelen/galvanize/capstone/FireWisdom/models/tfidf_model.pkl','wb') as f:
            pickle.dump(tfidf_model,f)
        self.X = tfidf_vectorizer.transform(self.contents)
        self.feature_names = tfidf_vectorizer.get_feature_names()


    def tf(self):
        print("Extracting tf features for LDA...")
        tf_vectorizer = CountVectorizer(max_df=.95, min_df=0.05, max_features=59)
        tf_model = tf_vectorizer.fit(self.contents)
        with open('/Users/jordanhelen/galvanize/capstone/FireWisdom/models/tf_model.pkl','wb') as f:
            pickle.dump(tf_model,f)
        self.X = tf_vectorizer.transform(self.contents)
        self.feature_names = tf_vectorizer.get_feature_names()


    def run_nmf(self):
        print("Running and pickling NMF model...")
        self.model = NMF(n_components=5, max_iter=10000, alpha=.1, l1_ratio=.5)
        self.model.fit(self.X)
        with open('/Users/jordanhelen/galvanize/capstone/FireWisdom/models/NMF_model.pkl','wb') as f:
            pickle.dump(self.model,f)

    def run_lda(self):
        print("Running and pickling LDA model...")
        self.model = LatentDirichletAllocation(n_components=5, max_iter=100,learning_method='online',learning_offset=50.,random_state=0)
        self.model.fit(self.X)
        with open('/Users/jordanhelen/galvanize/capstone/FireWisdom/models/LDA_model.pkl','wb') as f:
            pickle.dump(self.model,f)

    def print_top_words(self, model, feature_names, n_top_words=20):
        for topic_idx, topic in enumerate(model.components_):
            message = "Topic #%d: " % topic_idx
            message += " ".join([feature_names[i] for i in topic.argsort()[:-n_top_words - 1:-1]])
            print(message)
        print()


if __name__ == '__main__':
    sql = "SELECT event_desc, event_type FROM under_sampling_data;"
    nmf = NMF_LDA_class(sql)
    nmf.df_from_sql()
    nmf.clean_text()
    nmf.tfid()
    nmf.run_nmf()
    # nmf.tf()
    # nmf.run_lda()
    print(nmf.print_top_words(nmf.model, nmf.feature_names, 10))
