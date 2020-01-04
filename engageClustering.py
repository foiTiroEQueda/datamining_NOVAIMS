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
engageCatVar = df[['Educ', 'LivingArea', 'Children']].copy(deep=True)
engageNumVar = df[['YearsAsCustomer', 'AnnualSalary', 'CustMonVal']].copy(deep=True)
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
plt.plot(range(1, 11), wcss)
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
silhouette_avg = silhouette_score(engageNumVar_Norm, kmeansEngageNumSolo.labels_)
print("For n_clusters =", n_clusters,",the average silhouette_score is :", silhouette_avg)
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


