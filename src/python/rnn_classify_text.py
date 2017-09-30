import spacy, re
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from RNN import Build_RNN_model
from keras.models import load_model
import pickle

class RNN_model:
    def __init__(self, sql_code_str, model_class):
        self.engine = create_engine('postgresql://jordanhelen:password@localhost:5432/firewise')
        self.sql_code_str = sql_code_str
        self.rnn_model = load_model('/Users/jordanhelen/galvanize/capstone/FireWisdom/models/rnn_model.h5')
        with open('/Users/jordanhelen/galvanize/capstone/FireWisdom/models/lable_model.pkl','rb') as h:
            self.le_model = pickle.load(h)
        self.model_class = model_class
        self.df = None
        self.X = None

    def clean_text_model(self):
        self.model_class.df_from_sql()
        self.model_class.clean_text()
        self.model_class.tokenize()
        self.df = self.model_class.df
        self.X = self.model_class.X

    def run_data_in_RNN_model(self):
        X_predictions = self.rnn_model.predict(self.X)
        X_predictions = np.argmax(X_predictions, axis=1)
        le_predictions = self.le_model.inverse_transform(X_predictions)
        test = self.le_model.inverse_transform(2)
        print(le_predictions)
        print(test)

if __name__ == '__main__':
    sql_code_str = "SELECT description, event_id FROM old_community_event WHERE event_id in ('388','2439','2658','3723','4233','4479','4723','5796')"
    model_class = Build_RNN_model(sql_code_str)
    run = RNN_model(sql_code_str, model_class)
    run.clean_text_model()
    run.run_data_in_RNN_model()
