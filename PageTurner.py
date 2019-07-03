from bs4 import BeautifulSoup
from random import randint
from time import sleep
import requests
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
chrome_options = Options()
chrome_options.headless = True


def main():

    url_page = 'https://www.onepa.sg/cc/radin-mas-cc#tabs-2'   # specify the url
    print(url_page)     # print url page to visually signify start of program
    driver = webdriver.Chrome(chrome_options=chrome_options)    # run chrome web driver
    driver.get(url_page)    # get web page
    sleep(randint(20, 50))
    html = driver.page_source
    soup = BeautifulSoup(html)

    page_details = str(soup.find("div", attrs={"id": "content_0_pagination"}))
    quote_count = page_details.count("\"")
    temp_list = page_details.split("\"", quote_count + 1)
    total_item = int(temp_list[7])
    item_per_page = 21
    page_count = (total_item // item_per_page) + 1
    print(page_count)

    if page_count > 10 or page_count < 2:
        main()
    #
    # pager_next = driver.find_element_by_xpath("//*[@id='tabs-2']//*[contains(@class,'listingContainer clearfix')]"
    #                                           "//*[contains(@class='rightColContent loader dynamicPanelFluid')]"
    #                                           "//*[contains(@class='page_number')]//*[contains(@class='pager')]"
    #                                           "//*[contains(@class='pager-next')]")



    for i in range(2, page_count):
        try:
            pager_next = driver.find_element_by_xpath("//li[@class='pager-next']/span[1]")
            driver.execute_script("arguments[0].click();", pager_next)
            # pager_next.click()
        except Exception as e:
            print(e)
            break
        print(i)



    # for i in range(2, page_count + 1):
    #     try:
    #         if i == 2:
    #             print(i - 1)
    #             continue
    #         pager_page = driver.find_element_by_xpath("//*[@id='content_0_pagination']/ul/li[" + str(i) + "]/span")
    #         pager_page.click()
    #     except Exception as e:
    #         pass
    #     print(i - 1)


main()

# pages = soup.find_all("li", attrs={"class": "pager-page"})
# page_count = 0
# for page in pages:
#     page_count += 1
#     print(page_count)
#     print(page)
#

# pages = soup.select("select.data-pagination-total-item")
# for page in pages:
#     print(page)
# print([a.text for a in soup.select("a.search__results__list__item__entity")])
#
# for page in range(2, pages):
#     soup = BeautifulSoup(requests.get(url_page.format(page)).content)
#     print([a.text for a in soup.select("a.search__results__list__item__entity")])
