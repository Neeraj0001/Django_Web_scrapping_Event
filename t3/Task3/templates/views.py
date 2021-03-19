from django.shortcuts import render, redirect
from django.http import HttpResponse
from bs4 import BeautifulSoup
from urllib.request import urlopen
import re
import pandas as pd
from .models import Event_brite

mylist = []
df = pd.read_csv('./interest.csv')

mylist = df['Interested_Group'].tolist()
mylist = [x.lower() for x in mylist]


def scrap(request):
    context = {}

    return render(request, 'home.html', context)


def Eventbrite(request):
    context = {}
    Event_brite.objects.all().delete()
    input_link = "https://www.eventbrite.com/d/online/all-events/"
    html = urlopen(input_link)

    soup = BeautifulSoup(html, 'html.parser')

    title2 = soup.find_all(
        'div', class_="eds-event-card__formatted-name--is-clamped-three")
    time = soup.find_all('div', class_="eds-text-bs")
    links = soup.find_all('a', class_="eds-event-card-content__action-link")
    count = 0
    title = []
    date_time = []
    category = []
    url = []
    word=''
    for element in title2:
        if count % 2 == 0:
            title.append(element.get_text())
            print(element.get_text())
        count += 1

    count = 0
    for element in time:
        if count % 2 == 0:
            date_time.append(element.get_text())
            # print(element.get_text())
        count += 1
    count = 0
    for link in links:
        temp=[]
        if count%4==0:
            print(link.get('href'))
            html2 = urlopen(link.get('href'))

            soup2 = BeautifulSoup(html2, 'html.parser')
            for a in soup2.findAll('a', attrs={'class':'badge'}):
                temp.append(re.sub('[^a-zA-Z]','',a.text))
            
            temp2 = [x.lower() for x in temp] # make dict of list with less elements  
            for x in temp2:
                for y in mylist:
                    if x in y:
                        word+=y+' '
                category.append(word)
                word=''
        count += 1
    count = 0
    for i in title:
        Event_brite.objects.create(
            Event_Title=i, URL=url[count], Date_time=date_time[count], Category=category[count])
        count += 1
    obj = Event_brite.objects.all()
    context['Event'] = obj
    print(context)

    return render(request, 'eventbrite.html', context)


def Insider(request):
    pass


def res(request):
    context = {}

    return render(request, 'table.html', context)
