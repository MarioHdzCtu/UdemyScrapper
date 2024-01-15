from cgitb import handler
from reprlib import recursive_repr
import time
import attr
import attrs
from bs4 import BeautifulSoup
import bs4
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import httpx
import logging
import sys

logger = logging.getLogger('UdemyCourseScrapper.log')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler('UdemyScrepper.log')
formatter = logging.Formatter(fmt='%(asctime)s - %(levelname)s - %(message)s',datefmt='%Y-%m-%d %H:%M:%S')
handler.setFormatter(formatter)
logger.addHandler(handler)

url = 'https://blog.facialix.com/cupones/'
r: httpx.Response = httpx.get(url)
if r.status_code != 200:
    logger.error(f'The page {url} was not accessible. Status code recieved {r.status_code}. Exiting code.')
    sys.exit()

try:
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--user-agent=Chrome/77')

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    driver.get(url)
    logger.info('Chrome driver setup correctlty')
except Exception as e:
    logger.error(f'Chrome driver setup failed. {e}. Exiting code')
    sys.exit()

soup = BeautifulSoup(driver.page_source, features='lxml')

article_grid = soup.findChild(attrs={'class':'sek-grid-items sek-grid-layout sek-thumb-custom-height sek-shadow-on-hover sek-desktop-col-3 sek-all-col-3 sek-tablet-col-2 sek-mobile-col-1'})

if not isinstance(article_grid, bs4.Tag):
    logger.error('Could not find the article grid element in the page source. Exiting code.')
    sys.exit()

articles = article_grid.findChildren(attrs={'class':'sek-has-thumb'})

if len(articles) <= 0:
    logger.warning('No articles were found. Exiting program')
    sys.exit()

logger.info(f'Found {len(articles)} {"articles" if len(articles) > 1 else "article"}')

class Article:

    def __init__(self,article: bs4.element.Tag):
        self.__valid_article = False
        self.__article: bs4.element.Tag = article
        self.__blog_anchor = self.__article.find('a')
        if self.__blog_anchor is not None:
            self.__blog_link = self.__blog_anchor.attrs.get('href')

    @property
    def valid_article(self):
        return self.__valid_article
    
    @valid_article.setter
    def valid_article(self, val: bool):
        self.__valid_article = val

    @property
    def article(self):
        return self.__article

    @property
    def blog_anchor(self):
        return self.__blog_anchor
    
    @property
    def blog_link(self):
        return self.__blog_link

class FacialixPost:
    
    def __init__(self) -> None:
        pass

article = Article(article=articles[1])

driver.get(article.blog_link)

soup = BeautifulSoup(driver.page_source,features='lxml')

hr = soup.find('hr', attrs={'class':'wp-block-separator has-css-opacity'})

udemy_link = hr.find_previous_sibling('p').find('a').attrs.get('href')

driver.get(udemy_link)
wait = WebDriverWait(driver,50).until(lambda driver: driver.title != 'Just a moment...')
print(driver.title+'\n')
button = WebDriverWait(driver,50).until(EC.element_to_be_clickable((By.XPATH,'/html/body/div[1]/div[2]/div/div/div[2]/div[3]/div[2]/div[2]/div/div/div/div/div[4]/div/button')))
#s#oup = BeautifulSoup(driver.page_source,features='lxml')
#button = driver.find_element(By.XPATH,'/html/body/div[1]/div[2]/div/div/div[2]/div[3]/div[2]/div[2]/div/div/div/div/div[4]/div/button')
print('Button: ',button)
#button.click()
print('clicked')
print(driver.current_url)
#print(soup.find('button',attrs={'class':'ud-btn ud-btn-medium ud-btn-primary ud-heading-sm styles--btn--express-checkout--3h0xG'}))

