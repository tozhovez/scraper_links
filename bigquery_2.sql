

# What is the total number of world wide daily confirmed cases on the day Brazil had the most number of daily confirmed cases


# Result: only total_daily_confirmed_cases

select sum(daily_confirmed_cases) as total_daily_confirmed_cases
from `bigquery-public-data.covid19_ecdc.covid_19_geographic_distribution_worldwide`
where date in (select date from `bigquery-public-data.covid19_ecdc.covid_19_geographic_distribution_worldwide`
where daily_confirmed_cases in (select max(daily_confirmed_cases) as max_daily_confirmed_cases_in_brazil
from `bigquery-public-data.covid19_ecdc.covid_19_geographic_distribution_worldwide`
where countries_and_territories='Brazil') and countries_and_territories='Brazil')





# Result: with date and total_daily_confirmed_cases and total_confirmed_cases

select date, sum(daily_confirmed_cases) as total_daily_confirmed_cases, sum(confirmed_cases) as total_confirmed_cases
from  `bigquery-public-data.covid19_ecdc.covid_19_geographic_distribution_worldwide`  where
date in (select date  from  `bigquery-public-data.covid19_ecdc.covid_19_geographic_distribution_worldwide`
where daily_confirmed_cases in (select max(daily_confirmed_cases) as max_daily_confirmed_cases_in_brazil
 from  `bigquery-public-data.covid19_ecdc.covid_19_geographic_distribution_worldwide`
  where countries_and_territories='Brazil') and countries_and_territories='Brazil')
group by date



