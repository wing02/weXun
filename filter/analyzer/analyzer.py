import numpy as np
import matplotlib.pyplot as plt
import cPickle
import pdb

class Analyzer:
    def drawROC(self,results,flags):
        #pdb.set_trace()
        step=0.01
        rate=0
        TPRs=[]
        FPRs=[]
        for rate in np.linspace(0,1,101):
            TP=FP=TN=FN=0
            for result,flag in zip(results,flags):
                if result>rate and flag==1:
                    TP+=1
                elif result<=rate and flag==1:
                    FN+=1
                elif result>rate and flag==0:
                    FP+=1
                elif result<=rate and flag==0:
                    TN+=1
            #print (TP,TN,FP,FN)
            TPRs.append(float(TP)/(TP+FN))
            FPRs.append(float(FP)/(FP+TN))
        print ('Top 90 :',TPRs[90],FPRs[90])
        plt.plot(FPRs,TPRs)
        plt.grid()
        plt.show()

if __name__=='__main__':
    resultPath='filter/sexyImgFilter/data/result.pkl'
    results,flags=cPickle.load(open(resultPath))
    results=map(lambda x:x[1],results)
    analyzer=Analyzer()
    analyzer.drawROC(results,flags)
