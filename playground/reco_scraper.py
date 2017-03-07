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
        self.companies = ['nytorget-6', 'sveabad', 'inred-se-stockholm', 'furniturebox', 'forma-traningscenter-kallhall']
        self.token = 'organisationen'
        
    def init_scrape_websites(self):
        for company in self.companies:
            self.company_name = company
            self.request = requests.get("https://www.reco.se/" + self.company_name)
            self.soup = bs4.BeautifulSoup(self.request.content, "html.parser")
            self.scrape_website(self.soup, self.company_name)
    
    def scrape_website(self, soup, company):
        list_of_ul = soup.find(id = "review-list")
        list_of_li = list_of_ul.find_all("li")
        company = company.replace("-", " ")
        for row_number in range(0, len(list_of_li)):
            review = { 'text': "", 'rating': 0}
            review_text = list_of_li[row_number].find("div", attrs = {'class': 'ln3'})
            review_points = list_of_li[row_number].find("div", attrs = {'class': 'reco-rating rs'})
            review_points = review_points.find_all("span")
            text = ""
            
            for sentence in review_text:
                if isinstance(sentence, bs4.element.NavigableString):
                    sentence_string = str(sentence.string.replace("\n", " ").strip() + " ")
                    text += sentence_string.lower()
            
            if text.find(company) > -1:
                print(company)
                text = text.replace(company, self.token)
                
            review['text'] = text
            review['rating'] = len(review_points)  
            self.listOfRatings.append(review)
            
    def get_list(self):
        return self.listOfRatings
        

"""req = requests.get("https://www.reco.se/nytorget-6")
    soup = bs4.BeautifulSoup(req.content, "html.parser")
    
    list_of_ul = soup.find(id = "review-list")
    list_of_li = list_of_ul.find_all("li")
    listOfRatings = []
    
    for row_number in range(0, len(list_of_li)):
    review = { 'text': "", 'rating': 0}
    review_text = list_of_li[row_number].find("div", attrs = {'class': 'ln3'})
    review_points = list_of_li[row_number].find("div", attrs = {'class': 'reco-rating rs'})
    review_points = review_points.find_all("span")
    text = ""
    for sentence in review_text:
        if isinstance(sentence, bs4.element.NavigableString):
            sentence_string = str(sentence.string.replace("\n", " ").strip() + " ")
            text += sentence_string
    
    review['text'] = text
    review['rating'] = len(review_points)  
    listOfRatings.append(review)"""


    
