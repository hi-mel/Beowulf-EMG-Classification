
# EMG Data Processing Script
print("Emg Data Processing")

import math
import pdb
import os
import datetime
import csv
import numpy as np
import pigpio
from Linear_Classifier import linear_classifier

classifier = linear_classifier.LinearClassifier(9,3)
gpio = pigpio.pi()

start_time = datetime.datetime.now()
training_data = {'file':None, 'csv_writer':None}

# Mode options: 'training', 'predicting'
mode = 'predicting'

# Label options: 'rest', 'grip', 'flex'
label = 'flex'

# Labels stored in csv as integers: rest -> 0, grip -> 1, flex -> 2 
def label_to_int(gesture_label):
        if (gesture_label == 'rest'):
                return 0
        if (gesture_label == 'grip'):
                return 1
        if (gesture_label == 'flex'):
                return 2
        return -1


# Display emg data in human-readable way
def print_emg(emg):

        secondsSinceStart = (datetime.datetime.now().second-start_time.second+60)%60

	os.system('clear')
        for datum in emg:
                print('[' + '*'*int(datum/100))
        print ("EMG: " + str(emg) + " Seconds: " + str(secondsSinceStart))


# Control motors by gesture
def move_motors(gesture):
        # Rest: turn motor off
        if (gesture == 0):
                gpio.write(4,0)
                gpio.write(3,0)
        # Grip: move motor forward
        if (gesture == 1):
                gpio.write(4,0)
                gpio.write(3,1)
        # Flex: move motor backward
        if (gesture == 2):
                gpio.write(4,1)
                gpio.write(3,0)
                

# Main emg processing function
def proc_emg(emg, moving, times = []):

	print_emg(list(emg))
	
        if (mode == 'training' and training_data['csv_writer']):
                # Each row of training data contains 8 EMG samples followed by associated label
                training_data['csv_writer'].writerow(list(emg)+[label_to_int(label)])

        elif(mode == 'predicting' and classifier):
                gesture = -1
                
                add_one = np.ones((1,9))
                emg_features = np.array(list(emg)).astype(float)
                emg_features /= 1000.0
                add_one[0,:-1] = emg_features
                
                emg_features = add_one
                print(emg_features)
                gesture = classifier.predict(emg_features)                
                if (gesture == 0):
                        print('RESTING!')
                if (gesture == 1):
                        print('GRIPPING!')
                if (gesture == 2):
                        print('FLEXING!')
                move_motors(gesture)


# onPeriodic() is called periodically while the myo is connected.

# Myo will be locked on first call, at which point we must onlock it,
# set up global variables for runtime, and add emg processing handler.

def onPeriodic():

        # If myo is locked, unlock it and initialize script variables
	if not(myo.isUnlocked()):

                if (mode == 'training'):

                        if (training_data['file'] != None):
                                training_data['file'].close()

                        training_data['file'] = open('EMG_Training_Data/emg_training_data_'+label+'_'+datetime.datetime.now().strftime("%Y-%m-%d@%H:%M:%S")+'.csv','w+')
                        training_data['csv_writer'] = csv.writer(training_data['file'])

                elif (mode == 'predicting'):
                        classifier.fromFile('Linear_Classifier/rowan_rest_grip_flex_linear_classifier_3_99p.csv')

                myo.unlock("hold")
                myo.start_raw()
                myo.add_emg_handler(proc_emg)

        # Script is running   
        else:
                print(myo.conn)



def onUnlock():
	print("onUnlock")
	myo.rotSetCenter()
	myo.unlock("hold")
