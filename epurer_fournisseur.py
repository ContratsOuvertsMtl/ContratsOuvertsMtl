#!c:\python34\python.exe
# coding: utf8


"""Épurer le nom du fournisseur pour la recherche sur le site de Vue sur les contrats
Version 1.0, 2015-10-02
Développé en Python 3.4
Licence CC-BY-NC 4.0 Pascal Robichaud, pascal.robichaud.do101@gmail.com
"""


def epurer_fournisseur(nom_fournisseur):

    reponse = ""

    if nom_fournisseur:

        termes = [" inc.",
                  " inc",
                  " ltée",
                  " ltee"
                  "Les "]
    
        reponse = nom_fournisseur
    
        #Enlever les termes du nom du fournisseur
        for item in termes:
            
            if item in reponse:
                reponse = reponse.replace(item,"")
    
        reponse = reponse.strip()
    
    return reponse
