import numpy as np
import matplotlib.pyplot as plt

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
	
def lineChart(meanList, highList):
	mean = meanList
	high = highList

	N = len(mean)
	ind = np.arange(N)

	fig, ax = plt.subplots()

	ax.plot(ind,mean,'-r',label='Mean')
	ax.plot(ind,high,'-b',label='Highest')
	ax.set_ylabel('Fitness')
	ax.set_xlabel('Generations')
	ax.set_title('Fitness by Generation')
	ax.legend(loc='upper right')
	plt.show()
