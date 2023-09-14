import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import amcio

from os import name
if name == "nt":                                 #set for high dpi if run on windows
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)

#debug
modlists = []
neededMods = {}
extraMods = {}

def changePath():
    pass
def saveToFile():
    pass
def unsubOne():
    pass
def unsubAll():
    pass
def checkUpdate():
    pass
#end debug

def emptyHtmls():
    messagebox.showerror("Error", "No modlists found")

def refresh():
        """scan for modlist files and the contained mods"""
        modlists = amcio.searchModlists()
        modlistList.delete(0, tk.END)
        neededModsList.delete(0, tk.END)
        #getextramods and clear
        if len(modlists) == 0: emptyHtmls()
        else: 
            modlists, neededMods, neededDlcs = amcio.readModlists(modlists)
            for html in sorted(modlists): modlistList.insert(tk.END, html.removesuffix(".html"))
                #progress.set(int(((modlists.index(html)+1)/len(modlists))*100))
            for neededMod in sorted(neededMods.keys()): neededModsList.insert(tk.END, neededMod)

#main window
mainWindow = tk.Tk()
mainWindow.title("Arma 3 Mod Cleaner")
mainFrame = ttk.Frame(mainWindow, padding= "20 20 20 5")
mainFrame.rowconfigure([*range(8)], weight = 1, minsize = 10)
mainFrame.columnconfigure([*range(4)], weight = 1, minsize = 70)
mainFrame.grid()

#modlists
modlistLabel = ttk.Label(mainFrame, text= "Modlists")
modlistLabel.grid(row= 0, column= 0)
modlistFrame = ttk.Frame(mainFrame, relief= tk.GROOVE, borderwidth= 3)
modlistFrame.grid(row=1, column= 0, rowspan= 2)
modlistYScroll = ttk.Scrollbar(modlistFrame, orient= tk.VERTICAL)
modlistYScroll.grid(row = 0, column= 1, sticky= tk.NS)
modlistList = tk.Listbox(modlistFrame, activestyle= "none", height = 6, width= 25, listvariable= tk.Variable(value= modlists), yscrollcommand= modlistYScroll.set)
modlistList.grid(row= 0, column= 0)
modlistYScroll['command'] = modlistList.yview()

#modlists buttons
refreshModButton = ttk.Button(mainFrame, text= "Refresh", command= refresh)
refreshModButton.grid(row= 3, column= 0, pady= 20, sticky= tk.EW)
changePathButton = ttk.Button(mainFrame, text= "Change modlist directory", command=changePath())
changePathButton.grid(row= 4, column= 0, sticky= tk.EW)

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
neededModsList = tk.Listbox(neededModsFrame, activestyle= "none", height = 15, width= 40, listvariable= tk.Variable(value= neededMods), yscrollcommand= neededModsYScroll.set)
neededModsList.grid(row= 0, column= 0)
neededModsYScroll["command"] = neededModsList.yview

#extra mods list
extraModsLabel = ttk.Label(mainFrame, text= "Extra Mods")
extraModsLabel.grid(row= 0, column= 2, padx= (10, 20))
extraModsFrame = ttk.Frame(mainFrame, relief= tk.GROOVE, borderwidth= 3)
extraModsFrame.grid(row=1, column= 2, rowspan= 4, sticky= tk.NSEW, padx= (0, 20))
extraModsYScroll = ttk.Scrollbar(extraModsFrame, orient= tk.VERTICAL)
extraModsYScroll.grid(row = 0, column= 1, sticky= tk.NS)
extraModsList = tk.Listbox(extraModsFrame, activestyle= "none", height = 15, width= 40, listvariable= tk.Variable(value= extraMods), yscrollcommand= extraModsYScroll.set)
extraModsList.grid(row= 0, column= 0)
extraModsYScroll["command"] = extraModsList.yview

#extra mods buttons
extraButtonsFrame = ttk.Frame(mainFrame)
extraButtonsFrame.grid(row= 1, column= 3, rowspan= 4, sticky= tk.NSEW)
unsubOneButton = ttk.Button(extraButtonsFrame, text= "  Unsub selected  ", command= unsubOne())
unsubOneButton.grid(row= 0, column= 0, sticky= tk.EW, pady= (0, 20))
unsubAllButton = ttk.Button(extraButtonsFrame, text= "Unsub all", command= unsubAll())
unsubAllButton.grid(row= 1, column= 0, sticky= tk.EW, pady= (0, 20))
saveToFileButton = ttk.Button(extraButtonsFrame, text= "Save to file", command= saveToFile())
saveToFileButton.grid(row= 2, column= 0, sticky= tk.EW)


#additional buttons
checkUpdateButton = ttk.Button(mainFrame, text= "Check for updates", command= checkUpdate())
checkUpdateButton.grid(row= 6, column= 3, sticky= tk.EW)
checkSiteLabel = ttk.Label(mainFrame, text= "*link*Mod Cleaner by Alexein")
checkSiteLabel.grid(row= 7, column= 3, sticky= tk.EW)


refresh()
mainWindow.mainloop()