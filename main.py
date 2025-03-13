import os
from argparse import ArgumentParser
import json

from utils import * 
#from audio import * 

def main(input_file, input_text, input_params):

    print("Starting job")
    
    filename_input = input_file
    dir_name=os.path.dirname(filename_input)
    base_filename=os.path.splitext(os.path.basename(filename_input))[0] + '_output.jpg'
    filename_output = os.path.join(dir_name,base_filename)
    filename_cropped = filename_input + "_cropped.jpg"

    print("Output: {0}".format(filename_output))

    text = input_text
    
    img = cv2.imread(filename_input) 
    # Ottieni altezza, larghezza e numero di canali
    height, width, _ = img.shape

    print(f"Larghezza: {width}, Altezza: {height}")


    height, _, _ = img.shape  # Ottieni l'altezza dell'immagine
    scale_factor = height / 1200  # Calcola il fattore di scala rispetto all'altezza di riferimento

    params = {
        'first_loop' : {
            'min_font' : 0.3 * scale_factor,
            'max_font' : 0.4 * scale_factor
        },
        'second_loop' : {
            'min_font' : 1.3 * scale_factor,
            'max_font' : 2.7 * scale_factor
        },
        'third_loop' : {
            'min_font' : 1.3 * scale_factor,
            'max_font' : 4.7 * scale_factor
        }
    } 


    # Stampa dei parametri
    print("Paramtri per il testo:")
    print(json.dumps(params, indent=4))

    if (input_params["alg"] == "wind"):
        img = do_job(img, text, params)
    
    if (input_params["alg"] == "cont"):
        img = do_job_c(img, text, params)

    cv2.imwrite(filename_output, img)
    


parser = ArgumentParser()
parser.add_argument("-f", "--file", dest="inputFile", help="Open specified file")
parser.add_argument("-t", "--text", dest="inputText", help="Text to put on the image")
parser.add_argument("-tf", "--text-file", dest="inputTextFile", help="Text file with text to put on the image")
#parser.add_argument("-v", "--voice", dest="inputSTT", action="store_true", help="Use sst", default='False')
parser.add_argument("-a", "--alg", dest="algorithm",  help="Which effect to apply", default="wind")

args = parser.parse_args()
input_file = args.inputFile
if(args.inputText):
    input_text = args.inputText

if(args.inputTextFile):
    input_text = read_file(args.inputTextFile)

#if(args.inputSTT == True):
#    input_text = stt()

input_params = {
    'alg' : args.algorithm
}


print('Doing job on file:{0} with this text: {1}'.format(input_file,input_text))

main(input_file, input_text, input_params)

