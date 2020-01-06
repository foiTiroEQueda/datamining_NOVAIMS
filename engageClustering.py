# -*- coding: utf-8 -*-

#VarsEngage = df[['YearsAsCustomer', 'Educ', 'AnnualSalary', 'LivingArea', 'Children', 'CustMonVal',]].copy(deep=True)
#
#
#
#
#
#
#
#
#-------------------------------------------------------
#                  Variable Division                  
#-------------------------------------------------------
#Categorical Variables: Educ, LivingArea, Children
#Numerical Variables: YearsAsCustomer, AnnualSalary, CustMonVal
engageCatVar = df[['Educ', 'LivingArea', 'Children']].copy(deep=True).astype(str)
engageNumVar = df[['YearsAsCustomer', 'AnnualSalary', 'CustMonVal']].copy(deep=True)
engageCatVar['Children'] = (engageCatVar['Children'] == 'True').astype(int)
#
#
#
#
#
#
#
#-------------------------------------------------------
#                  Numerical Variables                  
#-------------------------------------------------------
scaler=StandardScaler()
engageNumVar_Norm =scaler.fit_transform(engageNumVar)
engageNumVar_Norm =pd.DataFrame(engageNumVar_Norm, columns=engageNumVar.columns)


#...................(only) K Means.......................
#elbow graph
wcss = []
for i in range(1, 11):
    kmeansElbow = KMeans(n_clusters=i, init='k-means++', max_iter=200, n_init=5, random_state=0)
    kmeansElbow.fit(engageNumVar_Norm)
    wcss.append(kmeansElbow.inertia_)
plt.plot(range(1, 11), wcss, '#ab7946')
plt.title('Elbow Graph')
plt.xlabel('Number of clusters')
plt.ylabel('WCSS')
plt.show()

#------------------ 3 clusters ------------
n_clusters=3
kmeansEngageNumSolo = KMeans(n_clusters=n_clusters, 
                random_state=0,
                n_init = 30,
                max_iter=200).fit(engageNumVar_Norm)  
    
my_clusters_engageNum_solo = kmeansEngageNumSolo.cluster_centers_ 

my_clusters_engageNum_solo = pd.DataFrame(my_clusters_engageNum_solo)



#denormalize
engageNumClustersKMeans = scaler.inverse_transform(my_clusters_engageNum_solo)
engageNumClustersKMeans = pd.DataFrame(engageNumClustersKMeans)
engageNumClustersKMeans.columns = engageNumVar_Norm.columns

#silhouette score
silhouette_avg_engagenum = silhouette_score(engageNumVar_Norm, kmeansEngageNumSolo.labels_)
print("For n_clusters =", n_clusters,",the average silhouette_score is :", silhouette_avg_engagenum)
#For n_clusters = 3 ,the average silhouette_score is : 0.24651668279691658

#obs in each cluster
obsInEachCluster_k3 = pd.DataFrame(kmeansEngageNumSolo.labels_)
obsInEachCluster_k3.columns = ['label']
obsInEachCluster_k3_0 = len(obsInEachCluster_k3.loc[obsInEachCluster_k3['label']==0])
obsInEachCluster_k3_1 = len(obsInEachCluster_k3.loc[obsInEachCluster_k3['label']==1])
obsInEachCluster_k3_2 = len(obsInEachCluster_k3.loc[obsInEachCluster_k3['label']==2])
del obsInEachCluster_k3
obsInEachCluster_k3 = pd.DataFrame([obsInEachCluster_k3_0, obsInEachCluster_k3_1, obsInEachCluster_k3_2])
del obsInEachCluster_k3_0
del obsInEachCluster_k3_1
del obsInEachCluster_k3_2

#labels
engagenumlabels = pd.DataFrame(kmeansEngageNumSolo.labels_)


#---------------------- 4 clusters ---------
n_clusters=4
kmeansEngageNumSolo4 = KMeans(n_clusters=n_clusters, 
                random_state=0,
                n_init = 30,
                max_iter=200).fit(engageNumVar_Norm)  
    
my_clusters_engageNum_solo4 = kmeansEngageNumSolo4.cluster_centers_ 

my_clusters_engageNum_solo4 = pd.DataFrame(my_clusters_engageNum_solo4)



#denormalize
engageNumClustersKMeans4 = scaler.inverse_transform(my_clusters_engageNum_solo4)
engageNumClustersKMeans4 = pd.DataFrame(engageNumClustersKMeans4)
engageNumClustersKMeans4.columns = engageNumVar_Norm.columns

