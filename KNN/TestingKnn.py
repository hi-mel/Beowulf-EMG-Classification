import pandas as pd
import KNN
import random
import time 

ds = pd.read_csv("breast-cancer-wisconsin.data.txt")#ds stands for dataset
ds.replace('?',-99999,inplace = True)
ds.drop(['id'],1,inplace = True)
full_data = ds.astype(float).values.tolist()
random.shuffle(full_data)#if the same data are used everytime ,the results will be the same everytime


#print(df.head())
 

test_size = 0.2
train_set = {2:[], 4:[]}
test_set = {2:[], 4:[]}
train_data = full_data[:-int(test_size*len(full_data))]
test_data = full_data[-int(test_size*len(full_data)):]

for i in train_data:
    train_set[i[-1]].append(i[:-1])

for i in test_data:
    test_set[i[-1]].append(i[:-1])

correct = 0
total = 0

startTime = time.time()
for group in test_set:
    for data in test_set[group]:
        vote = KNN.knnV2(train_set, data, 3)
        #print (vote)
        if group == vote:
            correct += 1
        total += 1
print (correct, total)
print ("AccuracyV2", float(correct)/total)
print(time.time() - startTime)

correct = 0
total = 0

startTime = time.time()
for group in test_set:
    for data in test_set[group]:
        vote = KNN.knnV2(train_set, data, 3)
        #print (vote)
        if group == vote:
            correct += 1
        total += 1
print (correct, total)
print ("AccuracyV1", float(correct)/total)
print (time.time() - startTime)
