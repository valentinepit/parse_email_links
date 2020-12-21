import bs4
import re

from pip._vendor import requests


def take_adress(file_name):
    #берет из файла адрес сайта и передает его в поиск
    em_list = []
    f = open(file_name, 'r', encoding='UTF8')
    for line in f:
        #take_text(line)
        take_text(line[:-1])
        break
    f.close()
    print(em_list)



def take_text(name):
    #забирает с сайта с именем name вессть текст
    html_txt = requests.get(name).content
    soup = bs4.BeautifulSoup(html_txt, 'html.parser')
    text = soup.find_all(string=re.compile('[\w\.-]+@[\w\.-]+(?:\.[\w]+)+'))
    print(text)

def poisk_tags(text):
    # ищет все ссылки на первой странице сайта
    pass

def poisk_email(text):
    #Ищет на странице все что может быть адресом электронной почты
    pass

def language(text):
    #определяет язык сайта
    pass

file = 'adres.txt'

take_adress(file)

