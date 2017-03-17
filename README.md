# Beowulf-EMG-Classification
Exoskeleton Classification Algorithms

Current state of this repo:

PyoManager library is used to collect EMG data from the Myo, which is connected to the Raspberry Pi via bluetooth.
The Global Mouse Control script under the PyoConnect_V2.0/scripts/ directory has been hacked to contain most of the logic we use for gesture classification. When the Myo is connected, it begins to call onPeriodic() preiodically. On the first call, the myo is unlocked, a raw emg data stream is initiated, and a function called proc_emg() is set up to recieve new emg data whenever it is available.

The functionality for handling emg data is all initiated there. Currently the data is only used for gesture recognition.


Gesture recognition is split into three tasks: data collection, training, and prediction.

In the data collection stage, the script is modified so that it simply reads the EMG data and writes it to a file. Before collecting the data, the tester and the user must agree on a gesture to perform. The tester then sets the variable 'label' in the Global Mouse Control script to said gesture, the user performs said gesture, and the tester runs the program to collect samples.
The samples will be written to timestamped CSV files, with the first 8 columns representing the emg data as floats and the final column will be an integer representing the gesture being performed.

In the training stage, the data is amalgamated into one master CSV file, and fed into the train() method of a Classifier. train_svm.py does this on an example linear classifier.
Once the classifier has been trained and tested using proper prctices, it can be used for gesture prediction. To do this, simply call the toFile() method of the classifier once it has been trained and tests with sufficient accuracy.

In the prediction stage, a classifier is loaded from file using the fromFile() method. It can then be inserted into the Global Mouse Control script and it's predict() method can be passed new emg data and can return its prediction as to the associated gesture.
In the current implementation, this prediction is used to control an H-bridge connected to the Raspberry Pi GPIO pins which powers a motor.
