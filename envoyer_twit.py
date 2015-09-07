#!c:\python34\python.exe
# coding: utf8

"""
Version 3.0, 2015-09-07
Développé en Python 3.4
Licence CC-BY-NC 4.0 Pascal Robichaud, pascal.robichaud.do101@gmail.com
"""


from twitter import *
import datetime
from left import *
        
        
def envoyer_twit(message):

    if message:
    
        message = message.strip()
        message = left(message, 140)
        
        t = Twitter(auth=OAuth(
                consumer_key='hu9JvN5KILdb5KTnQhmrvn2sY',
                consumer_secret='7SsnNhnTF7u0sWlGkdYFf15h22h7VCViTq38JjfqVdIom2OiFE',
                token='3431920684-Y2yDx74o5XG0GunDLLVyV47W01HHDK6KLZtST0j',
                token_secret='eudWwmgWcpp6GO5P9sNHAO0SkauK3Dxi35dJWKE16VMRb'     
                ))
 
        t.statuses.update(status = message)
