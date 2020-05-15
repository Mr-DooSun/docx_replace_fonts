# -*- coding: utf-8 -*-

#Script to convert Text in BwHebb Fonts to normal unicode Hebrew.
#copyright 2013 Benjamin Schnabel Benjamin-777@gmx.de www.benjaminschnabel.de
#Benjamin-777@gmx.de

import os
import sys
import string
import codecs
from docx import Document

#read line
def ReadLine(fread) :
    charfile = 'hebrew.txt'
    converter = 1
    lang = 1

    bwhebb = []
    hebrew = []
    result = ''
    indicator = False
    vowels = ''
    
    try: 
        c = open(charfile, 'r', encoding='utf-8')
    except (OSError, IOError):
        print('Character file not found, exiting...')
        sys.exit()
    
    #load characters and vowels in string    
    for character in c:
        character.encode(encoding='utf-8', errors='replace')
        character = character.strip()
        split = character.split(' ')
        if indicator == True:
            vowels += character[0]
        if 'vowels:' in character:
            indicator = True
        elif converter == 1:
            bwhebb.append(split[0])
            hebrew.append(split[-1])
        elif converter == 2:
            bwhebb.append(split[-1])
            hebrew.append(split[0])
    c.close()
    
    content = fread
    content = content.replace(' / ', '*')
    content = content.replace('* ','*')
    content = content[:-1]
    #replace vowels
    content = ReplaceVowels(content, vowels)
    #change RTL before replacing characters
    if lang == 1:
        content = ChangeRTL(content)

    #change characters one by one
    for i in range(len(bwhebb)):
        content = content.replace(bwhebb[i], hebrew[i])
    content = content.replace('*', '/')
    result += content + '\n'

    # document.close()
    if lang == 1:
        result = result +  u'\u200f'

    return result

def ReplaceVowels (content, vowels):
#change the place of the vowels with the consonant before it (RTL)
    content = ' ' + content + ' '
    for i in range(len(content)):
        for j in range(len(vowels)):
            if vowels[j] == content[i]:
                replace = list(content)
                replace[i] = content[i-1]
                replace[i-1] = content[i]
                content = ''.join(replace)
    content = content.strip()
    return content

#change RTL
def ChangeRTL(content) :
    result = ''
    for i in range(len(content)-1, -1, -1):
        result += content[i]
    return result


if __name__ =="__main__":
    fread = None
    result = None
    fread = '#r,a,'
    result = ReadLine(fread)
    print(result)