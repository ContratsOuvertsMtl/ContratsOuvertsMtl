#!c:\python34\python.exe
# coding: utf8


"""Extraire les contrats de l'ordre du jour
Version 3.0, 2015-09-07
Développé en Python 3.4
Licence CC-BY-NC 4.0 Pascal Robichaud, pascal.robichaud.do101@gmail.com
"""


import os
import datetime
import time
import csv                               
import re
from afficher_statut_traitement import *


def est_fichier_vide(path):
    return os.stat(path).st_size==0
 
 
#Fonction strip_bom
#Pour enlever \ufeff
def strip_bom(fileName):

    with open(fileName, encoding="utf-8", mode="r") as f:
        text = f.read()
        
    text = text.replace("\ufeff","")
    
    with open(fileName, encoding="utf-8", mode="w") as f:
        f.write(text)

        
#Fonction epurer_ligne
def epurer_ligne(texte):

    reponse = str(texte)
    reponse = reponse.strip()
    reponse = reponse.strip("[]")               #Épuration du texte extrait de l'ordre du jour
    reponse = reponse.replace("  "," ")         #Pour une raison inconnu, il y a plusieurs 2 espaces consécutifs dans l'ordre du jour
    reponse = reponse.replace(" , ",", ")       #Pour une raison inconnu, il y a plusieurs virgules précédées d'un espace
    reponse = reponse.replace(";"," ")          #Enlever les ; pour éviter des problème avec le CSV qui sera généré     
    reponse = reponse.replace("\""," ")
    reponse = reponse.replace(u"\u2018", "'")
    reponse = reponse.replace(u"\u2019", "'")
    reponse = reponse.replace(u"\u2013", "")
    reponse = reponse.replace(u"\x0c", "")
    reponse = reponse.replace("\x0c", "")
    reponse = reponse.replace("\n", "")

    return reponse

 
def epurer_contrat(texte,
                   no_decision,
                   titre,
                   pour,
                   no_dossier):

    if texte:
    
        reponse = texte
        
        if no_decision:
            reponse = reponse.replace(no_decision,"")
     
        if titre:
            reponse = reponse.replace(titre,"")

        if pour:   
            reponse = reponse.replace(pour,"")
            
        if no_dossier:
            reponse = reponse.replace(no_dossier,"")
        
        reponse = epurer_ligne(reponse)
    
    return reponse

    
#Fonction est_numero_de_page    
#Vérifie si la ligne est un numéro de page du PDF de l'ordre du jour
def est_numero_de_page(texte):

    reponse = False

    if texte:
  
        if texte.startswith("Page "):
            reponse = True
     
    return reponse


#Fonction est_huis_clos
#Vérifie si la décision est à huis clos, 
#en tel cas, il n'y a pas de contrat dans l'ordre du jour
def est_huis_clos(texte):
    
    reponse = False
    
    if texte:
        if texte.find("huis clos") > -1:
            reponse = True

    return reponse


def get_huis_clos(texte):

    reponse = "non"

    if texte:
    
        if est_huis_clos(texte):
        
            reponse = "oui"
            
    return reponse
    
    
def est_no_decision(texte):

    reponse = False
    
    if texte:
    
        if texte.startswith(PREFIXE_DECISION):
        
            reponse = True
        
    return reponse   

    
def get_no_decision(texte):

    reponse = ""
    
    if texte:
    
        if est_no_decision(texte):

            if len(texte) >= 6:                             

                reponse = left(texte,6)
  
    return reponse   


def get_titre(texte, no_decision):

    reponse = ""

    if texte:
    
        reponse = texte
        reponse = reponse.replace(no_decision, "")
        reponse = epurer_ligne(reponse)
        
    return reponse


def get_type_contrat(texte):

    reponse = ""

    type = [["appel d'offre public","Appel d'offre public"],
            ["appel d'offre sur inviotation", "Appel d'offre sur inviotation"],
            ["gré à gré","Gré à gré"]
           ]
           
    if texte:
        
        for item in type:
        
            if item[0] in texte:
            
                reponse = item[1]
     
    return reponse
        
    
