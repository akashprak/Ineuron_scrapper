from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException

from bs4 import BeautifulSoup as bs

from src.logger import logger


class curriculumScrapper:

    _options = Options()
    _options.add_argument('--headless=new')

    def __init__(self,course) -> None:
        self.course = course


    def _get_Html(self):
        """gets the HTML containing curriculum data from the website"""
        
        with Chrome(options=self._options) as driver:
            logger.info('Chromedriver started web scraping')

            driver.get(f"https://ineuron.ai/course/{self.course}")
            box = WebDriverWait(driver, 10).until(lambda x: x.find_element(
                By.CSS_SELECTOR,
                "div.CurriculumAndProjects_course-curriculum__C9K5U.CurriculumAndProjects_card__rF6YN.card"))

            try:
                driver.find_element(By.CSS_SELECTOR, "i.fas.fa-times").click()
                logger.info('popup closed')
            except NoSuchElementException:
                pass

            try:
                driver.find_element(By.CSS_SELECTOR, "span.CurriculumAndProjects_view-more-btn__iZ72A").click()
                logger.info('clicked to fully expand curriculum list')
            
            except NoSuchElementException:
                logger.exception("element doesn't exist inside HTML")

            finally:
                htmlBox = box.get_attribute('innerHTML')
                logger.info('required HTML extracted from the website')
                
        return htmlBox

    def scrape(self):
        """scrapes the curriculum data from the HTML"""

        soup = bs(self._get_Html(), 'html.parser')
        soup = soup.find_all("div", {"class":"CurriculumAndProjects_curriculum-accordion__fI8wj CurriculumAndProjects_card__rF6YN card"})
        curriculumData = dict()

        if soup:
            for head in soup:
                key = head.find("span").get_text()
                values = head.find_all(name="div", class_="CurriculumAndProjects_course-curriculum-list__OBOTg")
                curriculumData[key] = [k.find(string=True, recursive=False) for k in values]
            logger.info('data successfully extracted')
        
        else:
            logger.error('soup.findall() returned None')

        return curriculumData