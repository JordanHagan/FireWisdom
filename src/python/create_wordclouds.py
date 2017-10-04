import matplotlib.pyplot as plt
import pickle
import pandas as pd
import spacy, re
from string import punctuation, printable
from sqlalchemy import create_engine
from wordcloud import WordCloud
plt.style.use('ggplot')

class Make_Word_Cloud:
    def __init__(self):
        self.engine = create_engine('postgresql://jordanhelen:password@localhost:5432/firewise')
        self.topics =['Education Event', 'Community Preparedness', 'Home assessment', 'Mitigation Event', 'Distribution Event']

    def df_from_sql(self, sql):
        print("Bringing data in...")
        df = pd.read_sql(sql, self.engine)
        return df

    def clean_text(self, text):
        print("Lemmatizing, removing stop words, cleaning text...")
        punc_dict = {ord(punc): None for punc in punctuation}
        nlp = spacy.load("en")
        cleaned_text = []
        for i, line in enumerate(text):
            line = line.translate(punc_dict)
            clean_doc = "".join([char for char in line if char in printable])
            line = nlp(clean_doc)
            line_list = [re.sub("\W+","",token.lemma_.lower()) for token in line if token.is_stop == False]
            line_list = [token for token in line_list if token not in ('2015','2014','2016','fire','firewise')]
            cleaned_text.extend(line_list)
        return cleaned_text

    def make_the_cloud(self, cleaned_text_list, topic):
        print("Making pretty clouds!")
        cleaned_text = ' '.join(cleaned_text_list)
        wordcloud = WordCloud(background_color="white", max_words=100, width=1600, height=800).generate(cleaned_text)
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis("off")
        plt.savefig(topic)


if __name__ == '__main__':
    wc = Make_Word_Cloud()
    for topic in wc.topics:
        sql = "SELECT event_desc, event_type FROM under_sampling_data WHERE event_type = {};".format("'"+ topic +"'")
        df = wc.df_from_sql(sql)
        text_list = wc.clean_text(df[df.columns[0]].values)
        wc.make_the_cloud(text_list, topic)
