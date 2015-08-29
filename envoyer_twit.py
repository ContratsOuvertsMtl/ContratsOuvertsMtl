#!c:\python34\python.exe
# coding: utf8

"""
Télécharger les nouveaux fichiers PDF de l'ordre du jour sur le site de la Ville de Montréal

Version 1.1, 2015-08-22
Développé en Python 3.4
Licence CC-BY-NC 4.0 Pascal Robichaud, pascal.robichaud.do101@gmail.com
"""


from twitter import *
import datetime

def envoyer_twit(message):

    message = message.strip() + str(datetime.datetime.now())

    t = Twitter(auth=OAuth(
            consumer_key='',
            consumer_secret='',
            token='',
            token_secret=''     
            ))
    
    t.statuses.update(status = message)
