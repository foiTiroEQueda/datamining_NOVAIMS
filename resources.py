# -*- coding: utf-8 -*-

def corrMatrix(dataframe):
    corr = dataframe.corr()
    mask = np.zeros_like(corr, dtype=np.bool)
    mask[np.triu_indices_from(mask)]= True
    f, ax = plt.subplots(figsize=(11, 15)) 
    heatmap = sb.heatmap(corr, mask = mask , square = True, linewidths = .5,
                          cmap = "coolwarm", cbar_kws = {'shrink': .4, "ticks" : [-1, -0.5, 0, 0.5, 1]}, 
                          vmin = -1, vmax = 1, 
                          annot = True, annot_kws = {"size": 12})

