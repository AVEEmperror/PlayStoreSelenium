import selenium
from selenium import webdriver
import sys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
import time


PATH = r'Z:\Code\vscode\GooglePlaySeleniumScrap\driver\chromedriver.exe'  # without "r" driver can't find the .exe file, idk why.

driver = webdriver.Chrome(PATH)


# gets collections urls from the file specified in the sys.argv[1]
def get_coll_urls() -> list:

    file = r'GooglePlaySeleniumScrap\urls_collections.txt'
    
    with open(file, 'r') as f:
        urls = [url.strip('\n') for url in f.readlines()]
        print(urls)
        return urls


class SpiderUrl:
    """
    Crawls the google play collection('Top Free', 'Top Paid', 'Recoommended', etc; basically any play.google.com/store/apps/collection/...) and
    gets all the infromation about the apps in it.
    """


    def __init__(self, 
                coll_url: str,
                ):

        self.coll_url = coll_url
        self.driver = driver
        self.driver.get(self.coll_url)
 

    # Scrolls down until reaches the bottom of the page
    def scroll_down_inf(self):
        last_h = self.driver.execute_script('return document.body.scrollHeight')
        
        ELAPSED_LIMIT = 4  # set artificially for your internet speed
        time_start = time.perf_counter()
        while 1:
            time_now = time.perf_counter()
            elapsed = time_now - time_start
            if elapsed > ELAPSED_LIMIT:  #  if while cycle has been going for more than ELAPSED_LIMIT seconds, the end of the page is considered to be reached
                print('End of the page reached')
                break
            
            # tries to scroll down every 0.3 seconds and checks if scrolling happened
            self.driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
            time.sleep(0.3)
            new_h = self.driver.execute_script('return document.body.scrollHeight')
            if new_h > last_h:
                start = time.perf_counter()
                last_h = new_h


    # returns collection name and a list with all the urls of the apps in the collection.
    def crawl_links(self):
        elem_app_urls = self.driver.find_elements(By.CLASS_NAME, value='JC71ub')

        app_urls = [element.get_attribute('outerHTML') for element in elem_app_urls]  # full elements
        app_urls = [url[url.find('href="') + len('href="'):url.find('" ')] for url in app_urls]  # only the links (/store/app/details?id=template)
        app_urls = ['https://play.google.com' + url for url in app_urls]  # complete links to apps

        #elem_coll_name = self.driver.find_element(By.CLASS_NAME, value='sv0AUd bs3Xnd')
        elem_coll_name = self.driver.find_element(By.XPATH, '/html/body/div[1]/div[4]/c-wiz/div/c-wiz/div/c-wiz/c-wiz/c-wiz/div/div[1]/div/h2')
        coll_name = elem_coll_name.get_attribute('innerHTML')

        return(coll_name, app_urls)

    
    # closes the browser
    def quit(self):
        self.driver.quit()

    
    # opens a new tab, closes the previous one
    def open_new_tab(self):
        self.driver.execute_script("window.open('');")
        self.driver.close()

    
class SpiderApp:

    def __init__(self,
                 links: list
                 ) -> None:
                 
        self.links = links
        self.driver = driver


    def crawl_app(self, link: str):
        """
        Returns a DICT with a data of one application.
        """

        elem_search_keys = {
            'name': '//*[@itemprop = "name"]',
            'genre': '//*[@itemprop = "genre"]',
            'downloads': '//*[@class = "htlgb"]',
            'rating': '//*[@id="fcxH9b"]/div[4]/c-wiz/div/div[2]/div/div/main/div/div[1]/c-wiz/div[1]/div[1]',
            'reviews': '//*[@class = "AYi5wd TBRnV"]',
            'developer': '//*[@class = "T32cc UAO9ie"]'
            }

        self.driver.get(link)

        elements = {}

        # GET THE WEBELEMENTS
        for key in elem_search_keys:

            if key == 'downloads' or key == 'developer':  # for dow-s and dev you need find_elementS.
                pass

            else:
                try:
                    elements[key] = self.driver.find_element(By.XPATH, elem_search_keys[key])
                except NoSuchElementException:
                    print('NO_SUCH_ELEMENT_EXCEPTION: ', key)

        try:
            elements['downloads'] = driver.find_elements(By.XPATH, elem_search_keys['downloads'])[5]
        except NoSuchElementException:    
            print('NO_SUCH_ELEMENT_EXCEPTION: ', 'downloads')

        try:
            elements['developer'] = driver.find_elements(By.XPATH, elem_search_keys['developer'])[0]
        except NoSuchElementException:    
            print('NO_SUCH_ELEMENT_EXCEPTION: ', 'developer')

        #elements['name'] = self.driver.find_element(By.XPATH, elem_search_keys['name'])
        #elements['genre'] = self.driver.find_element(By.XPATH, elem_search_keys['genre'])
        #elements['reviews'] = self.driver.find_element(By.XPATH, elem_search_keys['reviews'])
        #elements['developer'] = driver.find_element(By.CSS_SELECTOR, elem_search_keys['developer'])

        data = {key: val.get_attribute('innerHTML') for key, val in elements.items()}

        return data

                
    def crawl_apps(self):
        """
        Returns a LIST of DICTS, where very DICT contains data about ONE application.
        """


        links = self.links
        data = []

        for link in links:

            # PRINT BLOCK
            cutoff = 'https://play.google.com/store/apps/details?id='
            name = link[link.find(''):]
            print('APP_SPIDER: Crawling', link[len(cutoff):])

            # BACKEND BLOCK
            try:
                data.append(self.crawl_app(link))
            except TimeoutException:
                print(F'TIMEOUTEXCEPTION: {name}')
        
        return data


    def quit(self):
        self.driver.quit()


if __name__ == '__main__':
    pass