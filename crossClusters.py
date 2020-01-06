# -*- coding: utf-8 -*-

#-------------------------------------------------------
#                     LOB Guide                  
#-------------------------------------------------------
#
#obsInEachClusterLOB - Nr of obs per cluster
#lob_labels - Labels
#lobClusters - Centroids
#silhouette_avg_lob - Silhouette Score
#
#
#
#-------------------------------------------------------
#                   Engage Guide                  
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
#engage_num_withProfit - Centroids with Estimated Annual Profit (discarding acq. cost)



#********************************************************************************************************************************
#                    Engage Cross
#********************************************************************************************************************************
#Lifetime value = (annual profit from the customer) X (number of years that they are a customer) - (acquisition cost) 

df_clustered_agg_engage = df_clustered.drop(columns=['CID'])
df_clustered_agg_engage = df_clustered_agg_engage.drop(columns=['LOB_Clusters'])

#Not so trustworthy Profit
profit = engageNumClustersKMeans['CustMonVal']/engageNumClustersKMeans['YearsAsCustomer']
profit = pd.DataFrame(profit)
engage_num_withProfit = engageNumClustersKMeans.copy(deep=True)
engage_num_withProfit['profit'] = profit


#Numerical Clusters
#0 - Median Old, Lowest Salary, Highest Value >>>> Keepers
#1 - Oldest Customers, Median Salary, Low Value >>>> ReThink
#2 - Newest Customers, Highest Salary, Median Value >>>> HighPotential

#Categorical Clusters
#0 - No High Educ, No Children
#1 - High Educ, No Children
#2 - High Educ, Children
#3 - No High Educ, Children


#Absolute Values
df_engage_agg_0 = df_clustered_agg_engage.loc[df_clustered_agg_engage['EngageNumerical_Clusters']==0]
df_engage_agg_1 = df_clustered_agg_engage.loc[df_clustered_agg_engage['EngageNumerical_Clusters']==1]
df_engage_agg_2 = df_clustered_agg_engage.loc[df_clustered_agg_engage['EngageNumerical_Clusters']==2]

df_engage_agg_0 = df_engage_agg_0.drop(columns=['EngageNumerical_Clusters'])
df_engage_agg_1 = df_engage_agg_1.drop(columns=['EngageNumerical_Clusters'])
df_engage_agg_2 = df_engage_agg_2.drop(columns=['EngageNumerical_Clusters'])


#df_engage_agg_0
dfea0_0 = len(df_engage_agg_0.loc[df_engage_agg_0['EngageCategorical_Clusters']==0])
dfea0_1 = len(df_engage_agg_0.loc[df_engage_agg_0['EngageCategorical_Clusters']==1])
dfea0_2 = len(df_engage_agg_0.loc[df_engage_agg_0['EngageCategorical_Clusters']==2])
dfea0_3 = len(df_engage_agg_0.loc[df_engage_agg_0['EngageCategorical_Clusters']==3])
del df_engage_agg_0
df_engage_agg_0 = pd.DataFrame([dfea0_0, dfea0_1, dfea0_2, dfea0_3])
del dfea0_0
del dfea0_1
del dfea0_2
del dfea0_3
df_engage_agg_0.columns = ['NumClust0']

#df_engage_agg_1
dfea0_0 = len(df_engage_agg_1.loc[df_engage_agg_1['EngageCategorical_Clusters']==0])
dfea0_1 = len(df_engage_agg_1.loc[df_engage_agg_1['EngageCategorical_Clusters']==1])
dfea0_2 = len(df_engage_agg_1.loc[df_engage_agg_1['EngageCategorical_Clusters']==2])
dfea0_3 = len(df_engage_agg_1.loc[df_engage_agg_1['EngageCategorical_Clusters']==3])
del df_engage_agg_1
df_engage_agg_1 = pd.DataFrame([dfea0_0, dfea0_1, dfea0_2, dfea0_3])
del dfea0_0
del dfea0_1
del dfea0_2
del dfea0_3
df_engage_agg_1.columns = ['NumClust1']

