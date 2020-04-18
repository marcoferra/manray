from argparse import ArgumentParser
import cv2
import numpy as np


from utils import * 

def do_job(input_file, input_text):
    print("Starting job")
    
    filename_input = input_file
    filename_output = filename_input + "_output.jpg"

    text = input_text
    img = cv2.imread(filename_input) 

    height, width, depth = img.shape
    
    print("Canny")
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    img_blur = cv2.medianBlur(gray, 5)
    circles = cv2.HoughCircles(img_blur, cv2.HOUGH_GRADIENT, 1, img.shape[0]/64, param1=200, 
                param2=10, minRadius=300, maxRadius=530)
    circles = np.uint16(np.around(circles))

    for i in circles[0, :]:
        cv2.circle(img, (i[0], i[1]), i[2], (0, 255, 0), 2)
        cv2.circle(img, (i[0], i[1]), 2, (0, 0, 255), 3)

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

