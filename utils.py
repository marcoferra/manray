import cv2 
import random
import sys
import numpy as np
from sklearn.cluster import KMeans
from collections import Counter
import math
import matplotlib.pyplot as plt

def get_dominant_color(image, k=4, image_processing_size = None):
    """
    takes an image as input
    returns the dominant color of the image as a list
    
    dominant color is found by running k means on the 
    pixels & returning the centroid of the largest cluster

    processing time is sped up by working with a smaller image; 
    this resizing can be done with the image_processing_size param 
    which takes a tuple of image dims as input

     get_dominant_color(my_image, k=4, image_processing_size = (25, 25))
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

    for n in range(0, 5):
        for c in colors:

            x = random.randint(0, width-1)
            y = random.randint(0, height-1)

            blue = c[0]
            red = c[1]
            green = c[2]
            color = (blue, red, green)

            text_size = random.uniform(text_range[0], text_range[1])

            paint_text(img, text, x, y, text_size, color)


def put_text_by_char(image, text, contours):
    
    print("Print text on contours")

    for c in contours:
        for l in c:
            for p in l:

                x = p[0]
                y = p[1]

                blue = 255
                red = 255
                green = 255
                color = (blue, red, green)

                text_size = (1.3, 2.0)
                text_s = text_size[0]

                paint_text(image, text, x, y, 1, color)

    return image

def do_job(img, text, params):

    height, width, depth = img.shape

    loops = int((height + width) * 2)
    print("height: {0}, width: {1}, loops: {2}".format(height, width, loops))

    print("Getting dominant colors")
    x_start = int(width * 0.20)
    x_end = int(width * 0.8)
    y_start = int(height * 0.30)
    y_end = int(height * 0.80)

    img_no_border = img[y_start:y_end, x_start:x_end]
    #cv2.imwrite(filename_cropped, img_no_border)
    dominant_colors = get_dominant_color(img_no_border)

    print("Blurring")
    ksize = (50, 50) 
    ksize = (10, 10) 
    img = cv2.blur(img, ksize)  

    print("First loop")
    min_font = params["first_loop"]["min_font"]
    max_font = params["first_loop"]["max_font"]
    text_range=(min_font, max_font)
    put_text(img, text, loops, text_range)

    print("Second loop")
    min_font = params["second_loop"]["min_font"]
    max_font = params["second_loop"]["max_font"]
    text_range=(min_font, max_font)
    loops = int(loops / 2)
    put_text(img, text, loops, text_range)

    print("Painting text with dominant colors")
    min_font = params["third_loop"]["min_font"]
    max_font = params["third_loop"]["max_font"]
    text_range=(min_font, max_font)
    print(dominant_colors)
    put_randomly_text(img, text, dominant_colors, text_range)

    print("Blurring again")
    ksize = (3, 3) 
    img = cv2.blur(img, ksize) 

    return img



def do_job_c(img, text, params):

    height, width, depth = img.shape

    loops = int((height + width) * 2)
    print("height: {0}, width: {1}, loops: {2}".format(height, width, loops))

    image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

    _, binary = cv2.threshold(gray, 80, 255, cv2.THRESH_BINARY_INV)

    contours, hierarchy = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    image = cv2.drawContours(image, contours, -1, (0, 255, 0), 2)

    put_text_by_char(image, "Bellissima", contours)

    img = image

    return img
