print("Global_Mouse_Control")
import math
import pdb
import os
import datetime
import csv
import numpy as np
import pigpio
from linear_classifier import LinearClassifier
start = datetime.datetime.now()

this_model = LinearClassifier(9,3)
gpio = pigpio.pi()

label = 'flex'
# rest label = 0
# grip label = 1
# flex label = 2

csvfile = open('EMG_Training_Data/emg_training_data_'+label+'_'+str(start)+'.csv','w+')
f = csv.writer(csvfile)

def onUnlock():
	print("onUnlock")
	myo.rotSetCenter()
	myo.unlock("hold")
	
def onPoseEdge(pose, edge):
	print("onPoseEdge")
	if (pose == 'fist') and (edge == "on"): 
		myo.mouse("left","click","")
	if (pose == 'fingersSpread') and (edge == "on"):
		myo.mouse("right","click","")

def print_emg(emg):
        for datum in emg:
                print('[' + '*'*int(datum/100))

def eval_label():
        if (label == 'rest'):
                return 0
        if (label == 'grip'):
                return 1
        if (label == 'flex'):
                return 2
        return -1

def move_motors(gesture):
        if (gesture == 0):
                gpio.write(4,0)
                gpio.write(3,0)
        if (gesture == 1):
                gpio.write(4,0)
                gpio.write(3,1)
        if (gesture == 2):
                gpio.write(4,1)
                gpio.write(3,0)
                

def proc_emg(emg, moving, times = []):
        secondsSinceStart = (datetime.datetime.now().second-start.second+60)%60
        f.writerow(list(emg)+[eval_label()])
	os.system('clear')
	print_emg(list(emg))
	print ("EMG: " + str(emg) + " Seconds: " + str(secondsSinceStart))
        gesture = -1
        if(this_model):
                gesture = this_model.predict(np.array(list(emg)+[1])[None])                

	if (gesture == 0):
                print('RESTING!')
        if (gesture == 1):
                print('GRIPPING!')
        if (gesture == 2):
                print('FLEXING!')
        move_motors(gesture)

def onPeriodic():
	print("onPeriodic")
	if myo.isUnlocked():
                print(myo.conn)
        else:
                myo.unlock("hold")
                myo.start_raw()
                myo.add_emg_handler(proc_emg)
                this_model.fromFile('rowan_rest_grip_flex_linear_classifier_100p.csv')



