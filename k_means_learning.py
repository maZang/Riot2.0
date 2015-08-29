import pandas as pd
import numpy as np
from sklearn import svm
from sklearn import preprocessing
from sklearn.cluster import KMeans
import RiotConsts as Consts 
import json

def main():
	data = pd.read_csv("./data.csv")
	X = data.values
	with open('champ_dict.json', 'r') as df:
		CHAMP_TO_MATRIX = json.load(df)
	X = _preprocess(X)
	initial_centroids = ['Thresh', 'Ashe', 'Annie', 'Shen', 'Riven']
	init_centroid_mtrx = np.empty(shape=[len(initial_centroids), Consts.BLACK_MARKET_FEATURES - 1])
	row_index = 0
	for champ in initial_centroids:
		row_num = CHAMP_TO_MATRIX[champ]
		init_centroid_mtrx[row_index, :] = X[row_num, :]
	kmean = KMeans(n_clusters = 5, init = init_centroid_mtrx, max_iter = 300)

def _preprocess(mtrx):
	num_games = mtrx[:, Consts.BLACK_MARKET_FEATURES-1]
	for col in range(1, mtrx.shape[1]):
		mtrx[:, col] = np.divide(mtrx[:, col], num_games)
	mtrx = mtrx[:, :Consts.BLACK_MARKET_FEATURES-1]
	print(mtrx.size)
	mtrx_scaled = preprocessing.scale(mtrx)
	return mtrx_scaled

if __name__ == "__main__":
	main()