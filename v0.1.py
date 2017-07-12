### NOTICE THE CODE FOR THE GUI WHICH I CREATED ALONG WITH THE DNA ANALYSIS SOFTWARE
## IS INCLUDED AT THE END OF THIS FILE (HOWEVER DUE TO CERTAIN BUGS I DIDN'T HAVE THE TIME
## to WORK OUT, I DECIDED TO COMMENT OUT THE GUI and ALLOW THE USER TO INTERACT WITH THE
##SOFTWARE THROUGH EITHER THE TERMINAL OR THROUGH THE PYTHON INTERPRETER) FEL FREE TO IMPLEMENT 
## THE GUI, BUT BE SURE TO MANUALLY ENABLE THE APPROPRIATE OUTPUTS 
 
## Created by Onur Kara, 2010

import re, os
fileToOpen = raw_input('File name: ')
f = open(fileToOpen, 'r').read()

pat = re.compile(r'^[\w\.]+[ \t]+[ATCG\-\?]+$', re.MULTILINE) ##dollar sign says end of line, used this to capture the tables,line by line
matches = pat.findall(f)
ins = re.compile(r'([\w\.]+)\s+(.+)')                         ##will capture the header as 1st group and sequence as 2nd group

d= {}                                         ##this dictionary contains every key:value pair matched from the file. looks like : d[x]= ['AAA-CCC--GG']
for pair in matches:                     ##for each match from pat, split the two groups into a key:value pair
    m = ins.match(pair)             ##will capture groups
    key = m.group(1)                ##take group 1 as key 
    val = m.group(2)               ##take group 2 as value
    if key in d:                  ###if the key is already in the dictionary, take the old value and concatenate it with the new sequence 
        d[key] += val           ##if the key already exists in the dict, concatenate the values and keep the key
    else:
        d[key] = val              ##if the key doesn't exist, create a key:value pair

SEE = d.keys()
SEE.sort()


length = len(d[SEE[0]])      ##PAUP sometime adds a extraneous lineage, with a shortened usless sequence, this wipes that out
dKEYS = []
for all in d:
    if len(d[all]) == length:
        dKEYS += str(all),
dKEYS.sort()
    


quick = re.compile(r'\-')
guyswithatleast1dash = {} ##dict to quickly populated by any sequence having a '-'
for mwmber in d:
    drink= quick.search(d[mwmber]) ##it will stop after the 1st - it finds in a sequence
    if type(drink) != type(None):
        guyswithatleast1dash[mwmber] = d[mwmber]

        
        
dash = re.compile(r'(\-+)')
newd = {}        ## dictionary containing only those keys whose value contain atleast 1 '-' separated by string occurance. Looks like: d[x]= ['---','-','------']
for x in guyswithatleast1dash :
    t = guyswithatleast1dash[x]
    roar = dash.findall(t)   ##searching each value of a key:value pair for '-'
    newd[x] = roar


    

dictofindex = {} ##did this in an attempt to optimize efficiency , so that in later steps it doesn't have to search for '-' in sequences that it knows doesn't contain them
## dictofindex looks like: d[x] = [1,2,3,4,5,9,88,89,90,100]
for ky in newd: ##for each key in the newd dictionary, count position of dashes (ordered but 1 continuous string for eqch sequence)
    position = [] ##indicates the position of each dash
    count = 0
    for char in guyswithatleast1dash[ky]:  ##for each character in each value (sequence), essentially iterates over the entire string of each '-' containing sequence
        count +=1
        if str(char) is '-':
            position += [count,] ##keeps track the position of dashes associated with each key
    dictofindex[ky] = position
##print 'dictofindex', dictofindex, '\n'


GorC = re.compile(r'[GC]')

dictofGC = {}
for key1 in d:       ##G C count in each sequence... 
    string = d[key1]
    dictofGC[key1] = string.count('C'), string.count('G')
    

