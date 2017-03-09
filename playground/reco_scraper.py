# -*- coding: utf-8 -*-

"""
Spyder Editor

This is a temporary script file.
"""

import requests
import bs4

class RecoWebScraper(object):
    
    def __init__(self):
        self.listOfRatings = []
        self.companies = ['nytorget-6', 'sveabad', 'inred-se-stockholm', 'furniturebox', 'forma-traningscenter-kallhall',
                          'kung-carls-bakficka', 'restaurang-rakan-stockholm']
        self.token = 'organisationen'
        
    def init_scrape_websites(self):
        for company in self.companies:
            self.company_name = company
            print("Extracting data from: {0}".format(self.company_name))
            self.request = requests.get("https://www.reco.se/" + self.company_name)
            self.soup = bs4.BeautifulSoup(self.request.content, "html.parser")
            self.scrape_website(self.soup, self.company_name)
    
    def scrape_website(self, soup, company):
        list_of_ul = soup.find(id = "review-list")
        list_of_li = list_of_ul.find_all("li")
        company = company.replace("-", " ")
        for row_number in range(0, len(list_of_li)):
            review = { 'text': "", 'rating': "", 'points': 0}
            review_text = list_of_li[row_number].find("div", attrs = {'class': 'ln3'})
            review_points = list_of_li[row_number].find("div", attrs = {'class': 'reco-rating rs'})
            review_points = review_points.find_all("span")
            text = ""
            
            for sentence in review_text:
                if isinstance(sentence, bs4.element.NavigableString):
                    sentence_string = str(sentence.string.replace("\n", " ").strip() + " ")
                    text += sentence_string.lower()
            
            if text.find(company) > -1:
                text = text.replace(company, self.token)
                
            review['text'] = text
            if len(review_points) < 3:
                review['rating'] = 'negative'
            elif len(review_points) > 3:
                review['rating'] = 'positive'
            else:
                review['rating'] = 'neutral'      
            review['points'] = len(review_points)
            self.listOfRatings.append(review)
            
    def get_list(self):
        return self.listOfRatings   
