# -*- coding: utf-8 -*-

#<garbage, don't use>

#Self Organizing Maps
   
import sqlite3
import os
import pandas as pd
import numpy as np
import seaborn as sb
import matplotlib
from matplotlib import pyplot as plt

import matplotlib
import math
import glob

import urllib3
import joblib
import random

from sompy.sompy import SOMFactory
from sompy.visualization.plot_tools import plot_hex_map
import logging



lob_som= df.loc[:,['Motor Premium',
       'Household Premium', 'Health Premium',
       'Life Premium', 'Work Premium']].reindex()

from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()


lob_norm = scaler.fit_transform(lob_som)
lob_norm = pd.DataFrame(lob_norm, columns = lob_som.columns)

X = lob_norm.values


names = ['Motor Premium',
       'Household Premium', 'Health Premium',
       'Life Premium', 'Work Premium']
sm = SOMFactory().build(data = X,
               mapsize=(10,10),
               normalization = 'var',
               initialization='pca',#'random', 'pca'
               component_names=names,
               lattice='hexa',#'rect','hexa'
               training = 'seq')#'seq','batch'



sm.train(n_job=4,
         verbose='info',
         train_rough_len=30,
         train_finetune_len=100)

final_clusters = pd.DataFrame(sm._data, columns = ['Motor Premium',
                                                   'Household Premium', 
                                                   'Health Premium',
                                                   'Life Premium',
                                                   'Work Premium'])
my_labels = pd.DataFrame(sm._bmu[0])
    
final_clusters = pd.concat([final_clusters,my_labels], axis = 1)

final_clusters.columns =['Motor Premium',
                         'Household Premium', 
                         'Health Premium',
                         'Life Premium',
                         'Work Premium','Lables']


from sompy.visualization.mapview import View2D
view2D  = View2D(10,10,"", text_size=7)
view2D.show(sm, col_sz=5, what = 'codebook',)#which_dim="all", denormalize=True)
plt.show()


from sompy.visualization.hitmap import HitMapView
sm.cluster(3)
hits  = HitMapView(10,10,"Clustering",text_size=7)
a=hits.show(sm, labelsize=12)
