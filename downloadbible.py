import requests
import bs4
from bs4 import BeautifulSoup
import re

### Data

OT = ['Genesis', 'Exodus', 'Leviticus', 'Numbers', 'Deuteronomy', 'Joshua', 'Judges', 'Ruth', '1Samuel', '2Samuel', '1Kings', '2Kings', '1Chronicles', '2Chronicles', 'Ezra', 'Nehemiah', 'Esther', 'Job', 'Psalms', 'Proverbs', 'Ecclesiastes', 'SongofSongs', 'Isaiah', 'Jeremiah', 'Lamentations', 'Ezekiel', 'Daniel', 'Hosea', 'Joel', 'Amos', 'Obadiah', 'Jonah', 'Micah', 'Nahum', 'Habakkuk', 'Zephaniah', 'Haggai', 'Zechariah', 'Malachi']
NT = ['Matthew', 'Mark', 'Luke', 'John', 'Acts', 'Romans', '1Corinthians', '2Corinthians', 'Galatians', 'Ephesians', 'Philippians', 'Colossians', '1Thessalonians', '2Thessalonians', '1Timothy', '2Timothy', 'Titus', 'Philemon', 'Hebrews', 'James', '1Peter', '2Peter', '1John', '2John', '3John', 'Jude', 'Revelation']
books = OT + NT

OTabbv = ['Gen', 'Exo', 'Lev', 'Num', 'Deu', 'Jos', 'Jud', 'Rut', 'FSa', 'SSa', 'FKi', 'SKi', 'FCh', 'SCh', 'Ezr', 'Neh', 'Est', 'Job', 'Psa', 'Pro', 'Ecc', 'Son', 'Isa', 'Jer', 'Lam', 'Eze', 'Dan', 'Hos', 'Joe', 'Amo', 'Oba', 'Jon', 'Mic', 'Nah', 'Hab', 'Zep', 'Hag', 'Zec', 'Mal']
NTabbv = ['Mat', 'Mar', 'Luk', 'Joh', 'Act', 'Rom', 'FCo', 'SCo', 'Gal', 'Eph', 'Phi', 'Col', 'FTh', 'STh', 'FTi', 'STi', 'Tit', 'Phm', 'Heb', 'Jam', 'FPe', 'SPe', 'FJo', 'SJo', 'TJo', 'Jde', 'Rev']
abbv = OTabbv + NTabbv

numchaptersOT = [50, 40, 27, 36, 34, 24, 21, 4, 31, 24, 22, 25, 29, 36, 10, 13, 10, 42, 150, 31, 12, 8, 66, 52, 5, 48, 12, 14, 3, 9, 1, 4, 7, 3, 3, 3, 2, 14, 4]
numchaptersNT = [28, 16, 24, 21, 28, 16, 16, 13, 6, 6, 4, 4, 5, 3, 6, 4, 3, 1, 13, 5, 5, 3, 5, 1, 1, 1, 22]
numchapters = numchaptersOT + numchaptersNT

# The list of books with substantial poetry, that is, Job, Psalms, Proverbs, SS, Isaiah, Jeremiah, Lamentations, Hosea, Joel, Amos, Obadiah, Micah, Nahum, Habakkuk, Zephaniah
poetry = [17,18,19,21,22,23,24,27,28,29,30,32,33,34,35]

OTbook2Heb = [1,2,3,4,5,6,7,29,8,8,9,9,25,25,35,35,33,27,26,28,31,30,10,11,32,12,34,13,14,15,16,17,18,19,20,21,22,23,24]

assert len(books)==66 and len(numchapters)==66


### Functions

# Takes in an integer i s.t. 0<=i<100, and returns the two-digit string, prefixing with 0 if necessary.
def twodigit(i):
    if i < 10:
        return '0'+str(i)
    return str(i)

