# -*- coding: utf-8 -*-
#*****************************************************************************
#************************************* 0 *************************************
#*****************************************************************************


#******************************** 0.1 IMPORTS ********************************

import sqlite3
import pandas as pd
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
import seaborn as sb
from matplotlib import pyplot as plt
import plotly.graph_objects as go
from plotly.offline import plot
import matplotlib.cm as cm
from sklearn.cluster import KMeans
import pylab as pl
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.metrics import silhouette_samples, silhouette_score
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import AgglomerativeClustering
import scipy.cluster.hierarchy as sch
from scipy.cluster.hierarchy import dendrogram, linkage
from kmodes.kmodes import KModes





pd.set_option('display.max_columns', 500)


#**************************** 0.2 DATA EXTRACTION ****************************
#conection to the db
#replace the string value "my_path" to the path of the db in your pc
my_path = 'C:/IMS_Mestrado/1oAno_1oSemestre/DataMining/Projeto/Materials/insurance.db'
con = sqlite3.connect(my_path)
cursor = con.cursor()

#list tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
print(cursor.fetchall())
#tables LOB and Engage

#create dfs from db tables
lob = pd.read_sql_query("""select * from LOB""",con)
engage = pd.read_sql_query("""select * from Engage""",con)
con.close()

#get to know columns
#print(lob.columns)
#print(engage.columns)

totalcols = pd.concat([pd.DataFrame(lob.columns), pd.DataFrame(engage.columns)])
totalcols = totalcols.reset_index()
totalcols = totalcols[0]
totalcols = totalcols.drop_duplicates()
totalcols = totalcols.reset_index()
totalcols = totalcols[0]
totalcols
#index, Customer Identity, Premiums in LOB: Motor, Premiums in LOB: Household
#Premiums in LOB: Health, Premiums in LOB:  Life, Premiums in LOB: Work Compensations
#First Policy´s Year, Brithday Year, Educational Degree,  Gross Monthly Salary
#Geographic Living Area, Has Children (Y=1), Customer Monetary Value, Claims Rate
#>>Matches project description