dictdash = {}       ## Lengths of each sting of '-' within a sequence i.e. d[x] = [48,3,5]. This says x has 3 seperate '-' strings with lenth 48,3 and 5 in that order
for key2 in newd:       
    stuff = []
    for more in newd[key2]:
        stuff += [len(more),] ##Finding the lengths of all strings of '-' in each sequence
    dictdash[key2] = stuff


rangedashes = {}            ##group together indices of consecutive '-' i.e d[x] = [[1,2,3,4,5],[50,51,52]] by far the most needlessly complex step ever
for Some_X in dictdash:     ##i used this to get lists of the indices within each sequence for each '-' in a string of '-'s (messy)
    blind = dictofindex[Some_X]
    deargod = dictdash[Some_X]
    jig = 0
    q = 0
    cars = []
    for e in deargod:
        jig += e            ###upper limit to slice
        ddd = blind[q:jig]   ###slicing based on the length of each '-' string in each sequence 
        cars +=[ddd,]         ###add to cars the range which correspond to each string of '-'s, group together each string of indices
        q = jig             ##not take the last upper limit, and make it your lower limit, and later on add the length of e to get the new upper limit
    rangedashes[Some_X] = cars

GCof5beforeandafter = {}    ##added this for my convenience for when I want to compare the 5 preceding and 5 successive characters after a string of '-'
indextocheck = {}       ##dictionary that shows Gs and Gs before and after strings of '-'s, and corresponds to their position
## indextocheck looks like: d[x] = ['[1,2,3,4,5]==>GCCGG', '[9,10,11,12,13==>ATTAG']
for dude in rangedashes:  ##for each key in dictionary rangedashes
    door = rangedashes[dude] ##door = value associated with the key
    bird = d[dude]  
    keepit = [] 
    another = []
    for lims in door: ##for every member from the value of the key:value pair
        lower = range(lims[0] - 6,lims[0] - 1) ##a range that starts with interger 6 below the start of a '-' string, and ending 1 before the start
        upper = range(lims[-1] , lims[-1] + 5) ##a range that starts with interger immediately after the end of a '-' string, and ending 5 after the start
        wall = '' ## empty string to collect sequence before '-'s string
        ground = '' ## empty string to collect sequence after '-'s string
        for x in lower: ## iterates through string
            if x > 0: ##don't want indices less than 0 because the sequence isn't circular i.e. 600 is not attached to 1
                wall += bird[x] ##if x greater than 0 than add to wall the character associated with the index (x)
            else:
                wall += '(N/A)'##if <= 0 than N/A
        for y in upper:   
            if y < (length - 1): ##if sequence has '-' within 5 spots of the end, don't include (N/A)
                ground += bird[y]
            else:
                ground += '(N/A)'
        fang = [e+1 for e in upper] ###did this for user readibilty, and avoid confusion so the indices matched the position indicators the program provides
        tang = [l+1 for l in lower] 
        keepit +=  str(tang)+'==>' + wall, \
                   str(fang) +'==>'+ ground ##add to keep it the range and sequence associated with that sequence
        another.append((wall,ground))
    GCof5beforeandafter[dude] = another
    indextocheck[dude] = keepit ##once all '-' strings in a sequence have been completed, at keepit to indexofcheck for that key, reset keepit, and start again
##print indextocheck
###print 'indextocheck', indextocheck, '\n'

cleandict = {}
for nag in rangedashes:
    yip = 0 ##corresponds to 1st entry
    hip = 1
    mahbelly = rangedashes[nag]
    emptyg= []
    for get in mahbelly:
        x = str(get[0]) + '-' + str(get[-1]) ### get[0] is position of the start of a '-' string and [-1] is the end
        jyes = indextocheck[nag][yip]
        jno = indextocheck[nag][hip]
        see = (jyes + ' ' + '-'+'('+ x +')'+'-' + ' ' + jno)
        yip += 2   ## used plus 2 through to jump through each pair corresponding to a '-'string
        hip += 2
        emptyg.append(see)
    cleandict[nag] = emptyg




