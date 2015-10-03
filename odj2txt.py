#!c:\python27\python.exe
# coding: utf8

"""Extraction des contrats des fichiers de l'ordre du jour

Convertit la section 20 - Affaires contractuelles 
du fichier PDF de l'ordre du jour en format texte.

Version 4.0, 2015-10-02
Développé en Python 3.4
Licence CC-BY-NC 4.0 Pascal Robichaud, pascal.robichaud.do101@gmail.com
"""


import os
import csv
import subprocess
from afficher_statut_traitement import *


    
def transformer_pdf_en_txt(fichier_PDF, REPERTOIRE_TXT):
    
    afficher_statut_traitement("Début de transformer_pdf_en_txt")
    
    # Titre de la section où se retrouvent les contrats.
    TITRE_SECTION_20 = " Affaires contractuelles"

    # Titre de la section suivant celle où se retrouvent les contrats.
    TITRE_SECTION_30 = " Administration et finances"
    SECTION_APRES = [" Administration et finances",
                     "30.01 Reddition de comptes"
                     "Réglementation",
                     "Urbanisme",
                     "Ressources humaines",
                     "Information",
                     "Motion des conseillers",
                     "Autres sujets"]

    prefixe_txt = os.path.splitext(os.path.basename(fichier_PDF))[0]
    fichier_TXT_temp = os.path.join(REPERTOIRE_TXT, prefixe_txt + '_temp.txt')
    fichier_TXT = os.path.join(REPERTOIRE_TXT, prefixe_txt + '.txt')
    odj_traites = open(fichier_TXT, "w")

    est_dans_section_affaires_contractuelles = False
    est_apres_section_affaires_contractuelles = False
    est_dans_section_suivante = False

    #Convertir le PDF en TXT
    commande = ""
    commande = commande + "c:\\contratsouvertsmtl\\pdftotext.exe -nopgbrk -enc UTF-8 "    
    commande = commande + fichier_PDF
    commande = commande + " " 
    commande = commande + fichier_TXT_temp
    
    subprocess.call(commande)
    
    #Traiter le fichier TXT pour ne garder que la section 20 - Affaires contractuelles
    with open(fichier_TXT_temp, 'r') as f:
        
        for ligne in f:
        
            #On vérifie si on est rendu à la section 20 Affaires contractuelles
            if not est_dans_section_affaires_contractuelles:
            
                if TITRE_SECTION_20 in ligne:
                    est_dans_section_affaires_contractuelles = True              

            else:
                #On est rendu à la section 30 Administration et finances, on arrête le traitement

                for item in SECTION_APRES:
                    if item in ligne:
                    #if ligne.endswith(item):
                        est_apres_section_affaires_contractuelles = True                 
                    
            if est_dans_section_affaires_contractuelles and not est_apres_section_affaires_contractuelles:
                # Ajouter la ligne dans le fichier fichier_TXT
                if not ligne.startswith("Page "):
                    if ligne:
                        odj_traites.writelines(ligne)
                    
    os.remove(fichier_TXT_temp)
                        
    odj_traites.close()
    
    afficher_statut_traitement("Fin de transformer_pdf_en_txt")
    
    return None

    
def main():
    """Partie principale du traitement.
       Transforme tous les fichiers PDF dans le répertoire désigné en fichiers texte.
    """

    afficher_statut_traitement("Debut du traitement odj2txt")

    # Répertoire où les fichiers PDF sont enregistrés
    REPERTOIRE_PDF = "C:\\ContratsOuvertsMtl\\Ordres_du_jour\\PDF"
    
    if not os.path.exists(REPERTOIRE_PDF):
        raise ValueError("Le repertoire " + REPERTOIRE_PDF + " pour les fichier PDF n'existe pas.")

    # Répertoire où le fichier texte résultant sera sauvegardé
    REPERTOIRE_TXT = "C:\\ContratsOuvertsMtl\\Ordres_du_jour\\TXT"
    
    #Si le répertoire n'existe pas pour le fichier texte résultat, on le crée
    if not os.path.exists(REPERTOIRE_TXT):
        os.makedirs(REPERTOIRE_TXT)
    
    #Passer au travers des fichiers PDF et les convertir en .TXT
    for filename in os.listdir(REPERTOIRE_PDF):
        fichier_PDF = os.path.join(REPERTOIRE_PDF, filename)
        print("Traitement du fichier %s" % fichier_PDF)
        transformer_pdf_en_txt(fichier_PDF, REPERTOIRE_TXT)

    afficher_statut_traitement("Fin du traitement odj2txt")
    
    return None

    
if __name__ == '__main__':
    main()
