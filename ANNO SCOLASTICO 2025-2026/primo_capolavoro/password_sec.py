import requests
import hashlib
import math
from termcolor import colored
import getpass
import sys


#la password viene codificata in encode("UTF-8"), cioè viene convertita in bytes
# poi viene calcolato l'hash SHA-1 di questa stringa codificata
# infine l'hash risultante viene convertito in una stringa esadecimale e trasformata in lettere maiuscole con .upper()


def hashed_password():
    """la password viene codificata in encode("UTF-8"), cioè viene convertita in bytes,
poi viene calcolato l'hash SHA-1 di questa stringa codificata e
infine l'hash risultante viene convertito in una stringa esadecimale e trasformata in lettere maiuscole con .upper().
Questo serve per essere gestita corretamente dall'API    
    """
    
    passwd = getpass.getpass(prompt='Password: ', stream=None)
    password = hashlib.sha1(passwd.encode("UTF-8")).hexdigest().upper()
    prefix = password[:5]
    suffix = password[5:]
    return prefix, suffix, passwd



def API_req(prefix):
    """
    Manda la richiesta all'API e fa il GET della risposta
    """
    
    url = f"https://api.pwnedpasswords.com/range/{prefix}"
    try:
        res = requests.get(url, timeout=5)
        return res
    except requests.exceptions.RequestException as e:
        print(colored(f"Errore di connessione: {e}", "yellow"))
        sys.exit(1)




def calculate_entropy(password):
    """
    Calcola l'entropia in bit (E = L * log2(R)).
    Più alta è l'entropia, più la password è casuale e resistente ai brute-force
    """
    if not password:
        return 0
    
    pool = 0
    if any(c.islower() for c in password): pool += 26
    if any(c.isupper() for c in password): pool += 26
    if any(c.isdigit() for c in password): pool += 10
    if any(not c.isalnum() for c in password): pool += 32
    
    if pool == 0: return 0
    
    
    entropy = len(password) * math.log2(pool)
    return round(entropy, 2)

def check_strength(password):
    """Analisi sicurezza password"""
    score = 0
    
    if len(password) >= 12: score += 2
    elif len(password) >= 8: score += 1
    if any(c.isdigit() for c in password): score += 1
    if any(c.isupper() for c in password) and any(c.islower() for c in password): score += 1
    if any(not c.isalnum() for c in password): score += 1
    return score



def password_check(response, suffix):
    """
    prende response lo divide in righe per poi controllare se la prima parte (prima dei due punti :) è identica al suffix.
    Se la trova la password è stata hackerata in qualche sito
    """
    
    response = response.text #.text to see the actual text and not the status code
    
    
    #VERSIONE VECCHIA OTTIMIZZABILE CON BLOCCO CODICE SUCCESSIVO
    # prefixs = []
    # text = ""
    # for linea in response:
    #     if linea != "\n":
    #         text += linea
    #     else:
    #         prefixs.append(text.strip("\r"))
    #         text = ""
            
        
            
    # .splitlines() divide il testo in una lista di righe automaticamente
    linee = response.splitlines()
    
        
    for ele in linee:
        controllo = ele.split(":")
        if suffix == controllo[0]:
            return f"La tua password è stata trovata in {controllo[1]} fughe dati", 1
        
    return "La tua password non è stata trovata in nessuna fuga di dati", 0
    
    
    
    
def main():
    pref, suff, password = hashed_password()
    response = API_req(pref)
    messaggio, codice = password_check(response, suff)
    
    entropy = calculate_entropy(password)
    score = check_strength(password)
  
    if codice == 1:
        print(colored(messaggio, "red", attrs=["bold"]))
    else:
        print(colored(messaggio, "green"))

    
    
    color = "green" if entropy > 60 else "yellow" if entropy > 35 else "red"
    print(f"Entropia: {colored(str(entropy) + ' bit', color, attrs=['bold'])}")
    
    livelli = {0:"PESSIMA", 1:"DEBOLE", 2:"MEDIA", 3:"BUONA", 4:"OTTIMA", 5:"ECCELLENTE"}
    print(f"Punteggio: {livelli.get(score)} ({score}/5)")
    
if __name__ == "__main__":
    main()

