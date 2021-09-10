# Traffic
Traffic is an implementation of a **Convolutional Neural Network** built with TensorFlow Keras Sequential Model.

The model classifies road signs based on images. For training and testing the model, the German Traffic Sign Recognition Benchmark (GTSRB) labeled dataset, which contains thousands of images of 43 different kinds of road signs, was used.

## Neural Network - model building process
When building a neural network model, the objective is to **minimize the loss function** and **maximize testing accuracy** (using the least possible resources). In order to achieve that we can explore and experiment different network structures and configurations. For this implementation, the experimentation process is described below:

## Experimentation Process 

### STEP 1
Started with a plain *'vanilla'* model with no convolution steps, a single hidden layer with 128 units and ReLu activation, and a dropout layer of 0.2 proportion as suggested by documentation. Results showed to be clearly inadequate.

After a different number of tries with different settings results didn't improve and still presented **high loss** and **low accuracy** in both training and testing, even with quadrupled units (512) or multi hidden layers were set.

Best run (Epoch 10 training results and testing results): 

`Epoch 10/10
500/500 [==============================] - 4s 9ms/step - loss: 3.5017 - accuracy: 0.0556
333/333 - 1s - loss: 3.4935 - accuracy: 0.0574`


### STEP 2
At this point a convolutional layer with 32 kernel filters and a pooling layer of (2 x 2) were added to model. 








