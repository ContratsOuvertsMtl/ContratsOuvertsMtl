#!c:\python34\python.exe
# coding: utf8


"""
Envoyer un message Twitter sur les nouveaux contrats

Version 4.0, 2015-10-02
Développé en Python 3.4
Licence CC-BY-NC 4.0 Pascal Robichaud, pascal.robichaud.do101@gmail.com
"""

from envoyer_twit import *
import csv
from afficher_statut_traitement import *
from left import *
from right import *
        
        
def formatter_montant(montant):

    reponse = ""

    if montant:
    
        reponse = left(montant, len(montant) - 3) + "$"
    
    return reponse

    
def informer_nouveaux_contrats(a_verifier):

    message = ""
    CONTRATS_TRAITES = "C:\\ContratsOuvertsMtl\\contrats_traites.csv"

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
            if "instance" not in ligne:      

                instance = ligne[0]
                date_rencontre = ligne[1]
                no_decision = ligne[2]
                titre = ligne[3]
                no_dossier = ligne[4]
                instance_reference = ligne[5]
                no_appel_offres = ligne[6]
                nbr_soumissions = ligne[7]
                pour = ligne[8]
                texte_contrat = ligne[9]
                fournisseur = ligne[10]
                montant = ligne[11]
                type_contrat = ligne[12]
                huis_clos = ligne[13]
                source = ligne[14]
                date_traitement = ligne[15]

                #S'il y a un montant, un fournisseur, un tire et le texte du contrat
                if montant and fournisseur and titre and texte_contrat:
                
                    message = instance + " " + right(date_rencontre,5) + "|" + formatter_montant(montant) + " à " + fournisseur + "|" + titre + "|" + texte_contrat
                    
                #S'il y a un montant et un fournisseur
                if montant and fournisseur and texte_contrat:
                
                    message = instance + " " + right(date_rencontre,5) + "|" + formatter_montant(montant) + " à " + fournisseur + "|" + texte_contrat
 
                #Il y a seulement un fournisseur
                elif fournisseur and not titre and not montant and texte_contrat:
                
                    message = instance + " " + right(date_rencontre,5) + "|Contrat à " + fournisseur + "|" + texte_contrat               
                
                #Décision en huis clos
                elif "huis clos" in titre:

                    message = instance + " " + right(date_rencontre,5) + "|Décision " + no_decision + " prise en huis clos." + "|" + texte_contrat

                else:
                
                    message = instance + " " + right(date_rencontre,5) + "|" + texte_contrat
                    
            if message and len(message) > 128:
                
                message = left(message, 128) + "..."
            
            message = message + " #polmtl"
            message = message.strip()
            if message is not " #polmtl" or right(message,9) is not ". #polmtl":
                print("----")
                print(message)
                envoyer_twit(message)
     
    afficher_statut_traitement("Fin du traitement informer_nouveaux_contrats")
    
if __name__ == '__main__':

    a_verifier = [
                    ["MHM",
                     "MHM",
                     "",
                     "http://ville.montreal.qc.ca/portal/page?_pageid=7957,88041590&_dad=portal&_schema=PORTAL",
                     ]
                 ]                
                 
    informer_nouveaux_contrats(a_verifier)
    
    
