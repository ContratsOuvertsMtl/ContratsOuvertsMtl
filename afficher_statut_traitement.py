#!c:\python34\python.exe
# coding: utf8

"""
Afficher le statut sur le traitement

Version 3.0, 2015-09-07
Développé en Python 3.4
Licence CC-BY-NC 4.0 Pascal Robichaud, pascal.robichaud.do101@gmail.com
"""

import datetime


def afficher_statut_traitement(statut):

    date_heure = datetime.datetime.now()
    statut = statut.strip()
    
    print(date_heure.strftime('%Y-%m-%d %H:%M:%S') + " " + statut)    
    
    return None
