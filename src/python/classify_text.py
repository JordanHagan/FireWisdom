import spacy, re
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from string import punctuation, printable
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import NMF, LatentDirichletAllocation
import pickle
from NMF_or_LDA import NMF_LDA_class
from keras.models import load_model
from collections import OrderedDict
import matplotlib.pyplot as plt

class Run_Model:
    def __init__(self, sql_code_str, model_class):
        self.engine = create_engine('postgresql://jordanhelen:password@localhost:5432/firewise')
        self.sql_code_str = sql_code_str
        self.model_class = model_class
        self.df = None
        self.contents = None
        self.tf_model = None
        self.LDA_model = None
        self.LDA_X = None
        self.LDA_doc_topic_dist = None
        self.tfidf_model = None
        self.NMF_model = None
        self.NMF_X = None
        self.NMF_doc_topic_dist = None

    def open_models(self):
        print('Unpickling models...')
        with open('/Users/jordanhelen/galvanize/capstone/FireWisdom/models/LDA_model.pkl', 'rb') as f:
            self.LDA_model = pickle.load(f)
        with open('/Users/jordanhelen/galvanize/capstone/FireWisdom/models/tf_model.pkl', 'rb') as t:
            self.tf_model = pickle.load(t)
        with open('/Users/jordanhelen/galvanize/capstone/FireWisdom/models/NMF_model.pkl', 'rb') as f:
            self.NMF_model = pickle.load(f)
        with open('/Users/jordanhelen/galvanize/capstone/FireWisdom/models/tfidf_model.pkl', 'rb') as t:
            self.tfidf_model = pickle.load(t)

    def get_data(self):
        self.model_class.df_from_sql()
        self.model_class.clean_text()
        self.df = self.model_class.df
        self.contents = self.model_class.contents
        self.df['cleaned_text'] = self.contents

    def run_data_in_TF_model(self):
        print("Running data through TF model...")
        self.LDA_X = self.tf_model.transform(self.contents)

    def run_data_in_LDA_model(self):
        print("Running data through LDA model...")
        self.LDA_doc_topic_dist = self.LDA_model.transform(self.LDA_X)

    def run_data_in_TFIDF_model(self):
        print("Running data through TFIDF model...")
        self.NMF_X = self.tfidf_model.transform(self.contents)

    def run_data_in_NMF_model(self):
        print("Running data through NMF model...")
        self.NMF_doc_topic_dist = self.NMF_model.transform(self.NMF_X)

    def combine_topics_to_df(self):
        sub_topic_array = [[i for i,val in enumerate(row) if val >.40] for row in self.LDA_doc_topic_dist]
        others_index = [i for i,x in enumerate(self.LDA_doc_topic_dist) if x[0]==0.2 and x[1]==0.2]
        topic_array = [[5] if i in others_index else x for i,x in enumerate(sub_topic_array)]
        final_topic_array = [[np.argmax(self.LDA_doc_topic_dist[i])] if x == [] else x for i,x in enumerate(topic_array)]
        lda_topic1 = [x[0] for x in final_topic_array]
        lda_topic2 = [x[1] if len(x) == 2 else None for x in final_topic_array]
        self.df['lda_topic1'] = lda_topic1
        self.df['lda_topic2'] = lda_topic2
        self.df[['event_id','cleaned_text','lda_topic1','lda_topic2']].to_sql('mapped_topics', self.engine, if_exists='append')
        mapping_dict = OrderedDict({'event': ['Distribution Event', 'Education Event', 'Home assessment', 'Community Preparedness', 'Mitigation Event', 'Other'],
                 'lda_reg_index': [2,4,1,0,3,5],
                 'lda_viz_index': [1,2,3,4,5,6],
                 'nmf_index': [0,3,1,2,4,5]})
        mapping_df = pd.DataFrame.from_dict(mapping_dict)
        mapping_df.to_sql('index_crosswalk', self.engine, if_exists='append')


if __name__ == '__main__':
    sql_code_str = "select description, event_id from old_community_event where description is not null or description <> '';"
    model_class = NMF_LDA_class(sql_code_str)
    run = Run_Model(sql_code_str, model_class)
    run.open_models()
    run.get_data()
    run.run_data_in_TF_model()
    run.run_data_in_LDA_model()
    # run.run_data_in_TFIDF_model()
    # run.run_data_in_NMF_model()
    run.combine_topics_to_df()
