import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
import webbrowser
import amcio

from os import name
if name == "nt":                                 #set for high dpi if run on windows
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)

#debug
modlists = []
neededMods = {}
extraMods = {}
whitelist = {}

def changeListPath():
    listPath = filedialog.askdirectory()
    amcio.recordSettings(newListPath = listPath)
    refresh()
    
def changeModPath():
    modPath = filedialog.askdirectory()
    amcio.recordSettings(newModPath = modPath)
    refresh()

def saveToWhitelist():
    for index in extraModsList.curselection():
        whitelist.update({extraModsList.get(index): extraMods.get(extraModsList.get(index))})
    amcio.saveToWhitelist(whitelist)
    refresh()

def removeFromWhitelist():
    removeList = []
    for index in neededModsList.curselection():
        removeList.append(neededModsList.get(index))
    amcio.removeFromWhitelist(removeList)
    refresh()    

def unsubOne():
    pass
def unsubAll():
    pass
def checkUpdate():
    webbrowser.open_new_tab("https://gitlab.com/Alexein/arma-3-mod-cleaner/-/releases")
#end debug

def emptyHtmls():
    messagebox.showerror("Error", "No modlists found.")

def modsNotFound():
    messagebox.showerror("Error", "Mod folder not found, manual setting required.")

def refresh():
        """scan for modlist files and the contained mods"""
        global extraMods
        try:
            amcio.getSettings()
        except Exception:
            modsNotFound()
        modlists = amcio.searchModlists()
        modlistList.delete(0, tk.END)
        neededModsList.delete(0, tk.END)
        extraModsList.delete(0, tk.END)
        if len(modlists) == 0: emptyHtmls()
        else:
            neededMods, neededDlcs = amcio.readModlists(modlists)
            whitelist = amcio.readWhitelist()
            extraMods = amcio.searchExtraMods(neededMods.values(), whitelist.values())
            for html in sorted(modlists, key= str.lower): modlistList.insert(tk.END, html.removesuffix(".html"))
                #progress.set(int(((modlists.index(html)+1)/len(modlists))*100))
            for neededMod in sorted(neededMods.keys(), key= str.lower): neededModsList.insert(tk.END, neededMod)
            if len(whitelist.keys()) > 0:
                neededModsList.insert(tk.END, "")
                neededModsList.insert(tk.END, "                               *Whitelist*")
                for whitelistedMod in sorted(whitelist.keys()): neededModsList.insert(tk.END, whitelistedMod)
            for extraMod in sorted(extraMods.keys(), key = str.lower): extraModsList.insert(tk.END, extraMod)
            #for neededdlc

#main window
mainWindow = tk.Tk()
mainWindow.title("Arma 3 Mod Cleaner")
mainFrame = ttk.Frame(mainWindow, padding= "20 20 20 5")
mainFrame.rowconfigure([*range(8)], weight = 1)
mainFrame.columnconfigure([*range(4)], weight = 1)
mainFrame.columnconfigure([0, 3], uniform= "x")
mainFrame.grid()

#modlists
modlistLabel = ttk.Label(mainFrame, text= "Modlists")
modlistLabel.grid(row= 0, column= 0)
modlistFrame = ttk.Frame(mainFrame, relief= tk.GROOVE, borderwidth= 3)
modlistFrame.grid(row=1, column= 0, rowspan= 2, sticky= tk.N)
modlistYScroll = ttk.Scrollbar(modlistFrame, orient= tk.VERTICAL)
modlistYScroll.grid(row = 0, column= 1, sticky= tk.NS)
modlistList = tk.Listbox(modlistFrame, activestyle= "none", height = 7, width= 25, listvariable= tk.Variable(value= modlists), yscrollcommand= modlistYScroll.set, exportselection= 0)
modlistList.grid(row= 0, column= 0)
modlistYScroll['command'] = modlistList.yview()

