from random import randint
from time import sleep
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
chrome_options = Options()
chrome_options.headless = True
from bs4 import BeautifulSoup

url_page = 'https://www.onepa.sg/cc/radin-mas-cc#tabs-2'   # specify the url
print(url_page)     # print url page to visually signify start of program
driver = webdriver.Chrome(chrome_options=chrome_options)    # run chrome web driver
driver.get(url_page)    # get web page
sleep(randint(10,50))
html = driver.page_source
soup = BeautifulSoup(html)
print("Finding...")

links = [a['href'] for a in soup.select('a[href]')]
filtered_link = list()
for link in links:
    if "https://www.onepa.sg/class/details/" in link:
        filtered_link.extend(link)
        print(link)