#df_engage_agg_2
dfea0_0 = len(df_engage_agg_2.loc[df_engage_agg_2['EngageCategorical_Clusters']==0])
dfea0_1 = len(df_engage_agg_2.loc[df_engage_agg_2['EngageCategorical_Clusters']==1])
dfea0_2 = len(df_engage_agg_2.loc[df_engage_agg_2['EngageCategorical_Clusters']==2])
dfea0_3 = len(df_engage_agg_2.loc[df_engage_agg_2['EngageCategorical_Clusters']==3])
del df_engage_agg_2
df_engage_agg_2 = pd.DataFrame([dfea0_0, dfea0_1, dfea0_2, dfea0_3])
del dfea0_0
del dfea0_1
del dfea0_2
del dfea0_3
df_engage_agg_2.columns = ['NumClust2']

engageAbsolutes = pd.concat([df_engage_agg_0, df_engage_agg_1, df_engage_agg_2], axis=1)
engageFrequency = engageAbsolutes.copy(deep=True)
engageFrequency['NumClust0'] = engageFrequency['NumClust0']/2808
engageFrequency['NumClust1'] = engageFrequency['NumClust1']/3739
engageFrequency['NumClust2'] = engageFrequency['NumClust2']/3514

#>>>should not be crossed

#********************************************************************************************************************************
#                    Lob and Engage Cross
#********************************************************************************************************************************


#Work Bench [review this]
df_clustered = df.copy(deep=True)
print(len(df_clustered))
print(len(lob_labels))
print(len(clusterskmodes4))
print(len(engagenumlabels))


df_clustered['LOB_Clusters'] = lob_labels[[0]]
df_clustered['EngageCategorical_Clusters'] = pd.DataFrame(clusterskmodes4)[[0]]
df_clustered['EngageNumerical_Clusters'] = engagenumlabels[[0]]

df_clustered = df_clustered.drop(columns=['Motor Premium', 'Household Premium', 'Health Premium', 'Life Premium', 'Work Premium', 'Educ', 'LivingArea', 'Children', 'CustMonVal', 'AnnualSalary', 'YearsAsCustomer'])
df_clustered_agg = df_clustered.drop(columns=['CID'])
df_clustered_agg_0 = df_clustered_agg.loc[df_clustered_agg['LOB_Clusters']==0]
df_clustered_agg_1 = df_clustered_agg.loc[df_clustered_agg['LOB_Clusters']==1]
df_clustered_agg_2 = df_clustered_agg.loc[df_clustered_agg['LOB_Clusters']==2]

#------------------------------ Cross Lob And Numerical ---------------------------------
#df_clustered_agg_0
temp0 = len(df_clustered_agg_0.loc[df_clustered_agg_0['EngageNumerical_Clusters']==0])
temp1 = len(df_clustered_agg_0.loc[df_clustered_agg_0['EngageNumerical_Clusters']==1])
temp2 = len(df_clustered_agg_0.loc[df_clustered_agg_0['EngageNumerical_Clusters']==2])
del df_clustered_agg_0
df_clustered_agg_0 = pd.DataFrame([temp0, temp1, temp2])
del temp0
del temp1
del temp2
df_clustered_agg_0.columns = ['LOB0']

#df_clustered_agg_1
temp0 = len(df_clustered_agg_1.loc[df_clustered_agg_1['EngageNumerical_Clusters']==0])
temp1 = len(df_clustered_agg_1.loc[df_clustered_agg_1['EngageNumerical_Clusters']==1])
temp2 = len(df_clustered_agg_1.loc[df_clustered_agg_1['EngageNumerical_Clusters']==2])
del df_clustered_agg_1
df_clustered_agg_1 = pd.DataFrame([temp0, temp1, temp2])
del temp0
del temp1
del temp2
df_clustered_agg_1.columns = ['LOB1']

#df_clustered_agg_2
temp0 = len(df_clustered_agg_2.loc[df_clustered_agg_2['EngageNumerical_Clusters']==0])
temp1 = len(df_clustered_agg_2.loc[df_clustered_agg_2['EngageNumerical_Clusters']==1])
temp2 = len(df_clustered_agg_2.loc[df_clustered_agg_2['EngageNumerical_Clusters']==2])
del df_clustered_agg_2
df_clustered_agg_2 = pd.DataFrame([temp0, temp1, temp2])
del temp0
del temp1
del temp2
df_clustered_agg_2.columns = ['LOB2']