#Fonction est_instance_reference
#Vérifie si la ligne indique l'instance qui a référé le contrat
def est_instance_reference(texte):
    
    reponse = False

    #CE : Comité exécutif
    #CM : Conseil municipal  
    #CG : Conseil d'agglomération   
    acronymes_instances = ["CE", "CM", "CG"]
    
    if texte:
        
        if texte:
                    
            for item in acronymes_instances:
                if texte.startswith(item):
                    reponse = True
                    break
        
    return reponse
  
  
#Fonction set_instance_reference
#Retourne l'instance qui a référé le contrat
def set_instance_reference(texte):
    
    reponse = ""
      
    instances = [["CE", "Comité exécutif"],
                 ["CM", "Conseil municipal"],
                 ["CG", "Conseil d'agglomération"]
                ]
    
    if texte:

            for item in instances:
                if texte.startswith(item[0]):
                    reponse = item[1]
        
    return reponse


def est_no_dossier(texte):

    reponse = False

    if texte:

        verification = re.search(r"\d{10}", texte)
        if verification:
            reponse = True
    
    return reponse
    
    
def get_no_dossier(texte):

    reponse = ""

    if texte:

        reponse = re.search(r"\d{10}", texte)
        if reponse:
            reponse = reponse.group()
    
    return reponse


#Fonction getNo_appel_offres
#Le numéro est toujours précédé de "offres public no " ou "offres public " et suivi par le nombre de soumissionaires entre parenthèses
#A FAIRE: il arrive que des caractères non significatifs se retrouvent à la fin du numéro. Voir à bonifier la fonction pour les enlever. (voir Issue #8))
def getNo_appel_offres(texte):

    no_appel_offre = ""
    
    if texte:
 
        if "offres public no " in texte:
            debut_no_appel_offre = texte.find("offres public no") + 15
            fin_no_appel_offre = texte.find(" (", debut_no_appel_offre)
            no_appel_offre = mid(texte, debut_no_appel_offre + 1, fin_no_appel_offre - debut_no_appel_offre)
            no_appel_offre = no_appel_offre.strip() 

        elif "offres public " in texte:
            debut_no_appel_offre = texte.find("offres public ") + 13
            fin_no_appel_offre = texte.find(" (", debut_no_appel_offre)
            no_appel_offre = mid(texte, debut_no_appel_offre + 1, fin_no_appel_offre - debut_no_appel_offre)
            no_appel_offre = no_appel_offre.strip()
            
    return no_appel_offre
        

#Fonction getNbr_soumissions
#Retourne le nombre de soumissionnaires pour l'appel d'offres effectué (si applicable)
def getNbr_soumissions(texte):
    
    position = -1                                                           #Variable utilisée pour retoruver le nombre de soumissionnaires
    temp = ""                                                               #Variable temporaire pour garder le caractère vérifié
    nbr_soumissions = ""                                                    #Nombre de soumissions
 
    if texte:

        if texte.find(" soumissionnaires)") > -1:

            position = texte.find(" soumissionnaire") - 1                   #Le mot soumissionaire est au singulier 
                                                                            #pour les cas où il n'y en a qu'un seul
            temp = mid(texte, position, 1)
            
            while (mid(texte, position, 1).isnumeric() and position >= 0):  #Même si la probabilité que position 
                                                                            #devienne plus petit que 0 est presque inexistante,
                nbr_soumissions = temp + nbr_soumissions                    #on fait une vérification à cet effet quand même.
                                                                            
                position = position - 1
                temp = mid(texte, position, 1)

            if not nbr_soumissions.isnumeric():                             #On fait une double vérification afin de s'assurer 
                nbr_soumissions = ""                                        #que le résultat est bien un nombre. 
                                                                            #On réinitialiuse nbr_soumissions si ce n'est pas un nombre.
               
    return nbr_soumissions

    
