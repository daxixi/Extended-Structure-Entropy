import numpy as np
import pandas as pd
import networkx as nx
import random
import time
import copy
import matplotlib.pyplot as plt

def draw_G(G):
    pos=nx.spring_layout(G)
    nx.draw(G,pos)
    labels = nx.get_edge_attributes(G,'weight')
    nx.draw_networkx_edge_labels(G,pos,edge_labels=labels)
    plt.axis('off')
    plt.show()
    
def calculate_entropy(G,MACTodevice,manufacturesTodevice,manulist,manufactures,manuTono):
    #calculate Entropy partited by manufactures
    manuNum=len(manufacturesTodevice)
    assert manuNum==len(manulist)
    outWeights=np.zeros(manuNum)
    inWeights=np.zeros(manuNum)
    outvolume=np.zeros(manuNum)
    involume=np.zeros(manuNum)
    graphvolume=G.size(weight='weight')
    print(graphvolume)
    commus=G.edges(data='weight')
    for s,d,w in commus:
        manus=manuTono[manufactures[MACTodevice[s]]]
        manud=manuTono[manufactures[MACTodevice[d]]]
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
        manuno=manuTono[manufactures[MACTodevice[n]]]
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

device=pd.read_csv('device.csv')
flows=pd.read_csv('16-09-24.csv')

deviceToMAC={}
MACTodevice={}
manufactures={}
usage={}
usageTodevice={}
manufacturesTodevice={}
usagelist=[]
manulist=[]
usageTono={}
manuTono={}
G=nx.DiGraph()

#readin necessary info
for i in range(device['List of Devices'].shape[0]):
    mac=device['MAC ADDRESS'][i]
    device_=device['List of Devices'][i]
    deviceToMAC[device_]=mac
    MACTodevice[mac]=device_
    G.add_node(mac,)
    manu=device['Manufacture'][i]
    use=device['Usage'][i]
    manufactures[device_]=manu
    usage[device_]=use
    if not use in usageTodevice:
        usageTodevice[use]=[device_]
        usagelist.append(use)
        usageTono[use]=len(usagelist)-1
    else:
        usageTodevice[use].append(device_)
    if not manu in manufacturesTodevice:
        manufacturesTodevice[manu]=[device_]
        manulist.append(manu)
        manuTono[manu]=len(manulist)-1
    else:
        manufacturesTodevice[manu].append(device_)
optional_attr={}
for node in G.nodes():
    optional_attr[node]={'manu':manufactures[MACTodevice[node]],'usage':usage[MACTodevice[node]]}
nx.set_node_attributes(G,optional_attr)

#for i in manufactures:
#    manufactures[i]=manulist[0]#random.choice(manulist)
#for i in usage:
#    usage[i]=usagelist[0]#random.choice(usagelist)

#add communications
for i in range(flows['Packet ID'].shape[0]):
    src=flows['eth.src'][i]
    dst=flows['eth.dst'][i]
    if (not src in MACTodevice) or (not dst in MACTodevice):
        continue
    times=flows['Size'][i]
    if G.has_edge(src,dst):
        G[src][dst]['weight']+=times
    else:
        G.add_edge(src,dst,weight=times)
assert G.number_of_nodes()==len(MACTodevice)

E,outvolume,involume,outWeights,inWeights=calculate_entropy(G,MACTodevice,manufacturesTodevice,
                                                            manulist,manufactures,manuTono)
print(E)
nx.write_gexf(G,'16-09-24.gexf')
#E=calculate_entropy(G,MACTodevice,usageTodevice,usagelist,usage,usageTono)
#print(E)

