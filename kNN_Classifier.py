import scipy
from matplotlib import pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import pandas as pd
import numpy as np
import numpy.matlib

def plotData(trainData, testData, classifiedTestLabels=None, pdf_name="plot.pdf", display_figure=True):
    colors = ["r", "g", "b", "m", "y"]
    fig = plt.figure()
    for i in range(1, 6):
        filteredTrain = trainData[trainData["TL"]==i]
        if classifiedTestLabels is not None:
            filteredTest = testData[classifiedTestLabels == i]
        else:
            filteredTest = testData[testData["TL"] == i]
        plt.scatter(filteredTest["x"], filteredTest["y"], c=colors[i - 1], marker="x")
        plt.scatter(filteredTrain["x"], filteredTrain["y"], c=colors[i - 1], marker="o")
    if display_figure:
        plt.show()
    pp = PdfPages(pdf_name)
    pp.savefig(fig)
    pp.close()

def kNN(trainData, testData, k=1, feedback_classification=False):
    pointArr = trainData.as_matrix(columns=trainData.columns[0:2])
    labelArr = trainData.as_matrix(columns=trainData.columns[2:]).astype(np.uint8)

    testArr = testData.as_matrix()
    results = np.zeros(testArr.shape[0])

    for i in range(0, testArr.shape[0]):
        #find the next point in the training set
        thisPt = testArr[i,:]
        # find the difference between each point in the test set and the point we are classifying
        distanceMat = pointArr - thisPt
        #square the x and y differences
        distanceMat = np.square(distanceMat)
        # add the difference in x and y value together
        # (no need to square this value, because we are looking at relative distances)
        distanceMat = np.sum(distanceMat, axis=1)
        #find the indices of the sorted list, so that we know which points are closest
        sort_indices = np.argsort(distanceMat)
        #sort the label array using these indices to find the top labels
        closestLabels = labelArr[sort_indices]
        closestLabels = closestLabels[0:k]
        #take the median of the top k results to find the class
        topResult = np.median(closestLabels)
        #store it in the array of other results
        results[i] = topResult
        if feedback_classification:
            pointArr = np.append(pointArr, thisPt.reshape(1,2), axis=0)
            labelArr = np.append(labelArr, topResult.reshape(1,1), axis=0)
    return results


data = pd.read_csv("knnDataSet.csv")
trainData = data[data["L"].notnull()]
testData = data[data["L"].isnull()]
plotData(trainData, testData, display_figure=False, pdf_name="GroundTruth.pdf")
newLabels = kNN(trainData[['x', 'y', 'L']], testData[['x', 'y']], k=1, feedback_classification=False)
plotData(trainData, testData, classifiedTestLabels=newLabels, pdf_name="K1.pdf", display_figure=False)
print (newLabels)