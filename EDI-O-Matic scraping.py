# -*- coding: utf-8 -*-
"""
Created on Fri Feb 28 09:22:18 2020

@author: PBu
"""

import requests
from bs4 import BeautifulSoup as soup
#import lxml.html as lh
#print(edi_soup.prettify())

def getState():
    """
    output: a list of strings with each State's link
    """
    r = requests.get('https://usclimatedata.com/climate/united-states/us')
    home_soup = soup(r.content)
    state_all = home_soup.find_all('a', {'class':'stretched-link'})
    state_link = []
    for each in state_all:
        state_link.append(each['href'])
    return state_link
    
def getCity(stateLink):
    """
    input: string link for one state
    output: a list of strings with each city's string link
    """
    url = 'https://usclimatedata.com' + stateLink
    r = requests.get(url)
    state_soup = soup(r.content)
    city_all = state_soup.find_all('a', {'class':'stretched-link'})
    city_link = []
    for each in city_all:
        city_link.append(each['href'])
    return city_link
    
def getDaily(cityLink):
    url = 'https://usclimatedata.com' + cityLink
    r = requests.get(url)
    daily_soup = soup(r.content)
#    daily_table = daily_soup.find_all('div', {'class':'daily_table_div'})
    
    return daily_soup

States = getState()
cities = []
for each in States:
    cities.extend(getCity(each))
    
daily = getDaily(cities[0])

print()


table = daily.find('div', {'class':'daily_table_div'})
table_2= table.tbody.find_all('tr')
dates = table_2.find_all('th')



payload = {'token': '6a0aca0ab33bcc798ddf9dafd2e95482qrbJRGKDUE/LavF+TRxgQ4vL3y2CdGUk5m+X5S849k4episMkQ==', 
           'page': 'climate', 'location':'usa10019', 'month': 3, 'tab': '#daily', 'action':'month_selection',
           'summary': 0, 'unit': 'american', 'unit_required': 0}
test = requests.post('https://usclimatedata.com/ajax/load-daily-content', data=payload )
















