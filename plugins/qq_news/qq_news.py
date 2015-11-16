import sys,os,time
reload(sys)
sys.setdefaultencoding('utf-8')

def _qq_news_index():
    return 'this is qq news!'

def run(app):
    app.add_url_rule('/qq_news/index', '_qq_news_index', _qq_news_index)