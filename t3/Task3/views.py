from django.shortcuts import render, redirect
from django.http import HttpResponse
from bs4 import BeautifulSoup
from urllib.request import urlopen
import re
import pandas as pd
from .models import Event_brite,Insider
mylist = []
df = pd.read_csv('interest.csv')

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
    for element in title2:
        if count % 2 == 0:
            if count < 19:
                title.append(element.get_text())
            else:
                break
            # print(element.get_text())
        count += 1

    count = 0
    for element in time:
        if count % 2 == 0:
            if count <19:
                date_time.append(element.get_text())
            else:
                break
            # print(element.get_text())
        count += 1
    count = 0
    for link in links:
        temp = []
        if count % 4 == 0:
            if count < 37:
                html2 = urlopen(link.get('href'))
                soup2 = BeautifulSoup(html2, 'html.parser')
                for a in soup2.findAll('a', attrs={'class': 'badge'}):
                    temp.append(re.sub('[^a-zA-Z]', '', a.text))
                url.append(link.get('href'))
                # make dict of list with less elements
                temp2 = [x.lower() for x in temp]
                category.append(check(temp2))
            else:
                break

        count += 1
    count = 0
    print(len(title), len(date_time), len(category), len(url))
    for i in title:
        Event_brite.objects.create(
            Event_Title=i, URL=url[count], Date_time=date_time[count], Category=category[count])
        count += 1
    obj = Event_brite.objects.all()
    context['Event'] = obj
    print(context)

    return render(request, 'eventbrite.html', context)


def insider(request):
    context={}
    Insider.objects.all().delete()
    input_link = "https://insider.in/online"
    html = urlopen(input_link)
    soup = BeautifulSoup(html, 'html.parser')
    Event_link=[]
    Event_tag=[]
    Event_title=[]
    Event_time=[]
    link = soup.find_all('div', attrs={'class':'event-card'})
    for i in link:
        link2 = i.find('a',href=True)
        Event_link.append("insider.in"+link2['href'])
        tag = i.find('span', class_="card-genre")
        Event_tag.append(tag.get_text())
        title = i.find('span', class_="event-card-name-string")
        Event_title.append(title.get_text())


        time = i.find('span', class_="event-card-date")
        Event_time.append(time.get_text())

    print(Event_title)
    for i in range(0,37,4):
        Insider.objects.create(
            Event_Title=Event_title[i], URL=Event_link[i], Date_time=Event_time[i], Category=Event_tag[i])
        
    obj = Insider.objects.all()
    context['Event'] = obj
    return render(request, 'insider.html', context)


def check(temp):
    word = ''
    for x in temp:
        for y in mylist:
            if x in y:
                word += y+' '
    if word =='':
        word = 'NONE'

    return word


def res(request):

    context = {}
    Int_link_insider=[]
    Non_Int_link_insider=[]
    Int_link_eventbrite=[]
    Non_Int_link_eventbrite=[]    
    input_link2 = "https://insider.in/online"
    html2 = urlopen(input_link2)
    soup2 = BeautifulSoup(html2, 'html.parser')
    for link in  soup2.find_all('a',href=re.compile("^(http|https)://")):
        Non_Int_link_insider.append(link['href'])
    link2 = soup2.find_all('div', attrs={'class':'event-card'})
    
    for i in link2:
        link2 = i.find('a',href=True)
        Int_link_insider.append("insider.in"+link2['href'])



    input_link = "https://www.eventbrite.com/d/online/all-events/"
    html = urlopen(input_link)
    soup = BeautifulSoup(html, 'html.parser')
    
    
    for link in  soup.find_all('a',href=re.compile("^(http|https)://")):
        if len(link['href']) < 45:
            Non_Int_link_eventbrite.append(link['href'])
    count=0
    links = soup.find_all('a', class_="eds-event-card-content__action-link")
    for link in links:
       
        if count % 4 == 0:
            if count <37:
                Int_link_eventbrite.append(link.get('href'))
        count+=1
    context['ILE']=Int_link_eventbrite
    context['NILE']=Non_Int_link_eventbrite
    context['ILI']=Int_link_insider[0:30:2]
    context['NILI']=Non_Int_link_insider
    print(context.keys())
    return render(request, 'table.html', context)
