#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import csv


def get_html(url):
    r = requests.get(url)
    return r.text


def get_total_pages(html):
    soup = BeautifulSoup(html, 'html.parser')
    divs = soup.find('div', class_='pagination-pages clearfix')
    pages = divs.find_all('a', class_='pagination-page')[-1].get('href')
    total_pages = pages.split('=')[1].split('&')[0]
    return int(total_pages)


def write_csv(data):
    with open('avito.csv', 'a', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow((data['title'], data['price'], data['url']))


def get_page_data(html):
    soup = BeautifulSoup(html, 'html.parser')
    divs = soup.find('div', class_='catalog-list')
    ads = divs.find_all('div', class_='item')
    #print((len(ads)))
    #print(ads[0])
    for ad in ads:
        try:
            #title = ad.find('div', class_='description').find('h3').text.strip()
            div = ad.find('div', class_='description').find('h3')
            if 'locust' not in div.text.lower():
                continue
            else:
                title = div.text.strip()
        except:
            title = ''
        try:
            div = ad.find('div', class_='about')
            array = ['Договорная', 'Цена не указана']
            for i in array:
               if i in div.text.lower():
                  continue
                print(div.text.strip())
            # if 'договорная' in div.text.lower():
            #     continue
            # if 'цена' in div.text.lower():
            #     continue
            else:
                  price = div.text.strip()
        except:
            price = '======================='
        try:
            #url = 'https://www.avito.ru' + ad.find('div', class_='description').find('h3').find('a').get('href')
            div = ad.find('div', class_='description').find('h3')
            url = "https://avito.ru" + div.find('a').get('href')
        except:
            url = ''

        #try:
        #    div = ad.find('div', class_='data')
         #   metro = div.find_all('p')[-1].text.strip()
        #except:
         #   metro = ''
        data = {'title':title, 'price':price, 'url':url}
        write_csv(data)


def main():
    url = 'https://www.avito.ru/rossiya?p=1&view=gallery&q=%D0%BC%D0%B8%D0%BD%D0%B8%D0%BF%D0%BE%D0%B3%D1%80%D1%83%D0%B7%D1%87%D0%B8%D0%BA+locust'
    base_url = 'https://www.avito.ru/rossiya?'
    page_part = 'p='
    query_part = '&q=%D0%BC%D0%B8%D0%BD%D0%B8%D0%BF%D0%BE%D0%B3%D1%80%D1%83%D0%B7%D1%87%D0%B8%D0%BA+locust'
    #print(url)
    #total_pages = get_total_pages(get_html(url))

    for i in range(1, 3):
        url_gen = base_url + page_part + str(i) + query_part
        html = get_html(url_gen)
        get_page_data(html)
        #print(html)


if __name__ == '__main__':
    main()