darsh = re.compile(r'([ATCG]+)')
newerd = {}        ## dictionary containing only those keys whose value contain atleast 1 '-' separated by string occurance. Looks like: d[x]= ['ATC','AAATCGCCGCCCTG]
for ex in guyswithatleast1dash :
    to = guyswithatleast1dash[ex]
    snoar = darsh.findall(to)   ##searching each value of a key:value pair for '-'
    newerd[ex] = snoar
###NOW TIME fOR FUNCTIONS
### ASSERT THAT INPUTS ARE IN DICTIONAARY!!




def userlist():   ##I creates this as a way to take an indefinite number of user inputs
    
    guystolook = []   
    while True:
        weee = raw_input('Sequence(s) to analyze(enter when done):')
        weee = weee.strip()
        if len(weee) == 0:
            break
        guystolook += (weee),
    return guystolook 


def getGandC_number_perSeq():  ##GC frequency per sequnce
    myList = userlist()
    for seq in myList:
        print seq + ': C = ' + str(dictofGC[seq][0]) + ', G = ' + str(dictofGC[seq][1])
        print dictofGC[seq][0],dictofGC[seq][1]
    return 

def PosOfDashes():  ##Get the position of insertion/deletion within sequence
    whichSEQS = userlist()
    for every in whichSEQS:
        print rangedashes[every]

    

def lengthseq(): ##this can always be displayed on a gui screen since its unchanged
    print 'Length of the sequence is: ' + str(length) + ' nucleotides'

def The5beforeAndAfterPositions():
    posit = userlist()
    for mem in posit:
        print indextocheck[mem]



def SEARCHandREPLACEbyIndex():  
    seq = []
    donde = raw_input('From which sequence: ')
    assert donde in newd
    track = len(dictofindex[donde])
    keeptrack = 0
   
    
    legals = ['A','C','T','G',r'-',r'?']
    while True:
        if keeptrack + 1== track:
            break
        else:
            for segment in newd[donde]:
                newstr = '' 
                
                for eachdash in segment:
                    ask_user = raw_input('Replace insertion/deletion at position '+ str(dictofindex[donde][keeptrack]) + ' with: ')
                    assert ask_user in legals 
                    newstr += ask_user
                    keeptrack +=1
                    
                seq.append(newstr)
               
            if keeptrack == track:
                break
##    
##    predicSeq = ''
####    indictdashx = rangeofdashes ###
##    tryincount = 0
##    whynot = newerd[donde]
##    if rangedashes[donde][0][0] > 1:
##            for segment in newerd:
##                    if tryincount < len(seq):
##                        predicSeq += segment + seq(tryincount)
##                    elif:
##                        len
##                        
    trycount = 0            ##i USE THESE TO REASSEMBLE PREDICTED SEQUENCE BASED ON WHAT THE USE THINKS IS APPROPRIATE WITH RESPECT TO LINEAGE
    trycountSegs = 0            ## the add segments before and after dash strings
    
    predicSeq = ''
##    indictdashx = rangeofdashes ###
    if rangedashes[donde][0][0] > 1:
        while True:
            if trycount == len(newerd[donde]) and len(seq) == trycountSegs:
                break
            elif len(newerd[donde]) > trycount and len(seq) > trycountSegs:
                predicSeq += newerd[donde][trycount] + seq[trycountSegs]
                trycountSegs +=1
                trycount +=1
                continue

            elif len(newerd[donde]) > trycount and len(seq) == trycountSegs:
                predicSeq += newerd[donde][trycount]
                trycount += 1
                continue
            elif len(newerd[donde])== trycount and len(seq) > trycountSegs:
                predicSeq += seg[trycountSegs]
                trycount += 1
                continue
            else:
                break

        
            
    
    print predicSeq                      


##        
##        
    
    



        ##return seq
        
                
        
                
            
        
    

   ### print type(seq), '\n',len(seq),'\n',seq






