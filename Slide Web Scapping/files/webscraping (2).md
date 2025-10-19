# Web screaping with Python

Web scraping is the process of extracting data from websites. It can be done using various libraries in Python, such as:
- `pandas`: scraping data from HTML tables and storing it in DataFrames.
- `requests`: for making HTTP requests to fetch web pages.
- `BeautifulSoup`: for parsing HTML and XML documents.
- `scrapy`: for building web crawlers and scraping large amounts of data.
- `selenium`: for automating web browsers and scraping dynamic content.
- `lxml`: for parsing XML and HTML documents.
- `html5lib`: for parsing HTML documents.

> In this guide, we will focus on using each of these libraries to scrape data from a website. We will cover the following topics:

> - Scraping and storing data with `pandas`
> - Making HTTP requests with `requests`
> - Parsing HTML with `BeautifulSoup`
> - Scraping dynamic content with `selenium`
> - Building a web crawler with `scrapy`
> - Best practices for web scraping
> - Legal and ethical considerations
> - Common pitfalls and how to avoid them
> - Conclusion and further resources

# Installation for web scraping libraries

Create a new conda/virtual environment and install the required libraries using pip:

```bash
# create a new conda environment
conda create -n webscraping_env python=3.10 -y
# activate the environment
conda activate webscraping_env
# install the required libraries
pip install pandas requests beautifulsoup4 scrapy selenium openpyxl lxml html5lib 
# must install libraries 
pip install ipykernel pipreqs seaborn matplotlib plotly