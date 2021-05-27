from django.shortcuts import render
from django.http import HttpResponse
from bs4 import BeautifulSoup
import requests
from urllib.request import urlopen
import operator
import json
from pprint import pprint
import requests
import extruct
from w3lib.html import get_base_url
import re
from .models import Event,Non_interesting
'''def get_html(url):
    """Get raw HTML from a URL."""
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Max-Age': '3600',
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
    }
    req = requests.get(url, headers=headers)
    return req.text
'''

def result(request):
    link=requests.get('https://insider.in/online') #main link
    #page = urlopen(link)
    #html = page.read().decode("utf-8")
    soup = BeautifulSoup(link.content, "html.parser") #soup object created
    

    eventurl=[]
    data=[]
    for elem in soup.find_all('a', href=re.compile('/event')): # find all the event liks in our link(since all event links end with /event)
        if(elem['href'] in eventurl or 'https://insider.in'+ elem['href'] in eventurl):
            pass
        elif elem['href'].endswith('/event'):
            if(elem['href'].startswith('https://insider.in')): # some of the links dont start with the given text and so we check 
                eventurl.append( elem['href'])
            else:
                eventurl.append(('https://insider.in'+ elem['href'])) # if doesnt start with it then along with the link we append that part and store in list
    
    links = []

    for link in soup.find_all('a',href=re.compile('^https://')):
       links.append(link['href'])

    noninteresting_url=list(filter(lambda x: x not in eventurl, links))

    for element in noninteresting_url:
        if(Non_interesting.objects.filter(url=element).exists()): # if object already created
            pass
        else:
            ob=Non_interesting.objects.create(url=element)
            ob.save()



    for i in range(0,10): #access first 10 links of event from eventurl
        print(eventurl[i])
        link1=requests.get(eventurl[i]) #get it in html form
        metadata = get_metadata(link1.text, eventurl[i]) # we get the structured data from the page using get_metadata it takes 2 args one is the html's text and other is the url
        data.append(metadata) #store the dict in a list
        if(Event.objects.filter(url=data[i]['url']).exists()): # if object already created
            pass
        else:
            obj=Event.objects.create(name=data[i]['name'],des=data[i]['description'],url=data[i]['url']) #create object for url to store data
            obj.save()
    
    #non=soup.findAll('a').get('href')
    #print(non)
    
        
    
    text=soup.find_all("a")
    mydata=Event.objects.all()
    return render(request,'app/result.html',{"text":mydata,"links":noninteresting_url})

def get_metadata(html: bytes, url: str): #function to get structured data
    """Fetch JSON-LD structured data."""
    metadata = extruct.extract(
        html,
        base_url=get_base_url(url),
        syntaxes=['json-ld'],
        uniform=True
    )['json-ld']
    if bool(metadata) and isinstance(metadata, list):
        metadata = metadata[0]
    return metadata

