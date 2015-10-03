#!c:\python34\python.exe
# coding: utf8

"""
Version 1.0, 2015-10-02
Développé en Python 3.4
Licence CC-BY-NC 4.0 Pascal Robichaud, pascal.robichaud.do101@gmail.com
"""

# http://ville.montreal.qc.ca/vuesurlescontrats/api/releases?q=1144119002&format=csv

# http://ville.montreal.qc.ca/vuesurlescontrats/?date_gt=2012-01-01&date_lt=2015-09-30&value_gt=0&value_lt=1000000000&type=contract&offset=0&limit=20&order_by=value&order_dir=desc&procuring_entity=comite-executif%3Bconseil-dagglomeration%3Bconseil-municipal%3Bfonctionnaires&activity=Arrondissements%3BCommunications+et+relations+publiques%3BD%C3%A9veloppement+%C3%A9conomique%3BEnvironnement%3BFoncier%3BGestion+de+l%27information%3BImmeubles+et+terrains%3BInfrastructures%3BJuridique%3BOrganisation+et+administration%3BRessources+financi%C3%A8res%3BRessources+humaines%3BRessources+mat%C3%A9rielles+et+services%3BS%C3%A9curit%C3%A9+publique%3BSports%2C+loisirs%2C+culture+et+d%C3%A9veloppement+social%3BTransport%3BUrbanisme+et+habitation%3BAutres

import requests
import csv
from epurer_fournisseur import *
from epurer_ligne import *
import json
from datetime import datetime


def set_type(texte):

    reponse = texte
    
    if texte:
    
        if "contract" in texte:
        
            reponse = "Contrat"
        
    return reponse
    
    
def enlever_u2019(texte):

    reponse = ""

    texte = texte.replace(u"\u2019", "'")
    
    return texte
    
    
def set_procuring_entity(autorite):

    reponse = ""

    if autorite:
        
        if "Comité exécutif" in autorite:
            reponse = "comite-executif"
            
        elif "Conseil d'agglomération" in autorite:
            reponse = "conseil-dagglomeration"
            
        elif "Conseil municipal" in autorite:
            reponse = "conseil-municipal"
            
        elif "Fonctionnaires" in autorite:
            reponse = "fonctionnaires"
            
        else:
            reponse = ""

    return reponse

            
