import pandas as pd
import numpy as np
import csv,re,sys,spacy
from sqlalchemy import create_engine
from string import punctuation, printable
import nltk
from nltk.corpus import treebank

punc_dict = {ord(punc): None for punc in punctuation}
nlp = spacy.load("en")
stop_words = ["a","the","and", "n't", "'s", "'m", "d"]

'''
1. Lower all of your text (although you could do this depending on the POS)
2. Strip out misc. spacing and punctuation
3. Remove stop words (careful they may be domain or use-case specific)
4. Stem/Lemmatize our text
5. Part-Of-Speech Tagging (spaCy is okay at this)
6. Expand feature matrix with N-grams
'''

def load_data_in(sql_code_str):
    engine = create_engine('postgresql://jordanhelen:password@localhost:5432/firewise')
    df = pd.read_sql(sql_code_str, engine)
    return list(df.description)

def clean_corpus(corpus):
    '''
    run through spacy, lemmatize, lower, remove stopwords and punctuation
    '''
    clean_corpus = []
    for doc in corpus:
        doc = doc.translate(punc_dict)
        clean_doc = "".join([char for char in doc if char in printable])
        doc = nlp(clean_doc)
        tokens = [re.sub("\W+","",token.lemma_.lower()) for token in doc] #if token.is_stop == False]
        clean_corpus.append(' '.join(w for w in tokens if w not in stop_words))
    return clean_corpus

def parse_trees(corpus):
    for doc in corpus:
        tokens = nltk.word_tokenize(doc)
        tagged = nltk.pos_tag(tokens)
        entities = nltk.chunk.ne_chunk(tagged)
        print(entities)

if __name__ == '__main__':
    sql_code_str = "select * from training_50_events;"
    corpus = load_data_in(sql_code_str)
    clean_corpus = clean_corpus(corpus)
    print(clean_corpus)
    #print(parse_trees(clean_corpus))