#Fonction get_fournisseur
#Retourne le nom du fournisseur dans le texte de la décision du contrat
def get_fournisseur(texte):

    reponse = ""
    position_debut_prefixe = -1
    position_debut_suffixe = -1
    
    prefixe_suffixe = [["Accorder un contrat à ", " pour "],
                       ["Accorder des contrat à ", " pour "],
                       ["Accorder un contrat à ", " d'une durée de "],
                       ["Accorder un contrat à l'entreprise ", " pour les travaux de "],
                       ["Accorder un contrat à la firme ", " pour les travaux "],
                       ["Accorder un contrat à les ", " pour l'achat "],
                       ["Accorder un contrat de services professionnels à ", " pour "],
                       ["Accorder à la firme ", " un contrat de "],
                       ["Conclure avec la firme ", "une entente-cadre "],
                       ["Conclure 2 ententes-cadres avec "," pour des travaux "],
                       ["Conclure une entente-cadre de services professionnels avec ", " pour la réalisation "],
                       [" Conclure avec ", " une entente-cadre "],
                       [" de gré à gré à la ", "  pour l'achat "],
                       ["Accorder un soutien financier de ", " pour réaliser  "]
                      ]

    #1. Rechercher le fournisseuur à partir de la liste de référence              
    with open(FICHIER_FOURNISSEUR, "r", encoding = "utf-8", ) as f:     
        reader = csv.reader(f, delimiter = ";")    
    
        for ligne in reader:
            
            temp_fournisseur = ligne[0] + " "
            temp_fournisseur = temp_fournisseur.strip()
            
            if temp_fournisseur in texte:
                reponse = temp_fournisseur
   
    #2. Le fournisseur n'a pas été trouvé dans la liste de référence
    #   on fait alors une recherche avec les termes clés 
    #   se trouvant avant et après le nom du fournisseur
    if not reponse:                                                     
                                                                                
        for i in prefixe_suffixe:

            position_debut_prefixe = texte.find(i[0])
            
            if position_debut_prefixe > -1:
                
                position_debut_suffixe = texte.find(i[1], position_debut_prefixe + len(i[0]))
                
                if position_debut_suffixe > -1:

                    reponse = mid(texte, position_debut_prefixe + len(i[0]), position_debut_suffixe - position_debut_prefixe - len(i[0]))

                    break

    #Enlever s'il y a une virgule après le nom
    #On ne fait pas un replace car il peut y avoir des virgules valides dans le nom du fournisseur
    if reponse:
        reponse = reponse.strip()       #Le strip() ne semble pas fonctionner
        if right(reponse, 1) == ",":
            reponse = left(reponse, len(reponse) - 1)
        if right(reponse, 2) == ", ":
            reponse = left(reponse, len(reponse) - 2)  

    return reponse  

    
#Fonction get_nombre_fournisseurs(texte)
def get_nombre_fournisseurs(texte, nbr_fournisseurs):
    
    reponse = nbr_fournisseurs

    if texte:
        reponse = nbr_fournisseurs + 1  

    return reponse
    
    
def get_montant(texte):

    reponse = ""

    if texte:
    
        reponse = re.search('\d[\d\s,.]*\$', texte)
        
        if reponse:
            reponse = reponse.group()
            reponse = reponse.replace(" ","")
            reponse = reponse.replace("$","")
            
            if not "," in reponse:
                reponse = reponse + ",00"

        else:
            reponse = ""
          
    return reponse

    
#Fonction left
def left(s, amount = 1, substring = ""):

    if (substring == ""):
        return s[:amount]
    else:
        if (len(substring) > amount):
            substring = substring[:amount]
        return substring + s[:-amount]
         
 
#Fonction mid
def mid(s, offset, amount):

    return s[offset:offset+amount]

                 
#Fonction right
def right(s, amount = 1, substring = ""):

    if (substring == ""):
        return s[-amount:]
    else:
        if (len(substring) > amount):
            substring = substring[:amount]
        return s[:-amount] + substring    
         
        
#Fonction test_Debug
def test_Debug(texte):
    
    #if True:
    if False:
        print(texte)
         

