import cv2

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
    cv2.imshow('Filtro - Scala di grigi', gray)

    # Premi 'q' per uscire
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Rilascia le risorse
cap.release()
cv2.destroyAllWindows()
