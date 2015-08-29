#!c:\python34\python.exe
# coding: utf8


"""
Version 2.0, 2015-08-28
Développé en Python 3.4
Licence CC-BY-NC 4.0 Pascal Robichaud, pascal.robichaud.do101@gmail.com
"""


import subprocess
from afficher_statut_traitement import *
from get_ODJ  import *
from odj2contrats import *
#from get_bitly.py import *
from envoyer_twit import *


def main():

    afficher_statut_traitement("Début du traitement principal")
    #a_verifier instance, lien de la page web
    #a_verifier = [
                    # ["Conseil municipal", 
                    # "http://ville.montreal.qc.ca/portal/page?_pageid=5798,85945578&_dad=portal&_schema=PORTAL"]
                 # ]  
    
    a_verifier = [
                    ["Comité exécutif",
                    "http://ville.montreal.qc.ca/portal/page?_pageid=5798,85931607&_dad=portal&_schema=PORTAL"]
                 ]   

    
    #Passer au travers des pages web à vérifier
    for item in a_verifier:
    
        #Télécharger le(s) fichier(s) PDF de l'ordre du jour 
        if get_ODJ(item[1]):
        
            #Convetir le(s) fichier(s) PDF en fichier(s) .txt
            #PDFMiner qui est utilisé ne fonctionne qu'en Python 2.7
            #D'où le fait qu'un subprocess soit utilisé
            subprocess.call("c:\python27\python.exe c:\ContratsOuvertsMtl\odj2txt.py")
            
            #Extraire les contrats en format .csv
            odj2contrats(item)       #item[1] = lien de la page source du PDF
            
            #Envoyer un message par Twitter
            #envoyer_twit("#ContratsOuvertsMtl: Nouveau contrat ")
            
    afficher_statut_traitement("Fin du traitement principal")
        
        
if __name__ == '__main__':
    main()
