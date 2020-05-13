from urllib.parse import quote
from datetime import datetime
import locale
import requests
from bs4 import BeautifulSoup
import string
 
 
def parse_page( req, page ):
    # https://www.avito.ru/moskva?q=mercedes&p=2
    req = "https://www.avito.ru/moskva?q=" + req + "&p=" + str( page )
    response = requests.get( req )
    if response.url == 'https://www.avito.ru/blocked':
        exit( "blocked user, try again later" )
    return requests.get( req ).text
 
def get_ads( page ):
    return _soup(page).find_all('div', attrs={'class': 'item_table-wrapper'})
 
def _soup( html ):
    return BeautifulSoup( html, 'lxml' )
 
def curr_ad( ad ):
    return {
        'title': get_title( ad ),
        'link': get_link( ad ),
        'price': get_price( ad ),
        'address' : get_address( ad ),
        'geo reference' : get_georef( ad )
    }
 
def get_title(ad):
    return ad.find('a', attrs={'class': 'snippet-link'})['title']
 
def get_link(ad):
    base_url = 'https://www.avito.ru'
    return base_url + ad.find('a', attrs={'class': 'snippet-link'})['href']
 
def get_price(ad):
    price = ad.find('span', attrs={'class': 'snippet-price'}).text
    # print( price )
    return price if price else "empty"
 
def get_address( ad ):
    try:
        addr = ad.find('span', attrs={'class': 'item-address-georeferences-item__content'}).text
    except:
        return "empty"
    return addr
 
def get_georef( ad ):
    try:
        geo = ad.find('span', attrs={'class': 'item-address-georeferences-item__after'}).text
    except:
        return "empty"
    return geo
 
 
   
def run():
 
    page = parse_page( "mercedes", 4 )
   
    ads = get_ads( page )
 
    f = open("result.txt", "w")
   
    for ad in ads:
        #print( curr_ad( ad ) )
        f.write( str( curr_ad( ad ) ) )
    f.close()
   
 
run()