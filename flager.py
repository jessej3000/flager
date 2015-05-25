from urllib.request import urlopen
from urllib.parse import urlparse
from os.path import basename
from tkinter import *
from tkinter import ttk

dicDef = {}
dicLink = {}
dicCount =  {}
exList = []

flagApp = Tk()
flagApp.geometry('700x600+100+100')
flagApp.title("Craiglist Flagger V0.1")
flagApp.resizable(0,0)

urlLbl = Label(flagApp,text='Url: ').place(x=20, y=20)
urlTxt = Entry(flagApp,width=95)
urlTxt.place(x=100, y=20)
urlTxt.focus_set()

repLbl = Label(flagApp,text='Repetition: ').place(x=20, y=50)
repTxt = Entry(flagApp,width=10)
repTxt.place(x=100, y=50)

excludeLine = Label(flagApp,text='--------------------------------------------------E X C L U D E  L I S T------------------------------------------------------------').place(x=20,y=80)
excludeTxt = Text(flagApp,width=81,height=7)
excludeTxt.place(x=23, y=110)

excludeLine = Label(flagApp,text='---------------------------------------------------F L A G  S T A T U S------------------------------------------------------------').place(x=20,y=260)
statusTxt = Text(flagApp,width=81,height=18)
statusTxt.place(x=23, y=290)

s_start = Scrollbar(flagApp)

s_start.place(x=675, y=290)

s_start.config(command=statusTxt.yview)
statusTxt.config(yscrollcommand=s_start.set)

v = StringVar()
statusLabel = Label(flagApp,textvariable=v)
statusLabel.place(x=20,y=582)

def gatherExcludeList():
    global exList
    exStr = excludeTxt.get('0.0',END)
    
    if exStr.strip():
        tmpList = exStr.split(',')

        for exItem in tmpList:
            exList.append(basename(exItem).split(".")[0])
        
    return

def GetATagValue(aTag):
    firstLocLi = aTag.find('>')+1
    return aTag[firstLocLi:aTag.find('<',firstLocLi)]

def gatherListToFlag():
    global dicDef
    global dicLink
    global dicCount

    print(urlTxt.get())
    #print(url)
    jobsdb = urlopen(urlTxt.get())

    parsed_uri = urlparse(urlTxt.get())
    domain = parsed_uri.netloc

    rowFound = 0    

    ahrefList = ""

    for htmlline in jobsdb.readlines():
        lineStr = str( htmlline, encoding='utf8' )
        try:
            if 'class="row"' in lineStr:
                rowFound = 1
            if rowFound and '<a href="' in lineStr:
                ahrefList = ahrefList + lineStr
                firstLoc = lineStr.find('"')+1
                id = basename(lineStr[firstLoc:lineStr.find('"',firstLoc)]).split(".")[0]

                if not id in exList:
                    click = 'http://' + domain + '/flag/?flagCode=15&postingID=' + id

                    dicLink[id] = click
                    dicDef[id] = GetATagValue(lineStr)
                    dicCount[id] = 0

                rowFound = 0
        
        except UnicodeDecodeError:
            print("Unicode Error")
    

def startFlagging(Iteration):
    global dicDef
    global dicLink
    global dicCount
    
    StatusBar = 0
    rotation = 0

    for num in range(0,Iteration):        
        innerCounter = 0
        rotation = rotation + 1
        for id in dicLink:
            urlopen(dicLink[id])
            dicCount[id] = dicCount[id] + 1
            innerCounter = innerCounter + 1
            #print(counter)
            #print(dicLink[id])

            statusTxt.delete('0.0',END)
            counter = 0

            for id in dicLink:
                counter = counter + 1
                try:
                    statusTxt.insert(INSERT,str(counter) + ') FLAG[' + str(dicCount[id]) + '] -> ' + dicDef[id] + '\n')                    
                except ValueError:
                    pass

            
            StatusBar = StatusBar + 1

            if StatusBar == 1:
                v.set('F------- [' + str(innerCounter) + '] Repetition(' + str(rotation) +')')
            elif StatusBar == 2:
                v.set('FL------ [' + str(innerCounter) + '] Repetition(' + str(rotation) +')')
            elif StatusBar == 3:
                v.set('FLA----- [' + str(innerCounter) + '] Repetition(' + str(rotation) +')')
            elif StatusBar == 4:
                v.set('FLAG---- [' + str(innerCounter) + '] Repetition(' + str(rotation) +')')
            elif StatusBar == 5:
                v.set('FLAGG--- [' + str(innerCounter) + '] Repetition(' + str(rotation) +')')
            elif StatusBar == 6:
                v.set('FLAGGI-- [' + str(innerCounter) + '] Repetition(' + str(rotation) +')')
            elif StatusBar == 7:
                v.set('FLAGGIN- [' + str(innerCounter) + '] Repetition(' + str(rotation) +')')
            elif StatusBar == 8:
                v.set('FLAGGING [' + str(innerCounter) + '] Repetition(' + str(rotation) +')')
                StatusBar = 0
                
            flagApp.update()
        
    v.set('Done Flagging ' +  str(innerCounter) + ' adds in ' + str(rotation) + ' Repetition')  

    return

def start():
    global dicDef
    global dicLink
    global dicCount
    global exList

    dicDef = {}
    dicLink = {}
    dicCount = {}
    exList = []

    gatherExcludeList()
    gatherListToFlag()
    startFlagging(int(repTxt.get()))
    
    return

searchBtn = Button(flagApp,text='Execute',width=90,command=start).place(x=27,y=230)

flagApp.mainloop()