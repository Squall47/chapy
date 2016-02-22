import socket
import threading
import sys
import pdb
from commande import Commande

hote = ''
port = 40000

class ThreadClient(threading.Thread):
	def __init__(self,conn):
		threading.Thread.__init__(self)
		self.connexion = conn

	def run(self):
		nom = self.getName()
		while True:
			try:
				if "nom" in connexions[nom]:
						msgClient = self.connexion.recv(1024)
						if msgClient.upper() == b"FIN" or msgClient ==b"":
								break
						self.traitement(nom,msgClient)
						
				else:
					nom_client = self.connexion.recv(1024)
					connexions[nom]["nom"] = nom_client.decode()
					message = "*%s vient de se connecter*"%(connexions[nom]["nom"])
					print("%s a choisit %s comme nom"%(nom,connexions[nom]["nom"]))
					count = 1
					for cle in connexions:
							if cle != nom and "nom" in connexions[cle]:
								connexions[cle]["connexion"].send(message.encode())
								count+=1
					bienvenue = "*Vous etes connecte. Il y a maintenant %d personne(s) sur le chat.*"%count
					self.connexion.send(bienvenue.encode())
			except socket.error:
				break
		self.deconnexion(nom)

	def deconnexion(self,nom):
		self.connexion.close()
		print("Client %s déconnecté." % nom)
		if "nom" in connexions[nom]:
			message = "*%s s'est déconnecté*"%connexions[nom]["nom"]
			for cle in connexions:
				if cle != nom and "nom" in connexions[cle]:
					connexions[cle]["connexion"].send(message.encode())
		del connexions[nom]        # supprimer son entrÃ©e dans le dictionnaire
		
	def traitement(self,nom,message):
		message = message.decode()
		if message[0:1] == "/":
			if message[1:] in Commande.commandes:
				retour = getattr(Commande,message[1:])(connexions)
				connexions[nom]["connexion"].send(retour.encode())
			else:
				retour = "La commande %s n'existe pas, utlisé la commande help pour plus d'informations"%message[1:]
				connexions[nom]["connexion"].send(retour.encode())
				 
		else:
			retour = "<%s> %s" % (connexions[nom]["nom"], message)
			print(retour)
			# Faire suivre le message Ã  tous les autres clients :
			for cle in connexions:
				connexions[cle]["connexion"].send(retour.encode())
						

my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
	my_socket.bind((hote,port))
except socket.error:
	print("La liaison a echoué")
	sys.exit()
print("Le serveur a démarré!")
print("Port d'écoute : "+str(port))
my_socket.listen(5)
connexions = {}

while True:
	connexion, adresse = my_socket.accept()
	th = ThreadClient(connexion)
	it = th.getName()
	connexions[it] = {}
	connexions[it]["connexion"] = connexion
	print("Client %s connecté, adresse IP %s, port %s." %(it, adresse[0], adresse[1]))
	th.start()
