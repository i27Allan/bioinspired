import numpy as np
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


def line_chart(means_list, highers_list, to_django=False):
    points = np.arange(len(means_list))
    plt.gca().set_color_cycle(['red', 'green', 'blue', 'yellow'])

    plt.plot(points, means_list)
    plt.legend(['Mean'], loc='upper left')
    plt.xlabel('# mutation')
    plt.ylabel('fitness')
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    mean = base64.b64encode(buf.getvalue()).decode()
    plt.gcf().clear()

    plt.plot(points, highers_list)
    plt.legend(['Highest'], loc='upper left')
    plt.xlabel('# mutation')
    plt.ylabel('fitness')
    buf2 = io.BytesIO()
    plt.savefig(buf2, format='png')
    highest = base64.b64encode(buf2.getvalue()).decode()
    plt.gcf().clear()

    return mean, highest

