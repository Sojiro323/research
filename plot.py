import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns

def image(score, ks, name, querys, title, xlabel,ylabel):

    colorlist = ["r", "g", "b", "c", "m", "#ff7f00", "k", "w"]

    sns.set_style("darkgrid")
    left = np.array(ks)

    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)

    for i, q in enumerate(querys):
        height = np.array(score[q])
        ax.plot(left, height, label=q, color=colorlist[i])

    ax.legend(loc='best')
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.savefig(name)
