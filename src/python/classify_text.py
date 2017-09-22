import spacy, re
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from string import punctuation, printable
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import NMF, LatentDirichletAllocation
import pickle
from NMF_or_LDA import NMF_LDA_class

class Run_Model:
    def __init__(self, sql_code_str, model_class):
        self.engine = create_engine('postgresql://jordanhelen:password@localhost:5432/firewise')
        self.sql_code_str = sql_code_str
        self.model_class = model_class
        self.df = None
        self.contents = None
        self.X = None
        self.text_model = None
        self.tf_model = None
        self.doc_topic_dist = None

    def open_models(self):
        print('Unpickling models...')
        with open('/Users/jordanhelen/galvanize/capstone/FireWisdom/models/text_model.pkl', 'rb') as f:
            self.text_model = pickle.load(f)
        with open('/Users/jordanhelen/galvanize/capstone/FireWisdom/models/tf_model.pkl', 'rb') as t:
            self.tf_model = pickle.load(t)

    def get_data(self):
        self.model_class.df_from_sql()
        self.model_class.clean_text()
        self.df = self.model_class.df
        self.contents = self.model_class.contents

    def run_data_in_TF_model(self):
        print("Runing data through TF model...")
        self.X = self.tf_model.transform(self.contents)

    def run_data_in_LDA_model(self):
        print("Runing data through LDA model...")
        self.doc_topic_dist = self.text_model.transform(self.X)

    def combine_topics_to_df(self):
        topic_array = np.argmax(self.doc_topic_dist, axis=1)
        self.df['topics'] = topic_array
        self.df[['event_id','topics']].to_sql('mapped_topics', self.engine)

if __name__ == '__main__':
    sql_code_str = "select description, event_id from old_community_event where description is not null or description <> '';"
    model_class = NMF_LDA_class(sql_code_str)
    run = Run_Model(sql_code_str, model_class)
    run.open_models()
    run.get_data()
    run.run_data_in_TF_model()
    run.run_data_in_LDA_model()
    run.combine_topics_to_df()
