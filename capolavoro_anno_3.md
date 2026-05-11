# Password Security Auditor
**Studente:** Mattia Alessi
**Classe:** 3° Q
**Anno scolastico:** 2025/2026

---

## 1. Introduzione e Obiettivi
L'obiettivo di questo progetto è lo sviluppo di un applicativo di analisi per la sicurezza informatica scritto in **Python**. Il software permette di valutare la robustezza delle credenziali d'accesso attraverso una doppia verifica:
* **Analisi Qualitativa e Quantitativa Locale:** Calcolo dell'entropia e verifica dei pattern strutturali.
* **Verifica di Integrità Online:** Controllo dell'esposizione della password in violazioni di dati (*data breach*) globali tramite protocolli di comunicazione sicura.

## 2. Architettura Logica (Workflow)
Il software segue il principio del **Privacy by Design**, assicurando che la password originale non lasci mai il dispositivo dell'utente e non venga mai trasmessa in chiaro sulla rete.

1.  **Acquisizione Input:** L'utente inserisce la password tramite terminale; il modulo `getpass` maschera i caratteri per prevenire lo *shoulder surfing*.
2.  **Valutazione dell'Entropia:** Viene calcolata l'**Entropia di Shannon** ($E = L \cdot \log_2(R)$) per misurare la resistenza teorica ad attacchi di tipo *brute-force*.
3.  **Hashing SHA-1:** La password viene trasformata in un'impronta digitale univoca (hash) non invertibile.
4.  **Protocollo K-Anonymity:**
    * **Scomposizione:** Lo script estrae i primi 5 caratteri dell'hash (prefisso).
    * **Interrogazione Anonima:** Solo il prefisso viene inviato all'API di *Have I Been Pwned*. Il server risponde con una lista di migliaia di suffissi corrispondenti.
5.  **Confronto Locale:** Il software confronta il suffisso memorizzato localmente con quelli ricevuti dal server. Se viene trovata una corrispondenza, la password è considerata compromessa.

## 3. Specifiche Tecniche
* **Linguaggio:** Python 3.11+
* **Librerie Standard:**
    * `hashlib`: Per la generazione del digest SHA-1.
    * `math`: Per i calcoli logaritmici dell'entropia.
    * `getpass`: Per l'acquisizione sicura dell'input.
* **Librerie Esterne:**
    * `requests`: Per la gestione delle chiamate HTTP verso l'endpoint API.
    * `termcolor`: Per migliorare l'esperienza utente (UX) tramite feedback cromatici.

## 4. Documentazione e Fonti
* [Have I Been Pwned API documentation](https://haveibeenpwned.com/API/v3#PwnedPasswords)
* [Python math library](https://docs.python.org/3/library/math.html)
* [NIST Digital Identity Guidelines](https://pages.nist.gov/800-63-3/) (Standard internazionale per la gestione delle password)
* [getpass documentation](https://docs.python.org/3/library/getpass.html)
* [hashlib documentation](https://docs.python.org/3/library/hashlib.html)


## 5. Percorso

1) Volevo capire se le password che uso sono già in circolazione o no in data breach pubblici, così ho fatto ricerche e sono venuto a conoscenza dell'API di Have I Been Pwned.

2) Leggendo la documentazione ho capito che inviare la password intera era un rischio per la privacy e non era consentito dall'API, quindi ho studiato e applicato il protocollo sha-1

3) Ho aggiunto la matematica (Entropia) per rendere il tool completo per avere una conferma della sicurezza della password