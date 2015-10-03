#!c:\python34\python.exe
# coding: utf8


"""
Télécharger les nouveaux fichiers PDF de l'ordre du jour sur le site de la Ville de Montréal

Version 4.0, 2015-10-02
Développé en Python 3.4
Licence CC-BY-NC 4.0 Pascal Robichaud, pascal.robichaud.do101@gmail.com
"""

import datetime
import os
import requests
import wget
from bs4 import (
    BeautifulSoup,
    BeautifulStoneSoup, 
)
from afficher_statut_traitement import *
    
    
def get_liens_fichiers_ODJ(LIEN_PREFIXE, a_verifier):

    liens_PDF2 = []

    r = requests.get(a_verifier) 
    r.encoding = "utf-8" 

    #Mettre le contenu de la page dans BeautifulSoup
    soup = BeautifulSoup(r.content, "html.parser") 

    liens_PDF = soup.find_all("a",{"class":"eMediumGrey10"}) 
    
    for item in liens_PDF:                                      
        liens_PDF2.append(LIEN_PREFIXE + item.get('href'))
    
    return liens_PDF2
    

def est_lien_traite(REPERTOIRE, lien_de_la_page):  

    """ Vérifie si le lien vers le fichier a déjà été traité
        Les liens sont conservés dans le fichier liens_traites.txt  
    """
    
    reponse = False
    
    with open(REPERTOIRE + "\\liens_traites.txt", 'r') as f:
        
        for ligne in f:   
            
            if lien_de_la_page.strip() in ligne.strip():
                reponse = True  
                break

    return reponse
    

def ajouter_lien_traite(REPERTOIRE, lien_de_la_page):
    
    with open(REPERTOIRE + "\\liens_traites.txt", 'a') as f:
        f.write("\n" + lien_de_la_page.strip())
        
    return None
    
    
def get_file(REPERTOIRE_PDF, lien_du_PDF):
                        
    afficher_statut_traitement("Début du téléchargement de " + lien_du_PDF)
    
    #fichier_PDF = os.path.join(REPERTOIRE_PDF, "\\odf.pdf")   ne marche pas avec os.path.join ??!!??
    fichier_PDF = REPERTOIRE_PDF + "\\odj.pdf"
    fichier = wget.download(lien_du_PDF, fichier_PDF)                   
    
    afficher_statut_traitement("Fin   du téléchargement de " + lien_du_PDF)
    
    return None

    
def get_ODJ(url):   
    """Partie principale du traitement.
       Télécharger les nouveaux fichiers d'ordre du jour
    """

    reponse = False
    
    #Répertoire de travail du script
    REPERTOIRE = "C:\\ContratsOuvertsMtl"

    # Répertoire où les fichiers PDF sont enregistrés
    REPERTOIRE_PDF = REPERTOIRE + "\\Ordres_du_jour\\PDF"
    
    # Début de l'hyperlien pour télécharger le fichier PDF de l'Ordre du jour
    # Le lien est donné en relatif dans le code HTML de la page
    LIEN_PREFIXE = "http://ville.montreal.qc.ca"

    afficher_statut_traitement("Début du traitement get_ODJ")
    
    #Scraper les liens des fichiers
    liens_PDF = get_liens_fichiers_ODJ(LIEN_PREFIXE, url)
    
    #Télécharger le fichier s'il n'a pas déjà été traité
    for lien in liens_PDF:

        if not est_lien_traite(REPERTOIRE, lien):

            get_file(REPERTOIRE_PDF, lien)
            
            ajouter_lien_traite(REPERTOIRE, lien)
            
            reponse = True

    afficher_statut_traitement("Fin   du traitement get_ODJ")
    
    return reponse
