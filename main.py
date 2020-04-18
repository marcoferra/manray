from argparse import ArgumentParser

from utils import * 

def do_job(input_file, input_text):
    print("Starting job")
    
    filename_input = input_file
    filename_output = filename_input + "_output.jpg"
    filename_cropped = filename_input + "_cropped.jpg"

    text = input_text
    img = cv2.imread(filename_input) 

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
    img = cv2.blur(img, ksize)  

    print("First loop")
    text_range=(0.3, 0.7)
    put_text(img, text, loops, text_range)

    print("Second loop")
    text_range=(0.3, 2.7)
    loops = int(loops / 2)
    put_text(img, text, loops, text_range)

    print("Painting text with dominant colors")
    text_range=(1.3, 2.7)
    put_randomly_text(img, text, dominant_colors, text_range)

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