def extract(tag):
    '''
    Takes in an HTML tag, and returns a string.
    Extracts the text inside the tag, preserving italics (<i> tags)
    and <span class="acolon"> and <span class="bcolon">, but ignoring
    <b> and <sup> tags.
    '''
    if isinstance(tag, bs4.element.NavigableString):
        return str(tag)
    r = ''
    for child in tag.contents:
        if child.name=='i':
            r = r + '<i>' + extract(child) + '</i>'
        elif child.name=='span' and ('colon' in child['class'][0]):
            assert child.contents == []
            assert len(child['class'])==1
            assert child['class'][0]=='acolon' or child['class'][0]=='bcolon'
            if r!='' and r[-1]=='/':
                r = r[:-1]
            r = r + '['+child['class'][0]+']'
        elif child.name!='b' and child.name!='sup':
            r = r + extract(child)
    assert '/[acolon]' not in r and '/[bcolon]' not in r
    return r

def extractVerseNumber(tag, numChapters): # The tag should be a <b> tag
    if numChapters > 1:
        chapter = str(tag.contents[1]['href'])
        chapter = chapter[:chapter.index('.')]

        verse = str(tag.contents[1].string)
        verse = int(verse[verse.index(':')+1:])
    else:
        assert numChapters == 1
        chapter = str(tag.contents[0]['href'])
        chapter = chapter[:chapter.index('.')]

        verse = str(tag.contents[0].string)
        verse = int(verse[verse.index(' ')+1:])

    return chapter, verse

# Given string s such as '23,1', extracts chapter,verse
def extractChapterVerse(s):
    assert re.compile('[0-9]+,[0-9]+').match(s)
    comma = s.index(',')
    return int(s[:comma]), int(s[comma+1:])

# Downloads Recovery html files and stores them in current working directory.
# Prepends 'prefix' to all the file names.
def download_recovery(prefix=''):
    for i in range(len(books)):
        for j in range(numchapters[i]):
            file = requests.get('https://text.recoveryversion.bible/'+twodigit(i+1)+'_'+books[i]+'_'+str(j+1)+'.htm')
            open('./'+prefix+twodigit(i+1)+'_'+books[i]+'_'+str(j+1)+'.htm', 'wb').write(file.content)

# Extract Bible
def extractBible():
    ''' Returns tuple (verses, psalms_headers, psalm119_headers)'''
    psalms_headers = []
    psalm119_headers = [] # a list of tuples of the form (169, '_ (Tav)'), first number indicates the verse right after the header.
    verses = []
    for i in range(len(books)):
        verses.append([])
        for j in range(numchapters[i]):
            verses[i].append([])
            if i==18: # We're in book of Psalms
                psalms_headers.append('')
            with open('./'+twodigit(i+1)+'_'+books[i]+'_'+str(j+1)+'.htm') as fp:
                soup = BeautifulSoup(fp, 'html.parser')
                tags = soup.find_all('p')
                k = 1
                for tag in tags:
                    if ('id' in tag.attrs):
                        if tag['id'] == 'Psa'+str(j+1)+'-0':
                            psalms_headers[j] = extract(tag)
                        elif 'Psa119-hebrew_' in tag['id'] and i==18 and j==118: # Psalm 119 has special hebrew alphabet headings
                            psalm119_headers.append((k, extract(tag)))
                        else:
                            assert (tag['id'] == abbv[i]+str(j+1)+'-'+str(k))
                            chapter, verse = extractVerseNumber(tag.contents[0], numchapters[i])
                            assert chapter==(twodigit(i+1)+'_'+books[i]+'_'+str(j+1)) and verse==k
                            verses[i][j].append(extract(tag))
                            k+=1
    return verses, psalms_headers, psalm119_headers

if False:
    verses, psalms_headers, psalm119_headers = extractBible()
    print (verses[22][5][2]) # Isaiah 6:3
    print (psalm119_headers)
    print (verses[4][31][0]) # Deut 32:1
    print (verses[39+3][2][15]) # John 3:16

    with open('recovery_bible_tuple.txt', 'w') as file:
        file.write(repr((verses, psalms_headers, psalm119_headers)))
else:
    with open('recovery_bible_tuple.txt', 'r') as file:
        verses, psalms_headers, psalm119_headers = eval(file.read())





