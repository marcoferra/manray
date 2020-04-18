import cv2 
import random
import sys
import numpy as np
from sklearn.cluster import KMeans
from collections import Counter
import math

def get_dominant_color(image, k=4, image_processing_size = None):
    """
    takes an image as input
    returns the dominant color of the image as a list
    
    dominant color is found by running k means on the 
    pixels & returning the centroid of the largest cluster

    processing time is sped up by working with a smaller image; 
    this resizing can be done with the image_processing_size param 
    which takes a tuple of image dims as input

    >>> get_dominant_color(my_image, k=4, image_processing_size = (25, 25))
    [56.2423442, 34.0834233, 70.1234123]
    """
    #resize image if new dims provided
    if image_processing_size is not None:
        image = cv2.resize(image, image_processing_size, 
                            interpolation = cv2.INTER_AREA)
    
    #reshape the image to be a list of pixels
    image = image.reshape((image.shape[0] * image.shape[1], 3))

    #cluster and assign labels to the pixels 
    clt = KMeans(n_clusters = k)
    labels = clt.fit_predict(image)

    #count labels to find most popular
    label_counts = Counter(labels)

    colors = list()

    for el in label_counts.most_common(10):
        #print('Current dominant colors is: labels({})'.format(el))
        color = clt.cluster_centers_[el[0]]
        print('Dominant color is: bgr({})'.format(color))
        colors.append(color)
    
    #print('Dominant colors count is: labels({})'.format(label_counts.most_common(5)))

    #subset out most popular centroid
    #dominant_color = clt.cluster_centers_[label_counts.most_common(1)[0][0]]
    #print('Dominant color is: bgr({})'.format(dominant_color))

    return colors


def read_file(filename):
    data = None

    with open(filename) as file:  
        data = file.read() 

    return data

def get_color_values():
    blue = randrange(0, 255)
    red = randrange(0, 255)
    green = randrange(0, 255)

    return [blue, red, green]


def reverse_color_values(values):
    blue = -values[0]
    red = -values[1]
    green = -values[2]

    return (blue, red, green)


def get_yes_or_not():
    yes = randrange(0, 1)
    
    return yes


def paint_text(img, text, x, y, text_size, color):

    font = cv2.FONT_HERSHEY_SIMPLEX
    dy = math.ceil(text_size * 20)

    for i, line in enumerate(text.split('\n')):
        y = y + i*dy
        cv2.putText(img, line , (x, y), font, text_size, color, 1, cv2.LINE_AA)


def put_text(img, text, loops, text_range=(0.3, 0.7)):

    height, width, depth = img.shape
  #  font = cv2.FONT_HERSHEY_SIMPLEX

    for j in range(0, loops):

        x = random.randint(0, width-1)
        y = random.randint(0, height-1)

        color = img[y, x]

        blue = color[0].item()
        red = color[1].item()
        green = color[2].item()

        color_tuple = (blue, red, green)

        text_size = random.uniform(text_range[0], text_range[1])

        #cv2.putText(img, text , (x, y), font, text_size, color, 1, cv2.LINE_AA)
        paint_text(img, text, x, y, text_size, color_tuple)

        if((j % 1000) == 0):
            sys.stdout.write('#')
            sys.stdout.flush()

    print("OK")

def put_randomly_text(img, text, colors, text_range=(0.3, 0.7)):

    height, width, depth = img.shape
    #font = cv2.FONT_HERSHEY_SIMPLEX

    for c in colors:

        x = random.randint(0, width-1)
        y = random.randint(0, height-1)

        blue = c[0]
        red = c[1]
        green = c[2]
        color = (blue, red, green)

        text_size = random.uniform(text_range[0], text_range[1])

        #cv2.putText(img, text , (x, y), font, text_size, color, 1, cv2.LINE_AA)
        paint_text(img, text, x, y, text_size, color)
