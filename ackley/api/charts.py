import numpy as np
import matplotlib
matplotlib.use('Agg')
import collections
import matplotlib.pyplot as plt
import io
import base64

def plotFitnes(listMean,listHigh):
    #len(mean/high) = quantidade de gerações
    mean = listMean
    high = listHigh

    N = len(mean)
    ind = np.arange(N)
    width = 0.35
    fig, ax = plt.subplots()
    rects1 = ax.bar(ind, mean, width, color='r')
    rects2 = ax.bar(ind + width, high, width, color='y')

    # add some text for labels, title and axes ticks
    ax.set_ylabel('Fitness')
    ax.set_title('Scores by Generation')
    ax.set_xticks(ind + width / 2)

    #lebels para cada geracao
    labels=[]
    for x in range(N):
        labels.append(x+1)

    #ax.set_xticklabels(('G1', 'G2', 'G3', 'G4', 'G5'))
    ax.set_xticklabels(labels)
    ax.legend((rects1[0], rects2[0]), ('Mean', 'Highest'))

    def autolabel(rects):
        #Attach a text label above each bar displaying its height
        for rect in rects:
            height = rect.get_height()
            ax.text(rect.get_x() + rect.get_width()/2., 1.05*height,
                    '%d' % int(height),
                    ha='center', va='bottom')

    autolabel(rects1)
    autolabel(rects2)

    plt.show()


def scatter_chart(highers_list, xlabel, ylabel):
    plt.gca().set_color_cycle(['red', 'green', 'blue', 'yellow'])
    count = collections.Counter(highers_list)
    points = np.array(list(count.keys()))
    incidence = np.array(list(count.values()))
    sizes = incidence**2
    plt.scatter(points, incidence, s=sizes, marker='o')
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    higher = base64.b64encode(buf.getvalue()).decode()
    plt.gcf().clear()
    return higher


def line_chart(points_list, legend, xlabel, ylabel):
    points = np.arange(len(points_list))
    plt.gca().set_color_cycle(['red', 'green', 'blue', 'yellow'])

    points_list = [round(p, 5) for p in points_list]
    plt.plot(points, points_list)
    plt.legend([legend], loc='upper left')
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    chart = base64.b64encode(buf.getvalue()).decode()
    plt.gcf().clear()

    return chart

