import spacy, re
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from string import punctuation, printable
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.layers import Embedding, LSTM, Dense, Dropout, Conv1D, MaxPooling1D
from keras.models import Sequential
from imblearn.over_sampling import SMOTE
from keras.models import load_model
import pickle

class Build_RNN_model:
    def __init__(self, sql_code_str):
        self.engine = create_engine('postgresql://jordanhelen:password@localhost:5432/firewise')
        self.sql_code_str = sql_code_str
        self.df = None
        self.X = None
        self.y = None
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
        self.model = None
        self.tokenizer = None
        self.score = None
        self.accuracy = None


    def df_from_sql(self):
        '''
        Bring in the data and split X and y values
        '''
        self.df = pd.read_sql(self.sql_code_str, self.engine)
        self.X = self.df[self.df.columns[0]].values
        self.y = self.df[self.df.columns[1]].values


    def make_labels(self):
        le_model = LabelEncoder()
        le_model = le_model.fit(self.y)
        with open('lable_model.pkl','wb') as f:
            pickle.dump(le_model,f)
        self.y = le_model.transform(self.y)


    def clean_text(self):
        '''
        Clean and Lemmatize X Text Values
        '''
        punc_dict = {ord(punc): None for punc in punctuation}
        nlp = spacy.load("en")
        for i, line in enumerate(self.X):
            line = line.translate(punc_dict)
            clean_doc = "".join([char for char in line if char in printable])
            line = nlp(clean_doc)
            line_list = [re.sub("\W+","",token.lemma_.lower()) for token in line if token.is_stop == False]
            self.X[i] = ' '.join(line_list)

    def tokenize(self):
        '''
        Tokenize and Pad the clean data to use in the Neural Network
        '''
        self.tokenizer = Tokenizer(num_words=600)
        self.tokenizer.fit_on_texts(self.X)
        X_sequences = self.tokenizer.texts_to_sequences(self.X)
        self.X = pad_sequences(X_sequences, maxlen=500)

    def train_test_split(self):
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(self.X, self.y, test_size=0.30)

    def resample(self):
        '''
        The data is imbalanced, we must fix that before we traing the RNN
               event_type       | count
        ------------------------+-------
         Community Preparedness |    30
         Home assessment        |    51
         Education Event        |   846
         Mitigation Event       |  1538
         Distribution Event     |   511
        '''
        sm = SMOTE(random_state=12)
        self.X_train, self.y_train = sm.fit_sample(self.X_train, self.y_train)


    def lstm(self):
        self.model = Sequential()
        self.model.add(Embedding(600, 128, input_length=500))
        self.model.add(Conv1D(64, 5, activation='relu'))
        self.model.add(LSTM(128, dropout=0.2, recurrent_dropout=0.2))
        self.model.add(Dense(6, activation='softmax'))
        self.model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
        self.model.fit(self.X_train, self.y_train, batch_size=128, epochs=9, class_weight='auto')
        self.model.save('rnn_model.h5')

    def get_score(self):
        self.score = self.model.evaluate(self.X_test, self.y_test)[0]
        self.accuracy = self.model.evaluate(self.X_test, self.y_test)[1]



if __name__ == '__main__':
    sql = "SELECT event_desc, event_type FROM clean_event_mapping WHERE event_type <> 'GIS';"
    rnn = Build_RNN_model(sql)
    rnn.df_from_sql()
    rnn.make_labels()
    rnn.clean_text()
    rnn.tokenize()
    rnn.train_test_split()
    rnn.lstm()
    rnn.get_score()
    print("Score: ", rnn.score)
    print("Accuracy: ", rnn.accuracy)