manuNum=len(manufacturesTodevice)
G_new=copy.deepcopy(G)
step=1000
#5000 is the cost
for c in range(5000):
    graphvolume=G_new.size(weight='weight')
    best=-1
    s=-1
    d=-1
    for i in range(manuNum):
        for j in range(i,manuNum):
            Xi=manufacturesTodevice[manulist[i]]
            Xj=manufacturesTodevice[manulist[j]]
            Xi=[deviceToMAC[x] for x in Xi]
            Xj=[deviceToMAC[x] for x in Xj]
            leastin=graphvolume
            leastout=graphvolume
            leastinlist=[]
            leastoutlist=[]
            for node in Xi+Xj:
                if G_new.in_degree(node)<leastin:
                    leastinlist=[node]
                    leastin=G_new.in_degree(node)
                elif G_new.in_degree(node)==leastin:
                    leastinlist.append(node)
                if G_new.out_degree(node)<leastout:
                    leastoutlist=[node]
                    leastout=G_new.out_degree(node)
                elif G_new.out_degree(node)==leastout:
                    leastoutlist.append(node)
            for u in Xi+Xj:
                for v in leastinlist:
                    if u==v:
                        continue
                    manu_u=manuTono[manufactures[MACTodevice[u]]]
                    manu_v=manuTono[manufactures[MACTodevice[v]]]
                    outWeights_=step*(manu_u==manu_v)+outWeights[manu_u]
                    inWeights_=step*(manu_u==manu_v)+inWeights[manu_v]
                    out_d=G_new.out_degree(u)
                    in_d=G_new.in_degree(v)
                    if outvolume[manu_u]==0 or out_d==0:
                        old=0
                    else:
                        old=out_d/outvolume[manu_u]*np.log2(out_d/outvolume[manu_u])
                    delta_out_1=-(out_d+step)/(outvolume[manu_u]+step)*np.log2((out_d+step)/(outvolume[manu_u]+step))+old
                    if involume[manu_v]==0 or in_d==0:
                        old=0
                    else:
                        old=in_d/involume[manu_v]*np.log2(in_d/involume[manu_v])
                    delta_in_1=-(in_d+step)/(involume[manu_v]+step)*np.log2((in_d+step)/(involume[manu_v]+step))+old
                    if outvolume[manu_u]==0:
                        old=0
                    else:
                        old=outWeights[manu_u]/graphvolume*np.log2(outvolume[manu_u]/graphvolume)
                    delta_out_2=-outWeights_/(graphvolume+step)*np.log2((outvolume[manu_u]+step)/(graphvolume+step))+old
                    if involume[manu_v]==0:
                        old=0
                    else:
                        old=inWeights[manu_v]/graphvolume*np.log2(involume[manu_v]/graphvolume)                          
                    delta_in_2= -inWeights_/(graphvolume+step)*np.log2((involume[manu_v]+step)/(graphvolume+step))+old
                    delta=delta_out_1+delta_in_1+delta_out_2+delta_in_2
                    if delta>best:
                        best=delta
                        s=u
                        d=v
                for v in leastoutlist:
                    if u==v:
                        continue
                    manu_u=manuTono[manufactures[MACTodevice[u]]]
                    manu_v=manuTono[manufactures[MACTodevice[v]]]
                    outWeights_=1*(manu_u==manu_v)+outWeights[manu_u]
                    inWeights_=1*(manu_u==manu_v)+inWeights[manu_v]
                    out_d=G_new.out_degree(u)
                    in_d=G_new.in_degree(v)
                    if outvolume[manu_u]==0 or out_d==0:
                        old=0
                    else:
                        old=out_d/outvolume[manu_u]*np.log2(out_d/outvolume[manu_u])
                    delta_out_1=-(out_d+step)/(outvolume[manu_u]+step)*np.log2((out_d+step)/(outvolume[manu_u]+step))+old
                    if involume[manu_v]==0 or in_d==0:
                        old=0
                    else:
                        old=in_d/involume[manu_v]*np.log2(in_d/involume[manu_v])
                    delta_in_1=-(in_d+step)/(involume[manu_v]+step)*np.log2((in_d+step)/(involume[manu_v]+step))+old
                    if outvolume[manu_u]==0:
                        old=0
                    else:
                        old=outWeights[manu_u]/graphvolume*np.log2(outvolume[manu_u]/graphvolume)
                    delta_out_2=-outWeights_/(graphvolume+step)*np.log2((outvolume[manu_u]+step)/(graphvolume+step))+old
                    if involume[manu_v]==0:
                        old=0
                    else:
                        old=inWeights[manu_v]/graphvolume*np.log2(involume[manu_v]/graphvolume)                          
                    delta_in_2= -inWeights_/(graphvolume+step)*np.log2((involume[manu_v]+step)/(graphvolume+step))+old
                    delta=delta_out_1+delta_in_1+delta_out_2+delta_in_2
                    if delta>best:
                        best=delta
                        s=v
                        d=u
    #print(best,s,d)
    if G_new.has_edge(s,d):
        G_new[s][d]['weight']+=step
    else:
        G_new.add_edge(s,d,weight=step)
    manu_s=manuTono[manufactures[MACTodevice[s]]]
    manu_d=manuTono[manufactures[MACTodevice[d]]]
    involume[manu_d]+=1
    outvolume[manu_s]+=1
    inWeights[manu_d]+=1*(manu_s==manu_d)
    outWeights[manu_s]+=1*(manu_s==manu_d)
E,outvolume,involume,outWeights,inWeights=calculate_entropy(G_new,MACTodevice,manufacturesTodevice,
                                                            manulist,manufactures,manuTono)
print(E)
nx.write_gexf(G_new,'new.gexf')

