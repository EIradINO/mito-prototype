from janome.tokenizer import Tokenizer
from janome.analyzer import Analyzer
from janome.charfilter import *
from janome.tokenfilter import *
from django.http import HttpResponse
from django.template import loader
import requests
from bs4 import BeautifulSoup


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
    # return HttpResponse(wordlist)


def scraping(request):
    site = requests.get(
        'https://www.nhk.or.jp/school/program/')
    data = BeautifulSoup(site.content, 'lxml')
    return HttpResponse(data.find('a').get('href'))
