import numpy as np
import matplotlib.pyplot as plt

class Analyzer:
    def drawROC(self,results):
        step=0.01
        rate=0
        TPRs=[]
        FPRs=[]
        for rate in np.linspace(0,1,101):
            TP=FP=TN=FN=0
            for result in resutls:
                if result[0]>rate and result[1]==1:
                    TP+=1
                elif result[0]<=rate and result[1]==1:
                    FN+=1
                elif result[0]>rate and result[1]==0:
                    FP+=1
                elif result[0]<rate and result[1]==0:
                    TN+=1
            TPRs.append(float(TP)/(TP+FN))
            FPRs.append(float(FP)/(FP+TN))
        print ('Top 90 :',TPRs[90],FPRs[90])
        plt.plot(FPRs,TPRs)
        plt.show()

if __name__=='__main__':
    resultPath='data/result.pkl'
    results,flags=cPickele.load(open(resultPath))
    results=map(lambda x:x[1],results)
    analyzer=Analyzer()
    analyzer.drawROC((results,flags))
