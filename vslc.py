#Scraper pour le site Vue sur les contrats
#Version 4.0, 2015-10-02
#Code développé en Python 3.4

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
    
    
#Fonction ligneContientContrat
#Vérifie si le numéro de décision est pour un contrat
#La ligne qui suit le numéro de décision contient le mot «contrat»
#La vérification serait à bonifier pour attraper plus de cas. 
#Mais pour une première vérification, plusieurs cas ont tout de même été repérés.
def ligneContientContrat(ligne):
    reponse = False

    if ligne.find("contrat") >= 0:
        reponse = True
        
    if ligne.find("t de la liste des contrats octroy") >= 0:
        reponse = False
 
    if ligne.find("examen des contrats") >= 0:
        reponse = False 
 
    if ligne.find("Lutte à la corruption") >= 0:
        reponse = False 
 
    return reponse
 
#Fonction pour déterminer siu la ligne du procès-verbal est un numnéro de décision
def estNumeroDecision(ligne):
    reponse = False
    
    if ligne.startswith(no_decision_prefixe):
        reponse = True
    
    return reponse

#Fonction pour déterminer siu la ligne du procès-verbal est un numnéro de dossier
def estNumeroDeDossier(ligne):
    reponse = False
    
    try:
        if len(ligne) >= 10:
            verifierNumeroDeDossier = right(ligne,10)
        
            if verifierNumeroDeDossier.isnumeric():
                reponse = True
                print("numero de dossier %s" & ligne)
    except:
        pass

    return reponse    
 
 #Fonction pour déterminer siu la ligne du procès-verbal est un numnéro de dossier
def getNumeroDeDossier(ligne):
    reponse = ""
    
    try:
        if len(ligne) >= 10:
            reponse = right(ligne,10)

    except:
        pass

    return reponse   
 
import os                   #Pour passer au travers des fichiers se trouvant dans le répertoire dir, voir la variable ci-dessous (C:\\vslc)
import csv                  #Pour sauvegarder les résultats dans le fichier verification.csv
import requests             #Pour interoger l'API

#Initialisation des variables
dir = "C:\\vslc"            #Emplacement des fichiers des procès verbaux (vlsc pour Vue sur les contrats)

#Ouverture du fichier pour les résultats du scraping
verification = open('verification.csv', "a", encoding="utf-8")

fverification = csv.writer(verification, delimiter = '|')       #Considérant qu'il est probable de trouver des virgules et des point-virgule dans les données, 
                                                                #on utilise | comme séparateur
fverification.writerow(["fichier_source", "date_proces_verbal", "no_decision", "decisionTrouveeSurLeSite", "no_dossier", "dossierTrouveeSurLeSite","texte_decision"])      #Écrire le nom des champs des données

