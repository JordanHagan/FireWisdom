import pandas as pd
import re
from sqlalchemy import create_engine

float_col_dict = {
    '2003': 'year_2003',
    '2004': 'year_2004',
    '2005': 'year_2005',
    '2006': 'year_2006',
    '2007': 'year_2007',
    '2008': 'year_2008',
    '2009': 'year_2009',
    '2010': 'year_2010',
    '2011': 'year_2011',
    '2012': 'year_2012',
    '2013': 'year_2013',
    '2014': 'year_2014',
    '2015': 'year_2015',
    '2016': 'year_2016',
    '2017': 'year_2017',
    'Lifetime_Investment': 'lifetime_investment',
    'TotalInvestment': 'totalinvestment',
    'ResidentCount':  'residentcount',
    'Chipper_Costs': 'chipper_costs',
    'Other_Equipment_Costs': 'other_equipment_costs',
    'Contractor_Costs': 'contractor_costs',
    'Home_Improvement_Costs': 'home_improvement_costs',
    'Grants': 'grants',
    'Hours_Investments': 'hours_investments',
    'Investments_Total': 'investments_total',
    'Lat': 'lat',
    'Lng': 'lng'
}

def clean_df(df):
    df=df.rename(columns = float_col_dict)
    for column in df.columns:
        if column in float_col_dict.values():
            df[column] = df[column].replace(r'\$', '', regex=True).replace(r'\,', '', regex=True).astype('float')
    return df

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
    lst_of_files = ['data/data_csv/old_active_map.csv',\
    'data/data_csv/old_community_correspondence.csv',\
    'data/data_csv/old_community_event_material.csv',\
    'data/data_csv/old_community_event.csv',\
    'data/data_csv/old_community_file.csv',\
    'data/data_csv/old_community_file_map.csv',\
    'data/data_csv/old_community_info.csv',\
    'data/data_csv/old_community_renewal.csv',\
    'data/data_csv/old_community_renewal_status_map.csv',\
    'data/data_csv/old_correspondence_type_map.csv',\
    'data/data_csv/FRW - Annual Program Growth.csv',\
    'data/data_csv/FRW - Application Status.csv',\
    'data/data_csv/FRW - Community Investment.csv',\
    'data/data_csv/FRW - Renewal Report.csv',\
    'data/data_csv/FRW - Risk Reduction Hours.csv',\
    'data/data_csv/FRW - Risk Reduction Investments.csv',\
    'data/data_csv/FRW - Site Directory.csv',\
    'data/data_csv/FRW - User List.csv',\
    'data/data_csv/FRW - Vegetation Removal Report.csv',\
    '/Users/jordanhelen/galvanize/capstone/data/data_csv/zip_codes_states.csv',\
    '/Users/jordanhelen/galvanize/capstone/data/population_growth_rate_data/PEP_2016_PEPANNCHIP.US12A_with_ann.csv',\
    '/Users/jordanhelen/galvanize/capstone/data/emergency_preparedness_census_data/AHS_2013_S06AOM_with_ann.csv',\
    '/Users/jordanhelen/galvanize/capstone/data/emergency_preparedness_census_data/AHS_2013_S06AOM_metadata.csv',\
    '/Users/jordanhelen/galvanize/capstone/data/data_csv/state_abb_crosswalk.csv']

    for fle in lst_of_files:
        save_to_db(fle)