for i in range(len(books)):
    for j in range(numchapters[i]):
        for k in range(len(verses[i][j])):
            prev_verse = verses[i][j][k-1] if k>0 else ''
            verse = verses[i][j][k]
            #while 'colon]' in verse:
            #    l = verse.find('colon]')
            #    if verse[l+6:].lstrip()[0].islower():
            #        print(OT[i] + ' ' + str(j+1)+':'+str(k+1))
            #    verse = verse[l+6:]
            #if verse[:8]!='[acolon]' and verse[:8]!='[bcolon]' and prev_verse!='' and (not (prev_verse[-1]=='.' or prev_verse[-1]=='?' or (prev_verse[-4:]=='</i>' and (prev_verse[-5]=='.' or prev_verse[-5]=='?')))):
                #print(OT[i] + ' ' + str(j+1)+':'+str(k+1))
            #if verse[-1]==':':
            #    print(OT[i] + ' ' + str(j+1)+':'+str(k+1)+' tricky')
            #elif ':' in verse:
            #    print(OT[i] + ' ' + str(j+1)+':'+str(k+1)+' reference')
            #if ':these' in verse or ':These' in verse:
            #    print(OT[i] + ' ' + str(j+1)+':'+str(k+1))

            sections = verse.split('?')
            if len(sections) >= 2:
                for part in sections[1:]:
                    if len(part.split())>=1:
                        word = part.split()[0]
                        if word[0].islower() or (len(word)>=4 and word[0:3]=='<i>' and word[3].islower()):
                            print(books[i] + ' ' + str(j+1)+':'+str(k+1), end=', ')

            '''
            if verse[:8]!='[acolon]' and verse[:8]!='[bcolon]' and prev_verse!='' and (prev_verse[-1]=='?' or (prev_verse[-4:]=='</i>' and prev_verse[-5]=='?')):
                print(books[i] + ' ' + str(j+1)+':'+str(k+1))
            '''




### Obsolete

#soup = BeautifulSoup('<p id="Rev18-6" class="verse"><b><a href="66_Revelation_1.htm">Rv 18</a><a href="66_Revelation_18.htm#Rev18">:6</a></b>Pay her back even as she has paid, and double <i>to her</i> double according to her works; in the cup which she has mixed, mix double to her.</p>', 'html.parser')
#tag = soup.p
#print(tag)
#print (tag.contents)
#print (extractNT(tag))

'''
NTstring = '<!doctype html> <html lang="en"><head><meta charset="utf-8"></head> <body>'
for i in range(len(NTverses)):
    NTstring = NTstring + '<b>'+NT[i]+'</b> '
    for j in range(numchaptersNT[i]):
        for k in range(len(NTverses[i][j])):
            NTstring = NTstring + NTverses[i][j][k] + ' '
NTstring = NTstring + '</body></html>'
NTfile = open("NT.htm", "w")
NTfile.write(NTstring)
NTfile.close()'''

'''
with open('/media/qq/Windows/Users/qqxia/Documents/Bible/Recovery/19_Psalms_18.htm') as fp:
    soup = BeautifulSoup(fp, 'html.parser')
    print(soup)
    tags = soup.find_all('p')
    #print (tags)
    for tag in tags:
        if ('id' in tag.attrs) and tag['id'] == 'Psa18-2':
            print (tag)
            print (tag.contents)
'''

'''
# Download all books in Mechon Mamre Hebrew-English bible.
for i in range(1,36):
    file = requests.get('http://www.mechon-mamre.org/e/et/et'+twodigit(i)+'.htm')
    open('/media/qq/Windows/Users/qqxia/Documents/Bible/hebrew_paragraphs/et'+twodigit(i)+'.htm', 'wb').write(file.content)
'''

