# Traffic
Traffic is an implementation of a **Convolutional Neural Network** built with TensorFlow Keras Sequential Model.

The model classifies road signs based on images. For training and testing the model, the German Traffic Sign Recognition Benchmark (GTSRB) labeled dataset, which contains thousands of images of 43 different kinds of road signs, was used.

## Neural Network - model building process
When building a neural network model, the objective is to **minimize the loss function** and **maximize testing accuracy** (using the least possible resources). In order to achieve that we can explore and experiment different network structures and configurations. For this implementation, the experimentation process is described below:

## Experimentation Process 

### STEP 1
setup a plain *'vanilla'* model with no convolution steps, a single hidden layer with documentation sugested *'default'* values of 128 units in it and ReLu activation, and a dropout layer of 0.2 proportion.  


