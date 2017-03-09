# -*- coding: utf-8 -*-
"""
Created on Tue Mar  7 15:44:48 2017

@author: Stoffe
"""
import csv
from reco_scraper import RecoWebScraper
from trustpilot_scraper import TrustPilotScraper


reco = RecoWebScraper()
reco.init_scrape_websites()
list_one = reco.get_list()

trustpilot = TrustPilotScraper()
trustpilot.init_scrape_websites()
list_two = trustpilot.get_list()

complete_list = list_one + list_two

f = open('dataset', 'w', encoding='utf-8')
try:
    writer = csv.writer(f)
    writer.writerow(('index', 'text', 'rating'))
    
    for i in range(0, len(list)):
        writer.writerow((i+1, list[i]['text'], list[i]['rating']))
finally:
    f.close()
    
print(open('dataset', 'r', encoding='utf-8').read())