#silhouette score
silhouette_avg = silhouette_score(engageNumVar_Norm, kmeansEngageNumSolo4.labels_)
print("For n_clusters =", n_clusters,",the average silhouette_score is :", silhouette_avg)
#For n_clusters = 4 ,the average silhouette_score is : 0.2583364625565981

#obs in each cluster
obsInEachCluster_k4 = pd.DataFrame(kmeansEngageNumSolo4.labels_)
obsInEachCluster_k4.columns = ['label']
obsInEachCluster_k4_0 = len(obsInEachCluster_k4.loc[obsInEachCluster_k4['label']==0])
obsInEachCluster_k4_1 = len(obsInEachCluster_k4.loc[obsInEachCluster_k4['label']==1])
obsInEachCluster_k4_2 = len(obsInEachCluster_k4.loc[obsInEachCluster_k4['label']==2])
obsInEachCluster_k4_3 = len(obsInEachCluster_k4.loc[obsInEachCluster_k4['label']==3])
del obsInEachCluster_k4
obsInEachCluster_k4 = pd.DataFrame([obsInEachCluster_k4_0, obsInEachCluster_k4_1, obsInEachCluster_k4_2, obsInEachCluster_k4_3])
del obsInEachCluster_k4_0
del obsInEachCluster_k4_1
del obsInEachCluster_k4_2
del obsInEachCluster_k4_3

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>engageNumClustersKMeans

#.......KMeans (k=50) and Hierarchical (after)...........

n_clusters=50
kmeansEngageNum = KMeans(n_clusters=n_clusters, 
                random_state=0,
                n_init = 30,
                max_iter=200).fit(engageNumVar_Norm)  
    
my_clusters_engageNum = kmeansEngageNum.cluster_centers_ 

my_clusters_engageNum = pd.DataFrame(kmeansEngageNum.cluster_centers_)


engageKMEANSNumVarLink = linkage(my_clusters_engageNum, method ='ward')
dendrogram(engageKMEANSNumVarLink, truncate_mode='lastp',  p=40, orientation='top', show_leaf_counts=True)


#...............(only) Hierarchical......................
engageNumVarLink = linkage(engageNumVar_Norm, method ='ward')
dendrogram(engageNumVarLink, truncate_mode='lastp',  p=40, orientation='top', show_leaf_counts=True)


hierclustengageBase = AgglomerativeClustering(n_clusters=3,
                                      affinity='euclidean',
                                      linkage='ward')
hierclustengage = hierclustengageBase.fit(engageNumVar_Norm)

#labels
hierclustengagelabels = pd.DataFrame(hierclustengage.labels_)
hierclustengagelabels.columns =  ['clust']

#put labels in engageNumVar ----> get engageClustered
engageClustered = engageNumVar.copy(deep=True)
engageClustered = pd.concat([engageClustered,hierclustengagelabels],axis=1)

#get cluster means
engageClusters = np.round(engageClustered.groupby(['clust']).mean(),decimals=2)




#----------
# RESUMO NUMERICAL VARIABLES
#----------
#From KMeans and Hierarchical, 3 methods were tried: 
#-KMeans with high K followed by hierarchical
#-Hierarchical only
#-Kmeans only
#--> Hierarchical revealed 3 clusters, but results were really bad
#--> KMeans with high k followed by hier. produced almost the same results as hierarchical alone
#--> KMeans alone revealed a bad elbow graph, with not so clear optimum number of clusters of 3 or 4
#    both number of clusters was tried, silhouette score was identical between them, and distribution of
#    observations for each cluster was satisfying in both cases.
#    Chosen number of clusters: 3. Produced the most interpretable and clear results

#
#
#
#
#
#
#
#-------------------------------------------------------
#                  Categorical Variables                  
#-------------------------------------------------------
#Given the random init (or any other init), it is not possible to replicate the same clustering solution
#For that, no loop will be built to evaluate silhouette scores. Instead, clustering solutions will be kept in variables(...)
#(...) and the best will be used

#------------------------------------------------------------------------
##>>>> With LivingArea
#......... 2 clusters ....................
n_clusters=2
# define the k-modes model
km2 = KModes(n_clusters=n_clusters, init='random', n_init=5, verbose=1)

# fit the clusters 
clusterskmodes2 = km2.fit_predict(engageCatVar)

silhouette_avg2 = silhouette_score(engageCatVar, km2.labels_)

#......... 3 clusters ....................
n_clusters=3
# define the k-modes model
km3 = KModes(n_clusters=n_clusters, init='random', n_init=5, verbose=1)

# fit the clusters 
clusterskmodes3 = km3.fit_predict(engageCatVar)

