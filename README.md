# DoneDeal.ie Nested Webscraper

This Python script is one component of the CarCompare meta-search engine (also on GitHub). 

## Purpose
This Python application (inc. BeautifulSoup library) is designed to scrape details of all 70,000+ car listings on DoneDeal and post them to an SQL database for the purpose of integrating this platform's market offerings with others, including CarZone, AutoTrader, Gumtree and cooperating dealerships' databases.

This database then feeds into a central repository for the CarCompare integrated trading platform (via a MuleSoft API network).

##Points of Note
When testing this script, a reasonably fast internet connection is necessary to avoid premature ConnectionTimeout and IncompleteRead errors.

This script is multithreaded (16 threads), though 16 threads are not required by the machine running the script. For example, on a machine with 8 threads, you will note a performance plateau beyond 8 threads, as your cores' resources will be time-spliced in order to simulate 16 parallel processes.




