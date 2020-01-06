# -*- coding: utf-8 -*-
#does not scale well to large datasets 

#*****************************Mean shift LOB*****************************#

#1. After training the model,  store the coordinates for the cluster centers.
to_MS = Lob_Norm

my_bandwidth = estimate_bandwidth(to_MS,
                               quantile=0.2,
                               n_samples=1000)

mslob = MeanShift(bandwidth=my_bandwidth,
               cluster_all = False,
               bin_seeding=True)

mslob.fit(to_MS)
labels = mslob.labels_
cluster_centers = mslob.cluster_centers_

labels_unique = np.unique(labels)
n_clusters_ = len(labels_unique)
#3 clusters


#Count
unique, counts = np.unique(labels, return_counts=True)

print(np.asarray((unique, counts)).T)
#[[  -1 5046]
#[   0 5114]
#[   1   18]]

print("Silhouette Coefficient: %0.3f"  % metrics.silhouette_score(to_MS, labels, metric='euclidean', sample_size=None, random_state=None))

#*****************************Mean shift ENGAGE*****************************#

MSNumVE = NumVE_Norm

my_bandwidthVE = estimate_bandwidth(MSNumVE, quantile=0.4, n_samples=1000)

msengage = MeanShift(bandwidth=my_bandwidthVE,
               cluster_all = False,
               bin_seeding=True)

msengage.fit(MSNumVE)
labelsVE = msengage.labels_
cluster_centers = msengage.cluster_centers_

labels_uniqueVE = np.unique(labelsVE)
n_clusters_VE = len(labels_uniqueVE)
#1 cluster: clearly not suitable for this data 


#Count
unique, counts = np.unique(labelsVE, return_counts=True)

print(np.asarray((unique, counts)).T)

print("Silhouette Coefficient: %0.3f"  % metrics.silhouette_score(MSNumVE, labelsVE, metric='euclidean', sample_size=None, random_state=None))
#Silhouette Coefficient: 0.213

