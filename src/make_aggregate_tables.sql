CREATE TABLE training_50_events AS
  SELECT event_id,
  description
  FROM old_community_event
  WHERE description is not null
  ORDER BY random() LIMIT 50;

CREATE TABLE all_standing_eda_data AS
  SELECT invest.name,
  invest.state,
  invest.county,
  invest.year_2003,
  invest.year_2004,
  invest.year_2005,
  invest.year_2006,
  invest.year_2007,
  invest.year_2008,
  invest.year_2009,
  invest.year_2010,
  invest.year_2011,
  invest.year_2012,
  invest.year_2013,
  invest.year_2014,
  invest.year_2015,
  invest.year_2016,
  invest.year_2017,
  invest.lifetime_investment,
  site.totalinvestment,
  site.approvalyear,
  site.residentcount,
  site.lat,
  site.lng,
  max(substring(renew.total_active_time from '(([0-9]+.*)*[0-9]+)'))::int * 365.25 as days_active
  FROM frw__site_directory as site
  LEFT JOIN frw__renewal_report as renew on site.name=renew.name and site.state = renew.state
  LEFT JOIN frw__community_investment as invest on invest.name=site.name and site.county = invest.county
  --Where invest.status = 'In Good Standing'
  GROUP BY 1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24
  --Having count(invest.name) > 1
  ORDER BY invest.name asc;