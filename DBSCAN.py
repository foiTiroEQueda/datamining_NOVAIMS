#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#********************************************LOB********************************************#
#2. CHOOSING THE EPS NUMBER  (https://towardsdatascience.com/machine-learning-clustering-dbscan-determine-the-optimal-value-for-epsilon-eps-python-example-3100091cfbc)

neighDBSCAN = NearestNeighbors(n_neighbors=2)
nbrsDBSCAN = neighDBSCAN.fit(Lob_Norm)
distances, indices = nbrsDBSCAN.kneighbors(Lob_Norm)

#sort and plot results
distances = np.sort(distances, axis=0)
distances = distances[:,1]
plt.plot(distances)

#3. CLUSTERING WITH DBSCAN
DBSCAN = DBSCAN(eps= 0.6, min_samples=10).fit(Lob_Norm)

DBSCANlabels = DBSCAN.labels_

# Number of clusters in labels, ignoring noise if present.
DBSCANn_clusters_ = len(set(DBSCANlabels)) - (1 if -1 in DBSCANlabels else 0)
DBSCAN_noise_ = list(DBSCANlabels).count(-1)

unique_clusters, counts_clusters = np.unique(DBSCAN.labels_, return_counts = True)
print(np.asarray((unique_clusters, counts_clusters)))

print('Estimated number of clusters: %d' % DBSCANn_clusters_ )
print('Estimated number of noise points: %d' % DBSCAN_noise_)
print("Silhouette Coefficient: %0.3f"  % metrics.silhouette_score(Lob_Norm, DBSCANlabels))

#[[  -1    0    1    2    3]
#[1209 8877   68   13   11]]
#Estimated number of clusters: 4
#Estimated number of noise points: 1209
#Silhouette Coefficient: 0.293

#4. 3D VISUALIZATION
from sklearn.decomposition import PCA
pca = PCA(n_components=2).fit(Lob_Norm)
pca_2d = pca.transform(Lob_Norm)
for i in range(0, pca_2d.shape[0]):
    if DBSCAN.labels_[i] == 0:
        c1 = plt.scatter(pca_2d[i,0],pca_2d[i,1],c='r',marker='+')
    elif DBSCAN.labels_[i] == 1:
        c2 = plt.scatter(pca_2d[i,0],pca_2d[i,1],c='g',marker='o')
    elif DBSCAN.labels_[i] == 2:
        c3 = plt.scatter(pca_2d[i,0],pca_2d[i,1],c='k',marker='v')
    elif DBSCAN.labels_[i] == 3:
        c4 = plt.scatter(pca_2d[i,0],pca_2d[i,1],c='y',marker='s')
    elif DBSCAN.labels_[i] == -1:
        c3 = plt.scatter(pca_2d[i,0],pca_2d[i,1],c='b',marker='*')

plt.legend([c1, c2, c3], ['Cluster 1', 'Cluster 2','Noise'])
plt.title('DBSCAN finds 2 clusters and noise')
plt.show()


#********************************************ENGAGE NUMERICAL********************************************#
#2. CHOOSING THE EPS NUMBER  
neighDBSCANEG = NearestNeighbors(n_neighbors=2)
nbrsDBSCANEG = neighDBSCANEG.fit(NumVE_Norm)
distancesVE, indices = nbrsDBSCANEG.kneighbors(NumVE_Norm)

#sort and plot results
distancesVE = np.sort(distancesVE, axis=0)
distancesVE = distancesVE[:,1]
plt.plot(distancesVE)

#3. CLUSTERING WITH DBSCAN
DBSCANVE = DBSCAN(eps= 0.4, min_samples=10).fit(NumVE_Norm)

DBSCANlabelsVE = DBSCANVE.labels_

# Number of clusters in labels, ignoring noise if present.
DBSCANVEn_clusters_ = len(set(DBSCANlabelsVE)) - (1 if -1 in DBSCANlabelsVE else 0)
DBSCANVE_noise_ = list(DBSCANlabelsVE).count(-1)

unique_clustersVE, counts_clustersVE = np.unique(DBSCANVE.labels_, return_counts = True)
print(np.asarray((unique_clustersVE, counts_clustersVE)))

print('Estimated number of clusters: %d' % DBSCANVEn_clusters_ )
print('Estimated number of noise points: %d' % DBSCANVE_noise_)
print("Silhouette Coefficient: %0.3f"  % metrics.silhouette_score(NumVE_Norm, DBSCANlabelsVE))
#[[  -1    0    1]
#[ 207 9953   18]]
#Estimated number of clusters: 2
#Estimated number of noise points: 207
#Silhouette Coefficient: 0.346