#Début du traitement pour extraire les informations sur les contrats 
#à partir du fichier texte de l'ordre du jour
def odj2contrats(a_verifier):

    #Initialisation des variables
    
    instance = a_verifier[0] 
    source = a_verifier[1]
    
    no_decision = ""
    pour = ""
    no_dossier = ""
    instance_reference = ""
    no_appel_offre = ""
    debut_no_appel_offre = ""
    fin_no_appel_offre = ""
    fournisseur = ""
    nbr_fournisseur = 0
    depense_totale = ""
    texte_contrat = ""
    #source = "http://ville.montreal.qc.ca/sel/adi-public/afficherpdf/fichier.pdf?typeDoc=odj&doc=7182"

    #Indiquer le début du traitement
    afficher_statut_traitement("Début du traitement odj2contrats")
    
    #Passer au travers des fichiers dans REPERTOIRE_TXT
    for filename in os.listdir(REPERTOIRE_TXT):
    
        fichier_TXT = os.path.join(REPERTOIRE_TXT, filename)
        
        print("Traitement du fichier %s" % fichier_TXT)
    
        #Enlever le BOM au début du fichier
        strip_bom(fichier_TXT)

        #Ouverture du fichier pour les résultats
        # if est_fichier_vide("C:\\ContratsOuvertsMtl\\contrats_traites.csv"):
            # contrats_traites = open("C:\\ContratsOuvertsMtl\\contrats_traites.csv", "a", encoding="utf-8")      
            # fcontrats_traites.writerow(["instance", "date_rencontre", "no_decision", "no_dossier", "instance_reference", "no_appel_offres", "nbr_soumissions", "pour", "texte_contrat", "fournisseur", "source", "date_traitement"])
            # contrats_traites.close()
       
        contrats_traites = open("C:\\ContratsOuvertsMtl\\contrats_traites.csv", "a", encoding="utf-8") 
        #contrats_traites = open("C:\\ContratsOuvertsMtl\\Production\\contrats_traites.csv", "a", encoding="utf-8")        
        fcontrats_traites = csv.writer(contrats_traites, delimiter = ';') 
        fcontrats_traites.writerow(["instance", "date_rencontre", "no_decision", "titre", 
                                    "no_dossier", "instance_reference", "no_appel_offres", 
                                    "nbr_soumissions", "pour", "texte_contrat", "fournisseur", 
                                    "montant", "type_contrat", "huis_clos", 
                                    "source", "date_traitement"])
       
        #Passer au travers du fichier texte de l'ordre du jour
        with open(fichier_TXT, "r", encoding = "utf-8", ) as f:

            for ligne in f:
            
                ligne.strip()
            
                if ligne:                                                       #Ne pas traiter les lignes vides
                
                    ligne2 = epurer_ligne(ligne)

                    if not est_numero_de_page(ligne2):                          #Ne pas traiter les lignes qui donnes le numéro de page du PDF
                    
                        #Début d'une décision
                        if est_no_decision(ligne2):
                            
                            #C'est une nouvelle décision,
                            #écrire le dernier contrat dans le fichier contrats_traites.txt
                            #Dans le traitement, sur la première décision, il n'y a encore rien à écrire
                            if no_decision:        
                               
                                no_appel_offre = getNo_appel_offres(texte_contrat)
                                nbr_soumissions = getNbr_soumissions(texte_contrat)
                                fournisseur = get_fournisseur(texte_contrat)
                                nbr_fournisseur = get_nombre_fournisseurs(fournisseur, nbr_fournisseur)
                                montant = get_montant(texte_contrat)
                                type_contrat = get_type_contrat(texte_contrat)
                                huis_clos = get_huis_clos(texte_contrat)
                                texte_contrat = epurer_contrat(texte_contrat,
                                                               no_decision,
                                                               titre,
                                                               pour,
                                                               no_dossier)
                                
                                #Écrire le nom des champs dans le fichier contrats_traites.csv
                                fcontrats_traites.writerow([instance, 
                                                            DATE_RENCONTRE, 
                                                            no_decision,
                                                            titre,
                                                            no_dossier, 
                                                            instance_reference, 
                                                            no_appel_offre, 
                                                            nbr_soumissions, 
                                                            pour, 
                                                            texte_contrat, 
                                                            fournisseur, 
                                                            montant,
                                                            type_contrat,
                                                            huis_clos,
                                                            STATUT,
                                                            source, 
                                                            DATE_TRAITEMENT])
                            
                            #Réinitialiser les variables
                            no_decision = get_no_decision(ligne2)               #Nouveau numéro de décision
                            titre = ""
                            pour = ""                                           #Initaliser le pour
                            no_dossier = ""                                     #Initaliser le numéro de dossier
                            instance_reference = ""                             #Initialiser l'instance référente du contrat
                            no_appel_offre = ""                                 #Initaliser le numéro d'appel d'offre
                            debut_no_appel_offre = ""
                            fin_no_appel_offre = ""
                            fournisseur = ""
                            montant = ""
                            type_contrat = "",
                            depense_totale = ""
                            texte_contrat = ""                                  #Initaliser le texte du contrat
                                
                        #L'instance référence du contrat
                        if est_instance_reference(ligne2):
                            instance_reference = set_instance_reference(ligne2)
                      
                        #La variable 'pour' est l'entité pour qui le contrat est adopté
                        if est_instance_reference(ligne2):                              
                            pour = set_instance_reference(ligne2)

                        #Numéro de dossier
                        if not no_dossier:
                            if est_no_dossier(ligne2):
                                no_dossier = get_no_dossier(ligne2)
                            
                        #Numéro de décision
                        if est_no_decision(ligne2):
                            no_decision = get_no_decision(ligne2)
                            titre = get_titre(ligne2, no_decision)

                        #Texte du contrat
                        #if no_dossier and ligne2:                               #Ne pas mettre le 'pour' dans le texte du contrat
                        if not texte_contrat:
                            texte_contrat = ligne2                          #C'est le début du texte du contrat, évite d'avoir un espace au début
                        else:    
                            if not est_instance_reference(ligne2):
                                texte_contrat = epurer_ligne(texte_contrat) + " " + ligne2
                                       
        #Écrire le dernier contrat
        no_appel_offre = getNo_appel_offres(texte_contrat)
        nbr_soumissions = getNbr_soumissions(texte_contrat)
        fournisseur = get_fournisseur(texte_contrat)
        montant = get_montant(texte_contrat)
        texte_contrat = epurer_contrat(texte_contrat,
                                       no_decision,
                                       titre,
                                       pour,
                                       no_dossier)
        fcontrats_traites.writerow([instance, 
                                    DATE_RENCONTRE, 
                                    no_decision, 
                                    titre,
                                    no_dossier, 
                                    instance_reference, 
                                    no_appel_offre, 
                                    nbr_soumissions, 
                                    pour, 
                                    texte_contrat, 
                                    fournisseur, 
                                    montant,
                                    type_contrat,
                                    huis_clos,
                                    STATUT,
                                    source, 
                                    DATE_TRAITEMENT])     

    #Indiquer que le traitement est terminé
    afficher_statut_traitement("Traitement termimé odj2contrats")

    
