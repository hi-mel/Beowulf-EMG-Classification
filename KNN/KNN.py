import numpy as npy
import time
import math
import warnings
from collections import Counter



def closestNeighbours(distance, eDistances, label):
    for i in range(0,(len(eDistances))): #the length of the label would be the value of k
        if distance < (eDistances[i][0]):
            eDistances[i] = [distance,label]

def knnV1(dataset, newData , k):
    if len(dataset) >= k :
        print "K has to be less than the total voting groups"
    if len(dataset) % k == 0:
        print "K cannot be multiple of the total voting groups"
    eDistances = [] #EUCLIDIAN DISTANCES list for points with the predict value
    for label in dataset: #Datapoint is the set of 8 numbers, datset is the collection of those datapoints. List of Lists 
        for features in dataset[label]:
            euclidianDistance = npy.linalg.norm(npy.array(features)-npy.array(newData))#using numpy function to calculate
            eDistances.append([euclidianDistance, label])
    eDistances.sort()
    eDistances = eDistances[:k]
    #print eDistances
    votes = [i[1] for i in eDistance]
    voteResult = Counter(votes).most_common(1)[0][0]#taking the first list in the ranking  list, and inside ththat list the first eklement is the label that we care aobout
    return voteResult 



def knnV2(dataset, newData , k):
    if len(dataset) >= k :
        print "K has to be less than the total voting groups"
    if len(dataset) % k == 0:
        print "K cannot be multiple of the total voting groups"
    eDistances = [[999999,0],[999999,0],[999999,0]] #EUCLIDIAN DISTANCES list for points with the predict value
    while len(eDistances) != k: #sizing the distance array to be the number of k. Minimum value should be 3.
        eDistances.append([999999,0])
    #print eDistances
    for label in dataset: #Datapoint is the set of 8 numbers, datset is the collection of those datapoints. List of Lists 
        for features in dataset[label]:
            euclidianDistance = npy.linalg.norm(npy.array(features)-npy.array(newData))#using numpy function to calculate 
            closestNeighbours(euclidianDistance, eDistances, label) #only saving the k-numbers of closest distances
    #print eDistances
    votes = [i[1] for i in eDistances [:k]]
    voteResult = Counter(votes).most_common(2)[0][0]
    return voteResult


                                                
