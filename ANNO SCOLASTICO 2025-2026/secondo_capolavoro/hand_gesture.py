import cv2 as cv
import mediapipe as mp
import time # serve per dare un timestamp ai frame (richiesto dai Tasks)
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import pickle
import csv
import os


# Setup di MediaPipe per trovare le mani
base_options = python.BaseOptions(model_asset_path='hand_landmarker.task') #scaricato dai link nel .md direttamente da google
options = vision.HandLandmarkerOptions(
    base_options=base_options,
    num_hands=2,             #max 2 mani (solo per future 2 persone 1 mano contro 1)
    min_hand_detection_confidence=0.7,
    running_mode=vision.RunningMode.VIDEO # dico al modello che è un video per fluidità
)

# Creo il detector 
detector = vision.HandLandmarker.create_from_options(options)


# connessioni della mano, per disegnare le linee tra i punti
CONNECTIONS = [
    (0, 1), (1, 2), (2, 3), (3, 4),       # Pollice
    (0, 5), (5, 6), (6, 7), (7, 8),       # Indice
    (5, 9), (9, 10), (10, 11), (11, 12),  # Medio
    (9, 13), (13, 14), (14, 15), (15, 16),# Anulare
    (13, 17), (17, 18), (18, 19), (19, 20),# Mignolo
    (0, 17)                               # Palmo
]


def capture(numero=False):
    cap = cv.VideoCapture(0) # 0 è la camera del pc, se ne ho altre posso mettere 1,2,3,etc...

    if not cap.isOpened():
        print("Cannot open camera")
        exit()

    while True:
       
        ret, frame = cap.read()  # Catturo il frame

        # Se il frame è letto bene ret è True
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break
        
        # Specchio l'immagine per comodità e per maggiore sicurezza del modello
        frame = cv.flip(frame, 1)
        
        # Cambio da BGR a RGB (MediaPipe lo richide)
        frame_rgb = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        
        
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame_rgb) #serve per convertire l'immagine 
                                                                              #in un formato che MediaPipe può usare
        
        
        # per la modalità VIDEO serve un timestamp 
        timestamp = int(time.time() * 1000)
        
        # Il modello guarda l'immagine e cerca i punti della mano
        results = detector.detect_for_video(mp_image, timestamp)
        
        # Se trova la mano disegna landmark
        if results.hand_landmarks:
            
            #sono il numero di mani trovate
            for hand in results.hand_landmarks:
                
                coords = [] #lista con coordinate punti
                #ogni mano dovrebbe avere 21 punti
                for coord in hand:
                    
                    x = int(coord.x * frame.shape[1]) #coordinata x
                    y = int(coord.y * frame.shape[0]) #coordinata y
                    coords.append((x, y))
                    
                    
                #disegno linee tra i punti usando le connessioni
                for strt, end in CONNECTIONS:
                    cv.line(frame, coords[strt], coords[end], (0, 255, 0), 2)
                
                #disegno i punti
                for i, (x, y) in enumerate(coords):
                    cv.circle(frame, (x, y), 5, (0, 0, 255), -1)
                    
                    if numero:
                        cv.putText(frame, str(i), (x, y), cv.FONT_HERSHEY_SIMPLEX, 0.3, (255, 255, 255), 1) #per vedere i numeri dei punti
        
        # Mostro il risultato uso frame BGR per non vedere rosso e blu invertiti
        cv.imshow('Frame', frame)
        
        
        if cv.waitKey(1) == ord('q'):
            break

    detector.close()
    cap.release()
    cv.destroyAllWindows()




def save_to_csv(data, label):
    file_path = 'dataset.csv'
   
    file_exists = os.path.isfile(file_path)
    
    with open(file_path, 'a', newline='') as f:
        writer = csv.writer(f)
        
        if not file_exists:
            header = []
            for i in range(21):
                header.extend([f'x{i}', f'y{i}', f'z{i}'])
            header.append('label')
            writer.writerow(header)
        
        row = data + [label]
        writer.writerow(row)
