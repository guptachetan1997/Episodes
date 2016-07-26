import requests
import os

def get_id_if(search_string):
	title_search_url = "http://www.omdbapi.com/?t=" + search_string.lower() + "&y=&plot=full&r=json"
	r = requests.get(title_search_url)
	data = r.json()
	if data['Response'] == 'True' and data['Type'] == 'series':
		return data['Title'],data['imdbID'],int(data['totalSeasons']),data['Plot'],data['Poster']
	else:
		return None,None,None,None,None

def get_full_season_data(search_string):
	tv_show_data = {}
	tv_show_data['Episode_data'] = {}
	(Title,imdbID,totalSeasons,Plot,Poster) = get_id_if(search_string)
	if imdbID is not None:
		tv_show_data['Title'] = Title
		tv_show_data['imdbID'] = imdbID
		tv_show_data['totalSeasons'] = totalSeasons
		tv_show_data['Plot'] = Plot
		tv_show_data['Poster'] = Poster
		id_url = "http://www.omdbapi.com/?i="+ imdbID + "&Season="
		for season in range(totalSeasons):
			r = requests.get(id_url+str(season+1))
			data = r.json()
			tv_show_data['Episode_data']['Season'+str(season+1)] = data
			tv_show_data['Episode_data']['Season'+str(season+1)]['count'] = len(tv_show_data['Episode_data']['Season'+str(season+1)]['Episodes'])
		return(tv_show_data)
	else:
		return None

def download_image(url, slug):
	r = requests.get(url)
	slug = slug + '.jpg'
	imageFile = open(os.path.join('media_cdn', os.path.basename(slug)), 'wb')
	for chunk in r.iter_content(100000):
		imageFile.write(chunk)
	imageFile.close()
	return os.path.join('media', os.path.basename(slug))
