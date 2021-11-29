# ECE-464-Databases

# Problem Set 1 Description

**Part 1**
Download the dataset and schema of sailors and boats from our in class discussion. Write SQL queries to answer the following questions. Include your query (and its output from your terminal in a presentable fashion) in your submissions.

List, for every boat, the number of times it has been reserved, excluding those boats that have never been reserved (list the id and the name).
List those sailors who have reserved every red boat (list the id and the name).
List those sailors who have reserved only red boats.
For which boat are there the most reservations?
Select all sailors who have never reserved a red boat.
Find the average age of sailors with a rating of 10.
For each rating, find the name and id of the youngest sailor.
Select, for each boat, the sailor who made the highest number of reservations for that boat.

**Part 2**
Represent the sailors and boats schema using an ORM - I prefer SQLAlchemy but students have the freedom to choose their own language and ORM. Show that it is fully functional by writing tests with a testing framework using the data from part 1 (writing the queries for the questions in Part 1) - I prefer pytest but students are have the freedom to choose their own testing framework.

**Part 3**
Students are hired as software consults for a small business boat rental that is experiencing a heavy influx of tourism in its area. This increase is hindering operations of the mom/pop shop that uses paper/pen for most tasks. Students should explore “inefficient processes” the business may have and propose ideas for improvements - in the form of a brief write-up. Expand the codebase from part 2 to include a few jobs, reports, integrity checks, and/or other processes that would be beneficial to the business. Use the data provided in part 1 and expand it to conduct tests and show functionality. Examples include, but are not limited to:

**Bi weekly payment query**
**Monthly accounting manager**
**Daily inventory control**
**Inventory repair tracker (and cost analysis)**

# Problem Set 2 Description

### Web scraper

Create a web scraper from a preapproved site and store the data in a NoSQL database.


Datasets scraped should be "large". One should be able to ask the database a question about the scraped data, and receive an answer instantaneously.

Submissions should include two parts; the code to scrape the site, queries to the new data


Example pages may include (but are not limited to):

###### Sandbox
* [WebScraping Sandbox](http://toscrape.com/)

###### Weather
* [Weather.gov](https://www.weather.gov/)

###### Movie
* [IMDB](https://www.imdb.com/)
* [MetaCritic](https://www.metacritic.com/)
* [RottenTomatos](https://www.rottentomatoes.com/)

###### Sports
* [NBA Stats](https://stats.nba.com/)
* [Fox Sports](https://www.foxsports.com/)

...

#### Tutorials
* https://www.scrapingbee.com/blog/web-scraping-101-with-python/
* https://oxylabs.io/blog/python-web-scraping
* https://realpython.com/python-web-scraping-practical-introduction/
