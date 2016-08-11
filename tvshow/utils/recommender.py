import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import scale
from .cts import build_training_set
import os

module_dir = os.path.dirname(__file__)

train_df = build_training_set()
x_train = scale(train_df.iloc[:, 5:])
y_train = train_df.iloc[:, 3]
x_train_labels = train_df.iloc[:, 0]

target_df = pd.read_csv(os.path.join(module_dir,'data.csv'))
target_df = pd.DataFrame(target_df)
target_df = target_df.append(train_df)
target_df = target_df.append(train_df)
target_df = target_df.drop_duplicates('SeriesName', keep=False)

x_target = scale(target_df.iloc[:, 5:])
x_target_labels = target_df.iloc[:, 0]

def get_recommendations():
	clf = RandomForestClassifier()
	clf.fit(x_train,y_train)

	y_target = clf.predict(x_target)

	new_df = pd.DataFrame()
	new_df['seriesName'] = x_target_labels
	new_df['tvdbID'] = target_df.iloc[:, 1]
	new_df['PredictedRating'] = y_target
	new_df['indicator'] = (target_df.iloc[:, 4]/target_df.iloc[:, 3])*new_df['PredictedRating']

	new_df = new_df.sort_values(['indicator'], ascending=False)
	return list(new_df.iloc[:, 1].head(n=9))
