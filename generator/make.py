# files used:
# --- configuration files ---
# config.txt       -> sets the available languages and the page's name
# subtitle.txt     -> small description in each language
# pages.txt        -> enumerates the pages and configures which pages are present in each language
# paths.txt        -> paths for files from the home dir
# --- page models ---
# model.html       -> model for the normal page
# index_model.html -> model for the home page
# --- page contents ---
# home.html        -> content for the home page
# x.html           -> content for the page x, declared at pages.txt

from os import mkdir
from os.path import exists
from shutil import copyfile, rmtree


# model for entries 
flagentry = "<li class=\"flag\"><a href=!link!><img src=!flagpath! align=left height=20></a></li>"
normalentry = "<li><a href=!link!>!pagename!</a></li>"
activeentry = "<li><a href=!link!><u>!pagename!</u></a></li>"

def readAndCut(path):
    s = open(path).read().splitlines()
    # removes empty line
    s = list(filter(lambda v: v != '', s))
    # filter comments
    s = list(filter(lambda v: v[0] != '#', s))
    return [i.split() for i in s]

def readNoCut(path):
    s = open(path).read().splitlines()
    # removes empty line
    s = list(filter(lambda v: v != '', s))
    # filter comments
    return list(filter(lambda v: v[0] != '#', s))

def putCitation(str):
    return '\"' + str + '\"'

def createsNavigationBar(i, j, languages, pagename, pagedisplayname, pageinlanguage):
    bar = ""
    for k in range(len(pagename)):
        if(pageinlanguage[k][j] == '1'):
            s = (normalentry if k != i else activeentry).replace('!pagename!', pagedisplayname[k][j]).replace('!link!', putCitation(pagename[k] + '.html'))
            bar = bar + s + '\n'
    for k in range(len(languages)):
        s = flagentry.replace('!flagpath!', putCitation(("" if j == 0 else "../") + 'flags/' + languages[k] + ('_on' if k == j else '_off') + ".png"))
        s = s.replace('!link!',
                      putCitation(("" if j == 0 else "../") +
                                  ("" if k == 0 else languages[k] + '/') +
                                  # if the page is not available in the targeted languages, redirects to homepage
                                  (pagename[i] if pageinlanguage[i][k] == '1' else 'index') +
                                  ".html"))
        bar = bar + s + '\n'
    return bar
                                                                                               
            

index_model = open('index_model.html').read()
model  = open('model.html').read()

pages = readAndCut('pages.txt')
config = readNoCut('config.txt')
paths = readAndCut('paths.txt')
subtitle = readNoCut('subtitle.txt')

languages = config[0].split()
myname = config[1]
pagename = [pg[0] for pg in pages]
pageinlanguage = [pg[1:(1 + len(languages))] for pg in pages]
pagedisplayname = [pg[(1 + len(languages)):(1 + 2 * len(languages))] for pg in pages]
                  
pagecontents = []
for name in pagename:
    pagecontents.append(
        open(name + '.html').read().split('!split!')
    )

homecontents = open('home.html').read().split('!split!')    

# creates out directory and subdirectories for the other languages
if exists('out'):
    rmtree('out')
mkdir('out')
mkdir('out/flags')

for pt in paths:
    copyfile(pt[1], 'out/' + pt[1])

for lang in languages:
    copyfile('flags/' + lang + '_off.png', 'out/flags/' + lang + '_off.png')
    copyfile('flags/' + lang + '_on.png', 'out/flags/' + lang + '_on.png')
    
for lang in languages[1:]:
    if not exists('out/' + lang):
        mkdir('out/' + lang)
        
# creates home page        
#for i in range(len(languages)):
 #   path = 'out/index.html' if i == 0 else 'out/' + languages[i] + '/index.html'
  #  s = index_model.replace('!name!', myname).replace('!textundername!', subtitle[i]).replace('!pagecontent!', homecontents[i])
   # for pt in paths:
#        s = s.replace(pt[0], putCitation(pt[1] if i == 0 else '../' + pt[1]))
 #   open(path, 'w').write(s)

# creates other pages       
#for j in range(len(pagename)):
 #   for i in range(len(languages)):
  #      if pageinlanguage[j][i] == '1':
   #         path = 'out/' + pagename[j] + '.html' if i == 0 else 'out/' + languages[i] + '/' + pagename[j] + '.html'
    #        s = model.replace('!name!', myname).replace('!pagecontent!', pagecontents[j][i]).replace('!pagename!', pagedisplayname[j][i])
     #       for pt in paths:
      #          s = s.replace(pt[0], putCitation(pt[1] if i == 0 else '../' + pt[1]))
       #     open(path, 'w').write(s)

contents = [homecontents] + pagecontents
pagename = ['index'] + pagename
pagedisplayname = [['Home' for i in range(len(languages))]] + pagedisplayname
pageinlanguage = [['1' for i in range(len(languages))]] + pageinlanguage

            
for j in range(len(pagename)):
    for i in range(len(languages)):
        if pageinlanguage[j][i] == '1':
            path = 'out/' + pagename[j] + '.html' if i == 0 else 'out/' + languages[i] + '/' + pagename[j] + '.html'
            s = (index_model if j == 0 else model).replace('!name!', myname).replace('!pagecontent!', contents[j][i])
            s = s.replace('!textundername!', subtitle[i]).replace('!pagename!', pagedisplayname[j][i])
            s = s.replace('!navigationbar!',
                          createsNavigationBar(j,i,languages,pagename,pagedisplayname,pageinlanguage))
            for pt in paths:
                s = s.replace(pt[0], putCitation(pt[1] if i == 0 else '../' + pt[1]))
            open(path, 'w').write(s)
            
