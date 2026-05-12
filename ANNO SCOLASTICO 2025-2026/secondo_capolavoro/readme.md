# Gesture Recognition 
**Studente:** Mattia Alessi  
**Classe:** 3° Q  
**Anno scolastico:** 2025/2026  

---

## 1. Introduzione e Obiettivi
L'obiettivo di questo progetto è la progettazione e l'implementazione di un sistema di **Computer Vision** e **Machine Learning** per il riconoscimento biometrico e gestuale. Il software è in grado di interpretare la morfologia della mano umana per classificare gesti specifici (Sasso, Carta, Forbice) in tempo reale tramite webcam.
Gli obiettivi principali includono:
* **Mappatura Spaziale:** Identificazione dei punti di snodo della mano (Landmarks) tramite visione artificiale.
* **Classificazione Predittiva:** Utilizzo di un modello statistico per l'inferenza istantanea basata su dataset personalizzati.

## 2. Architettura Logica (Workflow)
Il sistema opera attraverso una pipeline di elaborazione sequenziale che trasforma un flusso video grezzo in dati strutturati e, infine, in una decisione logica.

1. **Acquisizione e Pre-processing:** Cattura dei frame tramite OpenCV, applicazione di mirroring per facilitare l'interazione e conversione dello spazio colore da BGR a RGB per la compatibilità con i modelli di visione.
2. **Estrazione delle Caratteristiche (Feature Extraction):** * Utilizzo di **MediaPipe Hand Landmarker** per individuare 21 punti chiave (snodi ossei).
   * Generazione di un vettore di **63 caratteristiche** ($21 \text{ punti} \times 3 \text{ coordinate } x, y, z$) che descrivono univocamente la forma della mano.
3. **Normalizzazione (Scaling):** I dati grezzi vengono processati tramite `StandardScaler`. Questa fase è critica per assicurare che il modello sia invariante rispetto alla distanza della mano dalla webcam.
4. **Inferenza tramite Support Vector Machine (SVM):**
   * Il vettore normalizzato viene analizzato da un classificatore **SVC** con kernel **RBF** (Radial Basis Function).
   * Il modello calcola la classe di appartenenza confrontando i dati attuali con i pattern appresi durante l'addestramento.
5. **Output Visivo:** Il sistema esegue il rendering dei risultati sul feed video, sovrapponendo lo scheletro digitale e l'etichetta del gesto predetto.

## 3. Specifiche Tecniche
* **Linguaggio:** Python 3.11.x
* **Framework di Visione:**
    * `MediaPipe`: Per il tracciamento cinematico della mano in 3D.
    * `OpenCV`: Per la gestione del flusso video e dell'interfaccia grafica (GUI).
* **Framework di Machine Learning:**
    * `Scikit-learn`: Per la creazione della pipeline di addestramento e la gestione del classificatore SVM.
    * `Pickle`: Per la serializzazione del modello addestrato (`model.pkl`).


## 4. Documentazione e Fonti
* [MediaPipe Hand Landmarker Guide](https://ai.google.dev/edge/mediapipe/solutions/vision/hand_landmarker) (Modelli Google AI)
* [Scikit-learn SVC Documentation](https://scikit-learn.org/stable/modules/generated/sklearn.svm.SVC.html) (Support Vector Classification)
* [OpenCV Video Processing](https://docs.opencv.org/4.x/dd/d43/tutorial_py_video_display.html)
* [NIST Biometric Standards](https://www.nist.gov/programs-projects/biometrics) (Riferimenti internazionali per il riconoscimento biometrico)

## 5. Percorso e Sviluppo

1. **Analisi del Problema:** La sfida iniziale è stata capire come trasformare un'immagine video in informazioni geometriche manipolabili. Ho scelto MediaPipe perché permette di isolare la struttura della mano dal rumore di fondo dell'immagine.
2. **Data Engineering:** Ho implementato un sistema di acquisizione dati personalizzato (`addestra`) per popolare il `dataset.csv`. Questo mi ha permesso di capire l'importanza della qualità del dato: ho dovuto registrare gesti con diverse angolazioni per rendere l'AI resiliente ai cambiamenti di prospettiva.
3. **Ottimizzazione del Modello:** Ho sperimentato diversi kernel per l'algoritmo SVM, scegliendo infine il kernel **RBF**. Questa scelta tecnica è stata fondamentale per gestire la complessità dei movimenti delle dita, portando l'accuratezza del sistema sopra il 95% nei test di validazione.
