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
    
    
def plotlyOnTheGo(rx, ry):
    x = rx
    y = ry
    
    fig = go.Figure(data=[go.Bar(x=x, y=y, text=y.round(decimals=4),
                textposition='outside')])
    fig.update_traces(marker_color='rgb(171,121,70)', marker_line_color='rgb(171,121,70)',
                      marker_line_width=1.5, opacity=0.6)
    fig.update_layout(plot_bgcolor='rgb(255,255,255)', xaxis=dict(
            tickmode='linear'))
    plot(fig)
