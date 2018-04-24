from bs4 import BeautifulSoup
from requests import get
import pandas as pd
import operator
from time import sleep
from random import randint
from time import time
from warnings import warn
import re
# Variable of controlers
page_init = 0
page_final = 30
year_init = 2000
year_final = 2018
genre_number = 500
# Create a list with the genres found
def insert_uniques_items(items,uniques_items):
    for item in items:
        if item.strip() not in uniques_items:
            uniques_items.append(item.strip())
# Checks if the amount of 500 titles per genre has been reached
def check_is_limit_download(mydict):
    if len(mydict) <=0:
        return False
    for value in mydict.values():
        if value <= genre_number:
            return False
    return True
# Makes the requests to the title server
def get_titles(year_url,page,requests):
    # Declaring the lists to store data in
    names = []
    years = []
    ratings = []
    genres = []
    # Make a get request
    headers = {"Accept-Language": "en-US, en;q=0.5"}
    response = get('http://www.imdb.com/search/title?release_date=' + year_url +
    '&sort=num_votes,desc&page=' + page, headers = headers)
    if response.status_code != 200:
        warn('Request: {}; Status code: {}'.format(requests, response.status_code))
    page_html = BeautifulSoup(response.text, 'html.parser')
    # Select all the 50 movie containers from a single page
    movie_containers = page_html.find_all('div', class_ = 'lister-item mode-advanced')
    # For every movie of these 50
    for container in movie_containers:
            # Scrape the name
            name = container.h3.a.text
            names.append(name)
            # Scrape the year
            year = container.h3.find('span', class_ = 'lister-item-year').text
            #remove non-numeric characters
            year = re.sub('[^0-9]', '', year)
            years.append(int(year))
            # Scrape the IMDB rating
            rating = float(container.strong.text)
            ratings.append(rating)
            # Scrape the Genre
            genre = container.p.find('span', class_ = 'genre').text
            #remove empty characters and
            genre = genre.replace('\n', '').strip() 
            genres.append(genre)
            
    return pd.DataFrame({'movie': names,
                    'year': years,
                    'rating': ratings,
                    'genre':genres})
#----------------------------------------------------------------------------------------
# Variable to separete the data by genre
unique_genre = []
dict_genre = {}
# Variable contains the iformation about the movies
df = pd.DataFrame([])
movie_data_frame = pd.DataFrame([])
# Preparing the monitoring of the loop
start_time = time()
requests = 0
# delay to conect
sleep(randint(1,2))
while(not check_is_limit_download(dict_genre)):
    requests += 1
    elapsed_time = time() - start_time
    page_init = page_init+1
    if page_init > page_final:
        page_init = 0
        year_init = year_init+1
    if year_init > year_final:
        print("Date ended: "+ str(year_init))
        break
    print('\nRequest:{}; Year:{}; Page:{}; Frequency: {} requests/s; Time: {}s\n'.format(requests,year_init, page_init, requests/elapsed_time, elapsed_time))
    # Ensure that the program is not broken on a nonexistent page for the current year
    try:
        df = get_titles(str(year_init),str(page_init),requests)
        movie_data_frame = movie_data_frame.append(df)
    except:
        continue
    # remove duplicate entrys
    movie_data_frame = movie_data_frame.drop_duplicates(subset=['movie'])
    for genre in movie_data_frame['genre']:
        separate_splits = genre.split(',')
        insert_uniques_items(separate_splits,unique_genre)
    # Save a number of titles per genre in a dictionary
    for genre in unique_genre:
        movie_genre = movie_data_frame.loc[movie_data_frame['genre'].str.contains(genre)]
        if genre not in dict_genre:
            dict_genre.update({genre:len(movie_genre)})
        else:
            dict_genre[genre] = len(movie_genre)
    # Sorted dict genre        
    sorted_dict_genre = sorted(dict_genre.items(), key=operator.itemgetter(1), reverse= True)
    print(sorted_dict_genre)

print("-----------------------Genres found----------------------------------------")
sorted_dict_genre = sorted(dict_genre.items(), key=operator.itemgetter(1), reverse= True)
print("Genre lengh: "+ str(len(dict_genre)))
print(sorted_dict_genre)
# Sorted list of dataframes by rating
movie_data_frame = movie_data_frame.sort_values(by=['rating'])
for genre in unique_genre:
    movie_genre = movie_data_frame.loc[movie_data_frame['genre'].str.contains(genre)]
    movie_genre = movie_genre.head(genre_number)
    movie_genre_jsonl = movie_genre.to_json(orient='records',lines=True,force_ascii=False)
    # Saving data on files
    arq = open("files/"+genre+".txt","w")
    arq.writelines(movie_genre_jsonl)
    arq.close()
print("-----------------------Finished program-------------------------------------")
