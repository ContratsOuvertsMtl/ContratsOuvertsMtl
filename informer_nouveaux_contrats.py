#!c:\python34\python.exe
# coding: utf8


"""
Envoyer un message Twitter sur les nouveaux contrats

Version 1.0, 2015-08-29
Développé en Python 3.4
Licence CC-BY-NC 4.0 Pascal Robichaud, pascal.robichaud.do101@gmail.com
"""

from envoyer_twit import *
import csv
from afficher_statut_traitement import *


#Fonction left
def left(s, amount = 1, substring = ""):

    if (substring == ""):
        return s[:amount]
    else:
        if (len(substring) > amount):
            substring = substring[:amount]
        return substring + s[:-amount]
        
        
def formatter_montant(montant):

    reponse = ""

    if montant:
    
        reponse = left(montant, len(montant) - 3) + "$"
    
    return reponse

    
def informer_nouveaux_contrats(a_verifier):

    message = ""
    CONTRATS_TRAITES = "C:\\ContratsOuvertsMtl\\contrats_traites.csv"
    INSTANCE = a_verifier[2]

    # 0 instance
    # 1 date_rencontre
    # 2 no_decision
    # 3 titre
    # 4 no_dossier
    # 5 instance_reference
    # 6 no_appel_offres
    # 7 nbr_soumissions
    # 8 pour
    # 9 texte_contrat
    # 10 fournisseur
    # 11 montant
    # 12 type_contrat
    # 13 huis_clos
    # 14 source
    # 15 date_traitement

    
    afficher_statut_traitement("Début du traitement informer_nouveaux_contrats")
    
    with open(CONTRATS_TRAITES, "r", encoding = "utf-8", ) as f:     
        reader = csv.reader(f, delimiter = ";")    
    
        for ligne in reader:
        
            #Ne pas considérer la 1re ligne du nom des champs
            if "instance" not in ligne[0]:      
        
                #S'il y a un fournisseur
                if ligne[10]:                   
                
                    message = INSTANCE + " " + ligne[1] + ": Contrat de " + formatter_montant(ligne[11]) + " à " + ligne[10] + " " + ligne[3] + ", Dossier " + ligne[4]
                    
                #Décision en huis clos
                elif "huis clos" in ligne[3]:

                    message = INSTANCE + " " + ligne[1] + ": Décision " + ligne[2] + " prise en huis clos."

                else:
                
                    message = INSTANCE + " " + ligne[1] + ": " + ligne[9]
                    
            if len(message) > 140:
                
                message = left(message, 137) + "..."
            
            print(message)

            #envoyer_twit(message)
     
    afficher_statut_traitement("Fin du traitement informer_nouveaux_contrats")
    
if __name__ == '__main__':

    a_verifier = [
                    ["Comité exécutif",
                    "http://ville.montreal.qc.ca/portal/page?_pageid=5798,85931607&_dad=portal&_schema=PORTAL",
                    "CE"]
                 ] 
    informer_nouveaux_contrats(a_verifier[0])
