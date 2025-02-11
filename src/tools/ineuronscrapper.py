import requests
from bs4 import BeautifulSoup as bs
import json
from src.logger import logger


class scrapper:
    '''
    scrapes course data from the iNeuron website.
    Takes the website url as argument
    '''
    
    def __init__(self,url="https://ineuron.ai") -> None:
        
        logger.info('scrapper initiated')
        htmlpage = requests.get(url).text
        soup = bs(htmlpage , 'html.parser').find("script", {"id":"__NEXT_DATA__"})
        self._box = json.loads(soup.text)

    
    
    def course_categories(self) -> dict:
        """ returns the categories and subcategories of courses as key value pairs """

        logger.info('function called for listing course categories')
        cat = dict()
        for i in self._box['props']['pageProps']['initialState']['init']['categories'].values():
            cat[ i['title'] ] = i['subCategories'].values()
        return cat
    


    def AllCourses(self) -> dict:
        """ returns the details of all the courses from iNeuron """

        logger.info('function called for listing courses')
        Crs = self._box['props']['pageProps']['initialState']['init']['courses']
        return Crs