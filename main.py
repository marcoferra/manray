import os
from argparse import ArgumentParser
import json

from utils import * 
#from audio import * 

def video_show():
    # Apri la webcam (0 è la webcam di default)
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Errore: Impossibile accedere alla webcam.")
        exit()

    print("Premi 'q' per uscire.")

    while True:
        # Leggi un frame dalla webcam
        ret, frame = cap.read()

        if not ret:
            print("Errore nella lettura del frame.")
            break

        # Applica un filtro - ad esempio converti in scala di grigi
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Mostra il frame originale e quello filtrato
        cv2.imshow('Originale', frame)
        mio = get_image(frame, input_text, input_params)
        cv2.imshow('Filtro - Scala di grigi', mio)

        # Premi 'q' per uscire
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Rilascia le risorse
    cap.release()
    cv2.destroyAllWindows()


def get_image(img, input_text, input_params):

    text = input_text
    
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

    return img

parser = ArgumentParser()
parser.add_argument("-f", "--file", dest="inputFile", help="Open specified file")
parser.add_argument("-t", "--text", dest="inputText", help="Text to put on the image")
parser.add_argument("-tf", "--text-file", dest="inputTextFile", help="Text file with text to put on the image")
#parser.add_argument("-v", "--voice", dest="inputSTT", action="store_true", help="Use sst", default='False')
parser.add_argument("-a", "--alg", dest="algorithm",  help="Which effect to apply", default="wind")
parser.add_argument('--video', action='store_true', help='Applica filtro in scala di grigi')


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


print("Starting job")
print('Doing job on file:{0} with this text: {1}'.format(input_file,input_text))

if(args.video):
    print("Output: Video")
    video_show()
else:
    filename_input = input_file
    dir_name=os.path.dirname(filename_input)
    base_filename=os.path.splitext(os.path.basename(filename_input))[0] + '_output.jpg'
    filename_output = os.path.join(dir_name,base_filename)
    filename_cropped = filename_input + "_cropped.jpg"
    image_input = cv2.imread(input_file) 
    image_output = get_image(image_input, input_text, input_params)

    print("Output: {0}".format(filename_output))

    cv2.imwrite(filename_output, image_output)
    