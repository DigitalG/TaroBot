import requests
from html.parser import HTMLParser



class MyHTMLParser(HTMLParser):
    IsData = False
    result = []
    tmp = ''
    i = 0

    def handle_starttag(self, tag, attrs):
        if tag == 'div' and attrs == [('class', 'wysiwyg')]:
            self.IsData = True
            self.tmp += '---\n'
            #print("Encountered a start tag:", tag)

    def handle_endtag(self, tag):
        if tag == 'div':
            if self.IsData:
                self.i += 1
                self.IsData = False
                #self.tmp+= 'div-end----\n'
            #print("Encountered an end tag :", tag)

    def handle_data(self, data):
        if self.IsData:
            self.tmp += data.replace('\r', '').replace('\t', '').replace('\n\n','\n').replace('\n\n','\n').replace('τροπή','')


def parse(door):
    r = requests.get('https://www.taro.lv/ru/78_dverej/door_' + door, )
    r.encoding = 'utf-8'
    titles = ['Общее значение', 'Личностное состояние', 'На более глубоком уровне', 'Проффесиональная ситуация',
              'Финансовое положение', 'Личные отношения', 'Состояние здоровья', 'Перевернутая карта',
              'Проявления в сочетаниях', 'Архетипические соответствия', 'Копилка наблюдений']

    parser = MyHTMLParser()
    parser.feed(r.text)
    f = open('result.txt', 'w')
    # f.write(parser.tmp)
    for c in parser.tmp:
        f.write(c)
    f.close()
    #print(parser.result)
    # print(r.text)
