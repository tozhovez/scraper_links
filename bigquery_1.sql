##What are the countries ranked as 3rd and 7th by daily deaths (descending) on September 10th, 2020


WITH all_result as (SELECT  date,  daily_deaths,    countries_and_territories
FROM
  `bigquery-public-data.covid19_ecdc.covid_19_geographic_distribution_worldwide`
WHERE
  date='2020-09-10'
ORDER BY daily_deaths DESC
limit 7 ),
rank_3 as (select * from all_result limit 1 OFFSET 2),
rank_7 as(select * from all_result limit 1 OFFSET 6)
select * from rank_3
UNION ALL
select * from rank_7 ORDER BY daily_deaths DESC
