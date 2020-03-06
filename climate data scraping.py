# -*- coding: utf-8 -*-
"""
Created on Fri Feb 28 09:22:18 2020

@author: PBu
"""

import requests
from bs4 import BeautifulSoup as soup
import pandas as pd
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
    
def getDaily(aCity):
    """
    input: a string that represents one city's link
    output: a dataframe with daily weather data for the city
    """
    cityInfo = aCity.split('/')
    City = cityInfo[2]
    State = cityInfo[3]
    location = cityInfo[-1]
    allMonth = pd.DataFrame()
    for month in range(12):
        payload = {'token': '73dc72210f0761d5e8f5b169dd41a1d5flCB8chO7YAJwiL0feLL9XNm8C7MHw170EI+MrRQBdVTF1D0hA==',
                   'location':location, 'unit': 'american', 'page': 'climate', 'month': month+1, 'tab': '#daily', 'action':'month_selection',
                   'summary': 0, 'unit_required': 0}
        aMonth = requests.post('https://usclimatedata.com/ajax/load-daily-content', data=payload)
        month_soup = soup(aMonth.content)
        month_pd = pd.read_html(str(month_soup.find('table')))[0]
        month_pd.columns = ['DATE', 'HIGH', 'LOW', 'PREC_MON', 'PREC_YR', 'SNOW_MON', 'SNOW_YR']
        month_pd['CITY'] = City
        month_pd['STATE'] = State
        allMonth = allMonth.append(month_pd)
    return allMonth

States = getState()
cities = []
for each in States:
    cities.extend(getCity(each))
    
try:
    oneCity = getDaily(cities[7])
except:
    pass

