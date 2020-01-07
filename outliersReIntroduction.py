#!/usr/bin/env python3
# -*- coding: utf-8 -*-


#https://towardsdatascience.com/decision-tree-algorithm-explained-83beb6e78ef4
#https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.train_test_split.html


#****************************LOB*********************************************#
LobWithLabels= VarsLob.copy(deep=True)
LobWithLabels['KMeans']=kmeans.labels_

#in order to avoid overfitting, number of rules should be low
le = preprocessing.LabelEncoder()

'''lob_labels = pd.DataFrame(kmeans.labels_)
lob_labels1=kmeans.labels_

LobWithLabels= VarsLob.copy(deep=True)
LobWithLabels["Labels"]=lob_labels1'''


X = LobWithLabels[['Motor Premium', 'Household Premium', 'Health Premium', 'Life Premium', 'Work Premium']]
y =  LobWithLabels[['KMeans']] # Target variable


#split data
X_train, X_test, y_train, y_test =  train_test_split(X,y,test_size = 0.3, random_state= 0)

'''feature scaling
from sklearn.preprocessing import StandardScaler
sc_X = StandardScaler()
X_train = sc_X.fit_transform(X_train)
X_test = sc_X.transform(X_test)'''

#fit the model
classifier = DecisionTreeClassifier(random_state=0, max_depth=3)
classifier = classifier.fit(X_train,y_train)

#prediction
y_pred = classifier.predict(X_test)
#Accuracy
print('Accuracy Score:', metrics.accuracy_score(y_test,y_pred)) #0.9577603143418467

#Confusion matrix
from sklearn.metrics import confusion_matrix
cm = confusion_matrix(y_test, y_pred)
#It means 130 observations have been classified as false. Considering the
#dimension of the db is not bad

#visualize the tree
from sklearn.tree import export_graphviz
from sklearn.externals.six import StringIO  
from IPython.display import Image  
import pydotplus
dot_data = StringIO()
export_graphviz(classifier, out_file=dot_data,  
                filled=True, rounded=True,
                special_characters=True,feature_names = ['Motor Premium', 'Household Premium', 'Health Premium', 'Life Premium', 'Work Premium'],#class_names=clf.classes_
                )
graph = pydotplus.graph_from_dot_data(dot_data.getvalue())  

graph.write_png('lob.png')
Image(graph.create_png())


#import the lob outliers 
outliersforpredictionlob = [houseOutliers, healthOutliers, lifeOutliers, workOutliers, motorOutliers ]

outliersforpredictionlob = pd.concat(outliersforpredictionlob)

outliersforpredictionlob = outliersforpredictionlob [['Motor Premium', 'Household Premium', 'Health Premium', 'Life Premium', 'Work Premium']]

# Classify these new elements
profile_outliers = classifier.predict(outliersforpredictionlob)
outliersforpredictionlob['Cluster'] = profile_outliers


#****************************ENGAGE NUM*********************************************#
EngageNumWithLabels= VarsEngage.copy(deep=True)
EngageNumWithLabels['KMeans']=kmeansEngageNumSolo.labels_


le = preprocessing.LabelEncoder()


X = EngageNumWithLabels[['AnnualSalary', 'CustMonVal']]
y =  EngageNumWithLabels[['KMeans']] # Target variable


#split data
X_train, X_test, y_train, y_test =  train_test_split(X,y,test_size = 0.3, random_state= 0)

'''feature scaling
from sklearn.preprocessing import StandardScaler
sc_X = StandardScaler()
X_train = sc_X.fit_transform(X_train)
X_test = sc_X.transform(X_test)'''

#fit the model
classifier1 = DecisionTreeClassifier(random_state=0, max_depth=3) 
classifier1 = classifier1.fit(X_train,y_train)

#prediction
y_pred = classifier1.predict(X_test)
#Accuracy
print('Accuracy Score:', metrics.accuracy_score(y_test,y_pred)) #Accuracy Score: 0.6067452521283563

#Confusion matrix
from sklearn.metrics import confusion_matrix
cm = confusion_matrix(y_test, y_pred)
#It means 372 observations have been classified as false. 

#visualize the tree
from sklearn.tree import export_graphviz
from sklearn.externals.six import StringIO  
from IPython.display import Image  
import pydotplus
dot_data = StringIO()
export_graphviz(classifier1, out_file=dot_data,  
                filled=True, rounded=True,
                special_characters=True,feature_names = [ 'AnnualSalary', 'CustMonVal'],#class_names=clf.classes_
                )
graph = pydotplus.graph_from_dot_data(dot_data.getvalue())  

graph.write_png('lob.png')
Image(graph.create_png())

#import the engage outliers
outliersforpredictionengage = [monthSalaryOutliers, CustMonValOutliers]

outliersforpredictionengage = pd.concat(outliersforpredictionengage)

outliersforpredictionengage = outliersforpredictionengage[[ 'MonthSalary', 'CustMonVal']]

outliersforpredictionengage = outliersforpredictionengage[['MonthSalary', 'CustMonVal']]

outliersforpredictionengage['AnnualSalary'] = outliersforpredictionengage['MonthSalary']*14
outliersforpredictionengage = outliersforpredictionengage.drop(columns=['MonthSalary'])

# Classify these new elements
profile_outliers1 = classifier1.predict(outliersforpredictionengage)
outliersforpredictionengage['Engage_Clusters'] = profile_outliers1










