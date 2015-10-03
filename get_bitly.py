#!/usr/local/bin/python
# coding: utf8

"""
Obtenir un lien raccourci de Bitly

Version 4.0, 2015-10-02
Développé en Python 3.4
Licence CC-BY-NC 4.0 Pascal Robichaud, pascal.robichaud.do101@gmail.com
"""


import bitly_api


def get_lien_court(url):

    """Obtenir le lien court"""
    c = bitly_api.Connection(access_token="")
    
    sh = c.shorten(url)
    
    return sh['url']

    
def main():
 
    lien_court = get_lien_court('http://google.com/')
    
    print(lien_court)
    
    return None
    
    
if __name__ == '__main__':
   main()
