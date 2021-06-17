# Extend Structure Entropy of Graph to Weighted and Directed Graph under communites
The detailed information can be reffered to the [report](https://github.com/daxixi/Extended-Structure-Entropy/blob/main/report.pdf)

The code is an API of calculating the purposed entropy of a networkx graph
## Dataset
Three dataset is selected, [UNSW](https://iotanalytics.unsw.edu.au/iottraces.html), [Eucore email](http://snap.stanford.edu/data/email-Eu-core.html) and [facebook](http://snap.stanford.edu/data/ego-Facebook.html) dataset, the detailed information can be reffered to the report.

For each dataset, the example format of input file is given in the decption folder under each dataset
## Directed and weighted structural entropy
The definiton of the DWSE is in the report and entropy.py is an API to evaluate the DWSE of a given .gexf format file
## Deceptor
The decption folder implements the decptor algorithms introduced, due the variety of dataset. Each deceptor has silightly different implementation. 

In the file, we can change the step and costs to constructor different deceptors
## Classify
Use infomap algorithm to evaluate the performace of deceptor

## Announcement
This is an open souce project built in SJTU course EE447. Regarded as the course project, this repo has been finished. While, in the future further it will be further improved