'''
# lists of {S},{P}. An entry of the list S indicates a verse v s.t. an {S} occurs at the end of v. v is represented as a tuple (b,c,n) where b is the index of the book, c is the chapter minus one, and n is verse-number minus one. In this section of the script, we ignore Job, Psalms, and Proverbs, and we make special treatment for 1,2 Samuel, 1,2 Kings, 1,2 Chronicles, Ezra, Nehemiah.
# Also, we print out places where an {S} or {P} occurs in the middle of a verse.
S = []
P = []
OTversesParagraphs = [[[[] for k in range(len(OTverses[i][j]))] for j in range(len(OTverses[i]))] for i in range(len(OTverses))]
for i in range(len(OT)):
    if i<17 or i>19: # skip Job, Psalms, Proverbs for now
        if i<8 or i>15:
            with open('/media/qq/Windows/Users/qqxia/Documents/Bible/hebrew_paragraphs/et'+twodigit(OTbook2Heb[i])+'.htm') as fp:
                soup = BeautifulSoup(fp, 'html.parser')
                tags = soup.find_all('p')
                temp = []
                for tag in tags:
                    for child in tag.contents:
                        temp.append(child)
                tags = temp

                tagIndex = 0
                for j in range(numchaptersOT[i]):
                    for k in range(len(OTverses[i][j])):
                        assert tags[tagIndex].name = 'b'
                        assert (j+1,k+1) == extractChapterVerse(tags[tagIndex].string)
                        tagIndex += 1
                        while tagIndex < len(tags) and not (re.compile('[0-9]+,[0-9]+').match(tags[tagIndex].string)):
                            OTversesParagraphs[i][j][k].append(tags[tagIndex])
                            tagIndex += 1
        elif 8<=i and i<=13: # 1,2 Samuel, 1,2 Kings, 1,2 Chronicles
            pass
        else: # Ezra/Nehemiah
            assert 14<=i and i<=15
'''






'''
# Extract from ASV.
import csv

bible = [[[] for j in range(numchapters[i])] for i in range(len(books))]
# opening the CSV file
with open('../t_asv.csv', mode ='r') as file:
    # reading the CSV file
    csvFile = csv.reader(file)
    next(csvFile, None)
    for row in csvFile:
        i = int(row[1])-1; j = int(row[2])-1
        bible[i][j].append(row[4])



print (bible[42][2][15]) # John 3:16
print (bible[22][5][2]) # Isaiah 6:3


# lists of {S},{P}. An entry of the list S indicates a verse v s.t. an {S} occurs at the end of v. v is represented as a tuple (b,c,n) where b is the index of the book, c is the chapter minus one, and n is verse-number minus one. In this section of the script, we ignore Job, Psalms, and Proverbs, and we make special treatment for 1,2 Samuel, 1,2 Kings, 1,2 Chronicles, Ezra, Nehemiah.
# Also, we print out places where an {S} or {P} occurs in the middle of a verse.
S = []
P = []
OTversesParagraphs = [[[[] for k in range(len(bible[i][j]))] for j in range(len(bible[i]))] for i in range(len(bible))]
for i in range(len(OT)):
    if i<17 or i>19: # skip Job, Psalms, Proverbs for now
        if i<8 or i>15:
            with open('/media/qq/Windows/Users/qqxia/Documents/Bible/hebrew_paragraphs/et'+twodigit(OTbook2Heb[i])+'.htm', encoding='windows-1252') as fp:
                soup = BeautifulSoup(fp, 'html.parser')
                tags = soup.find_all('p')
                temp = []
                for tag in tags:
                    for child in tag.contents:
                        if child.name != 'br' and child.string != '\xa0':
                            temp.append(child)
                tags = temp
                print (tags)

                tagIndex = 0
                for j in range(numchaptersOT[i]):
                    for k in range(len(OTversesParagraphs[i][j])):
                        assert tags[tagIndex].name == 'b'
                        print (tags[tagIndex].string)
                        assert (str(j+1)+','+str(k+1)) == tags[tagIndex].string
                        tagIndex += 1
                        while tagIndex < len(tags) and not (re.compile('[0-9]+,[0-9]+').match(tags[tagIndex].string)):
                            OTversesParagraphs[i][j][k].append(tags[tagIndex])
                            tagIndex += 1
        elif 8<=i and i<=13: # 1,2 Samuel, 1,2 Kings, 1,2 Chronicles
            pass
        else: # Ezra/Nehemiah
            assert 14<=i and i<=15
print (OTversesParagraphs[25][1][9]) # Ezekiel 2:10
'''
