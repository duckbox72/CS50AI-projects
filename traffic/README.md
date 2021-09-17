# Traffic
Traffic is an implementation of a **Convolutional Neural Network** (CNN) built with TensorFlow Keras Sequential Model.

The model classifies road signs based on images. For training and testing the model, the German Traffic Sign Recognition Benchmark (GTSRB) labeled dataset, which contains thousands of images of 43 different kinds of road signs, was used.

## Neural Network - Model Building Process
The objective of a neural network is to provide a model capable of **minimize the loss function** and **maximize accuracy ratio** using the least possible resources. In order to achieve that, we can explore and experiment different structures with different combinations of layers and configurations. For this implementation, the experimentation process is described below:

## Experimentation Process 
### STEP 1
Started with a plain *'vanilla'* model with no convolutional steps, a single **hidden layer** with 128 units and ReLu activation, and a **dropout laye**r of 0.2 proportion as suggested by documentation. Results showed to be clearly inadequate.

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

But instead, in the seek of a smaller sized flattened layer, the kernel filters were kept at the original (3 x 3) size, added a second **convolutional layer** with 32 (3 x 3) filters, followed by a second **pooling layer**. This proved to increase efficiency, reaching a consistent loss close to 0.2000 and accuracy on the 0.9000 range.

#### BEST RUN - Epoch 10 training and testing results:
`Epoch 10/10
500/500 [==============================] - 12s 23ms/step - loss: 0.1565 - accuracy: 0.9565
333/333 - 2s - loss: 0.2036 - accuracy: 0.9560`

### STEP 4
Although the previous step's updates clearly generated better results, seemed that there was still some room for improvement, specially regarding the loss and some possible *overfitting*. In fact, after trying several different configurations , increasing the dropoff ratio to 0.40 proved to be efficient in preventing overfitting.

On the other hand, although small overall improvements were also observed in loss, the output appeared not to be consistent enough and further changes or additions in units or hidden layers turned to be resource consuming without bringing meaningfull overall improvements.

#### BEST RUN - Epoch 10 training and testing results:
`
Epoch 10/10
500/500 [==============================] - 13s 26ms/step - loss: 0.2101 - accuracy: 0.9391
333/333 - 2s - loss: 0.1376 - accuracy: 0.9649
`

### STEP 5

Finally, the attention went back to the **Convolutional Base**. After several experiments, and having in mind that a higher number of kernels could be afforded computationally in some layers where the width and height shrunk from previous pooling layer(s), some modifications were implemented:

- number of kernel filters on the first convolutional layer changed from 32 to 30 (3 x 3)

- number of kernel filters on the first convolutional layer changed from 32 to 60 (3 x 3)

- after the second pooling layer was added anhother convolutional layer with 60 kernel filters (3 x 3)

These modifications, specially the extra layer addition proved to significantly lower the loss ratio further, and most importantly brought consistency to the model, with much more similar outputs returned in diferent runs.

Below, a detailed summary of the final implemented model and the complete 'best' run log.

#### FINAL MODEL SUMMARY

```
Model: "sequential"
_________________________________________________________________
Layer (type)                 Output Shape              Param #   
=================================================================
conv2d (Conv2D)              (None, 28, 28, 30)        840       
_________________________________________________________________
max_pooling2d (MaxPooling2D) (None, 14, 14, 30)        0         
_________________________________________________________________
conv2d_1 (Conv2D)            (None, 12, 12, 60)        16260     
_________________________________________________________________
max_pooling2d_1 (MaxPooling2 (None, 6, 6, 60)          0         
_________________________________________________________________
conv2d_2 (Conv2D)            (None, 4, 4, 60)          32460     
_________________________________________________________________
flatten (Flatten)            (None, 960)               0         
_________________________________________________________________
dense (Dense)                (None, 128)               123008    
_________________________________________________________________
dropout (Dropout)            (None, 128)               0         
_________________________________________________________________
dense_1 (Dense)              (None, 43)                5547      
=================================================================
Total params: 178,115
Trainable params: 178,115
Non-trainable params: 0
_________________________________________________________________
```

#### BEST RUN
```
Epoch 1/10
500/500 [==============================] - 13s 25ms/step - loss: 2.5062 - accuracy: 0.4184
Epoch 2/10
500/500 [==============================] - 13s 25ms/step - loss: 0.7971 - accuracy: 0.7651
Epoch 3/10
500/500 [==============================] - 13s 25ms/step - loss: 0.4485 - accuracy: 0.8735
Epoch 4/10
500/500 [==============================] - 14s 27ms/step - loss: 0.3179 - accuracy: 0.9092
Epoch 5/10
500/500 [==============================] - 14s 28ms/step - loss: 0.2551 - accuracy: 0.9273
Epoch 6/10
500/500 [==============================] - 15s 29ms/step - loss: 0.2223 - accuracy: 0.9355
Epoch 7/10
500/500 [==============================] - 15s 30ms/step - loss: 0.2361 - accuracy: 0.9350
Epoch 8/10
500/500 [==============================] - 15s 29ms/step - loss: 0.1618 - accuracy: 0.9536
Epoch 9/10
500/500 [==============================] - 15s 30ms/step - loss: 0.1479 - accuracy: 0.9575
Epoch 10/10
500/500 [==============================] - 15s 30ms/step - loss: 0.1366 - accuracy: 0.9614
333/333 - 3s - loss: 0.0965 - accuracy: 0.9802
```
