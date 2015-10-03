#!c:\python34\python.exe
# coding: utf8


"""
Version 4.0, 2015-10-02
Développé en Python 3.4
Licence CC-BY-NC 4.0 Pascal Robichaud, pascal.robichaud.do101@gmail.com
"""
from sys import exit
from csv import *
import subprocess
from afficher_statut_traitement import *
from get_ODJ  import *
from odj2contrats import *
from informer_nouveaux_contrats import *


def get_liens_a_verifier():

    liens_a_verifier = []
    
    with open("C:\\ContratsOuvertsMtl\\liens_a_verifier.csv", "r") as csvfile:
        myreader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in myreader:
        
            if "nom" not in row:
                liens_a_verifier.append(row)
    
    return liens_a_verifier

def contrats_ouverts_mtl():

    afficher_statut_traitement("Début du traitement principal")
      
    a_verifier = get_liens_a_verifier()
    
    print(a_verifier)
    
    #Passer au travers des pages web à vérifier
    for item in a_verifier:
    
        print()
        print(item)

        #Télécharger le(s) fichier(s) PDF de l'ordre du jour 
        if get_ODJ(item[3]):
            
            #Extraire les contrats en format .csv
            odj2contrats(item)       #item[1] = lien de la page source du PDF
            
            #Envoyer un message par Twitter
            informer_nouveaux_contrats()
            
    afficher_statut_traitement("Fin   du traitement principal")
        
        
if __name__ == '__main__':
    contrats_ouverts_mtl()
