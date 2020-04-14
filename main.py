import cv2 
import random
import sys
import numpy as np


def getColorValues():
    blue = randrange(0, 255)
    red = randrange(0, 255)
    green = randrange(0, 255)

    return [blue, red, green]



def reverseColorValues(values):
    blue = -values[0]
    red = -values[1]
    green = -values[2]

    return (blue, red, green)

def getYesOrNot():
    yes = randrange(0, 1)
    
    return yes

def main():
    filename_input ="me.jpg"
    filename_output = filename_input + "_output.jpg"
    text = "Ego"
    img = cv2.imread(filename_input) 

    height, width, depth = img.shape

    font = cv2.FONT_HERSHEY_SIMPLEX

    loops = int((height + width) * 2)
    print(height, width, loops)

    for j in range(0, loops):

            x = random.randint(0, width-1)
            y = random.randint(0, height-1)
            color = img[y, x]

            blue = color[0].item()
            red = color[1].item()
            green = color[2].item()
            
            text_size = random.uniform(0.3, 5.5)

            cv2.putText(img, text , (x, y), font, text_size, (blue, red, green), 2, cv2.LINE_AA)

            if((j % 1000) == 0):
                sys.stdout.write('#')
                sys.stdout.flush()


    cv2.imwrite(filename_output, img)
    

main()
