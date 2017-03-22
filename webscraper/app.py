# -*- coding: utf-8 -*-
"""
Created on Tue Mar  7 15:44:48 2017

@author: Stoffe
"""
import csv
import random
from reco_scraper import RecoWebScraper
from trustpilot_scraper import TrustPilotScraper

reco = RecoWebScraper()
reco.init_scrape_websites()
list_one = reco.get_list()

trustpilot = TrustPilotScraper()
trustpilot.init_scrape_websites()
list_two = trustpilot.get_list()

complete_list = list_one + list_two
posArr = []
neuArr = []
negArr = []

pos = 0
neu = 0
neg = 0

for num in range(0, len(complete_list)):
    if complete_list[num]['points'] < 3:
        negArr.append(complete_list[num])
        neg += 1
    elif complete_list[num]['points'] > 3:
        posArr.append(complete_list[num])
        pos += 1
    else:
        neuArr.append(complete_list[num])
        neu += 1

""" Shuffled list for the first dataset """    
shuffled_list = list(complete_list)
random.shuffle(shuffled_list)

""" Shuffled list for the dataset with the same amount of positive and negative """
halv_posArr = []
halv_posArr_shuffled = list(posArr)
random.shuffle(halv_posArr_shuffled)
for x in range(0, int(len(halv_posArr_shuffled) / 2)):
    halv_posArr.append(halv_posArr_shuffled[x])
shuffled_list_same_amount = halv_posArr + negArr + neuArr
random.shuffle(shuffled_list_same_amount)

""" Shuffled list without neutral reviews """
shuffled_list_without_neu = posArr + negArr
random.shuffle(shuffled_list_without_neu)


f = open('datasetWithoutNeutral', 'w', encoding='utf-8')
try:
    writer = csv.writer(f)
    writer.writerow(('index', 'text', 'rating'))
    
    for i in range(0, len(shuffled_list_without_neu)):
        writer.writerow((i+1, shuffled_list_without_neu[i]['text'], shuffled_list_without_neu[i]['rating']))
finally:
    f.close()
    
print(open('datasetFullList', 'r', encoding='utf-8').read())