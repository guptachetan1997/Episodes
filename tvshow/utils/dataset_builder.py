import requests
from bs4 import BeautifulSoup
import random
from urllib.parse import quote
import time
import pandas as pd

user_agents = [
	'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11',
	'Opera/9.25 (Windows NT 5.1; U; en)',
	'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)',
	'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (like Gecko) (Kubuntu)',
	'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.142 Safari/535.19',
	'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:11.0) Gecko/20100101 Firefox/11.0',
	'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:8.0.1) Gecko/20100101 Firefox/8.0.1',
	'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.151 Safari/535.19',
	'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:41.0) Gecko/20100101 Firefox/41.0'
]

popular_networks = ['CBS', 'USA Network', 'AMC' , 'ABC (US)', 'Netflix', 'HBO', 'FOX', 'NBC', 'FX', 'BBC']

cols = [
'SeriesName',
'tvdbID',
'Network',
'tvdbRating',
'indicator']

genres = [
'Action',
'Adventure',
'Animation',
'Children',
'Comedy',
'Crime',
'Documentary',
'Drama',
'Family',
'Fantasy',
'Food',
'Game Show',
'Home and Garden',
'Horror',
'Mini-Series',
'Mystery',
'News',
'Reality',
'Romance',
'Science-Fiction',
'Soap',
'Special Interest',
'Sport',
'Suspense',
'Talk Show',
'Thriller',
'Travel',
'Western',
]

tv_df = pd.DataFrame(columns=cols+genres)


def get_shows_for_network(network):
	headers={'User-Agent':user_agents[random.randint(0,8)]}
	url = 'http://thetvdb.com/?language=7&genre=' + '&network=' + quote(network) + '&order=fanartcount%20desc&searching=Search&tab=advancedsearch'
	r = requests.get(url, headers=headers)
	html = r.text.encode('utf8')
	soup = BeautifulSoup(html, "lxml")
	ex = soup.find('table', attrs={'id':"listtable"})
	shows = ex.findAll('tr')
	for show in shows[1:51]:
		try:
			show_data = show.findAll('td')
			seriesName = show_data[1].text
			tvdbID = show_data[1].find('a')['href']
			tvdbID = tvdbID[tvdbID.find('id')+3:tvdbID.rfind('&')]
			show_genre = show_data[2].text
			rating = show_data[6].text
			fanart = show_data[7].text
			indicator = (float(fanart)*float(rating))
			show_genre = show_genre[1:len(show_genre)-1]
			show_genre = show_genre.split('|')
			show_genre_list = [0]*28
			length = len(show_genre)
			for genre in show_genre:
				show_genre_list[genres.index(genre)] = 1.0/length
			show_data = [seriesName, tvdbID , network, rating, indicator]
			global tv_df
			tv_df = tv_df.append(pd.DataFrame([show_data+show_genre_list], columns=cols+genres))
		except:
			pass

for network in popular_networks:
	print(network)
	get_shows_for_network(network)
	time.sleep(2)

tv_df.to_csv('data.csv', index=False)

df = pd.read_csv('data.csv')
df = pd.DataFrame(df)
df2 = df.sort_values('indicator', ascending=False)
print(df2.head())
df2.to_csv('data.csv', index=False)
