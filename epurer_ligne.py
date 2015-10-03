#!c:\python34\python.exe
# coding: utf8


"""
Version 1.0, 2015-09-07
Développé en Python 3.4
Licence CC-BY-NC 4.0 Pascal Robichaud, pascal.robichaud.do101@gmail.com
"""

def epurer_ligne(texte):

    reponse = ""
    
    if texte:
        reponse = str(texte)
        reponse = reponse.strip()
        reponse = reponse.strip("[]")               #Épuration du texte extrait de l'ordre du jour
        reponse = reponse.replace("  "," ")         #Pour une raison inconnu, il y a plusieurs 2 espaces consécutifs dans l'ordre du jour
        reponse = reponse.replace(" , ",", ")       #Pour une raison inconnu, il y a plusieurs virgules précédées d'un espace
        reponse = reponse.replace(";"," ")          #Enlever les ; pour éviter des problème avec le CSV qui sera généré     
        reponse = reponse.replace("\""," ")
        reponse = reponse.replace("-", "")
        reponse = reponse.replace(u"\u0153", "oe")
        reponse = reponse.replace(u"\u2018", "'")
        reponse = reponse.replace(u"\u2019", "'")
        reponse = reponse.replace(u"\u2013", "")
        reponse = reponse.replace(u"\u2014", "")
        reponse = reponse.replace(u"\x0c", "")
        reponse = reponse.replace("\x0c", "")
        reponse = reponse.replace("\n", "")

    return reponse
        
if __name__ == '__main__':
    epurer_ligne(arg)