def compareseq():
    
    '''positions can be a number or range'''
    ques = raw_input('Are you looking for a particular position (enter P)or a range of positions (enter R)? ')
    if ques != 'P' and ques != 'R':
        return 'Invalid Input', compareseq()
    hora = raw_input('TO compare all sequences enter ALL otherwise press enter: ? ')
    if hora == 'ALL':       
        if ques == 'P':
            where = int(raw_input('At position: '))
            print where
            fixer = where - 1 
            for ind in dKEYS:
                print d[ind][fixer] + ':' + str(ind)
            return

        elif ques == 'R':
            start = int(raw_input('Starting at position: '))
            fin = int(raw_input('Ending at position: '))
            indsStart2Fin = range(start, fin + 1)
            indecks = ''
            for spot in indsStart2Fin:
                indecks += str(spot)
            ##print indecks ##not working great bc of alignment after '9'############ASK HOW TO TABLE FORMAT
            for real in dKEYS:
                poss = ''
                for pet in range(start - 1, fin):
                    this = d[real][pet]
                    poss += this
                print poss,   real
            
    else:
        sequs = userlist()         
        for ii in sequs:
            assert ii in dKEYS ##did this just to get my feet wet with an assert stateement
        if ques == 'P':
            whee = int(raw_input('At position: '))
            print 'pos:'+ str(whee)
            fir = whee - 1
            for guy in sequs:
                print 'nuc', d[guy][fir],':   ', guy
        else: 
            start = int(raw_input('Starting at position: '))
            fin = int(raw_input('Ending at position: '))
            for eli in sequs:
                possi = ''
                for peti in range(start - 1, fin):
                    thisi = d[eli][peti]
                    possi += thisi
                print possi, eli
      
    
            
            

def palindromic(string):
    print string
    reverse = string[::-1]
    print reverse
    if len(string) <= 1:
        return True
    else :
        revcomp = ''
        for nucbase in reverse:
            if nucbase == 'A':
                nucbase = 'T'
                revcomp += nucbase
            elif nucbase == 'C':
                nucbase = 'G'
                revcomp += nucbase
            elif nucbase == 'G':
                nucbase = 'C'
                revcomp += nucbase
            else:
                nucbase = 'A'
                revcomp += nucbase
            
    if revcomp == string:
        return True, '/n'
    else:
        return False

##print palindromic('SSDDSS')
##print palindromic('LoPoL')
##print palindromic('PPgP')    



def freqAny():
    
    ANY = raw_input('Enter A,T,C,G,- or a sequence segment: ')
    WhichSEQ = userlist()
    for mber in WhichSEQ:
        
        hello = d[mber]
        matches = hello.count(ANY)
        print mber, ' contains ' + str(matches) +  ' occurances of ' +  ANY
        

           
    
     
    


    
def shortGCs():      ##freq Gs and Cs before and after for a sequence, and some other info (calls func compareGeeCee
    print '\n'
    quehora = raw_input('From which sequence would you like to compare G and C frequencies based on the nucleotides before an after an ins/del sequence ')   ##REMEMBER to define before:after -- GC pair
    if quehora not in cleandict:
        return 'Invalid Entry', 'Please enter the sequence of interest' , shortGCs()
    
    else: 
            print quehora
            for pair in GCof5beforeandafter[quehora]:
                print pair
                tot = GorC.findall(str(pair))
                aaar = len(pair[0])
                G = pair[0].count('G')
                cees1 = pair[0].count('C')   
                print   '(G', G, (float(G)/aaar)*100,'% : C', cees1, (float(cees1)/aaar)*100,'%)'  
                bbbr = len(pair[1])      
                Ge = pair[1].count('G')
                cees2 = pair[1].count('C') 
                print '(G', Ge, (float(Ge)/bbbr)*100,'% : C', cees2, (float(cees2)/bbbr)*100,'%)'
   
    


def PrintASeq():
    PrintSeq = raw_input('Which Sequence?')
    print d[PrintSeq]

def mirrorImages(ApaiR):
        manINmirror = (ApaiR[0][::-1],ApaiR[1])
        return manINmirror



    
