/*
Create active community table and all community tables for use in Pandas.
Comment out "WHERE invest.status = 'In Good Standing'" line
and change table name for all communities table
*/
CREATE TABLE only_active_eda_data AS
  SELECT site.name,
  site.state,
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
  site.site_mailing_address,
  max(substring(renew.total_active_time from '(([0-9]+.*)*[0-9]+)'))::int * 365.25 as days_active
  FROM frw__site_directory as site
  LEFT JOIN frw__renewal_report as renew on site.name=renew.name and site.state = renew.state
  LEFT JOIN frw__community_investment as invest on invest.name=site.name and site.county = invest.county
  WHERE site.status = 'In Good Standing'
  GROUP BY 1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25
  ORDER BY site.name asc;

/*
Bring together 2014 and 2015 self mapping of community events into one table for clean up
*/
CREATE TABLE event_mapping AS
  SELECT
  map_2014."comm id" as comm_id,
  map_2014."name" as comm_name,
  map_2014."firewise day event" as event_desc,
  map_2014."event type" as mapped_event_type,
  CASE when map_2014."renewal year" is null then 2014 else map_2014."renewal year" END as renewal_year
  FROM mapped_community_events_2014 as map_2014
  ----
  UNION
  ----
  SELECT
  map_2015."fwc id" as comm_id,
  map_2015."fwc name" as comm_name,
  map_2015."event description" as event_desc,
  map_2015."event type" as mapped_event_type,
  '2015' as renewal_year
  FROM mapped_community_events_2015 as map_2015;

/*
Clean up the mapped data and make table
*/
CREATE TABLE clean_event_mapping AS
  SELECT DISTINCT
  comm_id,
  comm_name,
  event_desc,
  renewal_year,
  CASE
    when mapped_event_type like '%Mit%' then 'Mitigation Event'
    when mapped_event_type like '%Edu%' then 'Education Event'
    when (mapped_event_type like '%Dis%' or mapped_event_type like '%Dst%') then 'Distribution Event'
    else mapped_event_type
  END AS event_type
  FROM event_mapping
  WHERE mapped_event_type is not null
  AND mapped_event_type <> 'No info'