silhouette_avg3 = silhouette_score(engageCatVar, km3.labels_)


#......... 4 clusters ....................
n_clusters=4
# define the k-modes model
km4 = KModes(n_clusters=n_clusters, init='random', n_init=5, verbose=1)

# fit the clusters 
clusterskmodes4 = km4.fit_predict(engageCatVar)

silhouette_avg4 = silhouette_score(engageCatVar, km4.labels_)

print(silhouette_avg2)
print(silhouette_avg3)
print(silhouette_avg4)
#0.2373255618792776
#0.33670269505630585
#0.16630893399074934

KModesCentroids = pd.DataFrame(km3.cluster_centroids_, columns = ["Educ","LivingArea","Children"])
print(KModesCentroids)

KModesCentroids2 = pd.DataFrame(km2.cluster_centroids_, columns = ["Educ","LivingArea","Children"])
print(KModesCentroids2)

KModesCentroids4 = pd.DataFrame(km4.cluster_centroids_, columns = ["Educ","LivingArea","Children"])
print(KModesCentroids4)




#------------------------------------------------------------------------
##>>>> Without LivingArea

engageCatVarA = engageCatVar.drop(columns=['LivingArea'])

#......... 2 clusters ....................
n_clusters=2
# define the k-modes model
km2a = KModes(n_clusters=n_clusters, init='random', n_init=5, verbose=1)

# fit the clusters 
clusterskmodes2a = km2a.fit_predict(engageCatVarA)

silhouette_avg2a = silhouette_score(engageCatVarA, km2a.labels_)

#......... 3 clusters ....................
n_clusters=3
# define the k-modes model
km3a = KModes(n_clusters=n_clusters, init='random', n_init=5, verbose=1)

# fit the clusters 
clusterskmodes3a = km3a.fit_predict(engageCatVarA)

silhouette_avg3a = silhouette_score(engageCatVarA, km3a.labels_)


#......... 4 clusters ....................
n_clusters=4
# define the k-modes model
km4a = KModes(n_clusters=n_clusters, init='random', n_init=5, verbose=1)

# fit the clusters 
clusterskmodes4a = km4a.fit_predict(engageCatVarA)

silhouette_avg4a = silhouette_score(engageCatVarA, km4a.labels_)

print(silhouette_avg2a)
print(silhouette_avg3a)
print(silhouette_avg4a)
#0.39038562304700297
#0.6680004716683238
#0.6976724262029244

KModesCentroidsA = pd.DataFrame(km3a.cluster_centroids_, columns = ["Educ","Children"])
print(KModesCentroidsA)

KModesCentroids2A = pd.DataFrame(km2a.cluster_centroids_, columns = ["Educ","Children"])
print(KModesCentroids2A)

KModesCentroids4A = pd.DataFrame(km4a.cluster_centroids_, columns = ["Educ","Children"])
print(KModesCentroids4A)

#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>4 clusters - clusterskmodes4a

engageWithLabels= VarsEngage.copy(deep=True)
engageWithLabels["CategoricalClusters"]=clusterskmodes4a

#obs in each cluster
obsInEachClusterCat = engageWithLabels["CategoricalClusters"]
obsInEachClusterCat = pd.DataFrame(obsInEachClusterCat)
obsInEachClusterCat.columns = ['label']
obsInEachClusterCat_0 = len(obsInEachClusterCat.loc[obsInEachClusterCat['label']==0])
obsInEachClusterCat_1 = len(obsInEachClusterCat.loc[obsInEachClusterCat['label']==1])
obsInEachClusterCat_2 = len(obsInEachClusterCat.loc[obsInEachClusterCat['label']==2])
obsInEachClusterCat_3 = len(obsInEachClusterCat.loc[obsInEachClusterCat['label']==3])

del obsInEachClusterCat
obsInEachClusterCat = pd.DataFrame([obsInEachClusterCat_0, obsInEachClusterCat_1, obsInEachClusterCat_2, obsInEachClusterCat_3])
del obsInEachClusterCat_0
del obsInEachClusterCat_1
del obsInEachClusterCat_2
del obsInEachClusterCat_3
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
#>>Categorical
#obsInEachClusterCat - Nr of obs per cluster
#clusterskmodes4a - Labels
#KModesCentroids4A - Centroids
#silhouette_avg4a - Silhouette Score
#
#>>Numerical
#obsInEachCluster_k3 - Nr of obs per cluster
#engagenumlabels - Labels
#engageNumClustersKMeans - Centroids
#silhouette_avg_engagenum - Silhouette Score
