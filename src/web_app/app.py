import pandas as pd
import json
from flask import Flask, request, render_template, jsonify
from sqlalchemy import create_engine
from collections import defaultdict
import pprint


app = Flask(__name__)

#Bring Data In
engine = create_engine('postgresql://jordanhelen:password@localhost:5432/firewise')
risk_df = pd.read_sql("Select * From front_end_display_data", engine)

#Clean up and combine all data for dictionary
risk_df = risk_df.fillna(0)
risk_df['name'] = [x.replace(u"\u2019","'").replace("/", ' ') for x in risk_df['name'].values]
yearly_investments = risk_df.as_matrix(['year_2003', 'year_2004', 'year_2005', 'year_2006', 'year_2007', 'year_2008', 'year_2009', 'year_2010', 'year_2011', 'year_2012','year_2013', 'year_2014', 'year_2015', 'year_2016', 'year_2017'])
event_info = risk_df.as_matrix(['edu_event', 'dist_event', 'home_assess', 'comm_prep','mitigation','other'])
clean_df = risk_df[['name', 'community_status', 'lifetime_investment', 'pop_percent_change', 'residentcount']]
clean_df['yearly_investments'] = yearly_investments.tolist()
clean_df['event_info'] = event_info.tolist()

# Make sub dictionary
sub_df = clean_df[['community_status', 'lifetime_investment', 'pop_percent_change','residentcount', 'yearly_investments', 'event_info']]
values = sub_df.values.tolist()
columns = sub_df.columns.values.tolist()
sub_dict = [dict(zip(columns, x)) for x in values]

#Make main dictionary
main_dict = {key:val for key, val in zip(clean_df['name'].values, sub_dict)}

@app.route('/')
def dashboard():
    return render_template('dashboard.html')

@app.route('/data')
def index():
    return json.dumps(main_dict)

@app.route('/lda_viz', methods = ['GET', 'POST'])
def lda_viz():
    return render_template('lda.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
