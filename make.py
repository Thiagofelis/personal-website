# files used:
# --- configuration files ---
# config.txt       -> sets the available languages and my name
# subtitles.txt     -> subtitles in each language
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


# models for entries 
flagentry = "<li class=\"flag\"><a href=!link!><img src=!flagpath! align=left height=20></a></li>"
normalentry = "<li><a href=!link!>!pagename!</a></li>"
activeentry = "<li><a href=!link!><u>!pagename!</u></a></li>"

def readAndCut(path):
# reads lines, remove empty liens and lines with coments,
# and then splits lines at spaces
    s = open(path).read().splitlines()
    # removes empty line
    s = list(filter(lambda v: v != '', s))
    # filter comments
    s = list(filter(lambda v: v[0] != '#', s))
    return [i.split() for i in s]

def readNoCut(path):
# reads lines, remove empty liens and lines with coments,
# but does NOT split lines at spaces    
    s = open(path).read().splitlines()
    # removes empty line
    s = list(filter(lambda v: v != '', s))
    # filter comments
    return list(filter(lambda v: v[0] != '#', s))

def putQuotes(str):
# put " " around string, to be used for links and paths    
    return '\"' + str + '\"'

def createsNavigationBar(i, j, languages, pagename, pagedisplayname, pageinlanguage):
# creates navigation bar of the i-th page on the j-th language
# order of languages and pages is the one given by pagename and languages
    bar = ""
    # adds entries to other pages of the same language
    for k in range(len(pagename)):
        if(pageinlanguage[k][j] == '1'):
            # if the k-th page is not available in the current language (j) then we dont add it to the navigation bar
            s = (normalentry if k != i else activeentry).replace('!pagename!', pagedisplayname[k][j]).replace('!link!', putQuotes(pagename[k] + '.html'))
            bar = bar + s + '\n'
    # adds entries to other languages of the same page
    for k in range(len(languages)):
        # flag of the current language takes the on version, while other languages take the off
        s = flagentry.replace('!flagpath!', putQuotes(("" if j == 0 else "../") + 'flags/' + languages[k] + ('_on' if k == j else '_off') + ".png"))
        # adds the link
        s = s.replace('!link!',
                      putQuotes(("" if j == 0 else "../") +
                                  ("" if k == 0 else languages[k] + '/') +
                                  # if the page is not available in the targeted language, redirects to homepage of the target langage
                                  (pagename[i] if pageinlanguage[i][k] == '1' else 'index') +
                                  ".html"))
        bar = bar + s + '\n'
    return bar
                                                                                               
            

index_model = open('index_model.html').read()
model  = open('model.html').read()

pages = readAndCut('pages.txt')
config = readNoCut('config.txt')
paths = readAndCut('paths.txt')
subtitles = readNoCut('subtitles.txt')

# first line of config contains the list of languages
languages = config[0].split()
# second line of config contains my name
# doest not split because my name can have spaces
myname = config[1]
# column 0 of pages contains the names
pagename = [pg[0] for pg in pages]
# columns 1 to num_languages contains indicator if page is present in language
pageinlanguage = [pg[1:(1 + len(languages))] for pg in pages]
# columns (num_languages + 1) to (2 num_languages) contains de display name in each language
# if page is not present in the corresponding language, then content will not be used
pagedisplayname = [pg[(1 + len(languages)):(1 + 2 * len(languages))] for pg in pages]

# reads the contents of the declared pages, on the order given
pagecontents = []
for name in pagename:
    pagecontents.append(
        open(name + '.html').read().split('!split!')
    )

# reads homepage contents
homecontents = open('home.html').read().split('!split!')    

# creates out directory, a subdirecoty for the flags and subdirectories for the other languages
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

# adds homepage data to the lists        
contents = [homecontents] + pagecontents
pagename = ['index'] + pagename
pagedisplayname = [['Home' for i in range(len(languages))]] + pagedisplayname
pageinlanguage = [['1' for i in range(len(languages))]] + pageinlanguage

            
for j in range(len(pagename)):
    for i in range(len(languages)):
        # if page not present in the language, dont create it
        if pageinlanguage[j][i] == '1':
            # defines page path
            path = 'out/' + pagename[j] + '.html' if i == 0 else 'out/' + languages[i] + '/' + pagename[j] + '.html'
            # replace model with all the specific data
            s = (index_model if j == 0 else model).replace('!name!', myname).replace('!pagecontent!', contents[j][i])
            s = s.replace('!textundername!', subtitles[i]).replace('!pagename!', pagedisplayname[j][i])
            s = s.replace('!navigationbar!',
                          createsNavigationBar(j,i,languages,pagename,pagedisplayname,pageinlanguage))
            # replace paths in the page
            for pt in paths:
                s = s.replace(pt[0], putQuotes(pt[1] if i == 0 else ('../' + pt[1])))
            # write in file
            open(path, 'w').write(s)
            
