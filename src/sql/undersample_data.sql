--CREATE TABLE under_sampling_data AS
  (SELECT
  event_desc,
  event_type
  FROM clean_event_mapping
  WHERE event_type in ('GIS', 'Community Preparedness', 'Home assessment'))

  UNION

  (SELECT
  event_desc,
  event_type
  FROM clean_event_mapping
  WHERE event_type = 'Education Event'
  ORDER BY random()
  LIMIT 50)

  UNION ALL

  (SELECT
  event_desc,
  event_type
  FROM clean_event_mapping
  WHERE event_type = 'Mitigation Event'
  ORDER BY random()
  LIMIT 60)


  UNION ALL

  (SELECT
  event_desc,
  event_type
  FROM clean_event_mapping
  WHERE event_type = 'Distribution Event'
  ORDER BY random()
  LIMIT 50)