def set_lien_vslc(nom_fournisseur):

    reponse = ""
    reponse_json = ""
    reponse_csv = ""
    
    montant_total = 0.0
    dernier_contrat = datetime.strptime("1900-01-01", "%Y-%m-%d")
    date_contrat = dernier_contrat

    #Extraire les données sur les contrats précédents du fournisseur en JSON
    if nom_fournisseur:
    
        nom_fournisseur = epurer_fournisseur(nom_fournisseur)
        nom_fournisseur = nom_fournisseur.replace(" ","%20")
        url_json = "http://ville.montreal.qc.ca/vuesurlescontrats/api/releases?q=" + epurer_fournisseur(nom_fournisseur) + '&format=json'
        # http://ville.montreal.qc.ca/vuesurlescontrats/api/releases?q=groupe%20mecano&format=json
        r_json = requests.get(url_json) 
        r_json.encoding = 'utf-8'

        if r_json.text:
        
            data_json = json.loads(r_json.text)
                    
            nbr_contrats = data_json["meta"]["count"]
            montant_total = data_json["meta"]["total_value"]
            montant_min = data_json["meta"]["min_value"]
            montant_max = data_json["meta"]["max_value"]       
            
            reponse_json = ""
            reponse_collapse = ""
            
            if nbr_contrats > 0:     
            
                reponse_json = reponse_json + '<div class="vslc">'
                reponse_json = reponse_json + '<b>Information du site Vue sur les contrats, contrats depuis 2012</b> (<a href="http://ville.montreal.qc.ca/vuesurlescontrats/?q=' + nom_fournisseur + '" target="_blank">Aller sur le site</a>)\n'
                if nbr_contrats:
                    reponse_json = reponse_json + '<div class="vslc_colonne1">Nombre de contrats:</div><div class="vslc_colonne2">' + str(nbr_contrats) + '</div>\n' 
                if montant_min:
                    reponse_json = reponse_json + '<div class="vslc_colonne1">Montant minimum:</div><div class="vslc_colonne2">' + '{:,.2f} $'.format(float(montant_min)) + '</div>\n' 
                if montant_max:
                    reponse_json = reponse_json + '<div class="vslc_colonne1">Montant maximum:</div><div class="vslc_colonne2">' + '{:,.2f} $'.format(float(montant_max)) + '</div>\n' 
 
                reponse_collapse = reponse_collapse + '<div class="exp-col-content-holder"><a class="expand-cnt-link"  href="#">Détail sur les anciens contrats</a>\n'
                reponse_collapse = reponse_collapse + '<div class="hidden-content">\n'
                                
                url_csv = "http://ville.montreal.qc.ca/vuesurlescontrats/api/releases?q=" + epurer_fournisseur(nom_fournisseur) + '&format=csv'
                r_csv= requests.get(url_csv) 
                r_csv.encoding = 'utf-8'
                
                data_csv = r_csv.text
                
                #Mettre les données dans un fichier temporaire csv
                with open("c:\\contratsouvertsmtl\\vslc.csv", encoding="utf-8", mode="w") as f:
                    f.write(data_csv)
                f.close()
                            
                #Ouvrir le fichier temporaire csv
                with open("c:\\contratsouvertsmtl\\vslc.csv", "r", encoding = "utf-8", ) as f:  
                    reader = csv.reader(f, delimiter = ",")    

                    # Champs du CSV
                    #  0 identifiant
                    #  1 date
                    #  2 montant
                    #  3 type
                    #  4 acheteur
                    #  5 activité
                    #  6 description
                    #  7 fournisseur
                    #  8 autorisation
                    #  9 décision
                    # 10 dossier
                        
                    for ligne in reader:
                    
                        if ligne:

                            if "identifiant" not in ligne[0]:

                                csv_identifiant = enlever_u2019(ligne[0])
                                csv_date = enlever_u2019(ligne[1])
                                if csv_date:
                                    date_contrat = datetime.strptime(csv_date, "%Y-%m-%d")
                                    if dernier_contrat < date_contrat:
                                        dernier_contrat = date_contrat
                                csv_montant = enlever_u2019(ligne[2])
                                csv_type = enlever_u2019(ligne[3])
                                csv_acheteur = enlever_u2019(ligne[4])
                                csv_activite = enlever_u2019(ligne[5])
                                csv_description = enlever_u2019(ligne[6])
                                csv_fournisseur = enlever_u2019(ligne[7])
                                csv_autorisation = enlever_u2019(ligne[8])
                                csv_no_decision = enlever_u2019(ligne[9])
                                csv_no_dossier = enlever_u2019(ligne[10])
                                
                                reponse_csv = reponse_csv + '<div class="vslc_detail">' + '\n'
                                                     
                                if csv_fournisseur:
                                    reponse_csv = reponse_csv + '<div class="vslc_colonne1">Fournisseur:</div><div class="vslc_colonne2">' + csv_fournisseur + '</div>\n'
                                if csv_date:
                                    reponse_csv = reponse_csv + '<div class="vslc_colonne1">Date:</div><div class="vslc_colonne2">' + csv_date + '</div>\n'
                                if csv_montant:
                                    reponse_csv = reponse_csv + '<div class="vslc_colonne1">Montant:</div><div class="vslc_colonne2">' '{:,.2f} $'.format(float(csv_montant)) + '</div>\n' 
                                if csv_type:    
                                    reponse_csv = reponse_csv + '<div class="vslc_colonne1">Type:</div><div class="vslc_colonne2">' + set_type(csv_type) + '</div>\n'
                                if csv_acheteur:
                                    reponse_csv = reponse_csv + '<div class="vslc_colonne1">Acheteur:</div><div class="vslc_colonne2"><a href = "http://ville.montreal.qc.ca/vuesurlescontrats/?q=' + csv_acheteur + '" target="_blank">' + csv_acheteur + '</a></div>\n'
                                if csv_activite:
                                    reponse_csv = reponse_csv + '<div class="vslc_colonne1">Activité:</div><div class="vslc_colonne2">' +  csv_activite + '</div>\n'
                                if csv_description:
                                    reponse_csv = reponse_csv + '<div class="vslc_colonne1">Description:</div><div class="vslc_colonne2">' + csv_description + '</div>\n'
                                if csv_autorisation:
                                    reponse_csv = reponse_csv + '<div class="vslc_colonne1">Autorisation:</div><div class="vslc_colonne2"><a href = "http://ville.montreal.qc.ca/vuesurlescontrats/?procuring_entity=' + set_procuring_entity(csv_autorisation) + '" target="_blank">' + csv_autorisation + '</a></div>\n'
                                if csv_no_dossier and "''" not in csv_no_dossier:
                                    reponse_csv = reponse_csv + '<div class="vslc_colonne1">Numéro de dossier:</div><div class="vslc_colonne2"><a href = "http://ville.montreal.qc.ca/vuesurlescontrats/?q=' + csv_no_dossier + '" target="_blank">' + csv_no_dossier + '</a></div>\n'
                                if csv_no_decision:
                                    reponse_csv = reponse_csv + '<div class="vslc_colonne1">Numéro de décision:</div><div class="vslc_colonne2">' +  csv_no_decision + '</div>\n'

                                reponse_csv = reponse_csv + '</div>' + '\n'

                reponse_csv = reponse_csv + '</div>' + '\n'                
                reponse_csv = reponse_csv + '</div>' + '\n'
                reponse_csv = reponse_csv + '</div>' + '\n'

                if montant_total:
                    reponse_json = reponse_json + '<div class="vslc_colonne1">Montant total:</div><div class="vslc_colonne2">' + '{:,.2f} $'.format(float(montant_total)) + '</div>\n' 
                    reponse_json = reponse_json + '<div class="vslc_colonne1">Dernier contrat:</div><div class="vslc_colonne2">{:%Y-%m-%d}'.format(dernier_contrat) + '</div>\n' 
   
            reponse = reponse_json + reponse_collapse + reponse_csv
           
    return reponse
    
if __name__ == '__main__':
    set_lien_vslc("GROUPE MECANO")
