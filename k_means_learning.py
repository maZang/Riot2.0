import pandas as pd
import numpy as np
from sklearn import svm
from sklearn import preprocessing
from sklearn.cluster import KMeans
import RiotConsts as Consts 
import json
import scipy
import matplotlib.pyplot as plt

from sklearn import metrics
from sklearn.cluster import KMeans
from sklearn.datasets import load_digits
from sklearn.decomposition import PCA
from sklearn.preprocessing import scale

roles = {0: "Assassin", 1: "Marksman", 2: "Physical Bruiser", 3: "Jungler", 4: "Mage", 5: "Support", 6: "Tank", 7: "Magical Bruiser"}

#previously main function
def get_k_learn():
#def main():
	data = pd.read_csv("./data1.csv")
	X = data.values
	with open('champ_dict.json', 'r') as df:
		CHAMP_TO_MATRIX = json.load(df)
	X, bad_values, scaler = _preprocess(X)
	X_means = X
	#remove bad values from X
	for row in bad_values:
		X_means = np.delete(X_means, row - 1, 0)
	#remove some features (e.g. gold_min because of dependence on cs_min)
	num_features_removed = 3
	#X_means = scipy.delete(X_means, len(Consts.STAT_TO_MATRIX) - 1 + Consts.VARIABLE_TO_MATRIX['gold_min'], 1)
	#X = scipy.delete(X, len(Consts.STAT_TO_MATRIX) - 1 + Consts.VARIABLE_TO_MATRIX['gold_min'], 1)
	#num_features_removed += 1
	#initialize centroids
	initial_centroids = ['Riven', 'Ashe', 'Renekton', 'LeeSin', 'Annie', 'Braum', 'Maokai', 'Singed']
	init_centroid_mtrx = np.empty(shape=[len(initial_centroids), Consts.BLACK_MARKET_FEATURES - num_features_removed])
	row_index = 0
	for champ in initial_centroids:
		row_num = CHAMP_TO_MATRIX[champ]
		init_centroid_mtrx[row_index, :] = X[row_num, :]
		row_index += 1
	kmean = KMeans(n_clusters = 5, init = init_centroid_mtrx, max_iter = 300, verbose = 1)
	kmean = kmean.fit(X_means, y = None)
	return kmean, scaler
	#clusters = kmean.predict(X)
	#champ_roles = make_role_dict(clusters, CHAMP_TO_MATRIX)
	#print(champ_roles)

def plot(X_means):
	#visualize (code retrieved from sci-kit learn)
	reduced_data = PCA(n_components=2).fit_transform(X_means)
	kmeans = KMeans(init='k-means++', n_clusters=7, n_init=10)
	kmeans.fit(reduced_data)

	# Step size of the mesh. Decrease to increase the quality of the VQ.
	h = .02     # point in the mesh [x_min, m_max]x[y_min, y_max].

	# Plot the decision boundary. For that, we will assign a color to each
	x_min, x_max = reduced_data[:, 0].min() + 1, reduced_data[:, 0].max() - 1
	y_min, y_max = reduced_data[:, 1].min() + 1, reduced_data[:, 1].max() - 1
	xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))

	# Obtain labels for each point in mesh. Use last trained model.
	Z = kmeans.predict(np.c_[xx.ravel(), yy.ravel()])

	# Put the result into a color plot
	Z = Z.reshape(xx.shape)
	plt.figure(1)
	plt.clf()
	plt.imshow(Z, interpolation='nearest',
        extent=(xx.min(), xx.max(), yy.min(), yy.max()),
        cmap=plt.cm.Paired,
        aspect='auto', origin='lower')
	plt.plot(reduced_data[:, 0], reduced_data[:, 1], 'k.', markersize=2)
	# Plot the centroids as a white X
	centroids = kmeans.cluster_centers_
	plt.scatter(centroids[:, 0], centroids[:, 1],
        marker='x', s=169, linewidths=3,
        color='w', zorder=10)
	plt.title('K-means clustering on League Champions\n'
        'Centroids are marked with white cross')
	plt.xlim(x_min, x_max)
	plt.ylim(y_min, y_max)
	plt.xticks(())
	plt.yticks(())
	plt.show()

def make_role_dict(clusters, CHAMP_TO_MATRIX):
	champ_roles = {}
	for i in range(0, len(CHAMP_TO_MATRIX)):
		for k, v in CHAMP_TO_MATRIX.items():
			if v == i:
				champ_roles[k] = roles[clusters[i]]
	return champ_roles

def _preprocess(mtrx):
	num_games = mtrx[:, Consts.BLACK_MARKET_FEATURES-1]
	#champs with 0 games
	bad_values = []
	for i, j in enumerate(num_games):
		if j == 0:
			bad_values.append(i)
	#replace bad rows with 0s
	zero_fill = np.zeros(shape=[1, Consts.BLACK_MARKET_FEATURES - 1])
	zero_fill = np.concatenate((zero_fill, np.reshape(np.array([1]), (1, 1))), axis = 1)
	for row in bad_values:
		mtrx[row] = zero_fill
	for col in range(1, mtrx.shape[1]):
		mtrx[:, col] = np.divide(mtrx[:, col], num_games)
	mtrx = mtrx[:, 1:Consts.BLACK_MARKET_FEATURES-2]
	mtrx_scaled = preprocessing.scale(mtrx)
	scaler = preprocessing.StandardScaler().fit(mtrx)
	return mtrx_scaled, bad_values, scaler
	#return mtrx

if __name__ == "__main__":
	main()