def addestra(numero=False):
    
    label = input("Che gesto registriamo? (sasso/carta/forbice): ")
    cap = cv.VideoCapture(0) # 0 è la camera del pc, se ne ho altre posso mettere 1,2,3,etc...

    if not cap.isOpened():
        print("Cannot open camera")
        exit()

    while True:
       
        ret, frame = cap.read()  # Catturo il frame

        # Se il frame è letto bene ret è True
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break
        
        # Specchio l'immagine per comodità e per maggiore sicurezza del modello
        frame = cv.flip(frame, 1)
        
        # Cambio da BGR a RGB (MediaPipe lo richide)
        frame_rgb = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        
        
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame_rgb) #serve per convertire l'immagine 
                                                                              #in un formato che MediaPipe può usare
        
        
        # per la modalità VIDEO serve un timestamp 
        timestamp = int(time.time() * 1000)
        
        # Il modello guarda l'immagine e cerca i punti della mano
        results = detector.detect_for_video(mp_image, timestamp)
        
        key = cv.waitKey(1) & 0xFF
        
        # Se trova la mano disegna landmark
        if results.hand_landmarks:
            
            #sono il numero di mani trovate
            for hand in results.hand_landmarks:
                
                coords = [] #lista con coordinate punti
                coords_csv = [] #lista coordinate per il CSV (futuro addestramento modello)
                
                
                #ogni mano dovrebbe avere 21 punti
                for coord in hand:
                    
                    x = int(coord.x * frame.shape[1]) #coordinata x
                    y = int(coord.y * frame.shape[0]) #coordinata y
                    coords.append((x, y))
                    
                    
                    coords_csv.extend([coord.x, coord.y, coord.z]) #aggiungo coordinate CSV
                    
                    
                #disegno linee tra i punti usando le connessioni
                for strt, end in CONNECTIONS:
                    cv.line(frame, coords[strt], coords[end], (0, 255, 0), 2)
                
                #disegno i punti
                for i, (x, y) in enumerate(coords):
                    cv.circle(frame, (x, y), 5, (0, 0, 255), -1)
                    
                    if numero:
                        cv.putText(frame, str(i), (x, y), cv.FONT_HERSHEY_SIMPLEX, 0.3, (255, 255, 255), 1) #per vedere i numeri dei punti

                if key == ord('s'):
                    save_to_csv(coords_csv, label)
                    print(f"Gesto {label} salvato")
        
        
        
        # Mostro il risultato uso frame BGR per non vedere rosso e blu invertiti
        cv.imshow('Frame', frame)
        
        
        if key == ord('q'):
            break

    detector.close()
    cap.release()
    cv.destroyAllWindows()


def gioca(model="model.pkl"):
    
    if not os.path.exists(model):
        return "Model not found"

    with open(model, 'rb') as f:
        model = pickle.load(f)

    
    print("Modello aperto")
    cap = cv.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret: break
        
        frame = cv.flip(frame, 1)
        frame_rgb = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame_rgb)
        timestamp = int(time.time() * 1000)
        results = detector.detect_for_video(mp_image, timestamp)

        if results.hand_landmarks:
            for hand in results.hand_landmarks:
                coords_pixel = []
                coords_input = []
                
                for coord in hand:
                    
                    x = int(coord.x * frame.shape[1])
                    y = int(coord.y * frame.shape[0])
                    coords_pixel.append((x, y))
                    
                    coords_input.extend([coord.x, coord.y, coord.z])

               
                prediction = model.predict([coords_input])
                gesto = prediction[0]

                
                for strt, end in CONNECTIONS:
                    cv.line(frame, coords_pixel[strt], coords_pixel[end], (0, 255, 0), 2)
                for (x, y) in coords_pixel:
                    cv.circle(frame, (x, y), 5, (0, 0, 255), -1)

                
                cv.putText(frame, gesto, (coords_pixel[0][0], coords_pixel[0][1] - 50), cv.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 3)

        cv.imshow('Riconoscimento Gesti', frame)
        if cv.waitKey(1) & 0xFF == ord('q'):
            break
        
        
    detector.close()
    cap.release()
    cv.destroyAllWindows()
  
  
  
  
  
  
  

  
gioca()