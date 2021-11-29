#Danny Hong ECE-464: PSET 2 Webscraper

import requests
import pymongo
from pymongo import MongoClient
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup

#connecting to the Mongo Client
client = MongoClient('localhost', 27017)

#initializing the database
db = client["Books"]
book_collection = db.book_collection

#defining the collect_info function which collects the relevant info for each book and inserts them to a MongoDB database
def collect_info(books):

    #collecting the titles of all the books
    title = books.h3.a["title"]

    #collecting book prices of all the books and strips the Euro sign off so that it can be stored as type float
    book_price = books.findAll("p", class_ = "price_color")
    price = book_price[0].text.strip()
    price = price[1:]
    price = float(price)

    #collecting availability status of all the books
    book_available = books.findAll("p", class_ = "instock availability")
    available = book_available[0].text.strip()

    #collecting the book ratings of all the books and then converting them to numeric form before storing it as type float
    book_rating = books.article.p["class"]
    rating = book_rating[1]
    if rating == 'One':
        rating = '1'
        rating = float(rating)
    if rating == 'Two':
        rating = '2'
        rating = float(rating)
    if rating == 'Three':
        rating = '3'
        rating = float(rating)
    if rating == 'Four':
        rating = '4'
        rating = float(rating)
    if rating == 'Five':
        rating = '5'
        rating = float(rating)

    #Collecting the links to the books and ensures that the links contain the 'catalogue' string
    book_link = books.h3.a["href"]
    if 'catalogue' not in book_link:
        link = 'http://books.toscrape.com/catalogue/' + book_link
    else:
        link = 'http://books.toscrape.com/' + book_link

    #inserts each book and their relevant information into the MongoDB database
    each_book = {'Book Title':title,
                       'Book Rating':rating,
                       'Book Price (in Euros)':price,
                       'Book Availability':available,
                       'Book Link':link}
    result = book_collection.insert_one(each_book)

#defining the main function
def main():
    
    #storing the website url as a string
    url = 'http://books.toscrape.com/'
    
    #sends a get request to the specified url
    page_html = requests.get(url)
 
    #calls on BeautifulSoup for parsing
    page_soup = soup(page_html.content, "html.parser")

    #grabs all the products under the specific list tag
    book_list = page_soup.findAll("li", class_= "col-xs-6 col-sm-4 col-md-3 col-lg-3")

    #calling on the collect_info function for each book
    for books in book_list:
        collect_info(books)

    #grabs the unique html string for the next page
    next_page = page_soup.find("li", class_= "next")

    #checks if there is a next page and if so, append the html string to the original url and then go on to
    #webscrape the books on the page. 
    while next_page is not None:
        next_page = next_page.a['href']

        #ensures that the html string contains the 'catalogue' string
        if 'catalogue' not in next_page:
            new_url = url + 'catalogue/' + next_page
        else:
            new_url = url + next_page

        newpage_html = requests.get(new_url)
        newpage_soup = soup(newpage_html.content, "html.parser")
        book_list2 = newpage_soup.findAll("li", class_= "col-xs-6 col-sm-4 col-md-3 col-lg-3")

        for books2 in book_list2:
            collect_info(books2)

        next_page = newpage_soup.find("li", class_= "next")

#runs the main function
if __name__=="__main__":
    main()