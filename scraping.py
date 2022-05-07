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
    wagatomo_spans = wagatomo_div.find_all('span')
    date_span =0
    title_span = [span.text for span in wagatomo_spans if '今週のことば' in span.text or 'わが友' in span.text]
    date_span = [span.text for span in wagatomo_spans if 'ts_days' in span.get('class')]
    title = title_span[0] if len(title_span) > 0 else ''
    to_day = date_span[0] if len(date_span) > 0 else ''
    wagatomo_p = wagatomo_div.find_all('p')
    texts:list[str] = [p.text for p in wagatomo_p]
    parse_text = texts[0].replace(' ','').replace('\u3000','\r\n\u3000')
    parse_title = title.replace(' ','').replace('\r\n','')
    result_text = f'{parse_title}　{to_day}{parse_text}'
    return result_text

# 
def get_content_by_url(url:str):
    req = requests.get(url)
    soup = BeautifulSoup(req.content,'html.parser')
    return soup



