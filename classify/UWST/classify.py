import numpy as np
import pandas as pd
import networkx as nx
import random
import time
import copy
import matplotlib.pyplot as plt
import scipy
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LinearRegression
from xgboost import XGBClassifier
from infomap import Infomap


manuTolabel={'SmartThings': 0, 'Amazone': 1, 'Netatmo': 2, 'TP-Link': 3, 'Samsung': 4, 'Google': 5, 'Insteon': 6, 'Withings': 7, 'Belkin': 8, 'Apple': 9, 'Nest': 10, 'Blipcare': 11, 'Lifx': 12, 'Triby': 13, 'Pixstar': 14, 'HP': 15}
#usageTolabel
manuTolabel={'Computer': 0, 'Others': 1, 'Monitor': 2}
MACTono={'d0:52:a8:00:67:5e': 0, '44:65:0d:56:cc:d3': 1, '70:ee:50:18:34:43': 2, 'f4:f2:6d:93:51:f1': 3, '00:16:6c:ab:6b:88': 4, '30:8c:fb:2f:e4:b2': 5, '00:62:6e:51:27:2e': 6, 'e8:ab:fa:19:de:4f': 7, '00:24:e4:11:18:a8': 8, 'ec:1a:59:79:f4:89': 9, '50:c7:bf:00:56:39': 10, '74:c6:3b:29:d7:1d': 11, 'ec:1a:59:83:28:11': 12, '18:b4:30:25:be:e4': 13, '70:ee:50:03:b8:ac': 14, '00:24:e4:1b:6f:96': 15, '74:6a:89:00:2e:25': 16, '00:24:e4:20:28:c6': 17, 'd0:73:d5:01:83:08': 18, '18:b7:9e:02:20:44': 19, 'e0:76:d0:33:bb:85': 20, '70:5a:0f:e4:9b:c0': 21, '08:21:ef:3b:fc:e3': 22, '30:8c:fb:b6:ea:45': 23, '40:f3:08:ff:1e:da': 24, '74:2f:68:81:69:42': 25, 'ac:bc:32:d4:6f:2f': 26, 'b4:ce:f6:a7:a3:c2': 27, 'd0:a6:37:df:a1:e1': 28, 'f4:5c:89:93:cc:85': 29, '14:cc:20:51:33:ea': 30}
noToMAC={v:k for k,v in MACTono.items()}
def shuffle(data,label):    
    index = [i for i in range(len(data))] 
    random.shuffle(index) 
    data = data[index]
    label = label[index] 
    return data,label

def predict(x):
    return np.round(cls.predict(x))
def getA(name):
    G=nx.read_gexf(name)
    A=nx.adjacency_matrix(G)
    A=np.array(A.toarray())
    A=A/np.linalg.norm(A,ord=2)
    labels=[]
    ct=0
    for n in G.nodes(data=True):
        manu=n[1]['usage']
        labels.append(manuTolabel[manu])
    im=Infomap('--directed')
    for edge in G.edges(data='weight'):
        s=MACTono[edge[0]]
        t=MACTono[edge[1]]
        im.add_link(s,t,edge[2])
    im.run()
    temp=np.zeros(len(labels))
    for node_id,module_id in im.modules:
        temp[node_id]=module_id
    y=[]
    for node in G.nodes():
        y.append(temp[MACTono[node]])
    return np.array(y),np.array(labels)

def matchpredict(y,labels):
    match=np.zeros((int(max(y))+1,max(labels)+1))
    for yy,ll in zip(y,labels):
        match[int(yy)][ll]+=1
    predicttotrue=np.zeros(match.shape[0])
    for i in range(predicttotrue.shape[0]):
        predicttotrue[i]=np.argmax(match[i])
    y_=np.zeros(y.shape[0])
    for i,yy in enumerate(y):
        y_[i]=predicttotrue[int(yy)]
    return y_

def calculate(y,labels):
    ct=0
    rt=0
    for i in range(labels.shape[0]-1):
        for j in range(i+1,labels.shape[0]):
            if (not labels[i]==labels[j])==(y[i]==y[j]):
                rt+=1
            ct+=1
    return rt/ct

y,labels=getA('16-09-24.gexf')
y=matchpredict(y,labels)
print(calculate(y,labels))
print(y)
y,labels=getA('new.gexf')
y=matchpredict(y,labels)
print(calculate(y,labels))
print(y)
