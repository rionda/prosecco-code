import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib    
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import math
import json
import datetime
import matplotlib.dates as mdates
import os.path
import pickle

def second_formatter(value, tick_number):
    return int(value / 1000.0)

sns.set(context='paper', style={'axes.axisbelow': True,
    'axes.edgecolor': '.8',
    'axes.facecolor': 'white',
    'axes.grid': True,
    'axes.labelcolor': '.15',
    'axes.linewidth': 0.5,
    'figure.facecolor': 'white',
    'font.family': [u'sans-serif'],
    'font.sans-serif': [u'Abel'],
    'font.weight' : u'light',
    'grid.color': '.8',
    'grid.linestyle': u'-',
    'image.cmap': u'Greys',
    'legend.frameon': False,
    'legend.numpoints': 1,
    'legend.scatterpoints': 1,
    'lines.solid_capstyle': u'butt',
    'text.color': '.15',
    'xtick.color': '.15',
    'xtick.direction': u'out',
    'xtick.major.size': 0.0,
    'xtick.minor.size': 0.0,
    'ytick.color': '.15',
    'ytick.direction': u'out',
    'ytick.major.size': 0.0,
    'ytick.minor.size': 0.0}, font_scale = 1.3)

flatui = ['#28aad5', '#b24d94', '#38ae97' ,'#ec7545']

runtimes = {}
with open('runtimes.pickle', 'rb') as handle:
    runtimes = pickle.load(handle)
print(runtimes)


prosecco_means = []
prosecco_std = []
prefixspan_means = []
prefixspan_std = []

datasets = ['BMS-0.03', 'KORSARAK-0.05', 'SIGN-0.40', 'BIBLE-0.40', 'FIFA-0.30']
prefixspan = runtimes['prefixspan']
prosseco = runtimes['prosecco']
for ds in prefixspan:
    if ds in datasets:

        r_ps = prefixspan[ds]
        
        prefixspan_means.append(np.array(r_ps).mean())
        b = np.array(r_ps).std() / math.sqrt(len(r_ps))
        prefixspan_std.append(1.96 * b)

        r_pr = prosseco[ds]
        prosecco_means.append(np.array(r_pr).mean())    
        b = np.array(r_pr).std() / math.sqrt(len(r_pr))
        prosecco_std.append(1.96 * b)

print()
print(len(prosecco_std), len(prefixspan_std))
print(datasets)


ind = np.arange(len(prosecco_means))  # the x locations for the groups
width = 0.35  # the width of the bars

f, (ax) = plt.subplots(1, 1, sharey=False, figsize=(5, 3.5)) 

rects1 = ax.bar(ind - width/2, prosecco_means, width, yerr=prosecco_std,
                color=flatui[0], label='ProSecCo')
rects2 = ax.bar(ind + width/2, prefixspan_means, width, yerr=prefixspan_std,
                color=flatui[1], label='PrefixSpan', hatch='//')

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('Runtime (s)')
ax.set_xticks(ind)
ax.set_xticklabels(datasets)
locs, labels = plt.xticks()
plt.setp(labels, rotation=45)    
ax.legend(loc='upper right')
ax.yaxis.set_major_formatter(plt.FuncFormatter(second_formatter))
ax.legend()
ax.set_ylim([0.0, 500000])

def autolabel(rects, xpos='center'):
    """
    Attach a text label above each bar in *rects*, displaying its height.

    *xpos* indicates which side to place the text w.r.t. the center of
    the bar. It can be one of the following {'center', 'right', 'left'}.
    """

    xpos = xpos.lower()  # normalize the case of the parameter
    ha = {'center': 'center', 'right': 'left', 'left': 'right'}
    offset = {'center': 0.5, 'right': 0.57, 'left': 0.43}  # x_txt = x + w*off

    newlist = sorted(rects, key=lambda x: x.get_x() , reverse=False)


    i = 0
    for rect in newlist:
        print(rect.get_x() )
        height = rect.get_height()
        text = np.mean(prosseco[datasets[i]]) / np.mean(prefixspan[datasets[i]])
        ax.text(rect.get_x() + rect.get_width()*offset[xpos], 1.05*height,
                '{:.2f}'.format(text) + 'x', ha=ha[xpos], va='bottom', fontsize=12)
        i += 1


autolabel(rects1, "center")

f.savefig('../fig/' + 'runtime.pdf', bbox_inches='tight')
plt.tight_layout()
plt.show()