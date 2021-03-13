from janome.tokenizer import Tokenizer
from janome.analyzer import Analyzer
from janome.charfilter import *
from janome.tokenfilter import *
from django.http import HttpResponse


def index(request):
    li = []
    text = "なんで空は青いの？"
    char_filters = [UnicodeNormalizeCharFilter()]
    tokenizer = Tokenizer()
    token_filters = [POSKeepFilter(['名詞', '形容詞'])]
    analyzer = Analyzer(char_filters=char_filters,
                        tokenizer=tokenizer, token_filters=token_filters)
    for token in analyzer.analyze(text):
        li.append(token.surface + ',')
    return HttpResponse(li)