def  compareGeeCee():  ###takes list arguement...TAKE SOMETHING TO CALL THIS
##compare the sequence of 5 nucleotides before and 5 after a insertion/deletion occurance/sequence, 
    

    

    ThIsOne = raw_input('Which sequence? ')
    for B4_and_AfTer in GCof5beforeandafter[ThIsOne]:
        print B4_and_AfTer
        b4 = B4_and_AfTer[0]
        AfTer = B4_and_AfTer[1]
        if b4 == AfTer:
            print 'Each of the 5 nucleotide(s) before the occurance of the insertion/deletion sequence match exactly to the 5 immediately after.'
        else:
            print 'The 5 nucleotide(s) before the occurance of the insertion/deletion sequence do not match the 5 immediately after.'
        
        newbie = mirrorImages(B4_and_AfTer)


        a1 = newbie[0]
        a2 = newbie[1]
        if a1 == a2:
            print 'These ARE mirror images.'
        else:
            print 'These ARE NOT mirror images.'
        
        
        emptystr = ''
        palli = B4_and_AfTer[0]
        pally = B4_and_AfTer[1]
        pally = pally[::-1]
        for serch in pally:
            if serch == 'A':
                emptystr += 'T'
            elif serch == 'T':
                emptystr += 'A'
            elif serch == 'G':
                emptystr += 'C'
            else :
                emptystr += 'G'
        print palli, '(5 nucleotides preceding deletion instance)','\n' , emptystr,   '(reverse complement of 5 post deletion nucleotides)'
        
        if emptystr == palli:
            print 'These sequences are palindromes.'
        else:
            print 'These sequences are not palindromes'
                
             

def doIT():
    print 'What would you like to do?', '\n', '1. Get length of sequences', '\n', '2. Get G/C Frequencies in sequence', '\n', '3. Analyze 5 leading and trailing nucleotides of dash segment' \
      , '\n', '4. Find the positions of insertion/deletion within sequence', '\n','5. Find the frequency of any nucleotide or segment in a sequence', '\n',\
      '6. Replace insertions/deletions with user prediction', '\n','7. Compare entire sequences of species or segments', '\n',\
      '8. Get frequency and percentage of G or C at leading and trailing positions for each insertion/deletion segments in a sequence.', '\n',\
      '9. Show a species entire sequence','\n', '10. See the segments 5 before and after a insertion/deletion string and their corresponding positions.' '\n' \
      ,'11. Test whether or not a sequence is a palindrome.' '\n'

    print 'All entries: ', '\n', dKEYS,'\n'
    print 'Sequences with atleast one insertion or deletion: ', '\n', guyswithatleast1dash.keys(),'\n'
    Task = raw_input('Which function would you like to use?: ')

    if Task == '1':
        lengthseq()
    if Task == '2':
        getGandC_number_perSeq()
    if Task == '3':
        compareGeeCee()
    if Task == '4':
        PosOfDashes()    
    if Task == '5':
        freqAny()
    if Task == '6':
        SEARCHandREPLACEbyIndex() 
    if Task == '7':
        compareseq()
    if Task == '8':
        shortGCs()
    if Task == '9':
        PrintASeq()
    if Task == '10':
        The5beforeAndAfterPositions()
    if Task == '11':
        forfun = palindromic(raw_input('Enter Sequence:' ))
        if forfun is True:
            print 'Yes, this is a palindrome'
        else:
            print 'Not a palindrome'
doIT()

question = raw_input('Would you like to do something else(Y or N)? ')
if question == 'Y' or 'y':
    doIT()
else: print 'Done'

    
    
    
        





