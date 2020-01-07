# -*- coding: utf-8 -*-


import matplotlib
import squarify

#*************************************************************************
#                                Frequencies
#*************************************************************************

#LOB frequency
obsInEachClusterLOB[0]
obsInEachClusterLOB['ClusterName'] = ['Motor', 'Health', 'House + Life + Work']
fig = plt.gcf()
ax = fig.add_subplot()
fig.set_size_inches(12.5, 7.5)

squarify.plot(label=obsInEachClusterLOB['ClusterName'],sizes=obsInEachClusterLOB[0], color = ['#ab7946', '#785430', '#d3b291'], alpha=.6)
plt.title("Percentage of total customers for each LOB cluster",fontsize=10,fontweight="bold")

plt.axis('off')
plt.show()


#Engage Numerical frequency
obsInEachCluster_k3[0]
obsInEachCluster_k3['ClusterName'] = ['Keepers', 'Re-Think', 'High Potential']
fig = plt.gcf()
ax = fig.add_subplot()
fig.set_size_inches(12.5, 7.5)

squarify.plot(label=obsInEachCluster_k3['ClusterName'],sizes=obsInEachCluster_k3[0], color = ['#d3b291', '#785430', '#ab7946'], alpha=.6)
plt.title("Percentage of total customers for each Engage Numerical cluster",fontsize=10,fontweight="bold")

plt.axis('off')
plt.show()


#Engage Categorical frequency
obsInEachClusterCat[0]
obsInEachClusterCat['ClusterName'] = ['No High Education, No Children', 'High Education, No Children', 'High Education, Children', 'No High Education, Children']


fig = plt.gcf()
ax = fig.add_subplot()
fig.set_size_inches(12.5, 7.5)

squarify.plot(label=obsInEachClusterCat['ClusterName'],sizes=obsInEachClusterCat[0], color = ['#785430', '#d3b291', '#ab7946', '#573d23'], alpha=.6)
plt.title("Percentage of total customers for each Engage Categorical cluster",fontsize=10,fontweight="bold")

plt.axis('off')
plt.show()

#*************************************************************************
#                                Mono vs Multi Policy
#*************************************************************************
motorPonly = df.loc[df['Motor Premium']!=0]
motorPonly = motorPonly.loc[motorPonly['Household Premium']==0]
motorPonly = motorPonly.loc[motorPonly['Life Premium']==0]
motorPonly = motorPonly.loc[motorPonly['Work Premium']==0]
motorPonly = motorPonly.loc[motorPonly['Health Premium']==0]
len(motorPonly)

housePonly = df.loc[df['Household Premium']!=0]
housePonly = housePonly.loc[housePonly['Motor Premium']==0]
housePonly = housePonly.loc[housePonly['Life Premium']==0]
housePonly = housePonly.loc[housePonly['Work Premium']==0]
housePonly = housePonly.loc[housePonly['Health Premium']==0]
len(housePonly)

lifePonly = df.loc[df['Life Premium']!=0]
lifePonly = lifePonly.loc[lifePonly['Motor Premium']==0]
lifePonly = lifePonly.loc[lifePonly['Household Premium']==0]
lifePonly = lifePonly.loc[lifePonly['Work Premium']==0]
lifePonly = lifePonly.loc[lifePonly['Health Premium']==0]
len(lifePonly)

workPonly = df.loc[df['Work Premium']!=0]
workPonly = workPonly.loc[workPonly['Motor Premium']==0]
workPonly = workPonly.loc[workPonly['Life Premium']==0]
workPonly = workPonly.loc[workPonly['Household Premium']==0]
workPonly = workPonly.loc[workPonly['Health Premium']==0]
len(workPonly)

healthPonly = df.loc[df['Health Premium']!=0]
healthPonly = healthPonly.loc[healthPonly['Motor Premium']==0]
healthPonly = healthPonly.loc[healthPonly['Life Premium']==0]
healthPonly = healthPonly.loc[healthPonly['Household Premium']==0]
healthPonly = healthPonly.loc[healthPonly['Work Premium']==0]
len(healthPonly)

#*************************************************************************
#                                House and no Life
#*************************************************************************
houseNoLife = df.loc[df['Household Premium']!=0]
houseNoLife = houseNoLife.loc[houseNoLife['Life Premium']==0]
len(houseNoLife)
len(houseNoLife)/len(df)*100

#*************************************************************************
#                                Children and no Life
#*************************************************************************
childrenNoLife = df.loc[df['Children']==True]
childrenNoLife = childrenNoLife.loc[childrenNoLife['Life Premium']==0]
len(childrenNoLife)
len(childrenNoLife)/len(df)*100

#*************************************************************************
#                                Children and no Health
#*************************************************************************
childrenNoHealth = df.loc[df['Children']==True]
childrenNoHealth = childrenNoHealth.loc[childrenNoHealth['Health Premium']==0]
len(childrenNoHealth)
len(childrenNoHealth)/len(df)*100

#*************************************************************************
#                           Total Premiums by Category
#*************************************************************************
totalPremiumMotor = df['Motor Premium'].sum()
totalPremiumHouse = df['Household Premium'].sum()
totalPremiumHealth = df['Health Premium'].sum()
totalPremiumLife = df['Life Premium'].sum()
totalPremiumWork = df['Work Premium'].sum()
print(totalPremiumMotor)
print(totalPremiumHouse)
print(totalPremiumHealth)
print(totalPremiumLife)
print(totalPremiumWork)
totalPremiumsAll = totalPremiumMotor + totalPremiumHouse + totalPremiumHealth + totalPremiumLife + totalPremiumWork
totalPremiumMotorPerc = totalPremiumMotor/totalPremiumsAll
totalPremiumHousePerc = totalPremiumHouse/totalPremiumsAll
totalPremiumHealthPerc = totalPremiumHealth/totalPremiumsAll
totalPremiumLifePerc = totalPremiumLife/totalPremiumsAll
totalPremiumWorkPerc = totalPremiumWork/totalPremiumsAll

print(totalPremiumMotorPerc)
print(totalPremiumHousePerc)
print(totalPremiumHealthPerc)
print(totalPremiumLifePerc)
print(totalPremiumWorkPerc)
totalPremiumsAll
