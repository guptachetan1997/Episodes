from tvshow.models import Show
import pandas as pd

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

def main():
	show_data = Show.objects.all()

	tv_df = pd.DataFrame(columns=cols+genres)

	for show in show_data:
		show_genre_list = [0]*28
		show_genre = show.get_genres
		length = len(show_genre)
		for genre in show_genre:
			show_genre_list[genres.index(genre)] = 1.0/length
		show_datas = [show.seriesName, show.tvdbID , show.network, show.siteRating, (float(show.siteRating)**2)*show.userRating]
		tv_df = tv_df.append(pd.DataFrame([show_datas+show_genre_list], columns=cols+genres))

	print(tv_df)
