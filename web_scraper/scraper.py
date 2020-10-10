import re
from requests import get
from bs4 import BeautifulSoup

import pandas as pd

url_apartments = 'https://tonaton.com/en/ads/ghana/apartments?sort=date&order=desc&buy_now=0&urgent=0&page='
url_house = 'https://tonaton.com/en/ads/ghana/houses?sort=date&order=desc&buy_now=0&urgent=0&page='
url_rooms = 'https://tonaton.com/en/ads/ghana/rooms?sort=date&order=desc&buy_now=0&urgent=0&page='
url_strent = 'https://tonaton.com/en/ads/ghana/short-term-rentals?sort=date&order=desc&buy_now=0&urgent=0&page='

num_apartment = 233
num_house = 182
num_rooms = 5
num_strent = 2

URL_OBJ = {
    "url": [url_apartments, url_house, url_rooms, url_strent],
    "pages": [num_apartment, num_house, num_rooms, num_strent]
}

com = None

for url, pages in zip(URL_OBJ["url"], URL_OBJ['pages']):
    main_ = []
    stringer = []
    for i in range(pages):
        response = get(url+str(i))
        html = BeautifulSoup(response.content, 'html.parser')
        for link in html.find_all('a', {'class': 'gtm-ad-item'}):
            for child in link.children:
                for strings_ in child.strings:
                    stringer.append(strings_)
            main_.append(stringer)
            stringer = []

    com = re.search('[^\/][\w]+(?=\?)', url)
    name = com.group() + '_001.csv'
    df = pd.DataFrame(main_)
    df.to_csv('./data/' + name, index=False)