#Vérifier les fichiers des procès-verbaux se trouvant dans le répertoire C:\vslc
for filename in os.listdir(dir):

    #Initialisation des variables
    no_decision_prefixe = ""            #Variable pour le préfixe à trouver dans le fichier du procès verbal pour une décision. Ex.: CM15 pour Conseil municipal de 2015
    no_decision = "vide"                #Variable pour le numéro de décision trouvé dans le procès verbal
    no_dossier = ""
    estUnContrat = False
    texte_decision = ""
    ligne_proces_verbal = ""
    dossierTrouveeSurLeSite = ""       #Variable pour indiquer si le numéro de décision a été trouvé via l'API du site
    pos = -1

    print('-'*60)
    print(filename)
    
    no_decision_prefixe = left(filename,2) + mid(filename, 7, 2) + " "    #Initialiser le préfixe du numéro des décisions 
    date_proces_verbal =  mid(filename, 5, 4) + "-" + mid(filename, 9, 2) + "-" + mid(filename, 11, 2)
    print(no_decision_prefixe)
    
    #Ouverture du fichier du procès verbal   
    #with open(dir + "\\" + filename, 'r', encoding = 'utf-8') as fproces_verbal:
    with open(dir + "\\" + filename, 'r', encoding = 'latin-1') as fproces_verbal:
        reader = csv.reader(fproces_verbal)
        
        #Passer au travers des ligne du procès-verbal
        for ligne in reader:
            
            try:

                if ligne[0]:     #Pour ne pas traiter les lignes vides
                
                    #Vérifie si la ligne du procès verbal est un numéro de décision
                    ligne_proces_verbal = ligne[0]
                    ligne_proces_verbal.encode('utf-8') 
                    ligne_proces_verbal.strip                
                
                    if estNumeroDecision(ligne_proces_verbal):
                        no_decision = left(ligne_proces_verbal, 9) #Il arrive qu'il y a du texte après le numéro de décision. On prend juste le 9 premiers caractères
                        no_dossier = ""
                        texte_decision = ""
                        ligne_proces_verbal = ""
                        estUnContrat = False
                        url = ""
                        pos = -999
                        dossierTrouveeSurLeSite = ""
                        decisionTrouveeSurLeSite = ""
            
                    #Vérifier si le numéro de décision est pour un contrat
                    elif no_decision != "vide":
                        
                        if ligneContientContrat(ligne[0]):

                            estUnContrat = True
                            texte_decision = texte_decision + ligne_proces_verbal
                        
                        if estUnContrat:
                        
                            if estNumeroDeDossier(ligne_proces_verbal):
                            
                                no_dossier = getNumeroDeDossier(ligne_proces_verbal)
                                print(no_dossier)
                                #Appel sur l'API du site: recherche par le numéro de dossier
                                url_dossier = "http://ville.montreal.qc.ca/vuesurlescontrats/api/releases?q=" + no_dossier
                                print(url)
                                r = requests.get(url_dossier) 
                                r.encoding = 'utf-8'
                                contrat = r.text

                                #Vérifier si le contrat a été trouvé par le numéro de dossier
                                if contrat.find("\"count\": 0")  > -1:
                                    dossierTrouveeSurLeSite = "non"                            #count = 0
                                else:
                                    dossierTrouveeSurLeSite = "oui" 
                                    
                                if contrat.find("\"count\": 1") > -1:
                                    dossierTrouveeSurLeSite = "oui"
                                    
                                if contrat.find("\"count\": 2") > -1:
                                    dossierTrouveeSurLeSite = "oui" 
                                    
                                if contrat.find("\"count\": 3") > -1:
                                    dossierTrouveeSurLeSite = "oui"    

                                if contrat.find("\"count\": 4") > -1:
                                    dossierTrouveeSurLeSite = "oui"      

                                if contrat.find("\"count\": 5") > -1:
                                    dossierTrouveeSurLeSite = "oui"                                

                                #Appel sur l'API du site: recherche par le numéro de décision
                                no_decision2 = no_decision.replace(" ","+")                     #Pour l'URL, il faut remplacer l'espace par un +
                                print(no_decision2)
                                url_decision = "http://ville.montreal.qc.ca/vuesurlescontrats/api/releases?q=" + no_decision2
                                print(url)
                                r = requests.get(url_decision) 
                                r.encoding = 'utf-8'
                                contrat = r.text

                                #Vérifier si le contrat a été trouvé par le numéro de dossier
                                if contrat.find("\"count\": 0")  > -1:
                                    decisionTrouveeSurLeSite = "non"                            #count = 0
                                else:
                                    decisionTrouveeSurLeSite = "oui" 
                                    
                                if contrat.find("\"count\": 1") > -1:
                                    decisionTrouveeSurLeSite = "oui"
                                    
                                if contrat.find("\"count\": 2") > -1:
                                    decisionTrouveeSurLeSite = "oui" 
                                    
                                if contrat.find("\"count\": 3") > -1:
                                    decisionTrouveeSurLeSite = "oui"    

                                if contrat.find("\"count\": 4") > -1:
                                    decisionTrouveeSurLeSite = "oui"      

                                if contrat.find("\"count\": 5") > -1:
                                    decisionTrouveeSurLeSite = "oui"           
                                    
                                #Affichage à l'écran   
                                print('*'*60)
                                print(filename)
                                print("Date du preces verbal: %s" % date_proces_verbal)
                                print("no_decision: %s" % no_decision)
                                print("dossierTrouveeSurLeSite: %s" % decisionTrouveeSurLeSite)
                                print("no_dossier: %s" % no_dossier)
                                print("dossierTrouveeSurLeSite: %s" % dossierTrouveeSurLeSite)
                                print(texte_decision)

                                #Écrire le résultat dans le fichier verification.txt
                                fverification.writerow([filename, date_proces_verbal, no_decision, decisionTrouveeSurLeSite, url_decision, no_dossier, dossierTrouveeSurLeSite, url_dossier, texte_decision])
                                
                                #Réinitialiser les variables
                                no_decision = "vide"
                                no_decision2 = ""
                                no_dossier = ""
                                texte_decision = ""
                                ligne_proces_verbal = ""
                                estUnContrat = False
                                url = ""
                                pos = -999
                                dossierTrouveeSurLeSite = ""
                                decisionTrouveeSurLeSite = ""
                    
            except:
                print("erreur")
                pass

#Fermer les fichiers            
fproces_verbal.close()

#Fin du traitement
print('-'*60)
print("Traitement terminé.")
print('-'*60)
