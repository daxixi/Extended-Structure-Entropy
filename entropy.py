import numpy as np
import pandas as pd
import networkx as nx
import random
import time
import copy
import matplotlib.pyplot as plt

'''
calculate the structure entropy for graph with communities:
support for directed graphs
input:
    G:networkx graph with weights-->edges, and manu attributes -->nodes
    manuNum: the number of communities
    manu means the number of clusters
output：
    E:structure entropy
    outvolume:
    involume: V_j in equation
    outWeights"
    inWeights: g_j in equation
'''
def calculate_entropy(G,manuNum=7):
    #calculate Entropy partited by manufactures
    outWeights=np.zeros(manuNum)
    inWeights=np.zeros(manuNum)
    outvolume=np.zeros(manuNum)
    involume=np.zeros(manuNum)
    graphvolume=G.size(weight='weight')
    print(graphvolume)
    commus=G.edges(data='weight')
    for s,d,w in commus:
        manus=G.nodes[s]['manu']
        manud=G.nodes[d]['manu']
        involume[manud]+=w
        outvolume[manus]+=w
        if not manus==manud:
            inWeights[manud]+=w
            outWeights[manus]+=w
    H_in_2=np.zeros(manuNum)
    H_out_2=np.zeros(manuNum)
    for i in range(manuNum):
        if outvolume[i]==0:
            H_out_2[i]=0
        else:
            H_out_2[i]=-outWeights[i]/graphvolume*np.log2(outvolume[i]/graphvolume)
        if involume[i]==0:
            H_in_2[i]=0
        else:
            H_in_2[i]=-inWeights[i]/graphvolume*np.log2(involume[i]/graphvolume)
    H_in_1=np.zeros(manuNum)
    H_out_1=np.zeros(manuNum)
    for n in G.nodes():
        manuno=G.nodes[n]['manu']
        ind=G.in_degree(n)
        outd=G.out_degree(n)
        if not involume[manuno]==0 and not ind==0:
            H_in_1[manuno]+=ind/involume[manuno]*np.log2(ind/involume[manuno])
        if not outvolume[manuno]==0 and not outd==0:
            H_out_1[manuno]+=outd/outvolume[manuno]*np.log2(outd/outvolume[manuno])
    H_in_1=-np.multiply(involume/graphvolume,H_in_1)
    H_out_1=-np.multiply(outvolume/graphvolume,H_out_1)
    H_in=H_in_1+H_in_2
    H_out=H_out_1+H_out_2
    E=np.sum(H_in)+np.sum(H_out)
    return E,outvolume,involume,outWeights,inWeights

def example():
    G=nx.read_gexf('new.gexf')
    E,outvolume,involume,outWeights,inWeights=calculate_entropy(G,7)
    print('WDC SE:',E)
