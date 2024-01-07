# -*- coding: utf-8 -*-
"""Копия блокнота "Hw2.ipynb"

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1in-HEIkmjDu9fUzZFg7WtxorgbECOHDx

# Домашнее задание 2

## pandas + парсинг

Здесь находится главная страница [Системного блока](https://sysblok.ru)

Соберите корпус новостей (можно спарсить все новости или небольшую часть)

Дедлайн: 29 декабря включительно
"""

# необходимые импорты
import requests # as rq
from bs4 import BeautifulSoup
import pandas as pd

"""### шаг 1"""

# соберите все ссылки на страницы с новостями (цикл for + range)
# 1 страница: https://sysblok.ru
# 2 страница: https://sysblok.ru/page/2
# последняя: https://sysblok.ru/page/16

all_page = ['https://sysblok.ru', ]

# ваш код


page = requests.get(all_page[0])

 # загружаем страницу по ссылке
print(page.status_code)

for i in range(2,17):
  all_page.append(all_page[0] + '/page/' + str(i) )
print(all_page)


# берет только 2 ссылки. что делать с остальными двумя?
#all_page = requests.get("https://sysblok.ru")
#soup = BeautifulSoup(all_page.text, features="html.parser")

"""### шаг 2"""

# с каждой страницы соберите ссылки на отдельные новости
# подсказка: родительский тег h2 (проверяйте по нему), нужный нам - a

all_links = []


# ваш код
for p in all_page:



  page = requests.get(p)
  soup = BeautifulSoup(page.text, features="html.parser")

  for link in soup.find_all('a'):
    if link.parent.name == 'h2':
      all_links.append(link.get('href'))

all_links

len(all_links)

"""### шаг 3

работаем с 1 новостью:

нас интересует название, автор, дата публикации, текст (дополнительно можно спарсить тематические категории)
"""

# для парсинга даты: извлеките текст из тега time

#import time #надо импортировать это?
news0=all_links[0]
page=requests.get(news0)

soup=BeautifulSoup(page.text, features="html.parser")
print(soup.find('time').text)
date=soup.find('time').text

# для парсинга заголовка: извлеките текст из тега h1


print(soup.find('h1').text)
title=soup.find('h1').text

# для парсинга текста: соберите все тексты из тега p и соедините в строку
# list object has no attribute 'text'
text_list=[]
for i in soup.find_all('p'):
  text_list.append(i.text.strip())

text='\n'.join(text_list)
print(text)

# автора собрать сложнее:
# достаем из тега meta как на паре или из тега a с проверкой на содержимое атрибута rel



#это тоже с методом мета, но по-другому
author = soup.find_all('meta', {'name' : 'author'})[0].attrs['content'] # вызовем автора по ключу (content) и сохраним в переменную
print(author )

# тематические категории:
# <a rel="category tag"> нужные нам категории </a>
# можно попробовать так:
# if i.get('rel') == ['category', 'tag']

tags=[]
for i in soup.find_all('a'):
  if i.get('rel') == ['category', 'tag']:
    tags.append(i.text)

tags_str=', '.join(tags)
tags_str

"""### шаг 4"""

# пишем функцию по сбору информации

# all_links / all_page??
# это по сбору news с тегом mb??? но не знаю подходит ли оно сюда
def get_news(news0):
  page=requests.get(news0)

  soup=BeautifulSoup(page.text, features="html.parser")
  title=soup.find('h1').text
  text_list=[]
  for i in soup.find_all('p'):
    text_list.append(i.text.strip())
  author = soup.find_all('meta', {'name' : 'author'})[0].attrs['content']

  text='\n'.join(text_list)
  date=soup.find('time').text
  tags=[]
  for i in soup.find_all('a'):
    if i.get('rel') == ['category', 'tag']:
      tags.append(i.text)
  tags_str=', '.join(tags)
  tags_str
  return news0, author, title, date, text, tags_str

# собираем все новости!
# полезно использовать try / except

#??? нашла в тетрадке про новости, но не знаю что оно делает
news = [] # список с новостями

for i in all_links:
  try:
        news.append(get_news(i))
  except:
        print(f'с сылкой {i} не работает')

print('Все в порядке!')

"""### шаг 5"""

# соберите всю собранную информацию в датафрейм


# это создание таблички
df = pd.DataFrame(news)
df.head()
#news0, author, title, date, text, tags_str
#это создание колонок, но я пока не знаю какие нужны
df.columns = ['link', 'author', 'title', 'date', 'text', 'tags']
df.head(1)



"""Готово!
Загрузите ваш код и собранные новости на GitHub
"""