REPERTOIRE_TXT = "C:\\ContratsOuvertsMtl\\Ordres_du_jour\\TXT"
#REPERTOIRE_TXT = "C:\\ContratsOuvertsMtl\\Production\\Ordres_du_jour\\TXT"
#FICHIER_ORDRE_DU_JOUR = "C:\\ContratsOuvertsMtl\\Ordres_du_jour\\TXT\\CE_ODJ_LP_ORDI_2015-08-12_08h30_FR.txt" #Emplacement du fichier du l'ordre du jour
FICHIER_FOURNISSEUR = "C:\\ContratsOuvertsMtl\\fournisseurs.csv"  						#Emplacement du fichier de la liste des founisseurs
#FICHIER_FOURNISSEUR = "C:\\ContratsOuvertsMtl\\Production\\fournisseurs.csv"  			#Emplacement du fichier de la liste des founisseurs
DATE_RENCONTRE = "2015-09-03"                           								#À changer
PREFIXE_DECISION = "20." 
STATUT = "Ordre du jour présenté"                               					    #À changer au besoin
DATE_TRAITEMENT = left(str(datetime.datetime.today()),19)  								#Date à laquelle le traitement des contrats a été faite
 																						#Arranger le format AAAA-MM-JJ
                                                                                        
def main():

    #a_verifier instance, lien de la page web
    a_verifier = [
                    ["Conseil municipal", 
                    "http://ville.montreal.qc.ca/portal/page?_pageid=5798,85945578&_dad=portal&_schema=PORTAL"]
                 ]
                 
    odj2contrats(a_verifier[0])
    
    return None
   
   
if __name__ == '__main__':
    main()

    
