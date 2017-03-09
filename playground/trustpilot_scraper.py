# -*- coding: utf-8 -*-
"""
Created on Thu Mar  9 10:53:29 2017

@author: Kristoffer
"""

import requests
import bs4
import langdetect

class TrustPilotScraper(object):
    
    def __init__(self):
        self.listOfRatings = []
        self.companies = ['ginatricot.se', 'www.vivamondo.se', 'members.com', 'www.rejta.se',
                          'www.blocket.se', 'www.nemid.nu', 'middagsfrid.se', 'www.ginza.se',
                          'software24.se', 'www.eciggshop.se', 'e-bloss.se', 'www.bahnhof.se',
                          'www.smartphoto.se', 'www.euroflorist.se', 'intima.se', '24.se',
                          'www.mytrendyphone.se', 'www.batterikungen.se', 'www.netonnet.se', 
                          'www.abcleksaker.se', 'www.br-leksaker.se', 'www.barnvagnslagret.se',
                          'www.cdon.se', 'www.cykelkraft.se', 'www.resfeber.se', 'www.travelstart.se',
                          'ctiparty.se', 'klarna.com/sv', 'www.komplett.se']
        self.token = 'organisationen'
        self.amount_pages = 3
        
    def init_scrape_websites(self):
        for company in self.companies:
            self.company_name = company
            for pages in range(0, self.amount_pages):
                print("Extracting data from: {1} on page {0}".format(pages + 1, self.company_name))
                if (pages + 1) == 1:
                    self.request = requests.get("https://se.trustpilot.com/review/" + self.company_name)
                else:
                    self.request = requests.get("https://se.trustpilot.com/review/" + self.company_name + "?page=" + str(pages + 1))
                self.soup = bs4.BeautifulSoup(self.request.content, "html.parser")
                self.scrape_website(self.soup, self.company_name)
    
    def scrape_website(self, soup, company):
        list_of_review_containers = soup.find(id = "reviews-container")
        list_of_reviews = list_of_review_containers.find_all("div", attrs = {'class': 'review-stack'})
        company = company.replace("-", " ")
        
        for row_number in range(0, len(list_of_reviews)):
            review = { 'text': "", 'rating': "", 'points': 0}
            review_text = list_of_reviews[row_number].find("div", attrs = {'class': 'review-body'})
            review_points = list_of_reviews[row_number].find("div", attrs = {'class': 'star-rating'})
            text = ""
            
            for sentence in review_text: 
                if isinstance(sentence, bs4.element.NavigableString):
                    try:
                        if langdetect.detect(sentence.string) == 'sv':
                            sentence_string = str(sentence.string.replace("\n", " ").strip() + " ")
                            text += sentence_string.lower()
                    except langdetect.lang_detect_exception.LangDetectException as e:
                        print(e)
            
            if text.find(company) > -1:
                text = text.replace(company, self.token)
            
            if text != "":
                review['text'] = text
                """review['rating'] = int(review_points.attrs['class'][1][-1])"""
                if int(review_points.attrs['class'][1][-1]) < 3:
                    review['rating'] = 'negative'
                elif int(review_points.attrs['class'][1][-1]) > 3:
                    review['rating'] = 'positive'
                else:
                    review['rating'] = 'neutral'
                review['points'] = int(review_points.attrs['class'][1][-1])
                self.listOfRatings.append(review)
            
    def get_list(self):
        return self.listOfRatings