import cv2 
import random
import sys
import numpy as np
from argparse import ArgumentParser
from sklearn.cluster import KMeans
from collections import Counter
import cv2 #for resizing image
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

def put_randomly_text(img, text, colors, loops, text_range=(0.3, 0.7)):

    height, width, depth = img.shape
    #font = cv2.FONT_HERSHEY_SIMPLEX


    for c in colors:
        for j in range(0, loops):
            x = random.randint(0, width-1)
            y = random.randint(0, height-1)

            blue = c[0]
            red = c[1]
            green = c[2]
            color = (blue, red, green)

            text_size = random.uniform(text_range[0], text_range[1])

            #cv2.putText(img, text , (x, y), font, text_size, color, 1, cv2.LINE_AA)
            paint_text(img, text, x, y, text_size, color)

def do_job(input_file, input_text):
    print("Starting job")
    
    filename_input = input_file
    filename_output = filename_input + "_output.jpg"
    filename_cropped = filename_input + "_cropped.jpg"

    text = input_text
    img = cv2.imread(filename_input) 

    height, width, depth = img.shape

    print("height: {0}, width: {1}, depth {2}".format(height, width, depth))

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
    #img = cv2.blur(img, ksize)  

    print("First loop")
    text_range=(0.3, 0.7)
    loops = int((height + width)) * 2
    put_text(img, text, loops, text_range)

    print("Second loop")
    text_range=(0.3, 1.7)
    loops = int(loops / 2)
    put_text(img, text, loops, text_range)

    print("Painting text with dominant colors")
    text_range=(1.3, 2.7)
    #put_randomly_text(img, text, dominant_colors, 1, text_range)

    print("Blurring again")
    ksize = (3, 3) 
    img = cv2.blur(img, ksize) 

    cv2.imwrite(filename_output, img)
    


parser = ArgumentParser()
parser.add_argument("-f", "--file", dest="inputFile", help="Open specified file")
parser.add_argument("-t", "--text", dest="inputText", help="Text to put on the image")
parser.add_argument("-tf", "--text-file", dest="inputTextFile", help="Text file with text to put on the image")

args = parser.parse_args()
input_file = args.inputFile
if(args.inputText):
    input_text = args.inputText

if(args.inputTextFile):
    input_text = read_file(args.inputTextFile)

print('Doing job on file:{0} with this text: {1}'.format(input_file,input_text))

do_job(input_file, input_text)

