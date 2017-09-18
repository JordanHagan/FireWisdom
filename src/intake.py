import pandas as pd
import re
from sqlalchemy import create_engine


def create_df(filepath):
    df = pd.read_csv(filepath)
    df.columns = [c.lower() for c in df.columns] #postgres doesn't like capitals or spaces
    return df

def create_sql_table(dataframe, table_name):
    engine = create_engine('postgresql://jordanhelen:password@localhost:5432/firewise')
    dataframe.to_sql(table_name, engine)

def create_table_names(fle):
    chunks = fle.split('/')
    name = re.findall('(.*?).csv', chunks[-1].lower().replace("-", "").replace(" ", "_"))[0]
    return name

def save_to_db(filepath):
    table_name = create_table_names(filepath)
    dataframe = create_df(filepath)
    cleaned_dataframe = clean_df(dataframe)
    create_sql_table(cleaned_dataframe, table_name)


if __name__ == '__main__':
    lst_of_files = ['']

    for fle in lst_of_files:
        save_to_db(fle)
