#!c:\python34\python.exe
# coding: utf8

"""
Version 4.0, 2015-10-02
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
                consumer_key='',
                consumer_secret='',
                token='',
                token_secret=''     
                ))
 
        t.statuses.update(status = message) 
 
        # Send images along with your tweets:
        # - first just read images from the web or from files the regular way:
        # with open("VilleEtTitre.JPG", "rb") as imagefile:
            # imagedata = imagefile.read()
        # - then upload medias one by one on Twitter's dedicated server
        # and collect each one's id:
        # t_up = Twitter(domain='upload.twitter.com',
        # auth=OAuth(
                # consumer_key='hu9JvN5KILdb5KTnQhmrvn2sY',
                # consumer_secret='7SsnNhnTF7u0sWlGkdYFf15h22h7VCViTq38JjfqVdIom2OiFE',
                # token='3431920684-Y2yDx74o5XG0GunDLLVyV47W01HHDK6KLZtST0j',
                # token_secret='eudWwmgWcpp6GO5P9sNHAO0SkauK3Dxi35dJWKE16VMRb'     
                # )
        # id_img1 = t_up.media.upload(media=imagedata)["media_id_string"]
        # id_img2 = t_up.media.upload(media=imagedata)["media_id_string"]
        # - finally send your tweet with the list of media ids:
        # t.statuses.update(status=message, media_ids=",".join([id_img1, id_img2]))
        # t.statuses.update(status=message, media_ids=",".join([id_img1]))