##def chart1():   ###table including the frequencies of each nucleotide
##    x = int(raw_input('Enter 0 for table of raw frequencies, Enter 1 for table of relative frequencies, Enter 2 for both: '))
##    if x == 0:
##        return   
##    if x == 1:
##        return
##    if x == 2:        
##        return
##onurs = 'OnurIsAwesome 1.0'
##import sys
##sys.path[:0] = ['../../..']
##import Tkinter
##from Tkinter import *
##
##
###frame = Frame()
###frame.pack()
##
####    
####import Tkinter as tk
####
####
####
####def graphem(seq, width=375, height=325,):
####    root = tk.Tk()
####    c = tk.Canvas(root, width=width, height=height, bg='white')
####    c.pack()
####    y_stretch = 1
####    y_gap = 5
####    x_stretch = 10
####    x_width = 10
####    x_gap = 10
####    for x, y in enumerate(data):
####        x0 = x * x_stretch + x * x_width + x_gap
####        y0 = height - (y * y_stretch + y_gap)
####        x1 = x * x_stretch + x * x_width + x_width + x_gap
####        y1 = height - y_gap
####        c.create_rectangle(x0, y0, x1, y1, fill="red")
####        c.create_text(x0+4, y0, anchor=tk.SW, text=str(y))
####    root.mainloop()
####
####data = getGandC_number_perSeq()
####graphem(data)
####
####
####
#### ##include some references to PAUP
##class MyMenu:
##    def __init__(self,parent):
##        self.balloon = Pmw.Balloon(parent)
##        menuDrop = Pmw.MenuBar(parent,hull_relief = 'raised', hull_borderwidth = 1, \
##                               balloon= self.balloon)
##        menuDrop.pack(fill = 'x')
##        self.menuDrop = menuDrop
##
##        menuDrop.addmenu('File', 'Close this window or exit')
##        menuDrop.addmenuitem('File', 'command','Close this window', command = PrintOne('Action: close'), label = 'Close')
## ##       menuDrop.addmenu('Analayzle', 'What would you like to do?')
## ##       menuDrop.addmenuitem('Action: close,'Things to do')
##
##        self.mainPart = Tkinter.Label(parent, text = '',
##                                      background = 'white', foreground = 'black', padx = 100,\
##                                      pady = 100)
##        self.mainPart.pack(fill = 'both', expand = 1)
##        
##                                    
##
##
##
##class PrintOne:
##    def __init__(self,text):
##        self.text = text
##
##    def __call__(self):
##        print self
##    
##        
##        
##                               
##
##
##
##class Checkbar(Frame):
##    def __init__(self, parent, picks=[], side = LEFT, anchor = NW, hull_height= 200):
##        Frame.__init__(self, parent)
##        self.vars = []
##        for pick in picks:
##            var = IntVar()
##            chk = Checkbutton(self, text=pick, variable=var)
##            chk.pack(side=LEFT, anchor = 'nw', expand=YES)
##            self.vars.append(var)
##    def state(self):
##        return map((lambda var: var.get()), self.vars)
##
##
###class Quitter(Frame):                         
###    def __init__(self, parent=None):          
###        Frame.__init__(self, parent)
###        self.pack()
###        widget = Button(self, text='Quit', command=self.quit)
###        widget.pack(expand=YES, fill=BOTH, side=LEFT)
###    def quit(self):Frame.quit(self)
##
##
##import Pmw
##if __name__ == '__main__':
##    root = Tkinter.Tk()
##    Pmw.initialise(root)
##    root.title(onurs)
##    widget = MyMenu(root)
##    lng = Checkbar(root, dKEYS)
##    tgl = Checkbar(root, ['All'])
##    lng.pack()
##    tgl.pack()
##    lng.config(relief=GROOVE, bd=2)
##
##    def allstates():
##        
##        checker= 0
##        checked = []
##        for quick in tgl.state():
##            if quick == 1:
##                print dKEYS
##                return
##            
##        else:
##            for check in lng.state():
##                if check == 1:
##                    checked.append(dKEYS[checker])
##                checker +=1
##            print checked
##            return
##                             
##                             
##    exitButton = Tkinter.Button(root, text = 'Exit', command =root.destroy)
## ##   Quitter(root).pack(side=RIGHT)
##    exitButton.pack(side = 'bottom')
##    Button(root, text='Done', command=allstates).pack(side=RIGHT)
##    root.mainloop()






