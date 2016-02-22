import os

class Commande():

	commandes = {
		"help" : "Affiche l'aide",
		"users" : "Affiche la liste des personnes connectées",
		"count_users" : "Affiche le nombre de personnes connectées"
	}

	def __init__(self):
		pass
	
	@staticmethod	
	def users(connexions):
		users = []
		for cle in connexions:
			if "nom" in connexions[cle]:
				users.append(connexions[cle]["nom"])
		retour = "\r\n".join(users)
		return retour
		
	@staticmethod
	def count_users(connexions):
		users = []
		for cle in connexions:
			if "nom" in connexions[cle]:
				users.append(connexions[cle]["nom"])
		retour = "Il y a %d personne(s) sur le chat"%len(users)
		return retour
		
	@staticmethod
	def help(connexions):
		retour = "Liste des commandes : \n"
		for cle in Commande.commandes:
			retour += "\r\n\t - %s : %s"%(cle,Commande.commandes[cle])
		return retour