lobnumabsolutes = pd.concat([df_clustered_agg_0, df_clustered_agg_1, df_clustered_agg_2], axis=1)
lobnumfreq = lobnumabsolutes.copy(deep=True)

lobnumfreq['LOB0'] = lobnumfreq['LOB0']/4134
lobnumfreq['LOB1'] = lobnumfreq['LOB1']/4157
lobnumfreq['LOB2'] = lobnumfreq['LOB2']/1770


#------------------------------ Cross Lob And Categorical ---------------------------------
df_clustered_agg = df_clustered.drop(columns=['CID'])
df_clustered_agg_0 = df_clustered_agg.loc[df_clustered_agg['LOB_Clusters']==0]
df_clustered_agg_1 = df_clustered_agg.loc[df_clustered_agg['LOB_Clusters']==1]
df_clustered_agg_2 = df_clustered_agg.loc[df_clustered_agg['LOB_Clusters']==2]

#df_clustered_agg_0
temp0 = len(df_clustered_agg_0.loc[df_clustered_agg_0['EngageCategorical_Clusters']==0])
temp1 = len(df_clustered_agg_0.loc[df_clustered_agg_0['EngageCategorical_Clusters']==1])
temp2 = len(df_clustered_agg_0.loc[df_clustered_agg_0['EngageCategorical_Clusters']==2])
temp3 = len(df_clustered_agg_0.loc[df_clustered_agg_0['EngageCategorical_Clusters']==3])

del df_clustered_agg_0
df_clustered_agg_0 = pd.DataFrame([temp0, temp1, temp2, temp3])
del temp0
del temp1
del temp2
del temp3
df_clustered_agg_0.columns = ['LOB0']

#df_clustered_agg_1
temp0 = len(df_clustered_agg_1.loc[df_clustered_agg_1['EngageCategorical_Clusters']==0])
temp1 = len(df_clustered_agg_1.loc[df_clustered_agg_1['EngageCategorical_Clusters']==1])
temp2 = len(df_clustered_agg_1.loc[df_clustered_agg_1['EngageCategorical_Clusters']==2])
temp3 = len(df_clustered_agg_1.loc[df_clustered_agg_1['EngageCategorical_Clusters']==3])

del df_clustered_agg_1
df_clustered_agg_1 = pd.DataFrame([temp0, temp1, temp2, temp3])
del temp0
del temp1
del temp2
del temp3
df_clustered_agg_1.columns = ['LOB1']

#df_clustered_agg_2
temp0 = len(df_clustered_agg_2.loc[df_clustered_agg_2['EngageCategorical_Clusters']==0])
temp1 = len(df_clustered_agg_2.loc[df_clustered_agg_2['EngageCategorical_Clusters']==1])
temp2 = len(df_clustered_agg_2.loc[df_clustered_agg_2['EngageCategorical_Clusters']==2])
temp3 = len(df_clustered_agg_2.loc[df_clustered_agg_2['EngageCategorical_Clusters']==3])

del df_clustered_agg_2
df_clustered_agg_2 = pd.DataFrame([temp0, temp1, temp2, temp3])
del temp0
del temp1
del temp2
del temp3
df_clustered_agg_2.columns = ['LOB2']


lobcatabsolute = pd.concat([df_clustered_agg_0, df_clustered_agg_1, df_clustered_agg_2], axis=1)
lobcatfreq = lobcatabsolute.copy(deep=True)

lobcatfreq['LOB0'] = lobcatfreq['LOB0']/4134
lobcatfreq['LOB1'] = lobcatfreq['LOB1']/4157
lobcatfreq['LOB2'] = lobcatfreq['LOB2']/1770


#------------------ Max ----------------------
#Lob 0 - Num 1 => Motor - ReThink
#Lob 1 - Num 2 => Health - HighPotential
#Lob 2 - Num 0 => (Household + Life + Work) - Keepers

#Lob 0 - Cat 2 => Motor - High Educ, Children
#Lob 1 - Cat 0 => Health - No High Educ, No Children
#Lob 2 - Cat 1 => (Household + Life + Work) - High Educ, no Children

