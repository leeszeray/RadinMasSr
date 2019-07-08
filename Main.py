import time
from bs4 import BeautifulSoup
from random import randint
from time import sleep
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from ScrapePages import extract_relevant_links, extract_individual_pages
from UploadFireBase import upload_data
import multiprocessing
import pandas as pd


def main():
    then = time.time()  # Time before the operations start
    chrome_options = Options()
    chrome_options.headless = True

    url_page = 'https://www.onepa.sg/cc/radin-mas-cc#tabs-2'  # specify the url
    print("Program started, scraping the following website:")
    print(url_page)  # print url page to visually signify start of program
    driver = webdriver.Chrome(chrome_options=chrome_options)  # run chrome web driver
    driver.get(url_page)  # get web page

    sleep(randint(20, 50))  # wait for page to load

    html = driver.page_source   # retrieve page source as html
    soup = BeautifulSoup(html)  # convert html to beautiful soup

    # retrieves the number of pages
    page_details = str(soup.find("div", attrs={"id": "content_0_pagination"}))  # retrieves page details
    quote_count = page_details.count("\"")  # count number of quotes within the page details
    temp_list = page_details.split("\"", quote_count + 1)  # spilt page details into a list based on number of quotes
    total_items = int(temp_list[7])  # total number of items are in the 7th slot
    print("There are supposedly: " + str(total_items) + " items, ")
    item_per_page = 21  # this number is fixed
    page_count = (total_items // item_per_page) + 1    # number of pages is derived from total_item and items_per_page
    print("over " + str(page_count) + " number of pages.")

    # Error handling in case page does not load or
    # loads all existing courses and interests from all CCs
    if page_count > 10 or page_count < 2:
        main()  # restart program

    # relevant links are filtered into the filtered_links list
    class_links, interest_links, event_links = extract_relevant_links(page_count, driver)

    # data from individual pages are appended into the data list
    #
    # link_list = [class_links, interest_links, event_links]
    # jobs = []
    # for list in link_list:
    #     p = multiprocessing.Process(target=extract_individual_pages, args=(list,))
    #     jobs.append(p)
    #     p.start()

    class_data = extract_individual_pages(class_links)
    interest_data = extract_individual_pages(interest_links)
    event_data = extract_individual_pages(event_links)

    class_df = pd.DataFrame(class_data)  # save to pandas data frame
    interest_df = pd.DataFrame(interest_data)  # save to pandas data frame
    event_df = pd.DataFrame(event_data)  # save to pandas data frame

    # class_df.to_csv('Class.csv')  # write to csv for visual checking
    class_df.to_json('classes.json')  # write to json for database

    # interest_df.to_csv('InterestDetails.csv')  # write to csv for visual checking
    interest_df.to_json('interests.json')  # write to json for database

    # event_df.to_csv('EventDetails.csv')  # write to csv for visual checking
    event_df.to_json('events.json')  # write to json for database

    print('Course, Interest Group and Event data saved.')


    upload_data('classes')   # uploads data onto fire base realtime database
    upload_data('events')   # uploads data onto fire base realtime database
    upload_data('interests')   # uploads data onto fire base realtime database

    print("Upload Complete!")

    now = time.time()  # current time is saved as now.

    print("It took: ", now - then, " seconds")  # prints time taken in seconds.


main()