#modlists buttons
modButtonsFrame = ttk.Frame(mainFrame)
modButtonsFrame.grid(row= 3, column= 0, rowspan= 2, sticky= tk.NSEW)
modButtonsFrame.columnconfigure(0, weight= 1)
refreshModButton = ttk.Button(modButtonsFrame, text= "Refresh", command= refresh)
refreshModButton.grid(row= 3, column= 0, pady= (20, 10), sticky= tk.EW)
changeListPathButton = ttk.Button(modButtonsFrame, text= "Change modlist directory", command=changeListPath)
changeListPathButton.grid(row= 4, column= 0, pady= (10, 10), sticky= tk.EW)
changeModPathButton = ttk.Button(modButtonsFrame, text= "Change mod directory", command= changeModPath)
changeModPathButton.grid(row= 5, column= 0,pady= (10), sticky= tk.EW)


#progress bar
progress = tk.IntVar()
progressBar = ttk.Progressbar(mainFrame, mode= "determinate", variable= progress)
progressBar.grid(row= 7, column= 0, sticky= tk.EW)

#needed mods list
neededModsLabel = ttk.Label(mainFrame, text= "Needed Mods")
neededModsLabel.grid(row= 0, column= 1, padx= (20, 10))
neededModsFrame = ttk.Frame(mainFrame, relief= tk.GROOVE, borderwidth= 3)
neededModsFrame.grid(row=1, column= 1, rowspan= 4, sticky= tk.NSEW, padx= (20, 20))
neededModsYScroll = ttk.Scrollbar(neededModsFrame, orient= tk.VERTICAL)
neededModsYScroll.grid(row = 0, column= 1, sticky= tk.NS)
neededModsList = tk.Listbox(neededModsFrame, activestyle= "none", height = 16, width= 40, listvariable= tk.Variable(value= neededMods), yscrollcommand= neededModsYScroll.set, exportselection= 0, selectmode= tk.MULTIPLE)
neededModsList.grid(row= 0, column= 0)
neededModsYScroll["command"] = neededModsList.yview

#extra mods list
extraModsLabel = ttk.Label(mainFrame, text= "Extra Mods")
extraModsLabel.grid(row= 0, column= 2, padx= (10, 20))
extraModsFrame = ttk.Frame(mainFrame, relief= tk.GROOVE, borderwidth= 3)
extraModsFrame.grid(row=1, column= 2, rowspan= 4, sticky= tk.NSEW, padx= (0, 20))
extraModsYScroll = ttk.Scrollbar(extraModsFrame, orient= tk.VERTICAL)
extraModsYScroll.grid(row = 0, column= 1, sticky= tk.NS)
extraModsList = tk.Listbox(extraModsFrame, activestyle= "none", height = 16, width= 40, listvariable= tk.Variable(value= extraMods), yscrollcommand= extraModsYScroll.set, exportselection= 0, selectmode= tk.MULTIPLE)
extraModsList.grid(row= 0, column= 0)
extraModsYScroll["command"] = extraModsList.yview

#extra mods buttons
extraButtonsFrame = ttk.Frame(mainFrame)
extraButtonsFrame.grid(row= 1, column= 3, rowspan= 4, sticky= tk.NSEW)
extraButtonsFrame.columnconfigure(0, weight= 1)
unsubOneButton = ttk.Button(extraButtonsFrame, text= "  Unsub selected  ", command= unsubOne)
unsubOneButton.grid(row= 0, column= 0, sticky= tk.EW, pady= (0, 20))
unsubAllButton = ttk.Button(extraButtonsFrame, text= "Unsub all", command= unsubAll)
unsubAllButton.grid(row= 1, column= 0, sticky= tk.EW, pady= (0, 20))
saveToFileButton = ttk.Button(extraButtonsFrame, text= "Whitelist selected", command= saveToWhitelist)
saveToFileButton.grid(row= 2, column= 0, sticky= tk.EW, pady= (0, 20))
removeFromFileButton = ttk.Button(extraButtonsFrame, text= "Remove from whitelist", command= removeFromWhitelist)
removeFromFileButton.grid(row= 3, column= 0, sticky= tk.EW)


#additional buttons
checkUpdateButton = ttk.Button(mainFrame, text= "Check for updates", command= checkUpdate)
checkUpdateButton.grid(row= 4, column= 3, sticky= tk.S + tk.EW)
checkSiteLabel = ttk.Label(mainFrame, text= "Mod Cleaner by Alexein v1.0")
checkSiteLabel.grid(row= 7, column= 3, sticky= tk.S + tk.E)

refresh()
mainWindow.mainloop()