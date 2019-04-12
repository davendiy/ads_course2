#!/usr/bin/env python3
# -*-encoding: utf-8-*-

from urllib.request import urlopen
from urllib.error import HTTPError
from urllib.parse import urljoin

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

    def __init__(self, url, key_re: re.compile, *args, **kwargs):
        """ Конструктор

        :param url: адреса сайту для нормального виводу відносних посилань
        :param key_re: регулярний вираз для пошуку
        :param args: додаткові параметри для html.parser.HTMLParser
        :param kwargs: додаткові параметри для html.parser.HTMLParser
        """
        html.parser.HTMLParser.__init__(self, *args, **kwargs)
        self.res_links = {}     # посилання, які було знайдено
        self._url = url
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
                self.res_links[urljoin(self._url, self._link)] = data.strip()

    def handle_endtag(self, tag):
        """ Обробити кінцевий тег

        :param tag: назва (тип) тегу
        """
        if tag in ['a', 'link', 'area']:
            self._in_tag = False


def parse_page(url, key_re):
    """ Функція-обгортка, яка повністю парсить сторінку.

    :param url: адреса сторінки
    :param key_re: скомпільований регулярний вираз
    :return: словник {url: text}
    """
    try:
        page = urlopen(url)
        encoding = getencoding(page)
        parser = Parser(url, key_re)
        converted_page = str(page.read(), encoding=encoding, errors='ignore')
        parser.feed(converted_page)
        return parser.res_links
    except HTTPError:
        return {}


if __name__ == '__main__':

    # тестування: намагаємось знайти новини за ключовими словами
    test_url = 'https://gordonua.com/'

    result = parse_page(test_url, re.compile('Порошенк'))
    for http, text in result.items():
        print(http, text, sep=': ')
