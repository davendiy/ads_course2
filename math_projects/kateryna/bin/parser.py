#!/usr/bin/env python3
# -*-encoding: utf-8-*-

from urllib.request import urlopen
from urllib.error import HTTPError

import html.parser
import re

P_ENC = r'\bcharset=(?P<ENC>.+)\b'    # регулярний вираз кодування html сторінки


def getencoding(http_file):
    """ Отримати кодування файлу http_file з Інтернет.
    """
    headers = http_file.getheaders()  # отримати заголовки файлу
    dct = dict(headers)  # перетворити у словник
    content = dct.get('Content-Type', '')  # знайти 'Content-Type'
    mt = re.search(P_ENC, content)  # знайти кодування (після 'charset=' )

    if mt:
        enc = mt.group('ENC').lower().strip()  # виділити кодування
    elif 'html' in content:
        enc = 'utf-8'
    else:
        enc = None
    return enc


class Parser(html.parser.HTMLParser):
    """ Клас, що парсить сторінку html і шукає в посилання,
    пов'язані з ключовими словами.
    """

    def __init__(self, key_re: re.compile, *args, **kwargs):
        html.parser.HTMLParser.__init__(self, *args, **kwargs)
        self.res_links = {}     # посилання, які було знайдено
        self._key_re = key_re   # ключові слова (регулярний вираз)
        self._in_tag = False    # True, якщо парсер відкрив необхідний тег
        self._link = ''         # змінна, яка тимчасово зберігає посилання

    def handle_starttag(self, tag, attrs):
        """ Обробити початковий тег

        :param tag: назва (тип) тегу
        :param attrs: атрибути тегу
        """
        attrs = dict(attrs)

        # нам необхідні теги, які є посиланнями
        if tag in ['a', 'link', 'area']:
            self._in_tag = True
            self._link = attrs.get('href', '')

    def handle_data(self, data):
        """ Обробити дані всередині тегу

        :param data: рядок
        """
        if self._in_tag:        # якщо ми всередині необхідного тегу
            res = self._key_re.search(data)   # шукаємо ключові слова
            if res and self._link:            # якщо є посилання і знайдені ключові слова - додаємо
                # в текстах дуже багато пробілів і символів переведення рядку
                self.res_links[self._link] = data.strip()

    def handle_endtag(self, tag):
        """ Обробити кінцевий тег

        :param tag: назва (тип) тегу
        """
        if tag in ['a', 'link', 'area']:
            self._in_tag = False


if __name__ == '__main__':

    # тестування: намагаємось знайти новини за ключовими словами
    # url = 'https://gordonua.com/news/kiev.html'
    url = 'https://ukraina.ru/news/'
    # url_start = 'https://gordonua.com'

    url_start = 'https://ukraina.ru'

    page = urlopen(url)
    encoding = getencoding(page)
    try:
        parser = Parser(re.compile('президент|выборы|Зеленск|Порошенк'))
        converted_page = str(page.read(), encoding=encoding, errors='ignore')
        parser.feed(converted_page)
        for row, words in parser.res_links.items():
            # якщо посилання відносне, то додаємо глобальну адресу сайту
            if 'https' not in row and 'http' not in row:
                row = url_start + row
            print(row, words)
    except HTTPError as e:
        print(e)
