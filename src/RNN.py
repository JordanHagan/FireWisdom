import spacy, re
import pandas as pd
from sqlalchemy import create_engine
from string import punctuation, printable
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from sklearn.preprocessing import LabelEncoder

class RNN:
    def __init__(self, sql_code_str):
        self.engine = create_engine('postgresql://jordanhelen:password@localhost:5432/firewise')
        self.sql_code_str = sql_code_str
        self.df = None
        self.y = None
        self.y_labels = None
        self.X = None
        self.X_padded_sequences= None

    def df_from_sql(self):
        '''
        Bring Data in from SQL
        SQL Code should only contain 2 columns (your X and y)
        X should be the first column, y second
        '''
        self.df = pd.read_sql(self.sql_code_str, self.engine)
        self.X = self.df[self.df.columns[0]].values
        self.y = self.df[self.df.columns[1]].values

    def make_labels(self):
        le = LabelEncoder()
        self.y_labels = le.fit_transform(self.y)

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
        tokenizer = Tokenizer()
        tokenizer.fit_on_texts(self.X)
        X_sequences = tokenizer.texts_to_sequences(self.X)
        self.X_padded_sequences = pad_sequences(X_sequences)


if __name__ == '__main__':
    sql = 'SELECT event_desc, event_type FROM clean_event_mapping;'
    rnn = RNN(sql)
    rnn.df_from_sql()
    rnn.make_labels()
    rnn.clean_text()
    rnn.tokenize()
    print(rnn.X_padded_sequences)
    print(rnn.y_labels)
