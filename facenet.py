from keras.models import Sequential
from keras.layers import Conv2D, ZeroPadding2D, Activation, Input, concatenate
from keras.models import Model
from keras.layers.normalization import BatchNormalization
from keras.layers.pooling import MaxPooling2D, AveragePooling2D
from keras.layers.merge import Concatenate
from keras.layers.core import Lambda, Flatten, Dense
from keras.initializers import glorot_uniform
from keras.engine.topology import Layer
from keras import backend as K
K.set_image_data_format('channels_first')
import pandas as pd
import cv2
import os
import numpy as np
from numpy import genfromtxt

import tensorflow as tf
from fr_utils import *
from inception_blocks_v2 import *

import matplotlib.pyplot as plt # plt show pic
import matplotlib.image as mpimg # mpimg read pic



np.set_printoptions(threshold=np.nan)#设置打印方式，设置打印输出数组的时候完全输出，不考虑中间数组数字用省略号代替




#to triplet_loss

def triplet_loss(y_true, y_pred, alpha = 0.2):
    """
    Implementation of the triplet loss as defined by formula (3)
    
    Arguments:
    y_true -- true labels, required when you define a loss in Keras, you don't need it in this function.
    y_pred -- python list containing three objects:
            anchor -- the encodings for the anchor images, of shape (None, 128)
            positive -- the encodings for the positive images, of shape (None, 128)
            negative -- the encodings for the negative images, of shape (None, 128)
    
    Returns:
    loss -- real number, value of the loss
    """
    
    anchor, positive, negative = y_pred[0], y_pred[1], y_pred[2]
    
    # Compute the (encoding) distance between the anchor and the positive, you will need to sum over axis=-1
    pos_dist = tf.reduce_sum(tf.square(tf.subtract(anchor,positive)),axis=-1)
    
    # Compute the (encoding) distance between the anchor and the negative, you will need to sum over axis=-1
    neg_dist = tf.reduce_sum(tf.square(tf.subtract(anchor,negative)),axis=-1)
    
    #  subtract the two previous distances and add alpha.
    basic_loss = tf.add(tf.subtract(pos_dist,neg_dist),alpha)
    # Step 4: Take the maximum of basic_loss and 0.0. Sum over the training examples.
    loss = tf.reduce_sum(tf.maximum(basic_loss,0))
    
    return loss



# zu verify

def verify(image_path, identity, database, model):
    """
    Function that verifies if the person on the "image_path" image is "identity".
    
    Arguments:
    image_path -- path to an image
    identity -- string, name of the person you'd like to verify the identity. Has to be a resident of the Happy house.
    database -- python dictionary mapping names of allowed people's names (strings) to their encodings (vectors).
    model -- your Inception model instance in Keras
    
    Returns:
    dist -- distance between the image_path and the image of "identity" in the database.
    door_open -- True, if the door should open. False otherwise.
    """
    
    
    # Compute the encoding for the image. Use img_to_encoding() see example above. 
    encoding = img_to_encoding(image_path, model)
    
    # Compute distance with identity's image (≈ 1 line)
    dist = np.linalg.norm(encoding-database[identity])
    
    # Open the door if dist < Schwellwert(0.5), else don't open 
    if dist<0.7:
        print("It's " + str(identity) + ", welcome home!")
        door_open = True
    else:
        print("It's not " + str(identity) + ", please go away")
        door_open = False
        
        
    return dist, door_open




#  Face Recognition: who_is_it
#Compute the target encoding of the image from image_path
#find the encoding from the database that has smallest distance with the target encoding.
#Initialize the min_dist variable to a large enough number (100). It will help you keep track of what is the closest encoding to the input's encoding.
#loop over the database dictionary's names and encodings. To loop use for (name, db_enc) in database.items().
#compute L2 distance between the target "encoding" and the current "encoding" from the database.
#If this distance is less than the min_dist, then set min_dist to dist, and identity to name.

def who_is_it(image_path, database, model):
    """
    Implements face recognition for the happy house by finding who is the person on the image_path image.
    
    Arguments:
    image_path -- path to an image
    database -- database containing image encodings along with the name of the person on the image
    model -- your Inception model instance in Keras
    
    Returns:
    min_dist -- the minimum distance between image_path encoding and the encodings from the database
    identity -- string, the name prediction for the person on image_path
    result -- the result to be printed in the GUI
    """
    
    
    ##Compute the target "encoding" for the image. Use img_to_encoding() see example above. ## 
    encoding = img_to_encoding(image_path, model)
    
    ##Find the closest encoding ##
    
    # Initialize "min_dist" to a large value, make it 100 maybe? 
    min_dist = 100
    
    # Loop over the database dictionary's names and encodings.
    for (name, db_enc) in database.items():
        
        # Compute L2 distance between the target "encoding" and the current "emb" from the database. 
        dist = np.linalg.norm(encoding-database[name])

        # If this distance is less than the min_dist, then set min_dist to dist, and identity to name. 
        if dist<min_dist:
            min_dist = dist
            identity = name


    #Schwellwert(0.5)
    if min_dist > 0.7:
        print("Not in the database.")
        result = "Not in the database."
    else:
        print ("it's " + str(identity) + ", the distance is " + str(min_dist))
        result = "it's " + str(identity) + ", the distance is " + str(min_dist)
    return min_dist, identity, result