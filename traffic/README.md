# Traffic
Traffic is an implementation of a **Convolutional Neural Network** (CNN) built with TensorFlow Keras Sequential Model.

The model classifies road signs based on images. For training and testing the model, the German Traffic Sign Recognition Benchmark (GTSRB) labeled dataset, which contains thousands of images of 43 different kinds of road signs, was used.

## Neural Network - Model Building Process
The objective of a neural network is to provide a model capable of **minimize the loss function** and **maximize accuracy ratio** using the least possible resources. In order to achieve that, we can explore and experiment different structures with different layers and configurations. For this implementation, the experimentation process is described below:

## Experimentation Process 
### STEP 1
Started with a plain *'vanilla'* model with no convolution steps, a single **hidden layer** with 128 units and ReLu activation, and a **dropout laye**r of 0.2 proportion as suggested by documentation. Results showed to be clearly inadequate.

After a number of tries with different settings, results didn't appear to improve and still presented **high loss** and **low accuracy** in both training and testing sets, even when quadrupled units (512) or multi hidden layers were set.

#### BEST RUN - Epoch 10 training and testing results: 

`Epoch 10/10
500/500 [==============================] - 4s 9ms/step - loss: 3.5017 - accuracy: 0.0556
333/333 - 1s - loss: 3.4935 - accuracy: 0.0574`


### STEP 2
At this point a **convolutional layer** with 32 (3 x 3) kernel filters and a **pooling layer** of (2 x 2) were **added** to model. 

Although improvements could be observed in both loss and accuracy markers, this structure still turned out not be able to create a consistent model, as it produced a wide range of (not optimal) results in different runs with the same configuration.

#### BEST RUN - Epoch 10 training and testing results:
`Epoch 10/10
500/500 [==============================] - 8s 16ms/step - loss: 1.1116 - accuracy: 0.6435
333/333 - 2s - loss: 0.7735 - accuracy: 0.7790`

### STEP 3
Experimented a number of different settings, adding hidden dense layers, changing number of units and dropout layer proportions, as well as several convolutional layer and pooling layer settings . Noted that the most positive changes in both results and consistency occured after increasing the kernel filters to a (6 x 6) size, bringing loss to the 0.4000- range and the accuracy to the 0.9000+ range.

But instead, in the seek of a smaller sized flattened layer, the kernel filters were kept at the original (3 x 3) size, added a second **convolutional layer** with 32 (3 x 3) filters, followed by a second **pooling layer**. This proved to increase efficiency, reaching a consistent loss close to 0.2000 and accuracy on the 0.9000+ range.

#### BEST RUN
`Epoch 10/10
500/500 [==============================] - 12s 23ms/step - loss: 0.1565 - accuracy: 0.9565
333/333 - 2s - loss: 0.2036 - accuracy: 0.9560`

### STEP 4
Although the updates made on the previous step clearly generated better results, seemed that there was still some room for improvement, specially regarding the loss score and a possible little *overfitting*. In fact, after trying several different configurations , increasing the dropoff ratio to 0.40 proved to prevent possible overfitting and lower the loss ratio without compromising accuracy. 




Finally, doubling hidden layer units to 256 seemed to improve result consistency, keeping testing loss below 0.2000 and accuracy close to 0.9500.

Further changes or additions, appeared to be resource consuming with no overall improvement to the model accuracy.


#### BEST RUN
```
Epoch 10/10
500/500 [==============================] - 13s 26ms/step - loss: 0.1221 - accuracy: 0.9691
333/333 - 2s - loss: 0.1240 - accuracy: 0.9742
```


increasing second layer to 64 increased testing set accuracy 
