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


def index(request):
    template = loader.get_template('prototype/index.html')
    return HttpResponse(template.render())


def analysis(request):
    wordlist = []
    text = "なんで空は青いの？"
    char_filters = [UnicodeNormalizeCharFilter()]
    tokenizer = Tokenizer()
    token_filters = [POSKeepFilter(['名詞', '形容詞'])]
    analyzer = Analyzer(char_filters=char_filters,
                        tokenizer=tokenizer, token_filters=token_filters)
    for token in analyzer.analyze(text):
        wordlist.append(token.surface)
    template = loader.get_template('prototype/analysis.html')
    context = {
        'wordlist': wordlist,
    }
    return HttpResponse(template.render(context, request))


def scraping(request):

    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)

    link_list = []
    link_title_list = []

    for i in range(1):
        url = 'https://www.nhk.or.jp/school/keyword/?kyoka=rika&grade=g5&cat=all&from={}&sort=ranking'.format(
            i*20+1)
        driver.get(url)
        html = driver.page_source.encode('utf-8')
        soup = BeautifulSoup(html, "html.parser")
        for link in soup.select('div.itemKyouka > a'):
            link_list.append(link.get('href'))
        time.sleep(1)

    template = loader.get_template('prototype/scraping.html')
    context = {
        'linklist': link_list,
    }
    return HttpResponse(template.render(context, request))
