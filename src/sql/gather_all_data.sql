-- SELECT DISTINCT site.name,
-- site.state,
-- site.city,
-- site.residentcount,
-- pop.change_2015_to_2016_num,
-- pop.change_2015_to_2016_percent,
-- cords.zip_code,
-- cords.latitude,
-- cords.longitude
-- FROM frw__site_directory as site
-- LEFT JOIN pop_growth as pop on site.state = pop.state and site.city = pop.city
-- LEFT JOIN firewise_corrected_cords cords on site.name = cords.name and site.city = cords.city
-- WHERE site.status <> 'Inactive'
-- ORDER BY site.city

-- CREATE TABLE topic1 AS
--   SELECT
--   new.name,
--   new.city,
--   new.county_y as county,
--   new.abbreviation,
--   invest.status as community_status,
--   invest.lifetime_investment,
--   pop.pop_percent_change,
--   CASE WHEN id.event = 'Education Event' then count(id.event) else 0 END as edu_event,
--   CASE WHEN id.event = 'Distribution Event' then count(id.event) else 0 END as dist_event,
--   CASE WHEN id.event = 'Home assessment' then count(id.event) else 0 END as home_assess,
--   CASE WHEN id.event = 'Community Preparedness' then count(id.event) else 0 END as comm_prep,
--   CASE WHEN id.event = 'Mitigation Event' then count(id.event) else 0 END as mitigation,
--   CASE WHEN id.event = 'Other' then count(id.event) else 0 END as other
--   FROM corrected_cords as new
--   LEFT JOIN old_community_info as old on lower(old.name)=lower(new.name) and old.state=new.abbreviation
--   LEFT JOIN old_community_event as old_event on old.community_id = old_event.community_id
--   LEFT JOIN mapped_topics as top on old_event.event_id = top.event_id
--   LEFT JOIN frw__community_investment as invest on invest.name = new.name and new.county_y = invest.county
--   LEFT JOIN frw__risk_reduction_hours as hours on hours.community_name = new.name and new.county_y = hours.county
--   INNER JOIN state_abb_crosswalk as st on st.abbreviation = new.abbreviation
--   LEFT JOIN county_pop_growth as pop on lower(new.county_y) = lower(pop.county) and st.state = pop.stname
--   LEFT JOIN index_crosswalk id on top.lda_topic1 = id.lda_reg_index
--   WHERE old.name is not null
--   GROUP BY 1,2,3,4,5,6,7,id.event
--   ORDER BY new.name;

--
-- CREATE TABLE all_events AS
--   SELECT *
--   FROM topic1
--   UNION
--   SELECT *
--   FROM topic2

CREATE TABLE front_end_display_data AS
  SELECT
  all_events.name,
  CASE WHEN community_status is null then 'Inactive' else community_status END as community_status,
  all_events.lifetime_investment,
  pop_percent_change,
  year_2003,
  year_2004,
  year_2005,
  year_2006,
  year_2007,
  year_2008,
  year_2009,
  year_2010,
  year_2011,
  year_2012,
  year_2013,
  year_2014,
  year_2015,
  year_2016,
  year_2017,
  residentcount,
  sum(edu_event) as edu_event,
  sum(dist_event) as dist_event,
  sum(home_assess) as home_assess,
  sum(comm_prep) as comm_prep,
  sum(mitigation) as mitigation,
  sum(other) as other
  from all_events
  left join all_investment_data invest on all_events.name = invest.name and all_events.county = invest.county
  group by 1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20
  order by 1
