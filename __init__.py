# -*- coding: utf-8 -*-

#Script to convert Text in BwHebb Fonts to normal unicode Hebrew.
#copyright 2013 Benjamin Schnabel Benjamin-777@gmx.de www.benjaminschnabel.de
#Benjamin-777@gmx.de

import os
import sys
import string
import codecs
from docx import Document


#Load file
def LoadFile() :
    fread = input('Enter input file:')
    print('[1] Bwhebb -> Hebrew')
    return fread

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
    
    try:
        document = Document(fread)
    except (OSError, IOError):
        print('Input file not found, exiting...')
        sys.exit()
    for content in document.paragraphs:
        content.text = content.text.replace(' / ', '*')
        content.text = content.text.replace('* ','*')
        content.text = content.text[:-1]
        #replace vowels
        content.text = ReplaceVowels(content.text, vowels)
        #change RTL before replacing characters
        if lang == 1:
            content.text = ChangeRTL(content.text)
        #change characters one by one
        for i in range(len(bwhebb)):
            content.text = content.text.replace(bwhebb[i], hebrew[i])
        content.text = content.text.replace('*', '/')
        result += content.text + '\n'
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

#write file
def  WriteFile(content) :
    content.encode(encoding='utf-8', errors='replace')
    print(content)
    fwrite = open('result_file.txt','w', encoding='utf-8')
    fwrite.writelines(content)
    fwrite.close()

fread = None
result = None    
fread = LoadFile() 
result = ReadLine(fread)
WriteFile(result)