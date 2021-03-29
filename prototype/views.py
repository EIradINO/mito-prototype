from janome.tokenizer import Tokenizer
from janome.analyzer import Analyzer
from janome.charfilter import *
from janome.tokenfilter import *
from django.http import HttpResponse
from django.template import loader
import requests
from bs4 import BeautifulSoup
import time
from selenium import webdriver
import chromedriver_binary
from collections import defaultdict


def index(request):
    template = loader.get_template('prototype/index.html')
    return HttpResponse(template.render())


def analysis(request):
    word_list = []
    text = "なんで空は青いの？"
    char_filters = [UnicodeNormalizeCharFilter()]
    tokenizer = Tokenizer()
    token_filters = [POSKeepFilter(['名詞', '形容詞'])]
    analyzer = Analyzer(char_filters=char_filters,
                        tokenizer=tokenizer, token_filters=token_filters)
    for token in analyzer.analyze(text):
        word_list.append(token.surface)
    template = loader.get_template('prototype/analysis.html')
    context = {
        'word_list': word_list,
    }
    return HttpResponse(template.render(context, request))


def scraping(request):

    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    link_list = {}
    # link_list = defaultdict(list)
    # sample_list = defaultdict(list)
    sample_list = {
        'a': ['ai', 'au', 'ae', 'ao'],
        'i': ['ii', 'iu', 'ie', 'io'],
        'u': ['ui', 'uu', 'ue', 'uo'],
        'e': ['ei', 'eu', 'ee', 'eo'],
    }

    for i in range(1):
        url = 'https://www.nhk.or.jp/school/keyword/?kyoka=rika&grade=g5&cat=all&from={}&sort=ranking'.format(
            i*20+1)
        driver.get(url)
        html = driver.page_source.encode('utf-8')
        soup = BeautifulSoup(html, "html.parser")

        for link in soup.select('div.itemKyouka > a'):
            mov_url = 'https:' + link.get('href')
            driver.get(mov_url)
            mov_html = driver.page_source.encode('utf-8')
            mov_soup = BeautifulSoup(mov_html, "html.parser")

            og_title = mov_soup.find(
                'meta', attrs={'property': 'og:title', 'content': True})
            og_description = mov_soup.find(
                'meta', attrs={'property': 'og:description', 'content': True})
            og_image = mov_soup.find(
                'meta', attrs={'property': 'og:image', 'content': True})

            link_list[mov_url] += [og_title['content'],
                                   og_description['content'], og_image['content']]

            time.sleep(1)
        time.sleep(1)

    template = loader.get_template('prototype/scraping.html')
    context = {
        'link_list': link_list,
    }
    return HttpResponse(template.render(context, request))
