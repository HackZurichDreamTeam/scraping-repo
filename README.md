# Data Scraping Repository for the MIGROS CHALLENGE

This is part of a larger project to improvement supply chain resilience using real-time warning systems from open-source data. For more information on how we use data please see our [migros analytics repo](https://github.com/HackZurichDreamTeam/migros-analytics). 

In this repository we scrape data from the open data sources: [severeweather.wmo.int](https://severeweather.wmo.int) - aggregator of current weather warnings across the globe, and [iccs-ccs.org](https://www.icc-ccs.org/index.php) - aggregator of piracy warnings across the globe. We use [googleapis](https://maps.googleapis.com) to obtain latitude and longitude coordinates of warning locations from text. 

We scrape every 30 minutes using [GitHub actions](https://github.com/features/actions).

To view our finished project see: [Supply Chain Resilience: Real-time Risk Warning at Hand](https://hackzurich22-4068.ew.r.appspot.com/admin/dashboard)
