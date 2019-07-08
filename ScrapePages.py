import time
from bs4 import BeautifulSoup
from random import randint
from time import sleep
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from multiprocessing import pool
import pandas as pd

then = time.time()  # Time before the operations start
chrome_options = Options()
chrome_options.headless = True


# function extracts relevant links pertaining to course or membership pages
# over a couple of pages
def extract_relevant_links(page_count, driver):

    class_links = list()  # list is created to store class links
    interest_links = list()    # list is created to store interest links
    event_links = list()  # list is created to store event links
    for i in range(1, page_count + 1):  # loop for number of pages

        try:

            sleep(randint(20, 50))  # wait for page to load
            html = driver.page_source   # retrieve page source as html
            soup = BeautifulSoup(html)  # convert html to beautiful soup

            links = [a['href'] for a in soup.select('a[href]')]     # retrieve all links within soup

            for link in links:

                if "https://www.onepa.sg/class/details/" in link:
                    class_links.append(link)  # append link to class_list
                    print("Appending link:" + link)

                elif "https://www.onepa.sg/interest/details/" in link:
                    interest_links.append(link)  # append link to interest_list
                    print("Appending link:" + link)

                elif "https://www.onepa.sg/event/details/" in link:
                    event_links.append(link)    # append link to event_list
                    print("Appending link:" + link)

            print("Page " + str(i) + " filtered!")

            pager_next = driver.find_element_by_xpath("//li[@class='pager-next']")  # find next element
            pager_next.click()  # click on next element

        except Exception as e:
            # print(e)
            print("Complete! Continuing onto next stage.")
            break

    driver.quit()   # quit driver to change session

    return class_links, interest_links, event_links   # returns complete list of filtered links


def extract_individual_pages(filtered_links):

    data = list()   # list is created to store important data from each page

    for product_link in filtered_links:

        driver = webdriver.Chrome(chrome_options=chrome_options)  # run chrome web driver
        driver.get(product_link)  # redirect to link on web driver

        # filters only class links, as data collected is different
        if "https://www.onepa.sg/class/details/" in product_link:

            product_name = driver.find_element_by_xpath("//div[@class='pageTitle']").text
            price = driver.find_element_by_xpath("//*[@id='accordionEvtFeeDetails']/div[1]/div").text
            date_time = driver.find_element_by_xpath("//*[@id='content_0_pnlCourseUpperLayer']/div/div[4]/div[1]/div/div/div/div").text
            session_no = driver.find_element_by_xpath("//*[@id='content_0_pnlCourseUpperLayer']/div/div[4]/div[2]/div/div/div/div").text
            class_schedule = driver.find_element_by_xpath("//*[@id='content_0_pnlCourseUpperLayer']/div/div[4]/div[3]/div/div/div").text
            location = driver.find_element_by_xpath("//*[@id='content_0_pnlCourseUpperLayer']/div/div[4]/div[4]/div/div/div").text
            venue = driver.find_element_by_xpath("//*[@id='content_0_pnlCourseUpperLayer']/div/div[4]/div[5]/div/div").text
            closing_date = driver.find_element_by_xpath("//*[@id='content_0_pnlCourseUpperLayer']/div/div[4]/div[6]/div/div/div").text
            vacancy_left = driver.find_element_by_xpath("//*[@id='content_0_pnlCourseUpperLayer']/div/div[4]/div[7]/div/div/div").text
            max_participant= driver.find_element_by_xpath("//*[@id='content_0_pnlCourseUpperLayer']/div/div[4]/div[8]/div/div/div").text

            data.append({"product_name": product_name, "product_link": product_link,
                         "price": price, "date_time": date_time,
                         "session_no": session_no, "class_schedule": class_schedule,
                         "location": location, "venue": venue,
                         "closing_date": closing_date, "vacancy_left": vacancy_left,
                         "max_participant": max_participant})

        # filters only interest group links, as data collected is different
        elif "https://www.onepa.sg/interest/details/"in product_link:

            product_name = driver.find_element_by_xpath("//div[@class='pageTitle']").text
            location = driver.find_element_by_xpath("//*[@id='content_0_pnlIG']/div/div[4]/div[1]/div/div/div").text
            membership_period = driver.find_element_by_xpath("//*[@id='content_0_pnlIG']/div/div[4]/div[2]/div/div/div/div").text
            vacancy = driver.find_element_by_xpath("//*[@id='content_0_pnlIG']/div/div[4]/div[3]/div/div/div").text

            # append dict to array
            data.append({"product_name": product_name, "product_link": product_link,
                         "location": location, "membership_period": membership_period, "vacancy": vacancy})

        elif "https://www.onepa.sg/event/details/" in product_link:

            product_name = driver.find_element_by_xpath("//div[@class='pageTitle']").text
            date_time = driver.find_element_by_xpath("//*[@id='content_0_pnlEventUpperLayer']/div/div[4]/div[1]/div/div/div/div").text
            location = driver.find_element_by_xpath("//*[@id='content_0_pnlEventUpperLayer']/div/div[4]/div[2]/div/div/div").text
            event_schedule = driver.find_element_by_xpath("//*[@id='content_0_pnlEventUpperLayer']/div/div[4]/div[3]/div/div/div/div").text
            venue = driver.find_element_by_xpath("//*[@id='content_0_pnlEventUpperLayer']/div/div[4]/div[4]/div/div/div").text
            closing_date = driver.find_element_by_xpath("//*[@id='content_0_pnlEventUpperLayer']/div/div[4]/div[5]/div/div/div").text
            vacancy_left = driver.find_element_by_xpath("//*[@id='content_0_pnlEventUpperLayer']/div/div[4]/div[6]/div/div/div").text
            max_participant = driver.find_element_by_xpath("//*[@id='content_0_pnlEventUpperLayer']/div/div[4]/div[7]/div/div/div").text

            # append dict to array
            data.append({"product_name": product_name, "product_link": product_link,
                         "date_time": date_time, "location": location,
                         "event_schedule": event_schedule, "venue": venue,
                         "closing_date": closing_date, "vacancy_left": vacancy_left,
                         "max_participant": max_participant})

        driver.quit()   # close driver
        print("Extraction complete for: " + product_link)

    return data


