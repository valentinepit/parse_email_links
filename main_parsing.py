'''Задача пройти по списку ссылок и получить все адреса элетронной почты на сайтах. Не только те что указаны ссыдками,
но и встречатся просто в тексте'''

import bs4, re, xlwt, openpyxl
from langdetect import detect
from pip._vendor import requests


def take_adress(file_name ,dic):
    #берет из файла адрес сайта и передает его в поиск
    em_list = []
    f = open(file_name, 'r', encoding='UTF8')
    for line in f:
        print(line)
        try:
            html_txt = requests.get(line[:-1]).content
            soup = bs4.BeautifulSoup(html_txt, 'html.parser')
            dic = take_text(soup, line.rstrip("\n"), dic)
            break
        except requests.exceptions.RequestException as e:
            continue
    f.close()
    return dic

def take_text(soup, file_name, dic):
    #забирает с сайта с именем name вессть текст
    email =[] #список адресов
    email.append(soup.find_all(string=re.compile('[\w\.-]+@[\w\.-]+(?:\.[\w]+)+')))#поиск на главной странице
    links = []
    temp =''
    lng = language(soup) #передаем содержимое на определение языка
    for i in soup.find_all('a', href=True): #вытаскиваем все ссылки
        if 'mailto' in i['href']: #если есть ссылка с текстом mailto
            temp = i['href'][7:]
        links.append(i['href']) #собирает все ссылки со страницы
    for i in range(len(links)-1, -1, -1): #убираем ссылки на внешние ресурсы и на index
        if 'http' in links[i] or links[i] == '/' or 'mailto' in links[i]:
            del links[i]
    for i in links: # перебираем все внутренние ссылки с главной страницы
        url_of = file_name + i
        email[0] += poisk_tags(url_of)[0]

    email = set(email[0])
    email = list(email)
    email.append(temp)

    for i in range(len(email)-1, -1, -1):
        if len(email[i]) > 40:
            del email[i]
    dic[file_name] = [email, lng]
    return (dic)

def poisk_tags(url_of):
    # Ищет на странице все что может быть адресом электронной почты
    html_txt = requests.get(url_of).content
    soup = bs4.BeautifulSoup(html_txt, 'html.parser')
    list_em = []
    list_em.append(soup.find_all(string=re.compile('[\w\.-]+@[\w\.-]+(?:\.[\w]+)+'))) #поиск в дочерних страницах
    return list_em

def language(soup):
    #определяет язык сайта
    s = ''
    for i in soup.find_all('h2'): #берем текст из всех заголовков h2 для анализа языка
        s = s + i.get_text() + ' '
    try:
        s = detect(s)
    except:
        return('en')
    #print(s)
    return s

def losk(dic):
    #причесываем список
    new_dic = {}
    for i in dic:
        new_dic[i] = []
        try:
            dic[i][0].remove('')
        except ValueError:
            print('OK')
        #new_dic[i] = dic[i][0]
        for k in range(len(dic[i][0])):
           s = re.findall('[\w\.-]+@[\w\.-]+(?:\.[\w]+)+', dic[i][0][k])
           if s in new_dic[i]:
               print('Yes')
               continue
           else:
               new_dic[i] += s
           print((re.findall('[\w\.-]+@[\w\.-]+(?:\.[\w]+)+', dic[i][0][k])))

        new_dic[i].append(dic[i][1])
        print(new_dic)
    return (new_dic)

def write_in_file(dic):
    book = xlwt.Workbook(encoding="utf-8")
    sheet1 = book.add_sheet('Emailes.xsl')
    sheet1.write(0, 0, 'Адрес сайта')
    sheet1.write(0, 1, 'Язык')
    sheet1.write(0, 2, 'E-mailes')
    k = 1;

    for i in dic:
        sheet1.write(k, 0, i)
        for j in range (len(dic[i])-1):
            sheet1.write(k, j+2, dic[i][j])
        sheet1.write(k, 1, dic[i][-1:])
        k += 1
    book.save('Emailes.xls')


dic = {}
file = 'adres.txt' #файл со списком адресов

dic = take_adress(file, dic)
#print(dic)
#f = open('base_of_email.txt', 'w', encoding='UTF8') #запись в файл результата
dic = losk(dic)
write_in_file(dic)
#for i in dic:
#    f.write(f'{i} : {dic[i]} "\n"')
#f.close()
