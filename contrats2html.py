#!c:\python34\python.exe
# coding: utf8


"""
Version 1.0, 2015-10-02
Développé en Python 3.4
Licence CC-BY-NC 4.0 Pascal Robichaud, pascal.robichaud.do101@gmail.com
"""

import csv
from epurer_fournisseur import *
from set_lien_vslc import *

def set_entete(ligne):

    html = ""
    
    if ligne:

        instance = ligne[0]
        date_rencontre =  ligne[1]
        date_traitement = "2015-09-29" #ligne[16]
        statut = ligne[14]
        source = ligne[15]

        html = html + '<div id="ordre_du_jour" class="div_entete">\n'
        #Instance
        if instance:
            html = html + '  <div class="ligne">'
            html = html + '    <div class="colonne_1">Instance:</div>'
            html = html + '    <div class="colonne_2" id="instance">' + instance + '</div>'
            html = html + '  </div>\n'
        
        #Date de la rencontre
        if date_rencontre:
            html = html + '  <div class="ligne">'
            html = html + '    <div class="colonne_1">Date de la rencontre:</div>'
            html = html + '    <div class="colonne_2 id="date_rencontre">' + date_rencontre + '</div>'
            html = html + '  </div>\n'
        
        #Statut
        if statut:
            html = html + '  <div class="ligne">'
            html = html + '    <div class="colonne_1">Statut:</div>'
            html = html + '    <div class="colonne_2" id="staut">' + statut + '</div>'
            html = html + '  </div>\n'
        
        #Source
        if source:
            html = html + '  <div class="ligne">'
            html = html + '    <div class="colonne_1">Source:</div>'
            html = html + '    <div class="colonne_2" id="source"><a href="' + source + '" target="_blank">Fichier PDF de l\'ordre du jour</a></div>'
            html = html + '  </div>\n'
        
        #Date du traitement
        if date_traitement:
            html = html + '  <div class="ligne">'
            html = html + '    <div class="colonne_1">Date du traitement:</div>'
            html = html + '    <div class="colonne_2" id="date_du_traitement">' + date_traitement + '</div>'
            html = html + '  </div>\n'
        
        #Fermeture de <div id="ordre_du_jour" class="div_entete">
        html = html + '</div>\n'        
        
        return html        
        
        
def set_decision(ligne):

    html = ""

    # 0	    instance
    # 1	    date_rencontre
    # 2	    no_decision
    # 3	    titre
    # 4	    no_dossier
    # 5	    instance_reference
    # 6	    no_appel_offres
    # 7	    nbr_soumissions
    # 8	    pour
    # 9	    texte_contrat
    # 10	fournisseur
    # 11	montant
    # 12	type_contrat
    # 13	huis_clos
    # 14	source
    # 15	date_traitement

    if ligne:

        no_decision = ligne[2]
        titre = ligne[3]
        no_dossier = ligne[4]
        instance_reference = ligne[5]
        no_appel_offres = ligne[6]
        nbr_soumissions = ligne[7]
        pour = ligne[8]
        texte_decision = ligne[9]
        fournisseur = ligne[10]
        montant = ligne[11].replace(",",".")
        type_contrat = ligne[12]
        huis_clos = ligne[13]
        statut = ligne[14]
        source = ligne[15]
                
        html = html + '\n' 
        
        #Liste des contrats
        html = html + '<div class="div_contrat">\n' 
        
        #No de décision
        if no_decision:
            html = html + '  <div class="ligne">\n'
            html = html + '    <div class="colonne_1">No décision:</div>\n'
            html = html + '    <div class="colonne_2">' + no_decision + '</div>\n'
            html = html + '  </div>\n'

        #Titre
        if titre:
            html = html + '  <div class="ligne">\n'
            html = html + '    <div class="colonne_1">Titre:</div>\n'
            html = html + '    <div class="colonne_2">' + titre + '</div>\n'
            html = html + '  </div>\n'        
        
        #Dossier
        if no_dossier:
            html = html + '  <div class="ligne">\n'
            html = html + '    <div class="colonne_1">Dossier:</div>\n'
            html = html + '    <div class="colonne_2">' + no_dossier + '</div>\n'
            html = html + '  </div>\n'                    
        
        #Fournisseur
        if fournisseur:
            html = html + '  <div class="ligne">\n'
            html = html + '    <div class="colonne_1">Fournisseur:</div>\n'
            html = html + '    <div class="colonne_2">' + fournisseur + '\n'
            html = html + '    ' + set_lien_vslc(fournisseur) + '</div>\n'            
            html = html + '  </div>\n'         
        
        #Montant
        if montant:
            html = html + '  <div class="ligne">\n'
            html = html + '    <div class="colonne_1">Montant:</div>\n'
            html = html + '    <div class="colonne_2">' + '{:,.2f} $'.format(float(montant)) + ' </div>\n'
            html = html + '  </div>\n'                 

        #Numéro d'appel d'offres
        if no_appel_offres:
            html = html + '  <div class="ligne">\n'
            html = html + '    <div class="colonne_1">Numéro d appel d offres:</div>\n'
            html = html + '    <div class="colonne_2"><a href="http://www.seao.ca/Recherche/rech_simpleresultat.aspx?SearchParameter=' + no_appel_offres + '&callingPage=2&Results=1" target="_blank">' + no_appel_offres + '</a></div>\n'
            html = html + '  </div>\n'          
            
        #Nombre de soumissions
        if nbr_soumissions:
            html = html + '  <div class="ligne">\n'
            html = html + '    <div class="colonne_1">Nombre de soumissions:</div>\n'
            html = html + '    <div class="colonne_2">' + nbr_soumissions + '</div>\n'
            html = html + '  </div>\n'         
        
        #Type de contrat
        if type_contrat:
            html = html + '  <div class="ligne">\n'
            html = html + '    <div class="colonne_1">Type de contrat:</div>\n'
            html = html + '    <div class="colonne_2">' + type_contrat + '</div>\n'
            html = html + '  </div>\n'         
            
        #Texte du contrat
        if texte_decision:
            html = html + '  <div class="ligne">\n'
            html = html + '    <div class="colonne_1">Texte de la décision:</div>\n'
            html = html + '    <div class="colonne_2">' + texte_decision + '</div>\n'
            html = html + '  </div>\n'          

        
        html = html + '</div>\n' 

    return html
        
def contrats2html():

    entete_complete = False     #Si l'en-tête est complété
    html = ""
    
    with open('contrats_traites.csv', 'r', encoding = 'utf-8') as f_csv:
        reader = csv.reader(f_csv,  delimiter=';')
    
        for ligne in reader:
 
            if ligne:
                
                instance = ligne[0]
                
                #En-tête de la page
                if not entete_complete and "instance" not in instance:                 
                    
                    html = html + set_entete(ligne)
                    html = html + set_decision(ligne)
                    
                    entete_complete = True
                
                #À partir du 2e contrat, ligne 3 du fichier
                elif "instance" not in instance:

                    html = html + set_decision(ligne) 

        html = html + '</div>\n'
        # print(html)
        
        fichier_html = open("fichier_html.html", "w")
        fichier_html.write(html)
        
if __name__ == '__main__':
    contrats2html()
