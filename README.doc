
Code:

   Write a scraper in a language of your choice (preferably Python/Go).
      ○ It should receive 2 params: initial url & max depth.
      ○ The scraper should start scraping from the initial url, find all the links inside the page & continue scraping them recursively (until reaching the max depth).
      ○ The scraper should save it results to a db of your choice (SQLite for example), each result should contain:
            i. url
            ii. source url (where it appeared)
            iii. depth from the initial url
            iv. page title
            v. all the links inside the page and their text.

                1. For example the “http://example.com” will contain title:
                “Example Domain” and links
                “https://www.iana.org/domains/example:’More Information...’”

      ○ The scraper should be multi-threaded so high-scale scraping (100k of requests) will finish in a reasonable time.

   Bonus:
      i. The scraper should support starting from where it stopped in case of a crash
      ii. Some of the sites detect scrapers and block them, describe 2 ways to avoid those blocks
         Answers: 1. use TOR 
                  2. use cloud instances in different regions and use different ip address 
                  3. try to find mirror site ( is a copy of a website hosted on another server)
                  4. try to find services rest api for sends an HTTP Request to the REST API and get information 
      



Technical:

I.
   A user requested a page from your server.
   This is the log from the serve-side:
      64.227.50.115 - [10/Oct/2000:13:55:36 -0700] 200
      "http://www.example.com/start.html" "Mozilla/5.0 (Windows NT 10.0; Win64; x64)
      AppleWebKit/537.36 (KHTML, like Gecko) Selenium Chrome/84.0.4147.135
      Safari/537.36

   What can we learn about this user? List all information you can deduce.

   ○ Answers:
      1. ip + possible geographic location
      2. date of request
      3. request was successful (code 200)
      4. user requested url using http (non-secured) protocol from port 80
      5. user requested data from domain www.example.com
      6. user requested the path "/start.html" from the domain above
      7. user used Selenium (qa tool) on Chrome version 84.0.4147.135 on Windows 10 x64


II.
   SQL
      ○ The questions are based on COVID19 publicly accessible BigQuery dataset -
         `bigquery-public-data.covid19_ecdc.covid_19_geographic_distribution_worldwide` (Google has a free Tier of up to 1 TB and there is no need to pay for querying)
      Use https://console.cloud.google.com/bigquery for querying
      ○ For each question please provide the query that will yield the answer to the question. The query can be nested and complex but it should be a single query and answer the question specifically.
      
      ○ Questions:
         i. What are the countries ranked as 3rd and 7th by daily deaths (descending) on September 10th, 2020
         ii. What is the total number of world wide daily confirmed cases on the day Brazil had the most number of daily confirmed cases

○ Answers:
   i. - bigquery_1.sql
        https://console.cloud.google.com/bigquery?sq=800890829489:4a34fb118d6e450daabd4c56217e6996
        Arpeely/results-20201203-174400.json
    ii. - bigquery_2.sql
        https://console.cloud.google.com/bigquery?sq=800890829489:14d96ac26251419296c8e873177e6165
        Arpeely/results-20201203-203059.json
