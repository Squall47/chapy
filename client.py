# Définition d'un client réseau gérant en parallèle l'émission
# et la réception des messages (utilisation de 2 THREADS).

host = '127.0.0.1'
port = 40000

is_connexion = True

import socket, sys, threading, pdb

class ThreadReception(threading.Thread):
    """objet thread gérant la réception des messages"""
    def __init__(self, conn):
        threading.Thread.__init__(self)
        self.connexion = conn           # réf. du socket de connexion
        
    def run(self):
        while True:
            message_recu = self.connexion.recv(1024)
            print(message_recu.decode())
			
            if message_recu ==b'' or message_recu.upper() == b"FIN":
                break
        # Le thread <réception> se termine ici.
        # On force la fermeture du thread <émission> :
        print("*Client arrêté. Connexion interrompue.*")
        self.connexion.close()
    
class ThreadEmission(threading.Thread):
    """objet thread gérant l'émission des messages"""
    def __init__(self, conn):
        threading.Thread.__init__(self)
        self.connexion = conn           # réf. du socket de connexion
        
    def run(self):
        while True:
            message_emis = input()
            self.connexion.send(message_emis.encode())

# Programme principal - Établissement de la connexion :
connexion = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = input("Adresse du serveur : ")

try:
    connexion.connect((host, port))
except socket.error:
    print("La connexion a échoué.")
    sys.exit()    
print("Connexion établie avec le serveur.")

nom = input("Veuillez entrer un nom : ")

connexion.send(nom.encode())
            
# Dialogue avec le serveur : on lance deux threads pour gérer
# indépendamment l'émission et la réception des messages :
th_E = ThreadEmission(connexion)
th_R = ThreadReception(connexion)



th_E.start()
th_R.start()
        