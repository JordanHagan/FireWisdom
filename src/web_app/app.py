import pandas as pd
import json
import pprint
from flask import Flask, request, render_template, jsonify, Response
from collections import defaultdict

import numpy as np

app = Flask(__name__)

#Bring Data In
risk_df = pd.read_csv('Firewise_final_data.csv')

#Clean up and combine all data for dictionary
risk_df = risk_df.fillna(0)
risk_df['name'] = [x.replace(u"\u2019","'").replace("/", ' ') for x in risk_df['name'].values]
yearly_investments = risk_df.as_matrix(['year_2003', 'year_2004', 'year_2005', 'year_2006', 'year_2007', 'year_2008', 'year_2009', 'year_2010', 'year_2011', 'year_2012','year_2013', 'year_2014', 'year_2015', 'year_2016', 'year_2017'])
event_info = risk_df.as_matrix(['edu_event', 'dist_event', 'home_assess', 'comm_prep','mitigation','other'])
population_change = risk_df.as_matrix(['pop_change_10_11', 'pop_change_11_12', 'pop_change_12_13', 'pop_change_13_14', 'pop_change_14_15', 'pop_change_15_16'])
clean_df = risk_df[['name', 'st_abb', 'city', 'community_status', 'lifetime_investment', 'residentcount']]
clean_df['yearly_investments'] = yearly_investments.tolist()
clean_df['event_info'] = event_info.tolist()
clean_df['pop_change'] = population_change.tolist()

# Make sub dictionary
sub_df = clean_df[['community_status', 'lifetime_investment','residentcount', 'yearly_investments', 'event_info', 'pop_change']]
values = sub_df.values.tolist()
columns = sub_df.columns.values.tolist()
sub_dict = [dict(zip(columns, x)) for x in values]

#Make main dictionary
main_dict = {key:val for key,val in zip(clean_df['name'].values +' ('+ clean_df['city'].values + ', ' + clean_df['st_abb'].values + ')', sub_dict)}

@app.route('/')
def dashboard():
    return render_template('dashboard.html')

@app.route('/data')
def index():
    resp = Response(json.dumps(main_dict))
    resp.headers['Content-Type'] = 'application/json'
    return resp

@app.route('/lda_viz', methods = ['GET', 'POST'])
def lda_viz():
    return render_template('lda.html')

@app.route('/leaderboard', methods = ['GET', 'POST'])
def leaderboard():
    return render_template('leaderboard.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True, threaded=True)
