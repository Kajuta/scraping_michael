from bs4 import BeautifulSoup

import requests

import util

# URLS
cnsSEIKYO_URL = {
    'wagatomo':'https://www.seikyoonline.com/news/wagatomo/'
}


def wagatomo_scrape():
    content = get_content_by_url(url=cnsSEIKYO_URL['wagatomo'])
    left_cont = content.find(id='left_main')
    atags = left_cont.find_all('a')

    # get wagatomo
    wagatomo_url_list = [atag.get('href') for atag in atags if 'article' in atag.get('href')]
    wagatomo_cont = get_content_by_url(url=f'https:{wagatomo_url_list[0]}')
    wagatomo_div = wagatomo_cont.find(class_='phase2_outer clearfix')
    date_span = wagatomo_div.find(class_='ts_days')
    wagatomo_p = wagatomo_div.find_all('p')
    texts:list[str] = [p.text for p in wagatomo_p]
    parse_text = texts[0].replace(' ','').replace('\u3000','\r\n\u3000')
    result_text = f'わが友に贈る　{date_span.text}{parse_text}'
    return result_text

# 
def get_content_by_url(url:str):
    req = requests.get(url)
    soup = BeautifulSoup(req.content,'html.parser')
    return soup



