#!c:\python34\python.exe
# coding: utf8


"""
Version 4.0, 2015-10-02
Développé en Python 3.4
Licence CC-BY-NC 4.0 Pascal Robichaud, pascal.robichaud.do101@gmail.com
"""

#Fonction right
def right(s, amount = 1, substring = ""):

    if (substring == ""):
        return s[-amount:]
    else:
        if (len(substring) > amount):
            substring = substring[:amount]
        return s[:-amount] + substring  

        
if __name__ == '__main__':
    right()
