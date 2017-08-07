from requests import get
from bs4 import BeautifulSoup
import pandas as pd
from time import sleep,time
from IPython.core.display import clear_output
from random import randint

pages=[str(i) for i in range(1,5)]
years_url=[str(i) for i in range(2000,2018)]

names=[]
years=[]
imdb_ratings=[]
metascores=[]
votes=[]

#Preparing the monitoring of the loop
start_time=time()
requests=0

#for every year in the interval 2000-2017
for year_url in years_url:
    #for every page in the interval 1-4
    for page in pages:
        #Make a get response
        response=get('http://www.imdb.com/search/title?release_date='+year_url+'&sort=num_votes,desc&page='+page)

        #pause the loop
        sleep(randint(8,15))

        #monitor the requests
        requests+=1
        elapsed_time=time()-start_time
        print('Request: {};Frequency: {} requests/s'.format(requests, requests/elapsed_time))
        clear_output(wait = True)

        #Throw a warning for non-200 status codes
        if response.status_code!=200:
            warn('Request: {}; Status code: {}'.format(requests,response.status_code))

        #Break the loop if the number of requests is greater than 72
        if requests>72:
            warn('Number of requests were greater than expected')
            break

        page_html=BeautifulSoup(response.text,'html.parser')
        movie_containers=page_html.find_all('div',class_="lister-item mode-advanced")
        for container in movie_containers:
            #Extracting data only if metascores are available
            if container.find('div',class_="inline-block ratings-metascore") is not None:
                #The names
                name=container.h3.a.text
                names.append(name)
                #The years
                year=container.h3.find('span',class_="lister-item-year text-muted unbold").text
                years.append(year)
                #The imdb ratings
                imdb_rating=container.find('strong').text
                imdb_ratings.append(imdb_rating)
                #The metascores
                metascore=container.find('div',class_="inline-block ratings-metascore").find('span').text
                metascores.append(metascore)
                #The number of votes
                vote=int(container.find('p',class_="sort-num_votes-visible").find('span',attrs={'name':'nv'})['data-value'])
                votes.append(vote)

movie_ratings=pd.DataFrame({'movie':names,
                    'year':years,
                    'imdb':imdb_ratings,
                    'metascore':metascores,
                    'votes':votes})
print(movie_ratings.info())
print(movie_ratings.head(10))
