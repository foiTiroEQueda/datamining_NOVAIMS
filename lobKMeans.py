# -*- coding: utf-8 -*-


#https://medium.com/@jyotiyadav99111/selecting-optimal-number-of-clusters-in-kmeans-algorithm-silhouette-score-c0d9ebb11308

#Lob Normalization
#using z score normalization
scaler=StandardScaler()
Lob_Norm =scaler.fit_transform(VarsLob)
Lob_Norm =pd.DataFrame(Lob_Norm, columns=VarsLob.columns)



#elbow graph
wcss = []
for i in range(1, 11):
    kmeansElbow = KMeans(n_clusters=i, init='k-means++', max_iter=200, n_init=5, random_state=0)
    kmeansElbow.fit(Lob_Norm)
    wcss.append(kmeansElbow.inertia_)
plt.plot(range(1, 11), wcss, '#ab7946')
plt.title('Elbow Graph')
plt.xlabel('Number of clusters')
plt.ylabel('WCSS')
plt.show()


n_clusters=3
kmeans = KMeans(n_clusters=n_clusters, 
                random_state=0,
                n_init = 30,
                max_iter=200).fit(Lob_Norm)  
    
my_clusters = kmeans.cluster_centers_ 

my_clusters = pd.DataFrame(kmeans.cluster_centers_)

#denormalize
lobClusters = scaler.inverse_transform(my_clusters)
lobClusters = pd.DataFrame(lobClusters)
lobClusters.columns = Lob_Norm.columns



silhouette_avg_lob = silhouette_score(Lob_Norm, kmeans.labels_)

print("For n_clusters =", n_clusters,",the average silhouette_score is :", silhouette_avg_lob)
#For n_clusters = 3 ,the average silhouette_score is : 0.34 (aprox)
#justify with what is said on the report about data quality hindering clustering quality

#-------------------------------------------------
#tried k means with large k and hierarchical on top of it, didn't work, dendrogram was not very clear and clustering solutions (for k=2 and k=5) were terrible
#-------------------------------------------------

#obs in each cluster
obsInEachClusterLOB = pd.DataFrame(kmeans.labels_)
obsInEachClusterLOB.columns = ['label']
obsInEachClusterLOB_0 = len(obsInEachClusterLOB.loc[obsInEachClusterLOB['label']==0])
obsInEachClusterLOB_1 = len(obsInEachClusterLOB.loc[obsInEachClusterLOB['label']==1])
obsInEachClusterLOB_2 = len(obsInEachClusterLOB.loc[obsInEachClusterLOB['label']==2])

del obsInEachClusterLOB
obsInEachClusterLOB = pd.DataFrame([obsInEachClusterLOB_0, obsInEachClusterLOB_1, obsInEachClusterLOB_2])
del obsInEachClusterLOB_0
del obsInEachClusterLOB_1
del obsInEachClusterLOB_2


lob_labels = pd.DataFrame(kmeans.labels_)
#
#
#
#
#
#
#
#-------------------------------------------------------
#                   Variables Guide                  
#-------------------------------------------------------
#
#obsInEachClusterLOB - Nr of obs per cluster
#lob_labels - Labels
#lobClusters - Centroids
#silhouette_avg_lob - Silhouette Score
